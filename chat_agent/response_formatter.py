"""
Response Formatter for FashionPulse Chat Agent
Formats database results into user-friendly chat responses
"""
import logging
from typing import List, Dict, Any, Optional
from config import ChatAgentConfig

class ResponseFormatter:
    def __init__(self):
        self.config = ChatAgentConfig()
        self.logger = logging.getLogger(__name__)
    
    def format_products_response(self, products: List[Dict[str, Any]], 
                                query_info: Dict[str, Any]) -> str:
        """Format product search results into chat response"""
        if not products:
            return self._format_no_results_response(query_info)
        
        # Start with greeting
        response = f"{self.config.RESPONSE_TEMPLATES['products_found']}\n\n"
        
        # Add query context
        context = self._build_query_context(query_info)
        if context:
            response += f"{context}\n\n"
        
        # Format each product
        for i, product in enumerate(products[:self.config.MAX_RESULTS], 1):
            response += self._format_single_product(product, i)
            response += "\n\n"
        
        # Add helpful footer
        if len(products) >= self.config.MAX_RESULTS:
            response += f"💡 Showing top {self.config.MAX_RESULTS} results. Need more specific results? Try adding color, price range, or gender!"
        
        return response.strip()
    
    def _format_single_product(self, product: Dict[str, Any], index: int) -> str:
        """Format a single product for display"""
        # Product name with emoji
        name = product.get('product_name', 'Unknown Product')
        
        # Price formatting
        price = product.get('price', 0)
        price_str = f"₹{int(price):,}" if price else "Price not available"
        
        # Color with emoji
        color = product.get('color', 'Not specified')
        
        # Gender with emoji
        gender = product.get('gender', 'Unisex')
        gender_emoji = self._get_gender_emoji(gender)
        
        # Category
        category = product.get('product_category', 'Fashion')
        
        # Build product line without stock information
        product_line = f"{index}️⃣ **{name}**\n"
        product_line += f"   💰 {price_str} | 🎨 {color} | {gender_emoji} {gender.title()}\n"
        product_line += f"   🏷️ {category}"
        
        return product_line
    
    def _format_no_results_response(self, query_info: Dict[str, Any]) -> str:
        """Format response when no products are found"""
        response = f"{self.config.RESPONSE_TEMPLATES['no_products']}\n\n"
        
        # Add specific suggestions based on what was searched
        suggestions = self._generate_search_suggestions(query_info)
        if suggestions:
            response += "💡 **Try searching for:**\n"
            for suggestion in suggestions:
                response += f"• {suggestion}\n"
        
        # Always show some popular products as alternatives
        response += "\n🔥 **Popular items you might like:**\n"
        response += "• Red dresses under ₹2000\n"
        response += "• Blue shirts for men\n" 
        response += "• Ethnic wear for women\n"
        response += "• Casual jeans under ₹1500\n"
        
        return response.strip()
    
    def _build_query_context(self, query_info: Dict[str, Any]) -> str:
        """Build context string showing what was searched"""
        context_parts = []
        
        if query_info.get('category'):
            context_parts.append(f"**{query_info['category'].title()}**")
        
        if query_info.get('color'):
            context_parts.append(f"in **{query_info['color'].title()}**")
        
        if query_info.get('gender'):
            context_parts.append(f"for **{query_info['gender'].title()}**")
        
        if query_info.get('max_price'):
            context_parts.append(f"under **₹{int(query_info['max_price']):,}**")
        
        if context_parts:
            return f"🔍 Searching: {' '.join(context_parts)}"
        
        return ""
    
    def _get_gender_emoji(self, gender: str) -> str:
        """Get appropriate emoji for gender"""
        gender_lower = gender.lower()
        if 'men' in gender_lower or 'male' in gender_lower:
            return "👨"
        elif 'women' in gender_lower or 'female' in gender_lower:
            return "👩"
        elif 'kid' in gender_lower or 'child' in gender_lower:
            return "👶"
        else:
            return "👤"
    
    def _get_stock_status(self, stock: int) -> str:
        """Get stock status with appropriate emoji"""
        if stock is None or stock == 0:
            return "❌ Out of Stock"
        elif stock <= 5:
            return f"⚠️ Only {stock} left"
        elif stock <= 20:
            return f"✅ {stock} in stock"
        else:
            return "✅ In Stock"
    
    def _generate_search_suggestions(self, query_info: Dict[str, Any]) -> List[str]:
        """Generate helpful search suggestions"""
        suggestions = []
        
        # If they searched for a specific category but no results
        if query_info.get('category'):
            category = query_info['category']
            suggestions.extend([
                f"{category.title()} in different colors (red, blue, black)",
                f"{category.title()} for different genders",
                f"{category.title()} with higher price range"
            ])
        
        # If they searched with price but no results
        if query_info.get('max_price'):
            price = query_info['max_price']
            suggestions.extend([
                f"Products under ₹{int(price * 1.5):,}",
                "Different product categories",
                "Remove color or gender filters"
            ])
        
        # General suggestions if no specific filters
        if not any([query_info.get('category'), query_info.get('color'), 
                   query_info.get('gender'), query_info.get('max_price')]):
            suggestions.extend([
                "Dresses for women under ₹2000",
                "Shirts for men in blue color", 
                "Ethnic wear under ₹1500",
                "Casual tops for women"
            ])
        
        return suggestions[:3]  # Return max 3 suggestions
    
    def format_greeting_response(self) -> str:
        """Format greeting response"""
        return f"{self.config.RESPONSE_TEMPLATES['greeting']}\n\n{self.config.RESPONSE_TEMPLATES['help']}"
    
    def format_help_response(self) -> str:
        """Format help response"""
        help_text = f"{self.config.RESPONSE_TEMPLATES['help']}\n\n"
        help_text += "**Example searches:**\n"
        help_text += "• \"Show me red dresses under ₹2000\"\n"
        help_text += "• \"Find jeans for men\"\n"
        help_text += "• \"Looking for ethnic wear for women\"\n"
        help_text += "• \"Blue shirts under ₹1500\"\n\n"
        help_text += "Just tell me what you're looking for! 😊"
        return help_text
    
    def format_error_response(self, error_message: str = None) -> str:
        """Format error response"""
        base_message = "Oops! Something went wrong 😅"
        if error_message:
            return f"{base_message}\n\n**Error:** {error_message}\n\nPlease try again or rephrase your request."
        return f"{base_message}\n\nPlease try again or ask for help!"
    
    def format_stats_response(self, stats: Dict[str, Any]) -> str:
        """Format database statistics response"""
        response = "📊 **FashionPulse Inventory Stats**\n\n"
        
        # Total products
        total = stats.get('total_products', 0)
        response += f"🛍️ **Total Products:** {total:,}\n\n"
        
        # By gender
        by_gender = stats.get('by_gender', {})
        if by_gender:
            response += "👥 **By Gender:**\n"
            for gender, count in by_gender.items():
                emoji = self._get_gender_emoji(gender)
                response += f"   {emoji} {gender.title()}: {count:,}\n"
            response += "\n"
        
        # Price range
        price_range = stats.get('price_range', {})
        if price_range:
            min_price = price_range.get('min_price', 0)
            max_price = price_range.get('max_price', 0)
            response += f"💰 **Price Range:** ₹{int(min_price):,} - ₹{int(max_price):,}\n"
        
        return response