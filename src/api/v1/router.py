from fastapi import APIRouter

from src.api.v1.endpoints import commands, status

API_V1_STR = "/api/v1"

api_router = APIRouter()
api_router.include_router(status.router, tags=["status"])
api_router.include_router(commands.router, tags=["commands"])
