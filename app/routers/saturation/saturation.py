from fastapi import APIRouter
from app.models import Patron, PatronDrink
from app.utils import SessionDep
from app.utils import calculate_bac


router = APIRouter()


@router.get("/saturation/{patron_id}", tags=["Saturation"])
async def saturation_check(session: SessionDep, patron_id: int):
    """Check the saturation of the API."""
    patron = Patron.read_patron(session, patron_id)
    patron_drinks, total, total_pages = PatronDrink.list_patron_drinks(
        session, patron_id, 0, 100
    )
    total_bac = 0.0
    drunk = False
    for drink in patron_drinks:
        drink_bac = calculate_bac(
            patron.weight,
            drink.abv,
            drink.volume,
            patron.gender,
            drink.created_at,
        )
        total_bac += drink_bac
    if total_bac < 0.08:
        drunk = False
    else:
        drunk = True

    message = "Patron is not drunk"
    if drunk:
        message = "Patron is drunk"

    return {
        "message": message,
        "bac": total_bac,
        "patron": patron_id,
        "patron_name": patron.name,
        "patron_weight": patron.weight,
        "drinks_consumed": patron_drinks,
    }


@router.get("/saturation/", tags=["Saturation"])
def get_all_patron_saturation(session: SessionDep):
    """Get all patron saturation levels"""
    patrons = Patron.read_patrons(session, 0, 100, False)
    results = []

    for patron in patrons:
        message = "Patron is not drunk"
        patron_drinks, total, total_pages = PatronDrink.list_patron_drinks(
            session, patron.id, 0, 100
        )
        total_bac = 0.0
        for drink in patron_drinks:
            drink_bac = calculate_bac(
                patron.weight,
                drink.abv,
                drink.volume,
                patron.gender,
                drink.created_at,
            )
        total_bac += drink_bac
        if total_bac > 0.08:
            message = "Patron is drunk"

        results.append(
            {
                "message": message,
                "bac": total_bac,
                "patron": patron.id,
                "patron_name": patron.name,
                "patron_weight": patron.weight,
                "drinks_consumed": patron_drinks,
            }
        )
    return results