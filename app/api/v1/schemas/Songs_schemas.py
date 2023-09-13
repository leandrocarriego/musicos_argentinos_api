from typing import Union
from pydantic import BaseModel
from app.api.v1.models.Genre_model import Genre
from app.api.v1.models.Artist_model import Artist
from app.api.v1.schemas.Genre_schemas import GenreResponse
from app.api.v1.schemas.Artist_schemas import ArtistResponse
from app.api.v1.schemas.Album_schemas import AlbumResponse


class Base(BaseModel):
    name: str
    duration: str


class SongCreate(Base):
    genre_id: str
    album_id: str


class SongUpdate(Base):
    genre_id: str
    album_id: str


class SongByGenre(Base):
    id: str
    album: AlbumResponse 


class SongByAlbum(Base):
    id: str
    genre: GenreResponse


class SongResponse(Base):
    id: str
    genre: GenreResponse
    album: AlbumResponse


