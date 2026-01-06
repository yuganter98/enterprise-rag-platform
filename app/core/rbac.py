from typing import Any

def has_role(user: Any, role_name: str) -> bool:
    """
    Checks if the user has a specific role.
    Expects user object to have a 'role' attribute with a 'name' property.
    """
    if not user or not user.role:
        return False
    return user.role.name == role_name

def is_admin(user: Any) -> bool:
    """Check if user has 'admin' role."""
    return has_role(user, "admin")

def is_hr(user: Any) -> bool:
    """Check if user has 'hr' role."""
    return has_role(user, "hr")
