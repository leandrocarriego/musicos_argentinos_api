from fastapi import APIRouter, HTTPException
from api.v1.schemas.Songs_schemas import SongCreate, SongUpdate, SongResponse
from api.v1.services.songs_service import (
    create_song_service,
    get_all_songs_service,
    get_song_by_id_service,
    update_song_service,
    delete_song_service,
)


router = APIRouter(prefix="/songs")

# POST routes
@router.post("/", status_code=201, response_model=SongResponse)
async def create_song_route(song_data: SongCreate) -> SongResponse:
    try:
        return await create_song_service(song_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# GET routes
@router.get("/", status_code=200, response_model=list[SongResponse])
async def get_all_songs_route() -> list[SongResponse]:
    try:
        return await get_all_songs_service()

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{song_id}", status_code=200, response_model=SongResponse)
async def get_one_song_route(song_id: str) -> SongResponse:
    try:
        return await get_song_by_id_service(song_id)

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


# PUT routes
@router.put("/{song_id}", status_code=201, response_model=SongResponse)
async def udpate_artist_route(song_id: str, song_data: SongUpdate) -> SongResponse:
    try:
        return await update_song_service(song_id, song_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# DELETE routes
@router.delete("/{song_id}", status_code=200)
async def delete_song_route(song_id: str) -> dict[str, str]:
    try:
        return await delete_song_service(song_id)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail={str(e)})
