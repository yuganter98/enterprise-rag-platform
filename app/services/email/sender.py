import smtplib
from email.mime.text import MIMEText
from typing import Dict, List
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.user import User
from app.models.email_log import EmailLog
from app.core.rbac import has_role


def resolve_recipients(db: Session, to_email: str) -> List[str]:
    """
    Expands the `to_email` field into a list of addresses.
    'all' means every active user; otherwise a comma-separated list.
    """
    if to_email.strip().lower() == "all":
        users = db.query(User).filter(User.is_active == True).all()  # noqa: E712
        return [u.email for u in users if u.email]
    return [e.strip() for e in to_email.split(",") if e.strip()]


def _deliver(recipients: List[str], subject: str, body: str) -> Dict[str, str]:
    """
    Sends one message per recipient (so addresses aren't exposed to each other)
    over a single SMTP connection. Falls back to printing when SMTP isn't configured.
    Returns a mapping of recipient -> status.
    """
    results: Dict[str, str] = {}

    if not (settings.SMTP_HOST and settings.SMTP_USER and settings.SMTP_PASSWORD):
        for to in recipients:
            print(f"--- [MOCK EMAIL] ---\nTo: {to}\nSubject: {subject}\nBody: {body}\n--------------------")
            results[to] = "sent"
        return results

    sender = settings.EMAILS_FROM_EMAIL or settings.SMTP_USER
    try:
        with smtplib.SMTP(settings.SMTP_HOST, int(settings.SMTP_PORT)) as server:
            if settings.SMTP_TLS:
                server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            for to in recipients:
                msg = MIMEText(body)
                msg["Subject"] = subject
                msg["From"] = sender
                msg["To"] = to
                try:
                    server.send_message(msg)
                    results[to] = "sent"
                except Exception as e:
                    results[to] = f"failed: {e}"
    except Exception as e:
        # Connection / login failure: everything not yet sent has failed
        for to in recipients:
            results.setdefault(to, f"failed: {e}")

    return results


def send_email(db: Session, user: User, to_email: str, subject: str, body: str) -> str:
    """
    Sends an email (mock or real) and logs it.
    Enforces RBAC: Only Admin/HR can send to 'all' or mass emails.
    """
    # 1. RBAC Check for Mass Email
    is_mass = to_email.strip().lower() == "all" or "," in to_email
    if is_mass and not (has_role(user, "admin") or has_role(user, "hr")):
        raise PermissionError("Only Admin or HR can send mass emails.")

    recipients = resolve_recipients(db, to_email)
    if not recipients:
        return "No recipients found."

    # 2. Send
    results = _deliver(recipients, subject, body)

    # 3. Log to DB (one row per recipient)
    for recipient, status in results.items():
        if status != "sent":
            print(f"[Email] Failed to send to {recipient}: {status}")
        db.add(EmailLog(
            recipient=recipient,
            subject=subject,
            status=status,
            triggered_by=user.id
        ))
    db.commit()

    sent = sum(1 for s in results.values() if s == "sent")
    failed = len(results) - sent
    if failed:
        return f"Sent to {sent} recipient(s), {failed} failed."
    return f"Sent to {sent} recipient(s)."
