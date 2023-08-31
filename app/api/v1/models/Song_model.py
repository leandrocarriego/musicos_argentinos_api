from pydantic import BaseModel


class Song(BaseModel):
    name: str
    duration: str
    genre_id: str
    album_id: str
