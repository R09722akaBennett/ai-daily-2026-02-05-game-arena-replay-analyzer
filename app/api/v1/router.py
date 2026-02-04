from fastapi import APIRouter

from app.api.v1.routes import health
from app.api.v1.routes import replay_analyzer

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(replay_analyzer.router)
