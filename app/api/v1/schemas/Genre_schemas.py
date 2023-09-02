from pydantic import BaseModel


class GenreCreate(BaseModel):
    name: str


class GenreUpdate(BaseModel):
    name: str


class GenreResponse(GenreUpdate):
    id: str