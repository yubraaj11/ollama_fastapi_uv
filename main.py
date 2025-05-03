import logging
import json
from test_ollama_uv.configs.logging_config import setup_logging
from fastapi import FastAPI
from test_ollama_uv.services.model_class import OllamaModel
from test_ollama_uv.prompts.prompt_templates import SYSTEMPROMPT

from test_ollama_uv.schemas.pydantic_schema import RecipeGen

setup_logging()
logger = logging.getLogger(__name__)

MODEL_NAME = "qwen"

model_obj = OllamaModel(MODEL_NAME)

app = FastAPI()


@app.get("/")
def test_ollama_uv():
    return {"message": "Hello, World!"}


@app.post("/generate")
def generate(userReq: RecipeGen):
    """
    Generate a response using the Ollama model.
    """

    messages = [
        {"role": "system", "content": SYSTEMPROMPT.RECIPE_GEN_SYS_PROMPT},
        {
            "role": "user",
            "content": f"Generate a recipe with the following ingredients: {userReq}",
        },
    ]
    try:
        response = model_obj.generate(user_message=messages)
        logger.info(f"Generated response: {response}")
        return json.loads(response)
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return {"error": "Failed to generate response."}


if __name__ == "__main__":
    import uvicorn
    import os

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))

    uvicorn.run(
        "main:app",  # Use "module:app_variable" format
        host=host,
        port=port,
        reload=True,  # Enable auto-reload
        reload_dirs=["./"],  # Directories to watch for changes
        log_level="info",
    )
