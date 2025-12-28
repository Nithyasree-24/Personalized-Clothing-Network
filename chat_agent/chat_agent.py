"""
Main Chat Agent for FashionPulse
Orchestrates query parsing, database search, response formatting, and LLM integration
"""
import logging
from typing import Dict, Any, Optional
from database import DatabaseHandler
from query_parser import QueryParser
from response_formatter import ResponseFormatter
from llm_integration import FalconEcommerceLLM
from config import ChatAgentConfig

class FashionPulseChatAgent:
    def __init__(self):
        self.config = ChatAgentConfig()
        self.db_handler = DatabaseHandler()
        self.query_parser = QueryParser()
        self.response_formatter = ResponseFormatter()
        self.llm = FalconEcommerceLLM()  # Initialize Falcon 7B LLM
        self.logger = logging.getLogger(__name__)
        
        # Initialize database connection
        self._initialize()
    
    def _initialize(self):
        """Initialize the chat agent"""
        try:
            if self.db_handler.connect():
                self.logger.info("🤖 FashionPulse Chat Agent initialized successfully")
                
                # Log LLM status
                if self.llm.is_model_loaded():
                    self.logger.info("🧠 Falcon 7B E-commerce LLM loaded successfully")
                else:
                    self.logger.warning("⚠️ LLM not loaded - using fallback responses")
            else:
                self.logger.error("❌ Failed to initialize chat agent - database connection failed")
        except Exception as e:
            self.logger.error(f"❌ Chat agent initialization error: {e}")
    
    def process_message(self, user_message: str) -> str:
        """
        Main method to process user message and return response
        Enhanced with LLM integration for comprehensive e-commerce support
        
        Args:
            user_message (str): User's input message
            
        Returns:
            str: Formatted response
        """
        try:
            self.logger.info(f"💬 Processing message: {user_message}")
            
            # Parse user query
            parsed_query = self.query_parser.parse_user_query(user_message)
            
            # Determine if this is a product search query
            is_product_query = self._is_product_search_query(parsed_query, user_message)
            
            if is_product_query:
                # Handle product search with database + LLM enhancement
                return self._handle_product_search_with_llm(parsed_query, user_message)
            else:
                # Handle general e-commerce queries with LLM
                return self._handle_general_ecommerce_query(user_message, parsed_query)
                
        except Exception as e:
            self.logger.error(f"❌ Error processing message: {e}")
            return self.response_formatter.format_error_response(str(e))
    
    def _is_product_search_query(self, parsed_query: Dict[str, Any], user_message: str) -> bool:
        """Determine if the query is primarily about product search"""
        
        # Check if query has product search criteria
        has_search_criteria = any([
            parsed_query['category'],
            parsed_query['color'], 
            parsed_query['gender'],
            parsed_query['max_price']
        ])
        
        # Check for product-related keywords
        product_keywords = [
            'show', 'find', 'search', 'looking for', 'want', 'need',
            'dress', 'shirt', 'jeans', 'top', 'bottom', 'wear',
            'clothes', 'clothing', 'fashion', 'style'
        ]
        
        message_lower = user_message.lower()
        has_product_keywords = any(keyword in message_lower for keyword in product_keywords)
        
        return has_search_criteria or has_product_keywords
    
    def _handle_product_search_with_llm(self, parsed_query: Dict[str, Any], user_message: str) -> str:
        """Handle product search queries with database results + LLM enhancement"""
        try:
            # First, search the database
            products = self.db_handler.search_products(
                category=parsed_query['category'],
                color=parsed_query['color'],
                gender=parsed_query['gender'],
                max_price=parsed_query['max_price'],
                limit=self.config.MAX_RESULTS
            )
            
            # Prepare context for LLM
            context = {
                'products': products,
                'query_type': 'product_search',
                'search_criteria': parsed_query
            }
            
            if products:
                # Products found - enhance response with LLM
                if self.llm.is_model_loaded():
                    # Use LLM to create personalized response
                    llm_response = self.llm.generate_response(user_message, context)
                    
                    # Combine LLM response with structured product data
                    structured_products = self.response_formatter.format_products_response(products, parsed_query)
                    
                    # Create enhanced response
                    enhanced_response = f"{llm_response}\n\n{structured_products}"
                    return enhanced_response
                else:
                    # Fallback to standard product response
                    return self.response_formatter.format_products_response(products, parsed_query)
            else:
                # No products found - use LLM for helpful suggestions
                if self.llm.is_model_loaded():
                    return self.llm.generate_response(user_message, context)
                else:
                    return self._try_broader_search_or_suggestions(parsed_query)
                    
        except Exception as e:
            self.logger.error(f"❌ Error in product search with LLM: {e}")
            return self.response_formatter.format_error_response()
    
    def _handle_general_ecommerce_query(self, user_message: str, parsed_query: Dict[str, Any]) -> str:
        """Handle general e-commerce queries (shipping, returns, policies, etc.) with LLM"""
        try:
            # Prepare context
            context = {
                'query_type': 'general_ecommerce',
                'intent': parsed_query.get('intent', 'unknown'),
                'original_message': user_message
            }
            
            # Use LLM for comprehensive e-commerce support
            if self.llm.is_model_loaded():
                return self.llm.generate_response(user_message, context)
            else:
                # Fallback to rule-based responses
                return self._handle_general_query_fallback(user_message)
                
        except Exception as e:
            self.logger.error(f"❌ Error in general e-commerce query: {e}")
            return self.llm._fallback_response(user_message, context)
    
    def _try_broader_search_or_suggestions(self, parsed_query: Dict[str, Any]) -> str:
        """Try broader search when no products found"""
        try:
            # Try without price filter
            if parsed_query['max_price']:
                broader_products = self.db_handler.search_products(
                    category=parsed_query['category'],
                    color=parsed_query['color'],
                    gender=parsed_query['gender'],
                    max_price=None,
                    limit=self.config.MAX_RESULTS
                )
                if broader_products:
                    response = f"No products found within your price range, but here are similar items:\n\n"
                    response += self.response_formatter.format_products_response(broader_products, parsed_query)
                    return response
            
            # Try with just category
            if parsed_query['category']:
                category_products = self.db_handler.search_products(
                    category=parsed_query['category'],
                    color=None,
                    gender=None,
                    max_price=None,
                    limit=self.config.MAX_RESULTS
                )
                if category_products:
                    response = f"Here are {parsed_query['category']} items available:\n\n"
                    response += self.response_formatter.format_products_response(category_products, parsed_query)
                    return response
            
            # Show random products as suggestions
            return self._show_random_products()
            
        except Exception as e:
            self.logger.error(f"❌ Error in broader search: {e}")
            return self.response_formatter.format_no_results_response(parsed_query)
    
    def _handle_general_query_fallback(self, message: str) -> str:
        """Fallback for general queries when LLM is not available"""
        message_lower = message.lower()
        
        # Check for stats request
        if any(word in message_lower for word in ['stats', 'statistics', 'inventory', 'total']):
            return self._get_inventory_stats()
        
        # Check for category listing
        if any(word in message_lower for word in ['categories', 'types', 'what do you have']):
            return self._get_available_categories()
        
        # Check for color listing
        if any(word in message_lower for word in ['colors', 'available colors']):
            return self._get_available_colors()
        
        # Default: show random products
        return self._show_random_products()
    
    def _get_inventory_stats(self) -> str:
        """Get and format inventory statistics"""
        try:
            stats = self.db_handler.get_stats()
            return self.response_formatter.format_stats_response(stats)
        except Exception as e:
            self.logger.error(f"❌ Error getting stats: {e}")
            return "Sorry, I couldn't fetch inventory statistics right now 😅"
    
    def _get_available_categories(self) -> str:
        """Get and format available categories"""
        try:
            categories = self.db_handler.get_categories()
            if categories:
                response = "🏷️ **Available Categories:**\n\n"
                for i, category in enumerate(categories[:15], 1):  # Show max 15
                    response += f"{i}. {category}\n"
                response += "\n💡 Just tell me what you're looking for!"
                return response
            else:
                return "Sorry, I couldn't fetch categories right now 😅"
        except Exception as e:
            self.logger.error(f"❌ Error getting categories: {e}")
            return "Sorry, I couldn't fetch categories right now 😅"
    
    def _get_available_colors(self) -> str:
        """Get and format available colors"""
        try:
            colors = self.db_handler.get_colors()
            if colors:
                response = "🎨 **Available Colors:**\n\n"
                color_list = ", ".join(colors[:20])  # Show max 20 colors
                response += f"{color_list}\n\n"
                response += "💡 Try: \"Show me red dresses\" or \"Find blue shirts for men\""
                return response
            else:
                return "Sorry, I couldn't fetch colors right now 😅"
        except Exception as e:
            self.logger.error(f"❌ Error getting colors: {e}")
            return "Sorry, I couldn't fetch colors right now 😅"
    
    def _show_random_products(self) -> str:
        """Show random products as suggestions"""
        try:
            products = self.db_handler.get_random_products(5)
            if products:
                response = "🎲 **Here are some popular items you might like:**\n\n"
                for i, product in enumerate(products, 1):
                    name = product.get('product_name', 'Unknown')
                    price = product.get('price', 0)
                    color = product.get('color', 'N/A')
                    category = product.get('product_category', 'Fashion')
                    
                    response += f"{i}. **{name}** - ₹{int(price):,}\n"
                    response += f"   🎨 {color} | 🏷️ {category}\n\n"
                
                response += "💡 Want something specific? Just ask! Example: \"Show red dresses under ₹2000\""
                return response
            else:
                return self.response_formatter.format_help_response()
        except Exception as e:
            self.logger.error(f"❌ Error showing random products: {e}")
            return self.response_formatter.format_help_response()
    
    def get_product_details(self, product_id: str) -> str:
        """Get detailed information about a specific product"""
        try:
            product = self.db_handler.get_product_by_id(product_id)
            if product:
                return self._format_product_details(product)
            else:
                return f"Sorry, I couldn't find product with ID: {product_id} 😅"
        except Exception as e:
            self.logger.error(f"❌ Error getting product details: {e}")
            return "Sorry, I couldn't fetch product details right now 😅"
    
    def _format_product_details(self, product: Dict[str, Any]) -> str:
        """Format detailed product information"""
        name = product.get('product_name', 'Unknown Product')
        price = product.get('price', 0)
        description = product.get('product_description', 'No description available')
        color = product.get('color', 'Not specified')
        size = product.get('size', 'Not specified')
        gender = product.get('gender', 'Unisex')
        category = product.get('product_category', 'Fashion')
        stock = product.get('stock', 0)
        
        response = f"🛍️ **{name}**\n\n"
        response += f"💰 **Price:** ₹{int(price):,}\n"
        response += f"🎨 **Color:** {color}\n"
        response += f"📏 **Size:** {size}\n"
        response += f"👤 **Gender:** {gender.title()}\n"
        response += f"🏷️ **Category:** {category}\n"
        response += f"📦 **Stock:** {self.response_formatter._get_stock_status(stock)}\n\n"
        response += f"📝 **Description:**\n{description}\n\n"
        
        # Add image if available
        image_url = product.get('product_image')
        if image_url:
            response += f"🖼️ [View Product Image]({image_url})"
        
        return response
    
    def get_llm_status(self) -> Dict[str, Any]:
        """Get LLM integration status"""
        return self.llm.get_model_info()
    
    def close(self):
        """Clean up resources"""
        try:
            self.db_handler.disconnect()
            self.logger.info("🔌 Chat agent closed successfully")
        except Exception as e:
            self.logger.error(f"❌ Error closing chat agent: {e}")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()