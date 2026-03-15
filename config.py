"""
Configuration settings for ScriptForge
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
BRAVE_API_KEY = os.getenv("BRAVE_API_KEY", "")

# Default AI provider (can be "deepseek", "anthropic", "gemini")
DEFAULT_AI_PROVIDER = "deepseek"

# API endpoints
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

# Model configurations
MODEL_CONFIGS = {
    "deepseek": {
        "model": "deepseek-chat",
        "max_tokens": 4000,
        "temperature": 0.7,
    },
    "anthropic": {
        "model": "claude-3-haiku-20240307",
        "max_tokens": 4000,
        "temperature": 0.7,
    },
    "gemini": {
        "model": "gemini-pro",
        "max_tokens": 4000,
        "temperature": 0.7,
    }
}

# Application settings
APP_NAME = "ScriptForge"
APP_VERSION = "1.0.0"
ENABLE_PRO_FEATURES = True  # Set to False for basic version

# File paths
TEMPLATES_DIR = "templates"
EXAMPLES_DIR = "examples"
EXPORT_DIR = "exports"

# Create necessary directories
for directory in [TEMPLATES_DIR, EXAMPLES_DIR, EXPORT_DIR]:
    os.makedirs(directory, exist_ok=True)

# Default templates
DEFAULT_TEMPLATES = {
    "youtube_explainer": {
        "name": "YouTube Explainer",
        "structure": [
            "Hook (0:00-0:30)",
            "Introduction (0:30-1:00)", 
            "Main Points (1:00-4:00)",
            "Conclusion (4:00-4:30)",
            "CTA (4:30-5:00)"
        ]
    },
    "tiktok_quicktip": {
        "name": "TikTok Quick Tip",
        "structure": [
            "Attention Grabber (0-3s)",
            "Problem Statement (3-10s)",
            "Solution (10-45s)",
            "Result/Proof (45-55s)",
            "CTA (55-60s)"
        ]
    }
}

# Export settings
EXPORT_FORMATS = ["txt", "docx", "json"]
DEFAULT_EXPORT_FORMAT = "txt"

# Search settings (for pro features)
BRAVE_SEARCH_URL = "https://api.search.brave.com/res/v1/web/search"
SEARCH_COUNT = 10  # Number of search results to fetch
TREND_ANALYSIS_DAYS = 7  # Look back 7 days for trends