import os
import uvicorn
from fastapi import FastAPI
from app.api.v1.routers.home_router import router as home_router
from app.api.v1.routers.auth_router import router as auth_router
from app.api.v1.routers import router as v1_router
from app.core.db_connection import db
from app.core.cors import add_cors_middleware

app = FastAPI()

add_cors_middleware(app)

app.include_router(home_router)
app.include_router(v1_router)
app.include_router(auth_router)
app.state.database = db

