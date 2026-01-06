import smtplib
from email.mime.text import MIMEText
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.email_log import EmailLog
from app.core.rbac import has_role
import os

def send_email(db: Session, user: User, to_email: str, subject: str, body: str) -> str:
    """
    Sends an email (mock or real) and logs it.
    Enforces RBAC: Only Admin/HR can send to 'all' or mass emails.
    """
    # 1. RBAC Check for Mass Email
    if to_email.lower() == "all" or "," in to_email:
        if not (has_role(user, "admin") or has_role(user, "hr")):
            raise PermissionError("Only Admin or HR can send mass emails.")

    # 2. Configuration (Real)
    # Use settings from app.core.config to match .env (SMTP_HOST, not SERVER)
    from app.core.config import settings
    
    smtp_server = settings.SMTP_HOST
    smtp_port = settings.SMTP_PORT
    smtp_user = settings.SMTP_USER
    smtp_password = settings.SMTP_PASSWORD
    
    status = "sent"
    
    try:
        if smtp_server and smtp_user and smtp_password:
            # Real sending logic
            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = settings.EMAILS_FROM_EMAIL or smtp_user
            msg["To"] = to_email
            
            with smtplib.SMTP(smtp_server, int(smtp_port)) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.send_message(msg)
            print(f"[Email] Sent to {to_email} via SMTP.")
        else:
            # Mock sending
            print(f"--- [MOCK EMAIL] ---\nTo: {to_email}\nSubject: {subject}\nBody: {body}\n--------------------")
            
    except Exception as e:
        status = f"failed: {str(e)}"
        print(f"[Email] Failed: {e}")

    # 3. Log to DB
    log_entry = EmailLog(
        recipient=to_email,
        subject=subject,
        status=status,
        triggered_by=user.id
    )
    db.add(log_entry)
    db.commit()
    
    return f"Email processed with status: {status}"
