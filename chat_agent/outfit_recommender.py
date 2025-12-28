"""
Outfit Recommender for Calendar Event Based System
Provides intelligent outfit suggestions based on gender and event type
"""
import logging
from typing import Dict, List, Any
from database import DatabaseHandler
from event_manager import EventManager

class OutfitRecommender:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db_handler = DatabaseHandler()
        self.event_manager = EventManager()
        
    def get_event_outfit_suggestions(self, gender: str, event_type: str, event_date: str = None) -> Dict[str, Any]:
        """Get outfit suggestions for specific event"""
        try:
            self.logger.info(f"👗 Getting outfit suggestions for {gender} {event_type}")
            
            # Get recommended categories for this event
            recommended_categories = self.event_manager.get_event_categories(gender, event_type)
            
            # Search for products in recommended categories
            all_products = []
            for category in recommended_categories:
                products = self.db_handler.search_products(
                    category=category,
                    color=None,
                    gender=gender.lower(),
                    max_price=None,
                    limit=3  # Limit per category for variety
                )
                all_products.extend(products)
            
            # Remove duplicates and limit total results
            seen_ids = set()
            unique_products = []
            for product in all_products:
                if product['product_id'] not in seen_ids:
                    unique_products.append(product)
                    seen_ids.add(product['product_id'])
                if len(unique_products) >= 8:  # Limit to 8 products total
                    break
            
            self.logger.info(f"✅ Found {len(unique_products)} outfit suggestions")
            
            return {
                'success': True,
                'products': unique_products,
                'categories': recommended_categories,
                'event_info': {
                    'gender': gender,
                    'event_type': event_type,
                    'event_date': event_date
                }
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error getting outfit suggestions: {e}")
            return {
                'success': False,
                'products': [],
                'categories': [],
                'error': str(e)
            }
    
    def get_formal_outfits(self, gender: str) -> List[Dict[str, Any]]:
        """Get formal outfit suggestions"""
        if gender.lower() == 'women':
            categories = ['Western Wear', 'Dresses']
        else:
            categories = ['Shirts']
        
        products = []
        for category in categories:
            category_products = self.db_handler.search_products(
                category=category,
                gender=gender.lower(),
                limit=3
            )
            products.extend(category_products)
        
        return products[:6]  # Return max 6 products
    
    def get_casual_outfits(self, gender: str) -> List[Dict[str, Any]]:
        """Get casual outfit suggestions"""
        if gender.lower() == 'women':
            categories = ['Tops and Co-ord Sets', 'Western Wear']
        else:
            categories = ['T-shirts', 'Shirts']
        
        products = []
        for category in categories:
            category_products = self.db_handler.search_products(
                category=category,
                gender=gender.lower(),
                limit=3
            )
            products.extend(category_products)
        
        return products[:6]  # Return max 6 products
    
    def get_ethnic_outfits(self, gender: str) -> List[Dict[str, Any]]:
        """Get ethnic/traditional outfit suggestions"""
        if gender.lower() == 'women':
            categories = ['Ethnic Wear', 'Dresses']
        else:
            categories = ['Shirts']  # Men's ethnic wear would be in shirts category
        
        products = []
        for category in categories:
            category_products = self.db_handler.search_products(
                category=category,
                gender=gender.lower(),
                limit=4
            )
            products.extend(category_products)
        
        return products[:8]  # Return max 8 products
    
    def get_party_outfits(self, gender: str) -> List[Dict[str, Any]]:
        """Get party outfit suggestions"""
        if gender.lower() == 'women':
            categories = ['Western Wear', 'Dresses', 'Tops and Co-ord Sets']
        else:
            categories = ['Shirts', 'T-shirts']
        
        products = []
        for category in categories:
            category_products = self.db_handler.search_products(
                category=category,
                gender=gender.lower(),
                limit=2
            )
            products.extend(category_products)
        
        return products[:6]  # Return max 6 products
    
    def format_outfit_response(self, products: List[Dict[str, Any]], event_type: str, gender: str) -> str:
        """Format outfit recommendation response"""
        if not products:
            return f"Sorry, I couldn't find suitable outfits for your {event_type}. Please browse our collection manually."
        
        response = f"✨ Perfect outfits for your {event_type}! Here are my top recommendations:\n\n"
        
        # Add styling tips based on event type
        event_lower = event_type.lower()
        if 'interview' in event_lower or 'office' in event_lower:
            response += "💼 **Professional Styling Tips:**\n"
            response += "• Choose well-fitted, conservative colors\n"
            response += "• Pair with formal shoes and minimal accessories\n"
            response += "• Ensure clothes are wrinkle-free and well-pressed\n\n"
        elif 'wedding' in event_lower or 'reception' in event_lower:
            response += "💒 **Wedding Styling Tips:**\n"
            response += "• Opt for rich fabrics and elegant designs\n"
            response += "• Add statement jewelry and formal footwear\n"
            response += "• Consider the venue and time of day\n\n"
        elif 'party' in event_lower or 'celebration' in event_lower:
            response += "🎉 **Party Styling Tips:**\n"
            response += "• Choose vibrant colors and trendy styles\n"
            response += "• Add fun accessories and comfortable shoes\n"
            response += "• Consider the party theme and venue\n\n"
        elif 'festival' in event_lower:
            response += "🎊 **Festival Styling Tips:**\n"
            response += "• Embrace traditional colors and patterns\n"
            response += "• Add cultural accessories and comfortable footwear\n"
            response += "• Choose breathable fabrics for comfort\n\n"
        
        response += f"Found {len(products)} perfect matches for you! Click any product to view details and add to cart."
        
        return response