from fastapi import APIRouter, HTTPException
from api.v1.schemas.Album_schemas import AlbumCreate, AlbumUpdate, AlbumResponse
from api.v1.services.albums_service import (
    create_album_service,
    get_all_albums_service,
    get_album_by_id_service,
    update_album_service,
    delete_album_service,
)


router = APIRouter(prefix="/albums")

@router.post("/", response_model=AlbumResponse)
async def create_album_route(album_data: AlbumCreate) -> AlbumResponse:
    try:
        return await create_album_service(album_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=list[AlbumResponse])
async def get_all_artists_route() -> list[AlbumResponse]:
    try:
        return await get_all_albums_service()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{album_id}", response_model=AlbumResponse)
async def get_one_album_route(album_id: str) -> AlbumResponse:
    try:
        return await get_album_by_id_service(album_id)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{album_id}", response_model=AlbumResponse)
async def udpate_album_route(album_id: str, album_data: AlbumUpdate) -> AlbumResponse:
    try:
        return await update_album_service(album_id, album_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{album_id}")
async def delete_album_route(album_id: str) -> dict[str, str]:
    try:
        return await delete_album_service(album_id)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail={str(e)})