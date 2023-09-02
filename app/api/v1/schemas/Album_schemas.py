from typing import List
from pydantic import BaseModel
from api.v1.schemas.Artist_schemas import ArtistResponse


class Base(BaseModel):
    name: str
    year: str


class AlbumCreate(Base):
    artist_id: str


class AlbumUpdate(Base):
    artist_id: str


class AlbumByArtist(Base):
    id: str


class AlbumResponse(AlbumByArtist):
    artist: ArtistResponse