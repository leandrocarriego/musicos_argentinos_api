from fastapi import APIRouter, HTTPException
from app.api.v1.models.Artist_model import Artist
from app.api.v1.schemas.Artist_schemas import ArtistCreate, ArtistUpdate, ArtistResponse
from app.api.v1.schemas.Album_schemas import AlbumByArtist
from app.api.v1.services.artists_service import (
    create_artist_service,
    get_all_artists_service,
    get_artist_by_id_service,
    update_artist_service,
    delete_artist_service,
)
from app.api.v1.services.albums_service import get_albums_by_artist_service


router = APIRouter(prefix="/artists")

# POST routes
@router.post("/", status_code=201, response_model=ArtistResponse)
async def create_artist_route(artist_data: ArtistCreate) -> ArtistResponse:
    try:
        return await create_artist_service(artist_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# GET routes
@router.get("/", status_code=200, response_model=list[Artist])
async def get_all_artists_route() -> list[Artist]:
    try:
        return await get_all_artists_service()

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{artist_id}", status_code=200, response_model=ArtistResponse)
async def get_one_artist_route(artist_id: str) -> ArtistResponse:
    try:
        return await get_artist_by_id_service(artist_id)

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{artist_id}/albums", status_code=200, response_model=list[AlbumByArtist])
async def get_one_artist_route(artist_id: str) -> list[AlbumByArtist]:
    try:
        return await get_albums_by_artist_service(artist_id)

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


# PUT routes
@router.put("/{artist_id}", status_code=201, response_model=ArtistResponse)
async def udpate_artist_route(artist_id: str, artist_data: ArtistUpdate) -> ArtistResponse:
    try:
        return await update_artist_service(artist_id, artist_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# DELETE routes
@router.delete("/{artist_id}", status_code=200)
async def delete_artist_route(artist_id: str) -> dict[str, str]:
    try:
        return await delete_artist_service(artist_id)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail={str(e)})
