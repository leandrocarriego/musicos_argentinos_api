from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from starlette import status
from app.core.config import settings
from app.api.v1.schemas.User import UserCreate, UserResponse
from app.api.v1.schemas.Token import Token
from app.auth import authenticate_user, create_access_token, get_user, create_user


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse
)
async def create_user_route(user_data: UserCreate):
    try:
        user = await get_user(user_data.username)
        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Error: the user '{user_data.username}' already exists",
            )
    except:
        pass
    
    try:
        return await create_user(user_data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    # Se verifica que usuario y contraseña coincidan
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Tiempo de expiracion de token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        {"sub": user.username, "id": user.id}, access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")