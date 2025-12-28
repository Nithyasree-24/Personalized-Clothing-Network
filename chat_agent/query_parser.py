"""
Natural Language Query Parser for FashionPulse Chat Agent
Extracts product type, color, gender, and price from user messages
"""
import re
import logging
from typing import Dict, Optional, List, Any
from config import ChatAgentConfig

class QueryParser:
    def __init__(self):
        self.config = ChatAgentConfig()
        self.logger = logging.getLogger(__name__)
    
    def parse_user_query(self, user_message: str) -> Dict[str, Any]:
        """
        Parse user message and extract search parameters
        Returns: {
            'category': str,
            'color': str, 
            'gender': str,
            'max_price': float,
            'intent': str,
            'original_message': str
        }
        """
        message = user_message.lower().strip()
        
        parsed_query = {
            'category': None,
            'color': None,
            'gender': None,
            'max_price': None,
            'intent': self._detect_intent(message),
            'original_message': user_message
        }
        
        # Extract category
        parsed_query['category'] = self._extract_category(message)
        
        # Extract color
        parsed_query['color'] = self._extract_color(message)
        
        # Extract gender
        parsed_query['gender'] = self._extract_gender(message)
        
        # Extract price
        parsed_query['max_price'] = self._extract_price(message)
        
        self.logger.info(f"🧠 Parsed query: {parsed_query}")
        return parsed_query
    
    def _detect_intent(self, message: str) -> str:
        """Detect user intent from message"""
        # Support/Policy keywords - HIGHEST PRIORITY
        support_keywords = [
            'delivery', 'shipping', 'return', 'refund', 'exchange', 'replace', 
            'payment', 'order', 'track', 'tracking', 'cancel', 'policy', 
            'support', 'help', 'customer care', 'customer service',
            'when will', 'how long', 'how many days', 'delivery time',
            'return policy', 'refund policy', 'exchange policy',
            'cod', 'cash on delivery', 'upi', 'card payment',
            'same day', 'express', 'fast delivery', 'urgent',
            'size guide', 'size chart', 'contact', 'phone number',
            'email', 'address', 'location', 'store'
        ]
        
        # Check for support intent FIRST
        if any(keyword in message for keyword in support_keywords):
            return 'support'
        
        # Greeting keywords
        greetings = ['hi', 'hello', 'hey', 'good morning', 'good evening', 'namaste']
        if any(word in message for word in greetings) and len(message.split()) <= 3:
            return 'greeting'
        
        # Product search keywords
        product_keywords = [
            'show', 'find', 'search', 'looking for', 'want', 'need', 'get me',
            'dress', 'shirt', 'jeans', 'saree', 'kurti', 'top', 'bottom',
            'clothes', 'clothing', 'fashion', 'wear', 'ethnic', 'western',
            'red', 'blue', 'black', 'white', 'green', 'pink', 'yellow',
            'men', 'women', 'kids', 'boys', 'girls', 'male', 'female',
            'under', 'below', 'price', 'cheap', 'expensive', 'budget'
        ]
        
        # Check for product search intent
        if any(keyword in message for keyword in product_keywords):
            return 'search'
        
        # General help
        help_words = ['what can you do', 'how to', 'guide', 'categories', 'colors']
        if any(word in message for word in help_words):
            return 'help'
        
        # Default to help for unclear messages
        return 'help'
    
    def _extract_category(self, message: str) -> Optional[str]:
        """Extract product category from message"""
        # Handle combined gender + category patterns first
        combined_patterns = {
            'mens shirt': 'shirt', 'men shirt': 'shirt', 'mens shirts': 'shirt',
            'womens dress': 'dress', 'women dress': 'dress', 'womens dresses': 'dress',
            'mens jeans': 'jeans', 'men jeans': 'jeans',
            'womens top': 'top', 'women top': 'top', 'womens tops': 'top',
            'mens kurti': 'kurti', 'men kurti': 'kurti',
            'womens saree': 'saree', 'women saree': 'saree',
            'kids dress': 'dress', 'kids shirt': 'shirt'
        }
        
        # Check combined patterns first
        for pattern, category in combined_patterns.items():
            if pattern in message:
                self.logger.info(f"🏷️ Found combined pattern: {pattern} → {category}")
                return category
        
        # Then check individual categories
        for category, variations in self.config.PRODUCT_CATEGORIES.items():
            for variation in variations:
                if variation in message:
                    self.logger.info(f"🏷️ Found category: {category} (matched: {variation})")
                    return category
        return None
    
    def _extract_color(self, message: str) -> Optional[str]:
        """Extract color from message"""
        for color, variations in self.config.COLOR_VARIATIONS.items():
            for variation in variations:
                if variation in message:
                    self.logger.info(f"🎨 Found color: {color} (matched: {variation})")
                    return color
        return None
    
    def _extract_gender(self, message: str) -> Optional[str]:
        """Extract gender from message"""
        for gender, variations in self.config.GENDER_MAPPING.items():
            for variation in variations:
                if variation in message:
                    self.logger.info(f"👤 Found gender: {gender} (matched: {variation})")
                    return gender
        return None
    
    def _extract_price(self, message: str) -> Optional[float]:
        """Extract maximum price from message"""
        # Look for price patterns
        price_patterns = [
            r'under (\d+)',
            r'below (\d+)', 
            r'less than (\d+)',
            r'within (\d+)',
            r'budget (\d+)',
            r'max (\d+)',
            r'maximum (\d+)',
            r'up to (\d+)',
            r'not more than (\d+)',
            r'around (\d+)',
            r'approximately (\d+)',
            r'about (\d+)',
            r'₹(\d+)',
            r'rs (\d+)',
            r'rupees (\d+)',
            r'(\d+) rupees',
            r'(\d+) rs',
            r'(\d+)₹'
        ]
        
        for pattern in price_patterns:
            match = re.search(pattern, message)
            if match:
                price = float(match.group(1))
                self.logger.info(f"💰 Found price: ₹{price}")
                return price
        
        # Look for standalone numbers that might be prices
        numbers = re.findall(r'\b(\d{3,5})\b', message)
        if numbers:
            # Take the first reasonable price (between 100-50000)
            for num in numbers:
                price = float(num)
                if 100 <= price <= 50000:
                    self.logger.info(f"💰 Inferred price: ₹{price}")
                    return price
        
        return None
    
    def validate_query(self, parsed_query: Dict[str, Any]) -> bool:
        """Validate if the parsed query has enough information for search"""
        has_category = parsed_query['category'] is not None
        has_color = parsed_query['color'] is not None
        has_gender = parsed_query['gender'] is not None
        has_price = parsed_query['max_price'] is not None
        
        # At least one filter should be present
        return has_category or has_color or has_gender or has_price
    
    def get_search_suggestions(self, message: str) -> List[str]:
        """Generate search suggestions based on partial input"""
        suggestions = []
        
        # If no clear intent, suggest popular searches
        if len(message.strip()) < 3:
            return [
                "Show me red dresses under ₹2000",
                "Find jeans for men",
                "Looking for ethnic wear for women",
                "Show casual shirts under ₹1500"
            ]
        
        # Category-based suggestions
        for category in self.config.PRODUCT_CATEGORIES.keys():
            if category in message.lower():
                suggestions.extend([
                    f"Show {category} for women",
                    f"Find {category} under ₹2000",
                    f"Looking for {category} in blue color"
                ])
                break
        
        return suggestions[:4]  # Return max 4 suggestions