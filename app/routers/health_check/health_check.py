"""Health Check Endpoint."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["health"])
async def health_check():
    """Check the health of the API."""
    return {"message": "API is healthy"}
