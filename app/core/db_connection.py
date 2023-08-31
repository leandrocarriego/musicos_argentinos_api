from motor.motor_asyncio import AsyncIOMotorClient
from core.config import settings


async def connect_to_database():
    try:
        client = AsyncIOMotorClient(settings.DB_URI)
        database = client.get_database(settings.MONGO_DB_NAME)
        print("Conexión exitosa a la base de datos.")
        return database
    except Exception as e:
        print(f"Error al conectar a la base de datos: {str(e)}")
        return None


async def get_collection_db(collection_name: str):
    try:
        database = await connect_to_database()
        collection = database[collection_name]
        return collection

    except Exception as e:
        raise Exception(f"Error retrieving collection: {collection_name}. {str(e)}")



