from datetime import datetime
from pydantic import BaseModel

class Artist(BaseModel):
    name: str
    birthdate: str
