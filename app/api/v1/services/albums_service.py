from core.db_connection import get_collection_db
from api.v1.models.Album_model import Album
from api.v1.schemas.Album_schemas import AlbumCreate, AlbumUpdate, AlbumResponse
from .artists_service import get_artist_by_id_service
from bson import ObjectId


async def create_album_service(album_data: AlbumCreate) -> AlbumResponse:
    try:
        albums_collection = await get_collection_db("albums")

        artist_to_response = await get_artist_by_id_service(album_data.artist_id)

        album = Album(
            name = album_data.name,
            year = album_data.year,
            artist_id = album_data.artist_id
        )

        new_album = await albums_collection.insert_one(album.dict())

        album_id = str(new_album.inserted_id)

        return AlbumResponse(id=album_id, artist=artist_to_response, **album.dict())

    except Exception as e:
        raise Exception(f"Error creating album: {str(e)}")


async def get_all_albums_service() -> list[AlbumResponse]:
    try:
        collection = await get_collection_db("albums")

        albums = []
        async for document in collection.find():
            artist_to_response = await get_artist_by_id_service(document["artist_id"])

            album = AlbumResponse(id=str(document["_id"]), artist=artist_to_response, **document)
            albums.append(album)

        return albums

    except Exception as e:
        raise Exception(f"Error retrieving albums: {str(e)}")


async def get_album_by_id_service(album_id: str) -> AlbumResponse:
    try:
        collection = await get_collection_db("albums")

        album = await collection.find_one({"_id": ObjectId(album_id)})
        if album:
            artist_to_response = await get_artist_by_id_service(album["artist_id"])

            return AlbumResponse(id=str(album["_id"]), artist=artist_to_response, **album)

        else:
            raise Exception("Album not found")

    except Exception as e:
        raise Exception(f"Error retrieving album with the id: {album_id}. {str(e)}")


async def update_album_service(album_id: str, album_data: AlbumUpdate) -> AlbumResponse:
    try:
        collection = await get_collection_db("albums")

        data_updated = album_data.dict()

        result_update = await collection.update_one(
            {"_id": ObjectId(album_id)}, {"$set": data_updated}
        )

        if result_update.modified_count is 1:
            updated_album = await collection.find_one({"_id": ObjectId(album_id)})
            if updated_album:
                artist_to_response = await get_artist_by_id_service(updated_album["artist_id"])

                return AlbumResponse(id=str(updated_album["_id"]), artist=artist_to_response, **updated_album)

            else:
                raise Exception("Album not found after update")
        else:
            raise Exception("Album update failed")

    except Exception as e:
        raise Exception(f"Error editing album with the id: {album_id}. {str(e)}")


async def delete_album_service(album_id: str) -> dict[str, str]:
    try:
        collection = await get_collection_db("albums")

        await collection.delete_one({"_id": ObjectId(album_id)})

        return {"message": "Album deleted successfully"}

    except Exception as e:
        raise Exception(f"Error deleting album with the id: {album_id}. {str(e)}")
