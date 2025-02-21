import logging

from fastapi import APIRouter, Query
from typing import Annotated

from app.schemas import ListPatrons

router = APIRouter()

from typing import Annotated, Literal

from fastapi import FastAPI, Query, Response,status
from pydantic import BaseModel, Field

app = FastAPI()


@router.get("/patrons/", tags=["patrons"], status_code=200)
async def read_patrons(
    query_params: Annotated[ListPatrons, Query()], response: Response
):
    """Retrieve a list of patrons"""
    logging.info(f"Query params: {query_params}")
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/patrons/{patron_id}", tags=["patrons"])
async def read_patron(patron_id: int):
    """Retrieve a single patron"""
    return {"username": "fakeuser", "patron_id": patron_id}


@router.post("/patrons/", tags=["patrons"])
async def create_patron():
    """Create a new patron"""
    return {"username": "fakeuser"}


@router.put("/patrons/{patron_id}", tags=["patrons"])
async def update_patron(patron_id: int):
    """Update a patron"""
    return {"username": "fakeuser", "patron_id": patron_id}


@router.delete("/patrons/{patron_id}", tags=["patrons"])
async def delete_patron(patron_id: int):
    return {"username": "fakeuser", "patron_id": patron_id}
