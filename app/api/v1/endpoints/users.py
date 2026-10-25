from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.models.role import Role
from app.models.user import User
from app.schemas.user import Role as RoleSchema, UserCreate, UserResponse
from app.core.security import get_password_hash
from app.core.rbac import has_role

router = APIRouter()

@router.get("/", response_model=List[UserResponse])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve users.
    """
    if has_role(current_user, "admin"):
        users = db.query(User).offset(skip).limit(limit).all()
        return users
    return [current_user]

@router.post("/", response_model=UserResponse)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new user. (Admin only)
    """
    if not has_role(current_user, "admin"):
        raise HTTPException(status_code=403, detail="Not authorized to create users")

    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )

    # Resolve the role explicitly instead of trusting hardcoded IDs
    if user_in.role_id is None:
        role = db.query(Role).filter(Role.name == "employee").first()
    else:
        role = db.query(Role).filter(Role.id == user_in.role_id).first()
    if not role:
        raise HTTPException(status_code=400, detail="Invalid role")
    
    user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        role_id=role.id,
        is_active=user_in.is_active,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/roles", response_model=List[RoleSchema])
def read_roles(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    List available roles.
    """
    return db.query(Role).order_by(Role.id).all()

@router.get("/me", response_model=UserResponse)
def read_user_me(
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user
