from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str
    full_name: str
    disabled: bool | None = None


class UserCreate(User):
    password: str


class UserResponse(UserCreate):
    id: str
    