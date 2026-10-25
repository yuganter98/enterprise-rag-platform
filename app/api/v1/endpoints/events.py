from typing import Any, List
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.db.session import SessionLocal
from app.models.event import Event
from app.models.user import User
from app.schemas.event import EventCreate, EventResponse
from app.core.rbac import has_role
from app.services.email.sender import send_email

router = APIRouter()


def notify_users_of_event(event_id: int, sender_id: int) -> None:
    """
    Emails every active user about a new event.
    Runs as a background task, so it opens its own DB session
    (the request's session is closed by the time this runs).
    """
    db = SessionLocal()
    try:
        event = db.query(Event).filter(Event.id == event_id).first()
        sender = db.query(User).filter(User.id == sender_id).first()
        if not event or not sender:
            return

        subject = f"New Event: {event.title}"
        body = f"""Hello,

A new event has been scheduled: {event.title}

Date: {event.date}
Location: {event.location or 'TBD'}

Description:
{event.description or ''}

See you there!
"""
        status_msg = send_email(db, sender, "all", subject, body)
        print(f"Event {event.id} notifications: {status_msg}")
    except Exception as e:
        print(f"Failed to send notifications for event {event_id}: {e}")
    finally:
        db.close()

@router.post("/", response_model=EventResponse)
def create_event(
    event_in: EventCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a new event and notify all users via email.
    Only Admin or HR can create events.
    """
    if not (has_role(current_user, "admin") or has_role(current_user, "hr")):
        raise HTTPException(status_code=403, detail="Not authorized to create events")

    # 1. Create Event
    event = Event(**event_in.model_dump(), created_by_id=current_user.id)
    db.add(event)
    db.commit()
    db.refresh(event)

    # 2. Notify all users after the response is sent, so the request isn't
    #    blocked on SMTP for every employee.
    background_tasks.add_task(notify_users_of_event, event.id, current_user.id)
    return event

@router.get("/", response_model=List[EventResponse])
def read_events(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve events.
    """
    events = db.query(Event).order_by(Event.date.desc()).offset(skip).limit(limit).all()
    return events
