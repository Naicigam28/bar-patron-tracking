import logging

from fastapi import APIRouter, Query
from typing import Annotated
from app.utils.Session import SessionDep
from app.schemas import ListPatrons, PatronResponse, PostPatron
from app.models import Patron

router = APIRouter()

from typing import Annotated, Literal

from fastapi import FastAPI, Query, Response, status
from pydantic import BaseModel, Field

app = FastAPI()


@router.get("/patrons/", tags=["patrons"], status_code=200)
async def read_patrons(
    session: SessionDep,
    query_params: Annotated[ListPatrons, Query()],
) -> PatronResponse:
    """Retrieve a list of patrons"""
    logging.info(f"Query params: {query_params}")

    current_page = query_params.page
    results_per_page = query_params.per_page
    patrons, total, total_pages = Patron.read_patrons(
        session=session, page=current_page, per_page=results_per_page
    )

    return PatronResponse(
        data=patrons,
        total=total,
        current_page=current_page,
        total_pages=total_pages,
        results_per_page=results_per_page,
    )


@router.get("/patrons/{patron_id}", tags=["patrons"])
async def read_patron(patron_id: int):
    """Retrieve a single patron"""
    return {"username": "fakeuser", "patron_id": patron_id}


@router.post("/patrons/", tags=["patrons"])
async def create_patron(session: SessionDep, request: PostPatron):
    """Create a new patron"""
    new_patron_request = request.model_dump()
    new_patron = Patron(**new_patron_request)
    return new_patron.create_patron(session)


@router.put("/patrons/{patron_id}", tags=["patrons"])
async def update_patron(patron_id: int):
    """Update a patron"""
    return {"username": "fakeuser", "patron_id": patron_id}


@router.delete("/patrons/{patron_id}", tags=["patrons"])
async def delete_patron(patron_id: int):
    return {"username": "fakeuser", "patron_id": patron_id}
