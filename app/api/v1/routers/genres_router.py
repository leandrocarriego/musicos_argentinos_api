from fastapi import APIRouter, HTTPException
from api.v1.schemas.Genre_schemas import GenreCreate, GenreUpdate, GenreResponse
from api.v1.services.genres_service import (
    create_genre_service,
    get_all_genres_service,
    get_genre_by_id_service,
    update_genre_service,
    delete_genre_service,
)


router = APIRouter(prefix="/genres")

@router.post("/", response_model=GenreResponse)
async def create_genre_route(genre_data: GenreCreate) -> GenreResponse:
    try:
        return await create_genre_service(genre_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=list[GenreResponse])
async def get_all_artists_route() -> list[GenreResponse]:
    try:
        return await get_all_genres_service()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{genre_id}", response_model=GenreResponse)
async def get_one_genre_route(genre_id: str) -> GenreResponse:
    try:
        return await get_genre_by_id_service(genre_id)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{genre_id}", response_model=GenreResponse)
async def udpate_genre_route(genre_id: str, genre_data: GenreUpdate) -> GenreResponse:
    try:
        return await update_genre_service(genre_id, genre_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{genre_id}")
async def delete_genre_route(genre_id: str) -> dict[str, str]:
    try:
        return await delete_genre_service(genre_id)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail={str(e)})
