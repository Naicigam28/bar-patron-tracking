import requests
import logging
import re

base_url = "https://www.thecocktaildb.com/api/json/v1/1/"
search_url = base_url + "search.php"
lookup_url = base_url + "lookup.php"


CONVERSIONS_RATES = {
    "oz": 29.5735,
    "dl": 100,
    "ml": 1,
    "cl": 10,
    "dash": 0.616186,
    "tsp": 5,
    "tblsp": 15,
    "cup": 240,
    "part": 30,
    "drop": 0.05,
    "pinch": 0.31,
    "splash": 3.697,
    "shot": 44.3603,
    "pint": 473.176,
    "quart": 946.353,
    "gallon": 3785.41,
    "bottle": 750,
}


def fetch_drinks(drink_id: int):
    """Fetch a drink by ID"""
    url = f"{lookup_url}?i={drink_id}"
    response = requests.request("GET", url)
    response_data = response.json()
    drinks_data = response_data.get("drinks", [])
    if drinks_data is None:
        drinks_data = []

    return drinks_data
    
def search_drinks(drink_name: str):
    """Search for a drink by name"""
    response = requests.request("GET", search_url)
    return response.json()


def search_coctails(name: str):
    """Search for a coctail by name"""
    url = search_url + f"?s={name}"
    response = requests.request("GET", url)
    response_data = response.json()
    drinks_data = response_data.get("drinks", [])
    if drinks_data is None:
        drinks_data = []

    return drinks_data
    


def list_all_coctails():
    """List all coctails"""
    response = requests.request("GET", search_url)
    return response.json()


def measure_unit_to_ml(measure: str) -> float:
    """Convert a measure unit to ml"""

    parts = measure.split(" ")
    if len(parts) < 2:
        return 0.0
    values = re.findall(r"\d+", parts[0])
    unit = parts[1]
    
    if unit in CONVERSIONS_RATES.keys() and len(values) > 0:
        result=CONVERSIONS_RATES[unit] * float(values[0])
        result = round(result, 2)
        return result
    return 0.0

def fetch_ingredients(ingredient_name: str):
    """Fetch a raw ingredient data by name"""
    url = f"{search_url}?i={ingredient_name}"
    response = requests.request("GET", url)
    response_data = response.json()
    ingredients_data = response_data.get("ingredients", [])
    if ingredients_data is None:
        ingredients_data = []
    return ingredients_data