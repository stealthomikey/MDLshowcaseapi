# in app/services/mealdb_service.py

import httpx
import asyncio
from typing import List, Dict, Any

class MealServiceError(Exception):
    pass

def _transform_meal_data(raw_meal: Dict[str, Any]) -> Dict[str, Any]:
    # This helper function does not need to be async
    if not raw_meal:
        return {}
    ingredients = []
    for i in range(1, 21):
        ingredient_name = raw_meal.get(f'strIngredient{i}')
        measure = raw_meal.get(f'strMeasure{i}')
        if ingredient_name and ingredient_name.strip():
            ingredients.append({"name": ingredient_name, "measure": measure or ""})
        else:
            break
    return {
        "idMeal": raw_meal.get('idMeal'),
        "strMeal": raw_meal.get('strMeal'),
        "strInstructions": raw_meal.get('strInstructions'),
        "strMealThumb": raw_meal.get('strMealThumb'),
        "strSource": raw_meal.get('strSource'),
        "ingredients": ingredients
    }

# NOTICE THE 'async def' HERE
async def search_meals_by_name(query: str, limit: int = 12) -> List[Dict[str, Any]]:
    api_url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={query}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url)
            response.raise_for_status()
        data = response.json()
        raw_meals = data.get('meals')
        if not raw_meals:
            return []
        transformed_meals = [_transform_meal_data(meal) for meal in raw_meals]
        return transformed_meals[:limit]
    except httpx.RequestError as e:
        raise MealServiceError(f"Error connecting to TheMealDB API: {e}")

# AND 'async def' HERE
async def get_random_meals(count: int = 4) -> List[Dict[str, Any]]:
    api_url = "https://www.themealdb.com/api/json/v1/1/random.php"
    try:
        async with httpx.AsyncClient() as client:
            tasks = [client.get(api_url) for _ in range(count)]
            responses = await asyncio.gather(*tasks)
        meals = []
        for res in responses:
            res.raise_for_status()
            raw_meal = res.json().get('meals')[0]
            meals.append(_transform_meal_data(raw_meal))
        return meals
    except httpx.RequestError as e:
        raise MealServiceError(f"Error connecting to TheMealDB API: {e}")