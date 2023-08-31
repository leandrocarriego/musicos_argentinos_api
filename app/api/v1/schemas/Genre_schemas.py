from pydantic import BaseModel


class GenreCreate(BaseModel):
    name: str

class GenreUpdate(BaseModel):
    name: str

class GenreResponse(BaseModel):
    id: str
    name: str