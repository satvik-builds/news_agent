"""
Configuration for the News Digest Agent
"""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY or GOOGLE_API_KEY == "paste_your_actual_key_here":
    raise ValueError(
        "⚠️ GOOGLE_API_KEY not found! Please set it in your .env file.\n"
        "Get your API key from: https://makersuite.google.com/app/apikey"
    )

# Set up for Gemini API (not Vertex AI)
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "False")
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY


@dataclass
class DigestConfiguration:
    """
    Configuration for the News Digest Agent.
    
    Attributes:
        worker_model: The main model used by agents for generation tasks
        critic_model: The model used for quality assessment
        max_articles: How many articles to process
        max_quality_iterations: How many times to improve the digest
        target_reading_time: Target minutes for the digest
        num_parallel_processors: Number of parallel processors to use
    """
    
    worker_model: str = "gemini-1.5-flash"  # Fast and efficient
    critic_model: str = "gemini-1.5-flash"  # For quality checks
    max_articles: int = 5  # Keep it small for faster results
    max_quality_iterations: int = 3  # Maximum improvement loops
    target_reading_time: int = 3  # 3-minute digest
    num_parallel_processors: int = 3  # 3 parallel agents


# Create the global configuration instance
config = DigestConfiguration()

print(f"✅ Configuration loaded successfully!")
print(f"📦 Worker Model: {config.worker_model}")
print(f"📰 Max Articles: {config.max_articles}")
print(f"🔁 Max Quality Iterations: {config.max_quality_iterations}")
