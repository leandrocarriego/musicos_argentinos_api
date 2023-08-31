from typing import List
from pydantic import BaseModel
from api.v1.schemas.Artist_schemas import ArtistResponse



class AlbumCreate(BaseModel):
    name: str
    year: str
    artist_id: str


class AlbumUpdate(BaseModel):
    name: str
    year: str
    artist_id: str


class AlbumResponse(BaseModel):
    id: str
    name: str
    year: str
    artist: ArtistResponse