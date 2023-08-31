from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from api.v1.schemas.User import User
from auth import get_current_active_user

router = APIRouter(prefix="/users", tags=["users"])

auth_and_active_dependency = Annotated[User, Depends(get_current_active_user)]

@router.get("/me/")
async def read_users_me(current_user: auth_and_active_dependency):
    if current_user is None:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
