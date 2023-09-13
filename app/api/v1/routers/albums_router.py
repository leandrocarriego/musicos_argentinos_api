from fastapi import APIRouter, HTTPException
from app.api.v1.schemas.Album_schemas import AlbumCreate, AlbumUpdate, AlbumResponse
from app.api.v1.schemas.Songs_schemas import SongByAlbum
from app.api.v1.services.albums_service import (
    create_album_service,
    get_all_albums_service,
    get_album_by_id_service,
    update_album_service,
    delete_album_service,
)
from app.api.v1.services.songs_service import get_songs_by_album_service


router = APIRouter(prefix="/albums")

# POST routes
@router.post("/", status_code=201, response_model=AlbumResponse)
async def create_album_route(album_data: AlbumCreate) -> AlbumResponse:
    try:
        return await create_album_service(album_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# GET routes
@router.get("/", status_code=200, response_model=list[AlbumResponse])
async def get_all_artists_route() -> list[AlbumResponse]:
    try:
        return await get_all_albums_service()

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{album_id}", status_code=200, response_model=AlbumResponse)
async def get_one_album_route(album_id: str) -> AlbumResponse:
    try:
        return await get_album_by_id_service(album_id)

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{album_id}/songs", status_code=200, response_model=list[SongByAlbum])
async def get_one_album_route(album_id: str) -> list[SongByAlbum]:
    try:
        return await get_songs_by_album_service(album_id)

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


# PUT routes
@router.put("/{album_id}", status_code=201, response_model=AlbumResponse)
async def udpate_album_route(album_id: str, album_data: AlbumUpdate) -> AlbumResponse:
    try:
        return await update_album_service(album_id, album_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# DELETE routes
@router.delete("/{album_id}", status_code=200)
async def delete_album_route(album_id: str) -> dict[str, str]:
    try:
        return await delete_album_service(album_id)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail={str(e)})