from pydantic import BaseModel


class Album(BaseModel):
    name: str
    year: int
    artist_id: str
    