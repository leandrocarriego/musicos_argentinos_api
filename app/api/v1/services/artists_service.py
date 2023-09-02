from core.db_connection import get_collection_db
from api.v1.models.Artist_model import Artist
from api.v1.schemas.Artist_schemas import ArtistCreate, ArtistUpdate, ArtistResponse
from bson import ObjectId


# GET services
async def get_all_artists_service() -> list[ArtistResponse]:
    try:
        collection = await get_collection_db("artists")

        artists = []
        async for document in collection.find():
            artist = ArtistResponse(id=str(document["_id"]), **document)
            artists.append(artist)

        return artists
    
    except Exception as e:
        raise Exception(e)


async def get_artist_by_id_service(artist_id: str) -> ArtistResponse:
    try:
        collection = await get_collection_db("artists")

        artist = await collection.find_one({"_id": ObjectId(artist_id)})
        if artist:
            return ArtistResponse(id=str(artist["_id"]), **artist)
            
        else:
            raise Exception("Artist not found")
    
    except Exception as e:
        raise Exception(f"Error retrieving artist with the id: {artist_id}. {str(e)}")


# CREATE services
async def create_artist_service(artist_data: ArtistCreate) -> ArtistResponse:
    try:
        collection = await get_collection_db("artists")

        artist = Artist(
            name = artist_data.name,
            birthdate = artist_data.birthdate
        )

        new_artist = await collection.insert_one(artist.dict())

        artist_id = str(new_artist.inserted_id)

        return ArtistResponse(id=artist_id, **artist.dict())

    except Exception as e:
        raise Exception(f"Error creating artist: {str(e)}")
    

# UPDATE services 
async def update_artist_service(artist_id: str, artist_data: ArtistUpdate) -> ArtistResponse:
    try:
        collection = await get_collection_db("artists")

        data_updated = artist_data.dict()

        result_update = await collection.update_one(
            {"_id": ObjectId(artist_id)},
            {"$set": data_updated}
            )

        if result_update.modified_count is 1:
            updated_artist = await collection.find_one({"_id": ObjectId(artist_id)})
            if updated_artist:
                return ArtistResponse(id=str(updated_artist["_id"]), **updated_artist)

            else:
                raise Exception("Artist not found after update")
        else:
            raise Exception("Artist update failed")

    except Exception as e:
        raise Exception(f"Error editing artist with the id: {artist_id}. {str(e)}")


# DELETE services
async def delete_artist_service(artist_id: str) -> dict[str, str]:
    try:
        collection = await get_collection_db("artists")

        await collection.delete_one({"_id": ObjectId(artist_id)})    

        return {"message": "Artist deleted successfully"}

    except Exception as e:
        raise Exception(f"Error deleting artist with the id: {artist_id}. {str(e)}")

        

