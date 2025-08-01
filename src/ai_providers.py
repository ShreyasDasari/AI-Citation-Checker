from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
import os
import json
import google.generativeai as genai
import time
import logging
from dotenv import load_dotenv

# Try to import streamlit for cloud deployment
try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False

# Load environment variables for local development
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIProvider(ABC):
    """Abstract base class for AI providers"""
    
    @abstractmethod
    def analyze_citation(self, prompt: str) -> str:
        """Analyze a citation using the AI model"""
        pass
    
    @abstractmethod
    def check_connection(self) -> bool:
        """Check if the API connection is working"""
        pass

class GeminiProvider(AIProvider):
    """Google Gemini API provider implementation with multi-model support"""
    
    # Available models in order of preference (fallback order)
    AVAILABLE_MODELS = [
        {
            'name': 'gemini-2.5-flash-lite',
            'description': 'Latest experimental flash model',
            'max_tokens': 1000,
            'temperature': 0.3
        },
        {
            'name': 'gemini-2.5-pro',
            'description': 'Fast and efficient model',
            'max_tokens': 1000,
            'temperature': 0.3
        },
        {
            'name': 'gemini-2.0-flash-lite',
            'description': 'Lightweight flash model',
            'max_tokens': 1000,
            'temperature': 0.3
        },
        {
            'name': 'gemini-2.5-flash',
            'description': 'High quality model',
            'max_tokens': 1000,
            'temperature': 0.3
        },
        {
            'name': 'gemini-2.0-flash',
            'description': 'Previous generation model',
            'max_tokens': 1000,
            'temperature': 0.3
        }
    ]
    
    def __init__(self, api_key: Optional[str] = None, preferred_model: Optional[str] = None):
        # Initialize rate limit tracking FIRST
        self.rate_limit_errors = {}
        self.rate_limit_reset_time = {}
        
        # Get API key from multiple sources
        self.api_key = api_key
        
        # Try Streamlit secrets first (for cloud deployment)
        if not self.api_key and HAS_STREAMLIT:
            try:
                self.api_key = st.secrets.get("GEMINI_API_KEY")
            except:
                pass
        
        # Then try environment variables (for local development)
        if not self.api_key:
            self.api_key = os.getenv("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
            
        if not self.api_key:
            raise ValueError("Gemini API key not provided. Please provide your API key or set GEMINI_API_KEY in your .env file (local) or secrets (Streamlit Cloud).")
        
        # Configure the API
        genai.configure(api_key=self.api_key)
        
        # Set preferred model if specified
        self.preferred_model = preferred_model
        self.current_model_index = 0
        self.model = None
        self.model_name = None
        
        # Initialize with preferred model or first available
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the model with fallback support"""
        models_to_try = self.AVAILABLE_MODELS.copy()
        
        # If preferred model is specified, try it first
        if self.preferred_model:
            # Find the preferred model in the list
            preferred_config = None
            for i, model_config in enumerate(models_to_try):
                if model_config['name'] == self.preferred_model:
                    preferred_config = model_config
                    models_to_try.pop(i)
                    models_to_try.insert(0, preferred_config)
                    break
        
        # Try each model until one works
        for i, model_config in enumerate(models_to_try):
            try:
                model_name = model_config['name']
                
                # Check if model is in rate limit cooldown
                if model_name in self.rate_limit_reset_time:
                    if time.time() < self.rate_limit_reset_time[model_name]:
                        logger.info(f"Model {model_name} is in rate limit cooldown, skipping...")
                        continue
                    else:
                        # Reset time has passed, clear the rate limit
                        del self.rate_limit_reset_time[model_name]
                        if model_name in self.rate_limit_errors:
                            del self.rate_limit_errors[model_name]
                
                logger.info(f"Attempting to initialize model: {model_name}")
                
                self.model = genai.GenerativeModel(
                    model_name,
                    generation_config=genai.GenerationConfig(
                        temperature=model_config['temperature'],
                        max_output_tokens=model_config['max_tokens'],
                    )
                )
                
                # Test the model with a simple prompt
                test_response = self.model.generate_content("Say 'OK' if you can read this.")
                if test_response and test_response.text:
                    self.model_name = model_name
                    self.current_model_index = i
                    logger.info(f"Successfully initialized model: {model_name}")
                    return
                    
            except Exception as e:
                logger.warning(f"Failed to initialize model {model_config['name']}: {str(e)}")
                continue
        
        raise ValueError("Failed to initialize any available model. Please check your API key and quota.")
    
    def _switch_to_next_model(self):
        """Switch to the next available model"""
        original_index = self.current_model_index
        attempts = 0
        
        while attempts < len(self.AVAILABLE_MODELS):
            self.current_model_index = (self.current_model_index + 1) % len(self.AVAILABLE_MODELS)
            model_config = self.AVAILABLE_MODELS[self.current_model_index]
            model_name = model_config['name']
            
            # Check if model is in rate limit cooldown
            if model_name in self.rate_limit_reset_time:
                if time.time() < self.rate_limit_reset_time[model_name]:
                    attempts += 1
                    continue
                else:
                    # Reset time has passed, clear the rate limit
                    del self.rate_limit_reset_time[model_name]
                    if model_name in self.rate_limit_errors:
                        del self.rate_limit_errors[model_name]
            
            try:
                logger.info(f"Switching to model: {model_name}")
                
                self.model = genai.GenerativeModel(
                    model_name,
                    generation_config=genai.GenerationConfig(
                        temperature=model_config['temperature'],
                        max_output_tokens=model_config['max_tokens'],
                    )
                )
                
                # Test the model
                test_response = self.model.generate_content("Say 'OK' if you can read this.")
                if test_response and test_response.text:
                    self.model_name = model_name
                    logger.info(f"Successfully switched to model: {model_name}")
                    return True
                    
            except Exception as e:
                logger.warning(f"Failed to switch to model {model_name}: {str(e)}")
            
            attempts += 1
        
        # If we couldn't switch to any model, try reinitializing
        self.current_model_index = original_index
        self._initialize_model()
        return False
    
    def analyze_citation(self, prompt: str, retry_count: int = 0) -> str:
        """Analyze citation using Gemini with automatic model fallback"""
        max_retries = min(3, len(self.AVAILABLE_MODELS))
        
        try:
            # System instruction for citation analysis
            system_prompt = """You are an expert citation analyst. Analyze citations for:
            1. Format correctness according to citation styles (APA, MLA, Chicago, Harvard and all other styles)
            2. Completeness of information (author, year, title, source, etc.)
            3. Common formatting errors and issues
            4. Specific improvements that would make the citation correct
            
            Always respond in valid JSON format with this exact structure:
            {
                "is_valid": boolean,
                "confidence_score": float between 0 and 1,
                "issues": ["specific issue 1", "specific issue 2"],
                "suggestions": ["specific suggestion 1", "specific suggestion 2"]
            }
            
            Be specific in your issues and suggestions. Don't use generic phrases."""
            
            # Combine system and user prompts
            full_prompt = f"{system_prompt}\n\n{prompt}"
            
            response = self.model.generate_content(full_prompt)
            
            # Clean response text
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            
            # Validate JSON
            try:
                result = json.loads(response_text)
                # Ensure all required fields are present
                if not all(key in result for key in ["is_valid", "confidence_score", "issues", "suggestions"]):
                    raise ValueError("Missing required fields in response")
                
                # Add model info to response
                result["model_used"] = self.model_name
                return json.dumps(result)
                
            except:
                # If JSON parsing fails, return a default response
                return json.dumps({
                    "is_valid": None,
                    "confidence_score": 0.0,
                    "issues": ["Unable to parse AI response"],
                    "suggestions": ["Please try again"],
                    "model_used": self.model_name
                })
            
        except Exception as e:
            error_message = str(e)
            logger.error(f"Error with model {self.model_name}: {error_message}")
            
            # Check for rate limit errors
            if "quota" in error_message.lower() or "rate" in error_message.lower() or "429" in error_message:
                # Mark this model as rate limited
                self.rate_limit_errors[self.model_name] = time.time()
                self.rate_limit_reset_time[self.model_name] = time.time() + 300  # 5 minute cooldown
                
                logger.info(f"Rate limit reached for {self.model_name}, attempting fallback...")
                
                # Try to switch to next model
                if retry_count < max_retries:
                    if self._switch_to_next_model():
                        return self.analyze_citation(prompt, retry_count + 1)
            
            # Handle other errors
            if "API key" in error_message:
                error_message = "Invalid API key. Please check your Gemini API key."
            
            return json.dumps({
                "is_valid": None,
                "confidence_score": 0.0,
                "issues": [f"API Error: {error_message}"],
                "suggestions": ["Please check your API configuration and try again"],
                "model_used": self.model_name,
                "error": True
            })
    
    def check_connection(self) -> bool:
        """Check Gemini API connection"""
        try:
            response = self.model.generate_content("Say 'connected' if you can read this.")
            return "connected" in response.text.lower()
        except:
            # Try to switch model if current one fails
            try:
                self._switch_to_next_model()
                response = self.model.generate_content("Say 'connected' if you can read this.")
                return "connected" in response.text.lower()
            except:
                return False
    
    def get_current_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        if self.model_name:
            for model_config in self.AVAILABLE_MODELS:
                if model_config['name'] == self.model_name:
                    return {
                        'name': self.model_name,
                        'description': model_config['description'],
                        'status': 'active',
                        'rate_limited': self.model_name in self.rate_limit_errors
                    }
        return {'name': 'Unknown', 'status': 'error'}
    
    def get_all_models_status(self) -> List[Dict[str, Any]]:
        """Get status of all available models"""
        models_status = []
        for model_config in self.AVAILABLE_MODELS:
            model_name = model_config['name']
            status = {
                'name': model_name,
                'description': model_config['description'],
                'active': model_name == self.model_name,
                'rate_limited': model_name in self.rate_limit_errors,
                'cooldown_remaining': 0
            }
            
            if model_name in self.rate_limit_reset_time:
                remaining = self.rate_limit_reset_time[model_name] - time.time()
                if remaining > 0:
                    status['cooldown_remaining'] = int(remaining)
                    
            models_status.append(status)
            
        return models_status

class MockProvider(AIProvider):
    """Mock provider for testing without API key"""
    
    def analyze_citation(self, prompt: str) -> str:
        """Return mock analysis"""
        # Extract citation text from prompt for more realistic mock response
        citation_text = prompt.split('"')[1] if '"' in prompt else "Unknown citation"
        
        # Simple heuristics for mock analysis
        has_year = any(char.isdigit() for char in citation_text)
        has_author = any(char.isupper() for char in citation_text[:20])
        
        return json.dumps({
            "is_valid": has_year and has_author,
            "confidence_score": 0.85 if (has_year and has_author) else 0.45,
            "issues": [] if (has_year and has_author) else ["Missing year information", "Author format unclear"],
            "suggestions": [] if (has_year and has_author) else ["Add publication year", "Format author as: LastName, F."],
            "model_used": "mock"
        })
    
    def check_connection(self) -> bool:
        """Always return True for mock provider"""
        return True