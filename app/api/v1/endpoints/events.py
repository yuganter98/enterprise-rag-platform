from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.models.event import Event
from app.models.user import User
from app.schemas.event import EventCreate, EventResponse
from app.core.rbac import has_role
from app.services.email.sender import send_email

router = APIRouter()

@router.post("/", response_model=EventResponse)
def create_event(
    event_in: EventCreate,
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

    # 2. Notify All Users
    users = db.query(User).filter(User.is_active == True).all()
    count = 0
    for user in users:
        if user.email:
            subject = f"New Event: {event.title}"
            body = f"""
            Hello {user.email},
            
            A new event has been scheduled: {event.title}
            
            Date: {event.date}
            Location: {event.location or 'TBD'}
            
            Description:
            {event.description}
            
            See you there!
            """
            try:
                send_email(db, current_user, user.email, subject, body)
                count += 1
            except Exception as e:
                print(f"Failed to send email to {user.email}: {e}")
    
    print(f"Event created and notified {count} users.")
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
