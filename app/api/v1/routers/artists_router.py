from fastapi import APIRouter, HTTPException
from api.v1.schemas.Artist_schemas import ArtistCreate, ArtistUpdate, ArtistResponse
from api.v1.services.artists_service import (
    create_artist_service,
    get_all_artists_service,
    get_artist_by_id_service,
    update_artist_service,
    delete_artist_service,
)


router = APIRouter(prefix="/artists")

@router.post("/", response_model=ArtistResponse)
async def create_artist_route(artist_data: ArtistCreate) -> ArtistResponse:
    try:
        return await create_artist_service(artist_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=list[ArtistResponse])
async def get_all_artists_route() -> list[ArtistResponse]:
    try:
        return await get_all_artists_service()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{artist_id}", response_model=ArtistResponse)
async def get_one_artist_route(artist_id: str) -> ArtistResponse:
    try:
        return await get_artist_by_id_service(artist_id)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{artist_id}", response_model=ArtistResponse)
async def udpate_artist_route(artist_id: str, artist_data: ArtistUpdate) -> ArtistResponse:
    try:
        return await update_artist_service(artist_id, artist_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{artist_id}")
async def delete_artist_route(artist_id: str) -> dict[str, str]:
    try:
        return await delete_artist_service(artist_id)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail={str(e)})
