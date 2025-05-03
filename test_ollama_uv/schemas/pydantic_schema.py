from pydantic import BaseModel, Field
from typing import Optional, List


class RecipeGen(BaseModel):
    ingredients: List[str] = Field(
        ..., description="List of ingredients to include in the recipe."
    )
    title: Optional[str] = Field(None, description="Title of the recipe.")


class RecipeResponse(BaseModel):
    title: str = Field(..., description="Title of the generated recipe.")
    steps: List[str] = Field(..., description="List of steps to prepare the recipe.")
