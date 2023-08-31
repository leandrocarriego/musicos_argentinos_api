from typing import Union
from pydantic import BaseModel
from api.v1.models.Genre_model import Genre
from api.v1.models.Artist_model import Artist
from api.v1.schemas.Genre_schemas import GenreResponse
from api.v1.schemas.Artist_schemas import ArtistResponse
from api.v1.schemas.Album_schemas import AlbumResponse


class SongCreate(BaseModel):
    name: str
    duration: str
    genre_id: str
    album_id: str


class SongUpdate(BaseModel):
    name: str
    duration: str
    genre_id: str
    album_id: str


class SongResponse(BaseModel):
    id: str
    name: str
    duration: str
    genre: GenreResponse
    artist: ArtistResponse
    album: AlbumResponse
