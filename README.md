# FastAPI Ollama and Uv

A modern API application using FastAPI framework, Ollama for LLM capabilities, and Uv package manager.

## Getting started

a. Clone this repo
```bash
git clone git@github.com:yubraaj11/ollama_fastapi_uv.git
cd ollama_fastapi_uv
```

b. Download packages
```bash
uv sync
```

c. Copy `.env.example` > `.env`
```bash
cp .env.example .env
```

## Running Locally

```bash
uv run main.py
```

Or use the uvicorn runner directly:

```bash
uvicorn main:app --reload
```

## Running Using Docker

```bash
sudo docker compose up
```

## Docker Setup Process
When running the application with Docker for the first time:

- Docker will download the Ollama container image
- The FastAPI application image will be built
- On initial startup, Ollama will download the LLM model (qwen:1.8b by default)
- Model download may take several minutes depending on your internet connection
- Once the model is downloaded, the application will be ready to use
- Subsequent startups will be much faster as the model is cached

## API Documentation

Once running, FastAPI automatically generates interactive API documentation. Access it at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc



## Resources

- [FastAPI Official Documentation](https://fastapi.tiangolo.com/)
- [Ollama GitHub Repository](https://github.com/ollama/ollama)
- [Uv Python Package Manager](https://github.com/astral-sh/uv)

## Troubleshooting

If you encounter issues with the Docker setup:

1. Check that ports 8000 and 11434 are not already in use
2. Verify the Ollama health check is passing (`docker ps` should show "healthy")
3. For "no module named" errors, rebuild the FastAPI container: `docker compose build fastapi`
