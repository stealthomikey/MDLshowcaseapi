from pydantic import BaseModel, HttpUrl, Field, ConfigDict 
from typing import List, Optional

class Ingredient(BaseModel):
    name: str
    measure: str

class MealDB(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )
    
    id: str = Field(..., alias='idMeal')
    name: str = Field(..., alias='strMeal')
    instructions: Optional[str] = Field(None, alias='strInstructions')
    thumbnail_url: Optional[HttpUrl] = Field(None, alias='strMealThumb')
    source_url: Optional[HttpUrl] = Field(None, alias='strSource')
    ingredients: List[Ingredient] = []