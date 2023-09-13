from fastapi import APIRouter, HTTPException
from app.api.v1.schemas.Genre_schemas import GenreCreate, GenreUpdate, GenreResponse
from app.api.v1.schemas.Songs_schemas import SongByGenre
from app.api.v1.services.genres_service import (
    create_genre_service,
    get_all_genres_service,
    get_genre_by_id_service,
    update_genre_service,
    delete_genre_service,
)
from app.api.v1.services.songs_service import get_songs_by_genre_service


router = APIRouter(prefix="/genres")

# POST routes
@router.post("/", status_code=201, response_model=GenreResponse)
async def create_genre_route(genre_data: GenreCreate) -> GenreResponse:
    try:
        return await create_genre_service(genre_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# GET routes
@router.get("/", status_code=200, response_model=list[GenreResponse])
async def get_all_artists_route() -> list[GenreResponse]:
    try:
        return await get_all_genres_service()

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{genre_id}", status_code=200, response_model=GenreResponse)
async def get_one_genre_route(genre_id: str) -> GenreResponse:
    try:
        return await get_genre_by_id_service(genre_id)

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    

@router.get("/{genre_id}/songs", status_code=200, response_model=list[SongByGenre])
async def get_all_artists_route(genre_id: str) -> list[SongByGenre]:
    try:
        return await get_songs_by_genre_service(genre_id)
    
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


# PUT routes
@router.put("/{genre_id}", status_code=201, response_model=GenreResponse)
async def udpate_genre_route(genre_id: str, genre_data: GenreUpdate) -> GenreResponse:
    try:
        return await update_genre_service(genre_id, genre_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# DELETE routes
@router.delete("/{genre_id}", status_code=200)
async def delete_genre_route(genre_id: str) -> dict[str, str]:
    try:
        return await delete_genre_service(genre_id)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail={str(e)})
