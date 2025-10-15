from typing import List
from fastapi import HTTPException, status, Depends
from app.utils.auth import get_current_user

def check_roles(allowed_roles: List[str]):
    """
    Dependency creator for role-based authentication.
    Usage:
        @router.get("/", dependencies=[Depends(check_roles(["admin"]))])
    """
    async def role_checker(current_user = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation not permitted. Required roles: {', '.join(allowed_roles)}"
            ) 
        return current_user
    return role_checker