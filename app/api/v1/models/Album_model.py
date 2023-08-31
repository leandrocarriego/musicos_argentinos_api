from typing import List
from pydantic import BaseModel
from .Artist_model import Artist
from .Genre_model import Genre
from bson import ObjectId

class Album(BaseModel):
    name: str
    year: int
    artist_id: str
    