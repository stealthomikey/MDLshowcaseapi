# app/routers/meals.py

from fastapi import APIRouter, Query, HTTPException, status
from typing import List, Annotated

# Import the new service functions and the schema
from app.services.mealdb_service import search_meals_by_name, get_random_meals
from app.schemas import MealDB

router = APIRouter(
    prefix="/meals",
    tags=["Meals (TheMealDB)"]
)

SearchQuery = Annotated[
    str,
    Query(min_length=2, description="Meal name.")
]

@router.get("/suggestions", response_model=List[MealDB])
async def get_meal_suggestions():
    return await get_random_meals(count=4)



@router.get("/search", response_model=List[MealDB])
async def search_meals(query: SearchQuery):
    meals = await search_meals_by_name(query=query, limit=12)
    if not meals:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No meals found matching '{query}'."
        )
    return meals