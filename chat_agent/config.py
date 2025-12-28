"""
Configuration for FashionPulse Chat Agent
"""
import os
from typing import Dict, List

class ChatAgentConfig:
    # Database Configuration
    DB_HOST = "localhost"
    DB_USER = "root"
    DB_PASSWORD = ""
    DB_NAME = "fashiopulse"
    DB_TABLE = "clothing"
    
    # Product Categories Mapping (updated to match actual database categories)
    PRODUCT_CATEGORIES = {
        'dresses': ['dress', 'dresses', 'gown', 'frock'],
        'hoodies': ['hoodie', 'hoodies', 'sweatshirt', 'pullover'],
        'bottom wear': ['jeans', 'denim', 'pants', 'trousers', 'jean', 'bottom', 'bottoms'],
        'ethnic wear': ['saree', 'sari', 'ethnic wear', 'ethnic', 'traditional', 'indian wear'],
        'shirts': ['shirt', 'shirts', 'formal shirt'],
        'kurti': ['kurti', 'kurta', 'ethnic top'],
        't-shirts': ['tshirt', 't-shirt', 'tee', 'casual shirt'],
        'tops and co-ord sets': ['top', 'tops', 'blouse', 'tunic', 'coord', 'co-ord'],
        'western wear': ['western', 'western wear'],
        "women's bottomwear": ['women bottom', 'women pants', 'women jeans', 'ladies bottom'],
        'formal': ['formal', 'office wear', 'business'],
        'casual': ['casual', 'everyday'],
        'party': ['party', 'evening', 'night out'],
        'sports': ['sports', 'gym', 'workout', 'athletic']
    }
    
    # Color Variations
    COLOR_VARIATIONS = {
        'red': ['red', 'crimson', 'scarlet', 'maroon'],
        'blue': ['blue', 'navy', 'royal blue', 'sky blue'],
        'black': ['black', 'dark', 'charcoal'],
        'white': ['white', 'cream', 'off-white', 'ivory'],
        'green': ['green', 'olive', 'forest green', 'mint'],
        'pink': ['pink', 'rose', 'magenta', 'fuchsia'],
        'yellow': ['yellow', 'golden', 'mustard'],
        'purple': ['purple', 'violet', 'lavender'],
        'brown': ['brown', 'tan', 'beige', 'khaki'],
        'gray': ['gray', 'grey', 'silver'],
        'orange': ['orange', 'peach', 'coral']
    }
    
    # Gender Mapping
    GENDER_MAPPING = {
        'men': ['men', 'man', 'male', 'boys', 'boy', 'guys', 'gents'],
        'women': ['women', 'woman', 'female', 'girls', 'girl', 'ladies', 'gals'],
        'kids': ['kids', 'children', 'child', 'baby', 'toddler']
    }
    
    # Price Keywords
    PRICE_KEYWORDS = [
        'under', 'below', 'less than', 'within', 'budget', 'max', 'maximum',
        'up to', 'not more than', 'around', 'approximately', 'about'
    ]
    
    # Response Templates
    RESPONSE_TEMPLATES = {
        'products_found': "Here are the best matches 😊",
        'no_products': "Sorry, I couldn't find matching products. Try changing color, category, gender or price ❤️",
        'greeting': "Hi! I'm your fashion assistant 👗 What are you looking for today?",
        'help': "I can help you find:\n• Dresses, tops, jeans, sarees, shirts\n• By color, gender, price range\n• Just tell me what you're looking for! 💫"
    }
    
    # Maximum results to return
    MAX_RESULTS = 10
    
    # Default price limit if none specified
    DEFAULT_MAX_PRICE = 10000