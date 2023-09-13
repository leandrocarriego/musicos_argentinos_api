from passlib.context import CryptContext
from app.core.db_connection import connect_to_database
from app.api.v1.schemas.User import UserCreate, UserResponse


# GET services
async def get_user(username: str):
    try:
        database = await connect_to_database()
        collection = database["users"]

        user = await collection.find_one({"username": username})

        if user:
            return UserResponse(id=str(user["_id"]), **user)

        else:
            raise Exception("User not found")

    except Exception as e:
        raise Exception(
            f"Error retrieving user with the username: {username}. {str(e)}"
        )


# CREATE services
async def create_user(user_data: UserCreate) -> UserResponse:
    bycrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    try:
        database = await connect_to_database()
        collection = database["users"]

        await collection.create_index([("username", 1)], unique=True)

        user = UserCreate(
            username=user_data.username,
            password=bycrypt_context.hash(user_data.password),
            email=user_data.email,
            full_name=user_data.full_name,
            disabled=False,
        )

        new_user = await collection.insert_one(user.dict())

        new_user_id = str(new_user.inserted_id)

        return {"id": new_user_id, **user.dict()}

    except Exception as e:
        raise Exception(f"Error creating user: {str(e)}")