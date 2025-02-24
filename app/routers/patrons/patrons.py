from fastapi.logger import logger

from fastapi import APIRouter, Query
from typing import Annotated
from app.utils.session import SessionDep
from app.schemas import ListPatrons, PatronResponse, PostPatron, Cocktail
from app.models import Patron, PatronDrink
from app.utils import fetch_drinks

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
    logger.info(f"Query params: {query_params}")

    current_page = query_params.page
    results_per_page = query_params.per_page

    if current_page < 0 or results_per_page < 0:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

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
async def read_patron(session: SessionDep, patron_id: int):
    """Retrieve a single patron"""
    patron = Patron.read_patron(session, patron_id)
    if not patron:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    patron = Patron.read_patron(session, patron_id)
    return patron


@router.post("/patrons/", tags=["patrons"])
async def create_patron(session: SessionDep, request: PostPatron):
    """Create a new patron"""
    new_patron_request = request.model_dump()
    new_patron = Patron(**new_patron_request)
    return new_patron.create_patron(session)


@router.put("/patrons/{patron_id}", tags=["patrons"])
async def update_patron(session: SessionDep, patron_id: int, request: PostPatron):
    """Update a patron"""
    mod_req = request.model_dump()
    patron = Patron.read_patron(session, patron_id)
    if not patron:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return Patron.update_patron(session, patron_id, mod_req)


@router.delete("/patrons/{patron_id}", tags=["patrons"])
async def delete_patron(session: SessionDep, patron_id: int):
    """Delete a patron"""
    patron = Patron.read_patron(session, patron_id)
    if not patron:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return Patron.delete_patron(session, patron_id)


@router.get("/patrons/{patron_id}/drinks", tags=["Drinks"])
async def list_patron_drinks(
    session: SessionDep, patron_id: int, query_params: Annotated[ListPatrons, Query()]
):
    """List all drinks for a patron"""
    current_page = query_params.page
    results_per_page = query_params.per_page
    if current_page == None or results_per_page == None:
        current_page = 0
        results_per_page = 25

    if current_page < 0 or results_per_page < 0:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

    patron_drinks, total, total_pages = PatronDrink.list_patron_drinks(
        session, patron_id, current_page, results_per_page
    )
    return PatronResponse(
        data=patron_drinks,
        total=total,
        current_page=current_page,
        total_pages=total_pages,
        results_per_page=results_per_page,
    )


@router.post("/patrons/{patron_id}/drinks/{drink_id}", tags=["Drinks"])
async def add_drink_to_patron(
    session: SessionDep,
    patron_id: int,
    drink_id: int,
):
    """Add a drink to a patron"""
    logger.info(f"Patron ID: {patron_id}")
    logger.info(f"Drink ID: {drink_id}")

    data = {"patron_id": patron_id, "drink_id": drink_id}

    if drink_id:
        drink = fetch_drinks(drink_id)
        # convert drink dict to Cocktail object
        if drink:
            drink = Cocktail(**drink[0])
            data["abv"] = drink.abv
            data["alcohol_type"] = drink.alcoholic
            data["volume"] = drink.volume

        patron_drink = PatronDrink(**data)
        patron_drink.create_patron_drink(session)
        logger.info(f"Drink: {drink}")
        return drink
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
