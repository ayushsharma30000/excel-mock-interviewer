# Gemini-specific LLM Configuration
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LLMConfig:
    """Configuration for Google Gemini API"""
    
    # Provider name
    PROVIDER = "gemini"
    
    # API Configuration
    API_KEY = os.getenv("GEMINI_API_KEY", "")
    MODEL = "gemini-pro"
    
    # API Endpoints
    BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
    
    # Rate Limiting
    MAX_REQUESTS_PER_MINUTE = 60  # Gemini free tier limit
    MAX_TOKENS_PER_REQUEST = 32768  # Gemini context window
    
    # Temperature settings for different use cases
    TEMPERATURE_EVALUATION = 0.3  # Lower for consistent evaluation
    TEMPERATURE_GENERATION = 0.7  # Higher for question variety
    
    # Retry Configuration
    MAX_RETRIES = 3
    RETRY_DELAY = 1  # seconds
    
    # Response Configuration
    MAX_OUTPUT_TOKENS = 2048
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        if not cls.API_KEY:
            raise ValueError(
                "GEMINI_API_KEY not found! "
                "Please set it in your .env file. "
                "Get your key from: https://makersuite.google.com/app/apikey"
            )
        return True

# Excel Interview Specific Configuration
class InterviewConfig:
    """Configuration for Excel Interview System"""
    
    # Interview Structure
    TOTAL_QUESTIONS = 5
    WARM_UP_QUESTIONS = 1
    CORE_QUESTIONS = 3
    SCENARIO_QUESTIONS = 1
    
    # Time Limits (in seconds)
    MAX_ANSWER_TIME = 300  # 5 minutes per question
    TOTAL_INTERVIEW_TIME = 1800  # 30 minutes total
    
    # Scoring Weights
    SCORING_WEIGHTS = {
        "technical_accuracy": 0.4,
        "practical_application": 0.3,
        "communication_clarity": 0.2,
        "problem_solving": 0.1
    }
    
    # Difficulty Levels
    DIFFICULTY_LEVELS = {
        "beginner": "Basic Excel functions and formatting",
        "intermediate": "Advanced formulas, pivot tables, data analysis",
        "advanced": "Complex scenarios, VBA, Power Query, optimization"
    }