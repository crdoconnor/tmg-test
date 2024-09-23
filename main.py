from fastapi import FastAPI
from http.client import OK
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from jinja2 import Environment, BaseLoader
from pathlib import Path
import json

load_dotenv()

app = FastAPI()

import nest_asyncio

nest_asyncio.apply()


class RecipeRequest(BaseModel):
    full_text: str


class RecipeResponse(BaseModel):
    Ingredient: str
    DishType: str
    MealType: str
    Occasion: str
    Cuisine: str
    Dietary: str


TAG_FOLDER = Path(__file__).parent.joinpath("tags")
INGREDIENTS = TAG_FOLDER.joinpath("ingredients.txt").read_text().split("\n")
DIETARY = TAG_FOLDER.joinpath("dietary.txt").read_text().split("\n")
CUISINE = TAG_FOLDER.joinpath("cuisine.txt").read_text().split("\n")
OCCASION = TAG_FOLDER.joinpath("occasion.txt").read_text().split("\n")
MEAL_TYPE = TAG_FOLDER.joinpath("meal-type.txt").read_text().split("\n")
DISH_TYPE = TAG_FOLDER.joinpath("dish-type.txt").read_text().split("\n")


def recipe_prompt():
    template = Environment(loader=BaseLoader).from_string(
        Path(__file__).parent.joinpath("system.txt").read_text()
    )
    return template.render(
        ingredients="\n".join(INGREDIENTS),
        dietary="\n".join(DIETARY),
        cuisine="\n".join(CUISINE),
        occasion="\n".join(OCCASION),
        meal_type="\n".join(MEAL_TYPE),
        dish_type="\n".join(DISH_TYPE),
    )


def validation_errors(json_response):
    errors = []
    if json_response["Ingredient"] not in INGREDIENTS:
        errors.append(
            f"Ingredient '{json_response['Ingredient']}' is not, in the list of ingredients, please try again with an ingredient from the list"
        )
    if json_response["Dietary"] not in DIETARY:
        errors.append(
            f"Dietary category '{json_response['Dietary']}' is not, in the dietary category list, please try again with a dietary category from the list"
        )
    if json_response["Cuisine"] not in CUISINE:
        errors.append(
            "Cuisine '{json_response['Cuisine']}' is not, in the list of ingredients, please try again with an cuisine from the list"
        )
    if json_response["Occasion"] not in OCCASION:
        errors.append(
            "Occasion '{json_response['Occasion']}' is not, in the list of ingredients, please try again with an occasion from the list"
        )
    if json_response["MealType"] not in MEAL_TYPE:
        errors.append(
            "Meal type '{json_response['MealType']}' is not, in the list of ingredients, please try again with a meal type from the list"
        )
    if json_response["DishType"] not in DISH_TYPE:
        errors.append(
            "Dish type '{json_response['DishType']}' is not, in the list of ingredients, please try again with an meal type from the list"
        )

    return errors


@app.post("/", response_model=RecipeResponse, status_code=OK)
async def recipe(request: RecipeRequest):
    chat = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), temperature=0.0)

    messages = [
        SystemMessage(content=recipe_prompt()),
        HumanMessage(content=request.full_text),
    ]

    for _ in range(5):
        ai_message = chat(messages)
        json_response = json.loads(ai_message.content)
        errors = validation_errors(json_response)
        if len(errors) == 0:
            break
        messages.append(ai_message)
        messages.append(HumanMessage(content="\n".join(errors)))

    return RecipeResponse(
        Ingredient=json_response["Ingredient"],
        DishType=json_response["DishType"],
        MealType=json_response["MealType"],
        Occasion=json_response["Occasion"],
        Cuisine=json_response["Cuisine"],
        Dietary=json_response["Dietary"],
    )
