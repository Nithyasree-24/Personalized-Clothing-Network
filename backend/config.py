import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = os.getenv('DB_NAME', 'fashiopulse')
    JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key')
    PORT = int(os.getenv('PORT', 5000))
    
    # API Keys
    RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY', '')
    RAPIDAPI_KEY_EBAY = os.getenv('RAPIDAPI_KEY_EBAY', '')  # Can be same or different key
    HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY', '')  # For Virtual Try-On
