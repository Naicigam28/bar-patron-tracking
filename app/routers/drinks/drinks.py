from fastapi import APIRouter, Response, status
from app.utils import search_coctails
from app.schemas import Cocktail

router = APIRouter()

@router.get("/drinks", tags=["Drinks"], status_code=200)
async def get_drinks(search: str):
    """Get all drinks"""
    if search is None or search.strip() == "":
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    results=search_coctails(search)

    if len(results) == 0:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    #convert the results to a list of Cocktail objects
    results = [Cocktail(**result) for result in results]
    return results
    
    