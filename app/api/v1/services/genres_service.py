from core.db_connection import get_collection_db
from api.v1.models.Genre_model import Genre
from api.v1.schemas.Genre_schemas import GenreCreate, GenreUpdate, GenreResponse
from bson import ObjectId


# GET services
async def get_all_genres_service() -> list[GenreResponse]:
    try:
        collection = await get_collection_db("genres")

        genres = []
        async for document in collection.find():
            genre = GenreResponse(id=str(document["_id"]), **document)
            genres.append(genre)

        return genres

    except Exception as e:
        raise Exception(e)


async def get_genre_by_id_service(genre_id: str) -> GenreResponse:
    try:
        collection = await get_collection_db("genres")

        genre = await collection.find_one({"_id": ObjectId(genre_id)})
        if genre:
            return GenreResponse(id=str(genre["_id"]), **genre)

        else:
            raise Exception("Genre not found")

    except Exception as e:
        raise Exception(f"Error retrieving genre with the id: {genre_id}. {str(e)}")


# CREATE services
async def create_genre_service(genre_data: GenreCreate) -> GenreResponse:
    try:
        collection = await get_collection_db("genres")

        genre = Genre(name=genre_data.name)

        new_genre = await collection.insert_one(genre.dict())

        genre_id = str(new_genre.inserted_id)

        return GenreResponse(id=genre_id, **genre.dict())

    except Exception as e:
        raise Exception(f"Error creating genre: {str(e)}")


# UPDATE services
async def update_genre_service(genre_id: str, genre_data: GenreUpdate) -> GenreResponse:
    try:
        collection = await get_collection_db("genres")

        data_updated = genre_data.dict()

        result_update = await collection.update_one(
            {"_id": ObjectId(genre_id)}, {"$set": data_updated}
        )

        if result_update.modified_count is 1:
            updated_genre = await collection.find_one({"_id": ObjectId(genre_id)})
            if updated_genre:
                return GenreResponse(id=str(updated_genre["_id"]), **updated_genre)

            else:
                raise Exception("Genre not found after update")
        else:
            raise Exception("Genre update failed")

    except Exception as e:
        raise Exception(f"Error editing genre with the id: {genre_id}. {str(e)}")


# DELETE services
async def delete_genre_service(genre_id: str) -> dict[str, str]:
    try:
        collection = await get_collection_db("genres")

        await collection.delete_one({"_id": ObjectId(genre_id)})

        return {"message": "Genre deleted successfully"}

    except Exception as e:
        raise Exception(f"Error deleting genre with the id: {genre_id}. {str(e)}")
