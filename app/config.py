import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application configuration loaded from environment variables."""

    # Qdrant configuration
    QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")

    # Google Gemini configuration
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    # App configuration
    APP_PORT = int(os.getenv("APP_PORT", 8000))
    APP_HOST = os.getenv("APP_HOST", "0.0.0.0")

    # Vector store configuration
    # 384 is the dimensionality of the multilingual MiniLM sentence-transformer model
    VECTOR_SIZE = 384
    COLLECTION_PREFIX = "startup_advisor"

    # Data / ingestion configuration
    DATA_DIR = "data"
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50


settings = Settings()
