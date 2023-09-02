from pydantic import BaseModel


class ArtistCreate(BaseModel):
    name: str
    birthdate: str


class ArtistUpdate(BaseModel):
    name: str
    birthdate: str


class ArtistResponse(ArtistUpdate):
    id: str