from dataclasses import dataclass
from typing import Optional, List, Dict

@dataclass
class Settings:
    """Application settings"""
    api_provider: str = "gemini"
    api_key: Optional[str] = None
    use_mcp: bool = False
    preferred_style: str = "auto"
    confidence_threshold: float = 0.7
    show_detailed_analysis: bool = True
    enable_web_search: bool = True
    preferred_model: Optional[str] = None  # Preferred model to use
    enable_model_fallback: bool = True  # Enable automatic fallback to other models
    
    def is_valid(self) -> bool:
        """Check if settings are valid"""
        return bool(self.api_key)
    
    def get_provider_name(self) -> str:
        """Get human-readable provider name"""
        return "Google Gemini"
    
    def get_style_name(self) -> str:
        """Get human-readable style name"""
        if self.preferred_style == "auto":
            return "Auto-detect"
        return self.preferred_style.upper()

# Default settings
DEFAULT_SETTINGS = Settings()

# Available AI models
AVAILABLE_MODELS = {
    "gemini-2.5-flash-lite": {
        "name": "Gemini 2.5 Flash Lite",
        "description": "Fastest response time, most cost-effective",
        "provider": "google",
        "recommended_for": "Quick citation checks, high volume analysis"
    },
    "gemini-2.5-flash": {
        "name": "Gemini 2.5 Flash",
        "description": "Fast with improved quality",
        "provider": "google",
        "recommended_for": "Balanced speed and accuracy"
    },
    "gemini-2.0-flash-lite": {
        "name": "Gemini 2.0 Flash Lite",
        "description": "Previous generation lightweight model",
        "provider": "google",
        "recommended_for": "Basic citation validation"
    },
    "gemini-2.0-flash": {
        "name": "Gemini 2.0 Flash",
        "description": "Previous generation balanced model",
        "provider": "google",
        "recommended_for": "Standard citation analysis"
    },
    "gemini-2.5-pro": {
        "name": "Gemini 2.5 Pro",
        "description": "Highest quality, most accurate",
        "provider": "google",
        "recommended_for": "Complex citations, detailed analysis"
    },
    "gemma-3-1b-it": {
        "name": "Gemma 3 1B IT",
        "description": "Lightweight open model",
        "provider": "google",
        "recommended_for": "Basic validation, offline capable"
    },
    "gemma-3n-e2b-it": {
        "name": "Gemma 3N E2B IT",
        "description": "Efficient Gemma variant",
        "provider": "google",
        "recommended_for": "Quick checks, resource-limited environments"
    },
    "gemma-3n-e4b-it": {
        "name": "Gemma 3N E4B IT",
        "description": "Larger Gemma variant",
        "provider": "google",
        "recommended_for": "Better accuracy than smaller Gemma models"
    }
}

# Model selection presets
MODEL_PRESETS = {
    "speed": {
        "name": "Speed Priority",
        "description": "Fastest response times",
        "models": ["gemini-2.5-flash-lite", "gemini-2.0-flash-lite", "gemma-3-1b-it"]
    },
    "balanced": {
        "name": "Balanced",
        "description": "Good balance of speed and quality",
        "models": ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-2.5-flash-lite"]
    },
    "quality": {
        "name": "Quality Priority",
        "description": "Most accurate results",
        "models": ["gemini-2.5-pro", "gemini-2.5-flash", "gemma-3n-e4b-it"]
    },
    "cost": {
        "name": "Cost Effective",
        "description": "Minimize API costs",
        "models": ["gemini-2.5-flash-lite", "gemma-3-1b-it", "gemma-3n-e2b-it"]
    }
}

# Citation style configurations
CITATION_STYLES = {
    "apa": {
        "name": "APA (American Psychological Association)",
        "description": "Common in psychology, education, and social sciences",
        "example": "Smith, J. (2023). Title of work. Publisher.",
        "inline_example": "(Smith, 2023)"
    },
    "mla": {
        "name": "MLA (Modern Language Association)",
        "description": "Common in humanities, literature, and arts",
        "example": 'Smith, John. "Title of Work." Publisher, 2023.',
        "inline_example": "(Smith 45)"
    },
    "chicago": {
        "name": "Chicago Manual of Style",
        "description": "Common in history and some social sciences",
        "example": "Smith, John. Title of Work. City: Publisher, 2023.",
        "inline_example": "(Smith 2023, 45)"
    },
    "harvard": {
        "name": "Harvard Referencing",
        "description": "Common in UK and Australian universities",
        "example": "Smith, J. 2023, Title of work, Publisher, City.",
        "inline_example": "(Smith 2023)"
    },
    "ieee": {
        "name": "IEEE",
        "description": "Common in engineering and technical fields",
        "example": '[1] J. Smith, "Title of work," Publisher, 2023.',
        "inline_example": "[1]"
    }
}

# File upload configurations
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_FILE_TYPES = ["txt", "pdf", "docx", "md"]
FILE_TYPE_NAMES = {
    "txt": "Plain Text",
    "pdf": "PDF Document",
    "docx": "Word Document",
    "md": "Markdown"
}

# API configurations
API_TIMEOUT = 30  # seconds
MAX_RETRIES = 3
RATE_LIMIT_COOLDOWN = 300  # 5 minutes in seconds

# Analysis configurations
MIN_CITATION_LENGTH = 10  # characters
MAX_CITATIONS_PER_ANALYSIS = 500
BATCH_SIZE = 10  # for batch processing

# UI configurations
THEME_COLORS = {
    "primary": "#3b82f6",
    "success": "#10b981",
    "warning": "#f59e0b",
    "error": "#ef4444",
    "info": "#3b82f6",
    "background": "#f8fafc",
    "text": "#1e293b",
    "muted": "#64748b"
}

# Model status indicators
MODEL_STATUS_COLORS = {
    "active": "#10b981",
    "rate_limited": "#ef4444",
    "available": "#3b82f6",
    "unavailable": "#64748b"
}