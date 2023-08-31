from datetime import datetime
from pydantic import BaseModel


class ArtistCreate(BaseModel):
    name: str
    birthdate: str

class ArtistUpdate(BaseModel):
    name: str
    birthdate: str

class ArtistResponse(BaseModel):
    id: str
    name: str
    birthdate: str