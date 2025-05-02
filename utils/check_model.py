from test_ollama_uv.configs.logging_config import setup_logging
import logging
import os
import httpx
import time

setup_logging()
logger = logging.getLogger(__name__)

# Get Ollama host from environment variable with default
# OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

async def check_model_async(model_name):
    """Asynchronous version of check_model function"""
    try:
        async with httpx.AsyncClient() as client:
            # List available models
            response = await client.get(
                f"{OLLAMA_HOST}/api/tags",
                timeout=30.0
            )
            logger.info(f"Response: {response.text}")
            
            if response.status_code != 200:
                logger.error(f"Failed to list models. Status code: {response.status_code}")
                logger.error(f"Response: {response.text}")
                return False
            
            available_models = response.json().get("models", [])
            clean_model_list = [model["name"] for model in available_models]
            logger.info(f"Available models: {clean_model_list}")
            
            if model_name in clean_model_list:
                logger.info(f"Model {model_name} is available.")
                return True
            else:
                logger.error(f"Model {model_name} is not available. Pulling the model.")
                
                # Pull the model
                pull_response = await client.post(
                    f"{OLLAMA_HOST}/api/pull",
                    json={"name": model_name},
                    timeout=600.0  # 10 minute timeout for pulling models
                )
                
                if pull_response.status_code != 200:
                    logger.error(f"Failed to pull model. Status code: {pull_response.status_code}")
                    logger.error(f"Response: {pull_response.text}")
                    return False
                
                logger.info(f"Model {model_name} pulled successfully.")
                return True
                
    except Exception as e:
        logger.error(f"Error checking/pulling model: {str(e)}")
        return False

def check_model(model_name):
    """
    Check if a model exists and pull it if it doesn't.
    This is a synchronous wrapper around the async function.
    """
    try:
        # Create a new event loop for the synchronous context
        import asyncio
        
        # For Python 3.7+
        try:
            return asyncio.run(check_model_async(model_name))
        except RuntimeError:
            # If there's already an event loop running, use a different approach
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(check_model_async(model_name))
            finally:
                loop.close()
                
    except Exception as e:
        logger.error(f"Failed during model check: {str(e)}")
        return False
    