from fastapi import APIRouter
from .users_router import router as users_router
from .expenses_router import router as expenses_router
from .artists_router import router as artists_router
from .albums_router import router as albums_router
from .genres_router import router as genres_router
from .songs_router import router as songs_router


router = APIRouter(prefix="/api/v1",)

router.include_router(users_router)
router.include_router(expenses_router)

router.include_router(artists_router)
router.include_router(albums_router)
router.include_router(genres_router)
router.include_router(songs_router)

