import ollama
from test_ollama_uv.configs.logging_config import setup_logging
import logging
from utils.check_model import check_model
from test_ollama_uv.schemas.pydantic_schema import RecipeResponse

setup_logging()
logger = logging.getLogger(__name__)


class OllamaModel:
    def __init__(self, model_name: str = "qwen:1.8b"):
        self.model_name = model_name
        
        # Make sure the model_name is not None before checking
        if self.model_name is not None:
            # Check if the model exists, and if not, try to pull it
            if not check_model(self.model_name):
                logger.warning(f"Model {self.model_name} not available locally. Attempting to pull...")
                # Add code to pull the model here
                # You can uncomment the pull code in your check_model_async function
                # Or implement a direct pull here:
                try:
                    # Directly pull using ollama client
                    ollama.pull(self.model_name)
                    logger.info(f"Successfully pulled model {self.model_name}")
                except Exception as e:
                    logger.error(f"Failed to pull model {self.model_name}: {e}")
            
            # Initialize model after ensuring it exists (or after pull attempt)
            try:
                self.model = ollama.Model(model_name)
                logger.info(f"Model {self.model_name} loaded successfully.")
            except Exception as e:
                logger.error(f"Error loading model {self.model_name}: {e}")
        else:
            logger.error("No model name provided.")
    
    def generate(self, user_message):
        """
        Generate a response using the Ollama model.
        """
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=user_message,
                format=RecipeResponse.model_json_schema(),
                options={
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "frequency_penalty": 0.5,
                    "presence_penalty": 0.5,
                },
            )
            return response.message.content
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {"error": f"Failed to generate response: {str(e)}"}