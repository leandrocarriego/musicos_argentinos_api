from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel
from starlette import status
from core.config import settings
from core.db_connection import connect_to_database
from passlib.context import CryptContext
from jose import jwt, JWTError
from api.v1.schemas.Token import Token
from api.v1.schemas.User import UserCreate, UserResponse, User

# router = APIRouter(prefix="/auth", tags=["auth"])

# Esto se ocupa de encriptar la contraseña
bycrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Este es el portador del token, este es el endpoint del token
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


# class User(BaseModel):
#     username: str
#     email: str
#     full_name: str
#     disabled: bool | None = None


# class UserCreate(User):
#     password: str


# class UserResponse(UserCreate):
#     id: str


# class Token(BaseModel):
#     access_token: str
#     token_type: str


# services
async def create_user(user_data: UserCreate) -> UserResponse:
    try:
        database = await connect_to_database()
        collection = database["users"]

        await collection.create_index([("username", 1)], unique=True)

        user = UserCreate(
            username=user_data.username,
            password=bycrypt_context.hash(user_data.password),
            email=user_data.email,
            full_name=user_data.full_name,
            disabled=False,
        )

        new_user = await collection.insert_one(user.dict())

        new_user_id = str(new_user.inserted_id)

        return {"id": new_user_id, **user.dict()}

    except Exception as e:
        raise Exception(f"Error creating user: {str(e)}")


async def get_user(username: str):
    try:
        database = await connect_to_database()
        collection = database["users"]

        user = await collection.find_one({"username": username})

        if user:
            return UserResponse(id=str(user["_id"]), **user)

        else:
            raise Exception("User not found")

    except Exception as e:
        raise Exception(
            f"Error retrieving user with the username: {username}. {str(e)}"
        )


# auth routers
# @router.post(
#     "/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse
# )
# async def create_user_route(user_data: UserCreate):
#     try:
#         user = await get_user(user_data.username)
#         if user:
#             raise HTTPException(
#                 status_code=status.HTTP_409_CONFLICT,
#                 detail=f"Error: the user '{user_data.username}' already exists",
#             )
#     except:
#         pass
    
#     try:
#         return await create_user(user_data)
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))



# Toma la contraseña ingresada por el usuario y la cotraseña encriptada de la db y las compara
def verify_password(plain_password: str, hashed_password: str):
    return bycrypt_context.verify(plain_password, hashed_password)


async def authenticate_user(username: str, password: str):
    """
    Primero: comprueba que el usuario esta en la base de datos
    Segundo: compara la contraseña ingresada con la encriptada de la base de datos
    Finalmente retorna el usuario si esta todo ok
    """
    user = await get_user(username)

    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Recibe la data para codificar
    Si se le paso un tiempo de expiracion se le suma ese tiempo al momento actual
    sino se le da un tiempo de expiracion de 15 minutos
    Se suma a la data para codificar
    Se codifica y retorna el JWT
    """

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    encode_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encode_jwt


token_dependency = Annotated[str, Depends(oauth2_bearer)]


async def get_current_user(token: token_dependency):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Aca se decodifica el JWT
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        user_id: str = payload.get("id")
        username: str = payload.get("sub")

        if username is None or user_id is None:
            raise credentials_exception

        user = await get_user(username)
        return user

    except JWTError:
        raise credentials_exception


auth_dependency = Annotated[User, Depends(get_current_user)]


async def get_current_active_user(current_user: auth_dependency):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user


# Esta ruta se encarga de autenticar el usuario y crear el JWT
# @router.post("/login", response_model=Token)
# async def login_for_access_token(
#     form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
# ):
#     # Se verifica que usuario y contraseña coincidan
#     user = await authenticate_user(form_data.username, form_data.password)

#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     # Tiempo de expiracion de token
#     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

#     access_token = create_access_token(
#         {"sub": user.username, "id": user.id}, access_token_expires
#     )

#     return Token(access_token=access_token, token_type="bearer")


# auth_and_active_dependency = Annotated[User, Depends(get_current_active_user)]


# @router.get("/users/me/")
# async def read_users_me(current_user: auth_and_active_dependency):
#     if current_user is None:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user
