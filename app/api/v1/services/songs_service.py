from core.db_connection import get_collection_db
from api.v1.models.Song_model import Song
from api.v1.schemas.Songs_schemas import SongCreate, SongUpdate, SongResponse
from .genres_service import get_genre_by_id_service
from .albums_service import get_album_by_id_service
from bson import ObjectId


async def create_song_service(song_data: SongCreate) -> SongResponse:
    try:
        collection = await get_collection_db("songs")

        song = Song(
            name=song_data.name,
            duration=song_data.duration,
            genre_id=song_data.genre_id,
            album_id=song_data.album_id,
        )

        new_song = await collection.insert_one(song.dict())

        song_id = str(new_song.inserted_id)

        genre_to_response = await get_genre_by_id_service(song.genre_id)
        album_to_response = await get_album_by_id_service(song.album_id)

        return SongResponse(
            id=song_id,
            genre=genre_to_response,
            artist=album_to_response.artist,
            album=album_to_response,
            **song.dict(),
        )

    except Exception as e:
        raise Exception(f"Error creating song: {str(e)}")


async def get_all_songs_service() -> list[SongResponse]:
    try:
        collection = await get_collection_db("songs")

        songs = []
        async for document in collection.find():
            genre_to_response = await get_genre_by_id_service(document["genre_id"])
            album_to_response = await get_album_by_id_service(document["album_id"])

            song = SongResponse(
                id=str(document["_id"]),
                genre=genre_to_response,
                artist=album_to_response.artist,
                album=album_to_response,
                **document,
            )
            songs.append(song)

        return songs

    except Exception as e:
        raise Exception(f"Error retrieving songs: {str(e)}")


async def get_filtered_songs_service(condition: dict[str, str]) -> list[SongResponse]:
    try:
        collection = await get_collection_db("songs")

        songs = []
        async for document in collection.find(condition):
            song = SongResponse(id=str(document["_id"]), **document)
            songs.append(song)

        return songs

    except Exception as e:
        raise Exception(f"Error retrieving songs: {str(e)}")


async def get_song_by_id_service(song_id: str) -> SongResponse:
    try:
        collection = await get_collection_db("songs")

        song = await collection.find_one({"_id": ObjectId(song_id)})
        if song:
            genre_to_response = await get_genre_by_id_service(song["genre_id"])
            album_to_response = await get_album_by_id_service(song["album_id"])

            return SongResponse(
                id=str(song["_id"]),
                genre=genre_to_response,
                artist=album_to_response.artist,
                album=album_to_response,
                **song,
            )

        else:
            raise Exception("Song not found")

    except Exception as e:
        raise Exception(f"Error retrieving song with the id: {song_id}. {str(e)}")


async def update_song_service(song_id: str, song_data: SongUpdate) -> SongResponse:
    try:
        collection = await get_collection_db("songs")

        data_updated = song_data.dict()

        result_update = await collection.update_one(
            {"_id": ObjectId(song_id)}, {"$set": data_updated}
        )

        if result_update.modified_count is 1:
            updated_song = await collection.find_one({"_id": ObjectId(song_id)})
            if updated_song:
                genre_to_response = await get_genre_by_id_service(
                    updated_song["genre_id"]
                )
                album_to_response = await get_album_by_id_service(
                    updated_song["album_id"]
                )

                return SongResponse(
                    id=str(updated_song["_id"]),
                    genre=genre_to_response,
                    artist=album_to_response.artist,
                    album=album_to_response,
                    **updated_song,
                )

            else:
                raise Exception("Song not found after update")
        else:
            raise Exception("Song update failed")

    except Exception as e:
        raise Exception(f"Error editing song with the id: {song_id}. {str(e)}")


async def delete_song_service(song_id: str) -> dict[str, str]:
    try:
        collection = await get_collection_db("songs")

        await collection.delete_one({"_id": ObjectId(song_id)})

        return {"message": "Song deleted successfully"}

    except Exception as e:
        raise Exception(f"Error deleting song with the id: {song_id}. {str(e)}")
