from pydantic import BaseModel, Field
from typing import Optional
import requests

from datetime import datetime
from app.models import Patron
from app.utils import measure_unit_to_ml, fetch_ingredients


base_url = "https://www.thecocktaildb.com/api/json/v1/1/"
search_url = base_url + "search.php"
lookup_url = base_url + "lookup.php"


class Ingredient(BaseModel):
    """Used to transform the data from the API into a Pydantic model."""

    ingredient_name: str
    ingredient_measure: str
    ingredient_measure_ml: float
    ingredient_alcoholic: bool = False
    ingredient_type: Optional[str] = None
    ingriedient_id: Optional[int] = None
    ingredient_abv: Optional[float] = None

    def __init__(self, **data):
        temp = {}
        temp["ingredient_name"] = data["name"]
        temp["ingredient_measure"] = data["measure"]
        temp["ingredient_measure_ml"] = measure_unit_to_ml(data["measure"])

        ingredient_data = fetch_ingredients(temp["ingredient_name"])
        if ingredient_data:

            if len(ingredient_data) > 0:

                ingredient = ingredient_data[0]
                temp["ingredient_alcoholic"] = ingredient["strAlcohol"] == "Yes"
                temp["ingredient_type"] = ingredient["strType"]
                temp["ingriedient_id"] = ingredient["idIngredient"]
                temp["ingredient_abv"] = ingredient["strABV"]

        super().__init__(**temp)


class Cocktail(BaseModel):
    """Used to transform the data from the API into a Pydantic model."""

    id: int
    name: str
    ingredients: list[Ingredient]
    instructions: str
    glass: str
    category: str
    alcoholic: str
    image: str
    volume: float = 0.0
    abv: float = 0.0

    def __init__(self, **data):
        temp = {}
        temp["ingredients"] = []
        for i in range(1, 16):
            if f"strIngredient{i}" in data:
                ingredient_name = data.get(f"strIngredient{i}")
                ingredient_measure = data.get(f"strMeasure{i}")
                is_valid_name = (
                    ingredient_name is not None and ingredient_name.strip() != ""
                )
                is_valid_measure = (
                    ingredient_measure is not None and ingredient_measure.strip() != ""
                )
                if is_valid_name and is_valid_measure:
                    temp["ingredients"].append(
                        Ingredient(name=ingredient_name, measure=ingredient_measure)
                    )
        temp["id"] = data["idDrink"]
        temp["name"] = data["strDrink"]
        temp["instructions"] = data["strInstructions"]
        temp["glass"] = data["strGlass"]
        temp["category"] = data["strCategory"]
        temp["alcoholic"] = data["strAlcoholic"]
        temp["image"] = data["strDrinkThumb"]
        super().__init__(**temp)
        self.calculate_volume()
        self.calculate_abv()

    def calculate_abv(self):
        """Calculate the ABV of a cocktail."""

        total_volume = self.volume
        total_abv = 0.0
        for ingredient in self.ingredients:
            ingredient_abv = ingredient.ingredient_abv
            ingredient_measure_ml = ingredient.ingredient_measure_ml
            if ingredient_abv is None:
                ingredient_abv = 0.0
            if ingredient_measure_ml is None:
                ingredient_measure_ml = 0.0
            total_abv += ingredient_abv * (
                ingredient.ingredient_measure_ml / total_volume
            )
        total_abv = round(total_abv, 2)
        self.abv = total_abv
        return total_abv

    def calculate_volume(self):
        """Calculate the volume of a cocktail. In ml"""
        self.volume = 0.0
        for ingredient in self.ingredients:

            self.volume += ingredient.ingredient_measure_ml
        return self.volume
