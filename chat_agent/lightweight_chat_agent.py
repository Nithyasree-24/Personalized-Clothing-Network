"""
Lightweight Chat Agent for FashionPulse
Works immediately without heavy LLM models - uses enhanced rule-based responses
"""
import logging
from typing import Dict, Any, Optional, List
from database import DatabaseHandler
from query_parser import QueryParser
from response_formatter import ResponseFormatter
from config import ChatAgentConfig

class LightweightFashionPulseChatAgent:
    def __init__(self):
        self.config = ChatAgentConfig()
        self.db_handler = DatabaseHandler()
        self.query_parser = QueryParser()
        self.response_formatter = ResponseFormatter()
        self.logger = logging.getLogger(__name__)
        
        # E-commerce knowledge base for comprehensive responses
        self.ecommerce_knowledge = {
            "shipping": {
                "standard": "5-7 business days",
                "express": "2-3 business days", 
                "overnight": "Next business day",
                "free_shipping_threshold": 1500
            },
            "returns": {
                "window": "30 days",
                "condition": "unworn with tags",
                "process": "Contact customer service or use our return portal"
            },
            "sizing": {
                "guide": "Check our size chart for accurate measurements",
                "exchange": "Free size exchanges within 15 days"
            },
            "payment": {
                "methods": ["Credit Card", "Debit Card", "UPI", "Net Banking", "COD"],
                "security": "All payments are secured with 256-bit SSL encryption"
            },
            "support": {
                "hours": "9 AM - 9 PM IST",
                "channels": ["Chat", "Email", "Phone"],
                "response_time": "Within 24 hours"
            }
        }
        
        # Initialize database connection
        self._initialize()
    
    def _initialize(self):
        """Initialize the chat agent"""
        try:
            if self.db_handler.connect():
                self.logger.info("🤖 Lightweight FashionPulse Chat Agent initialized successfully")
            else:
                self.logger.error("❌ Failed to initialize chat agent - database connection failed")
        except Exception as e:
            self.logger.error(f"❌ Chat agent initialization error: {e}")
    
    def process_message(self, user_message: str) -> str:
        """
        Main method to process user message and return response
        Enhanced with comprehensive e-commerce support and flow handling
        
        Args:
            user_message (str): User's input message or JSON flow data
            
        Returns:
            str: Formatted response
        """
        try:
            self.logger.info(f"💬 Processing message: {user_message}")
            
            # Check if this is a flow message (JSON format)
            try:
                import json
                flow_data = json.loads(user_message)
                if isinstance(flow_data, dict) and 'type' in flow_data:
                    return self._handle_flow_message(flow_data)
                elif isinstance(flow_data, dict) and 'message' in flow_data:
                    # Regular message with flow context
                    actual_message = flow_data['message']
                    flow_context = {
                        'flow': flow_data.get('flow', 'none'),
                        'flowData': flow_data.get('flowData', {})
                    }
                    return self._process_message_with_flow_context(actual_message, flow_context)
            except (json.JSONDecodeError, ValueError):
                # Not JSON, process as regular message
                pass
            
            # Parse user query
            parsed_query = self.query_parser.parse_user_query(user_message)
            
            # Determine if this is a product search query
            is_product_query = self._is_product_search_query(parsed_query, user_message)
            
            if is_product_query:
                # Handle product search with database
                return self._handle_product_search(parsed_query, user_message)
            else:
                # Handle general e-commerce queries with enhanced responses
                return self._handle_general_ecommerce_query(user_message, parsed_query)
                
        except Exception as e:
            self.logger.error(f"❌ Error processing message: {e}")
            return self.response_formatter.format_error_response(str(e))
    
    def _handle_flow_message(self, flow_data: Dict[str, Any]) -> str:
        """Handle flow-specific messages (Face Tone, Body Fit, and Event flows)"""
        try:
            flow_type = flow_data.get('type')
            
            if flow_type == 'faceToneFlow':
                return self._handle_face_tone_flow(flow_data)
            elif flow_type == 'bodyFitFlow':
                return self._handle_body_fit_flow(flow_data)
            elif flow_type == 'eventOutfitSuggestion':
                return self._handle_event_outfit_suggestion(flow_data)
            else:
                return "Sorry, I don't understand that flow type."
                
        except Exception as e:
            self.logger.error(f"❌ Error handling flow message: {e}")
            return "Sorry, I encountered an error processing your request."
    
    def _handle_face_tone_flow(self, flow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle Face Tone flow product search"""
        try:
            color = flow_data.get('color', '').lower()
            gender = flow_data.get('gender', '').lower()
            category = flow_data.get('category', '')
            
            self.logger.info(f"🎨 Face Tone Flow - Color: {color}, Gender: {gender}, Category: {category}")
            
            # Search products based on face tone flow criteria
            products = self.db_handler.search_products(
                category=category,
                color=color,
                gender=gender,
                max_price=None,
                limit=10
            )
            
            self.logger.info(f"🔍 Face Tone Flow found {len(products)} products")
            
            if products:
                response_text = f"🎨 Perfect match! Here are {color} {category.lower()} for {gender} that will complement your skin tone:"
                return {
                    'type': 'face_tone_flow_result',
                    'response': response_text,
                    'products': products,
                    'search_criteria': {
                        'color': color,
                        'gender': gender,
                        'category': category
                    }
                }
            else:
                return {
                    'type': 'face_tone_flow_result',
                    'response': f"Sorry, no matching {color} {category.lower()} found for {gender}. Please try different options.",
                    'products': [],
                    'search_criteria': {
                        'color': color,
                        'gender': gender,
                        'category': category
                    }
                }
                
        except Exception as e:
            self.logger.error(f"❌ Error in face tone flow: {e}")
            return {
                'type': 'face_tone_flow_result',
                'response': "Sorry, I couldn't process your face tone selection right now.",
                'products': [],
                'error': str(e)
            }
    
    def _handle_body_fit_flow(self, flow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle Body Fit flow product search with intelligent recommendations"""
        try:
            gender = flow_data.get('gender', '').lower()
            body_shape = flow_data.get('bodyShape', '')
            category = flow_data.get('category', '')
            color = flow_data.get('color', '')
            
            self.logger.info(f"👕 Body Fit Flow - Gender: {gender}, Body Shape: {body_shape}, Category: {category}, Color: {color}")
            
            # If we have all parameters, search for products
            if category and color:
                products = self.db_handler.search_products(
                    category=category,
                    color=color.lower(),
                    gender=gender,
                    max_price=None,
                    limit=10
                )
                
                self.logger.info(f"🔍 Body Fit Flow found {len(products)} products")
                
                if products:
                    response_text = f"👕 Perfect fit! Here are {color.lower()} {category.lower()} that will look amazing on your {body_shape.lower()} body shape:"
                    return {
                        'type': 'body_fit_flow_result',
                        'response': response_text,
                        'products': products,
                        'search_criteria': {
                            'gender': gender,
                            'body_shape': body_shape,
                            'category': category,
                            'color': color
                        }
                    }
                else:
                    return {
                        'type': 'body_fit_flow_result',
                        'response': f"Sorry, no matching {color.lower()} {category.lower()} found for {gender}. Please try different options.",
                        'products': [],
                        'search_criteria': {
                            'gender': gender,
                            'body_shape': body_shape,
                            'category': category,
                            'color': color
                        }
                    }
            else:
                # Return step-by-step guidance (handled by frontend)
                return {
                    'type': 'body_fit_flow_step',
                    'response': "Let me guide you through finding the perfect fit!",
                    'products': [],
                    'flow_data': flow_data
                }
                
        except Exception as e:
            self.logger.error(f"❌ Error in body fit flow: {e}")
            return {
                'type': 'body_fit_flow_result',
                'response': "Sorry, I couldn't process your body fit selection right now.",
                'products': [],
                'error': str(e)
            }
    
    def get_body_shape_recommendations(self, gender: str, body_shape: str) -> List[str]:
        """Get recommended categories based on gender and body shape"""
        
        # Body shape recommendations based on fashion expertise
        recommendations = {
            'women': {
                'hourglass': ['Dresses', 'Western Wear', 'Tops and Co-ord Sets'],  # Emphasize waist
                'pear': ['Tops and Co-ord Sets', 'Western Wear', 'Ethnic Wear'],    # Balance upper body
                'apple': ['Dresses', 'Tops and Co-ord Sets', 'Western Wear'],       # Create waist definition
                'rectangle': ['Dresses', 'Western Wear', 'Ethnic Wear'],            # Create curves
                'inverted triangle': ['Dresses', 'Western Wear', 'Ethnic Wear']     # Balance shoulders
            },
            'men': {
                'rectangle': ['Shirts', 'T-shirts', 'Hoodies'],      # Add structure
                'triangle': ['Shirts', 'Hoodies', 'T-shirts'],       # Balance proportions
                'inverted triangle': ['T-shirts', 'Shirts', 'Hoodies'], # Complement broad shoulders
                'oval': ['Shirts', 'T-shirts', 'Hoodies'],           # Streamline silhouette
                'trapezoid': ['Shirts', 'T-shirts', 'Hoodies']       # Enhance upper body
            }
        }
        
        gender_key = gender.lower()
        shape_key = body_shape.lower()
        
        if gender_key in recommendations and shape_key in recommendations[gender_key]:
            return recommendations[gender_key][shape_key]
        
        # Fallback to all categories for that gender
        if gender_key == 'women':
            return ['Western Wear', 'Dresses', 'Ethnic Wear', 'Tops and Co-ord Sets']
        else:
            return ['Shirts', 'T-shirts', 'Hoodies']
    
    def _handle_event_outfit_suggestion(self, flow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle event-based outfit suggestions"""
        try:
            gender = flow_data.get('gender', '').lower()
            event_type = flow_data.get('eventType', '').lower()
            event_date = flow_data.get('eventDate', '')
            
            self.logger.info(f"📅 Event Outfit Suggestion - Gender: {gender}, Event: {event_type}, Date: {event_date}")
            
            # Get recommended categories based on gender and event type
            recommended_categories = self._get_event_categories(gender, event_type)
            
            # Search for products in recommended categories
            all_products = []
            for category in recommended_categories:
                products = self.db_handler.search_products(
                    category=category,
                    color=None,
                    gender=gender,
                    max_price=None,
                    limit=3  # Limit per category to get variety
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
            
            self.logger.info(f"🔍 Event Outfit Suggestion found {len(unique_products)} products")
            
            if unique_products:
                response_text = f"✨ Perfect outfits for your {event_type} on {event_date}! Here are my top recommendations:"
                return {
                    'type': 'event_outfit_result',
                    'response': response_text,
                    'products': unique_products,
                    'event_info': {
                        'gender': gender,
                        'event_type': event_type,
                        'event_date': event_date,
                        'categories': recommended_categories
                    }
                }
            else:
                return {
                    'type': 'event_outfit_result',
                    'response': f"Sorry, I couldn't find suitable outfits for your {event_type}. Please try browsing our collection manually.",
                    'products': [],
                    'event_info': {
                        'gender': gender,
                        'event_type': event_type,
                        'event_date': event_date,
                        'categories': recommended_categories
                    }
                }
                
        except Exception as e:
            self.logger.error(f"❌ Error in event outfit suggestion: {e}")
            return {
                'type': 'event_outfit_result',
                'response': "Sorry, I couldn't process your event outfit request right now.",
                'products': [],
                'error': str(e)
            }
    
    def _get_event_categories(self, gender: str, event_type: str) -> List[str]:
        """Get recommended categories based on gender and event type"""
        
        event_type_lower = event_type.lower()
        
        if gender == 'women':
            # Women's event-based recommendations
            if any(keyword in event_type_lower for keyword in ['job', 'interview', 'office', 'meeting', 'work']):
                return ['Western Wear', 'Tops and Co-ord Sets', 'Dresses']
            elif any(keyword in event_type_lower for keyword in ['wedding', 'engagement', 'reception', 'marriage']):
                return ['Ethnic Wear', 'Dresses']
            elif any(keyword in event_type_lower for keyword in ['birthday', 'party', 'night out', 'celebration', 'club']):
                return ['Western Wear', 'Dresses', 'Tops and Co-ord Sets']
            elif any(keyword in event_type_lower for keyword in ['college', 'daily', 'casual', 'university', 'school']):
                return ['Tops and Co-ord Sets', 'Western Wear', 'Dresses']
            elif any(keyword in event_type_lower for keyword in ['festival', 'diwali', 'pongal', 'navratri', 'eid', 'onam', 'traditional']):
                return ['Ethnic Wear', 'Dresses']
            elif any(keyword in event_type_lower for keyword in ['family', 'temple', 'religious', 'function']):
                return ['Ethnic Wear', 'Dresses']
            elif any(keyword in event_type_lower for keyword in ['travel', 'trip', 'photoshoot', 'vacation', 'holiday']):
                return ['Western Wear', 'Dresses', 'Tops and Co-ord Sets']
            else:
                # Default for women
                return ['Western Wear', 'Dresses', 'Tops and Co-ord Sets']
        
        else:  # men
            # Men's event-based recommendations
            if any(keyword in event_type_lower for keyword in ['job', 'interview', 'office', 'meeting', 'work']):
                return ['Shirts']
            elif any(keyword in event_type_lower for keyword in ['wedding', 'engagement', 'reception', 'marriage']):
                return ['Shirts']
            elif any(keyword in event_type_lower for keyword in ['party', 'celebration', 'night out', 'club']):
                return ['Shirts', 'T-shirts']
            elif any(keyword in event_type_lower for keyword in ['college', 'daily', 'casual', 'university', 'school']):
                return ['T-shirts', 'Shirts']
            elif any(keyword in event_type_lower for keyword in ['festival', 'diwali', 'pongal', 'eid', 'onam', 'traditional']):
                return ['Shirts']
            elif any(keyword in event_type_lower for keyword in ['travel', 'trip', 'photoshoot', 'vacation', 'holiday']):
                return ['Shirts', 'T-shirts']
            else:
                # Default for men
                return ['Shirts', 'T-shirts']
    
    def _process_message_with_flow_context(self, message: str, flow_context: Dict[str, Any]) -> str:
        """Process regular message with flow context"""
        # For now, just process as regular message
        # You could add flow-aware processing here if needed
        parsed_query = self.query_parser.parse_user_query(message)
        is_product_query = self._is_product_search_query(parsed_query, message)
        
        if is_product_query:
            return self._handle_product_search(parsed_query, message)
        else:
            return self._handle_general_ecommerce_query(message, parsed_query)
    
    def _is_product_search_query(self, parsed_query: Dict[str, Any], user_message: str) -> bool:
        """Determine if the query is primarily about product search"""
        
        message_lower = user_message.lower().strip()
        
        # Handle greetings and casual conversation first
        greeting_words = [
            'hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening',
            'how are you', 'what\'s up', 'whatsup', 'sup', 'greetings'
        ]
        
        # If it's just a greeting, don't treat as product search
        if any(greeting in message_lower for greeting in greeting_words) and len(message_lower.split()) <= 3:
            return False
        
        # Handle general conversation
        general_conversation = [
            'thank you', 'thanks', 'bye', 'goodbye', 'see you', 'nice', 'great',
            'awesome', 'cool', 'ok', 'okay', 'yes', 'no', 'maybe'
        ]
        
        if any(word in message_lower for word in general_conversation) and len(message_lower.split()) <= 2:
            return False
        
        # Check if query has explicit product search criteria
        has_search_criteria = any([
            parsed_query['category'],
            parsed_query['color'], 
            parsed_query['gender'],
            parsed_query['max_price']
        ])
        
        # Check for explicit product search intent
        explicit_search_words = [
            'show me', 'find me', 'search for', 'looking for', 'i want', 'i need',
            'can you show', 'display', 'browse', 'shop for'
        ]
        
        has_explicit_search = any(phrase in message_lower for phrase in explicit_search_words)
        
        # Check for product-related keywords (but only if combined with search intent)
        product_keywords = [
            'dress', 'shirt', 'jeans', 'top', 'bottom', 'wear', 'clothes', 'clothing'
        ]
        
        has_product_keywords = any(keyword in message_lower for keyword in product_keywords)
        
        # Only treat as product search if:
        # 1. Has explicit search criteria, OR
        # 2. Has explicit search words, OR  
        # 3. Has product keywords AND search intent words
        return has_search_criteria or has_explicit_search or (has_product_keywords and has_explicit_search)
    
    def _handle_product_search(self, parsed_query: Dict[str, Any], user_message: str) -> str:
        """Handle product search queries with database results"""
        try:
            # Search the database
            products = self.db_handler.search_products(
                category=parsed_query['category'],
                color=parsed_query['color'],
                gender=parsed_query['gender'],
                max_price=parsed_query['max_price'],
                limit=self.config.MAX_RESULTS
            )
            
            if products:
                # Products found - return formatted response
                return self.response_formatter.format_products_response(products, parsed_query)
            else:
                # No products found - try broader search or suggestions
                return self._try_broader_search_or_suggestions(parsed_query)
                    
        except Exception as e:
            self.logger.error(f"❌ Error in product search: {e}")
            return self.response_formatter.format_error_response()
    
    def _handle_general_ecommerce_query(self, user_message: str, parsed_query: Dict[str, Any]) -> str:
        """Handle general e-commerce queries with comprehensive responses"""
        try:
            message_lower = user_message.lower().strip()
            
            # Handle greetings first
            greeting_words = [
                'hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening',
                'how are you', 'what\'s up', 'whatsup', 'sup', 'greetings'
            ]
            
            if any(greeting in message_lower for greeting in greeting_words):
                return self._handle_greeting(user_message)
            
            # Handle casual conversation
            if any(word in message_lower for word in ['thank you', 'thanks', 'ty']):
                return self._handle_thanks()
            
            if any(word in message_lower for word in ['bye', 'goodbye', 'see you', 'cya']):
                return self._handle_goodbye()
            
            if any(phrase in message_lower for phrase in ['how are you', 'how do you do']):
                return self._handle_how_are_you()
            
            if any(word in message_lower for word in ['nice', 'great', 'awesome', 'cool', 'amazing']):
                return self._handle_positive_feedback()
            
            # Shipping queries
            if any(word in message_lower for word in ['shipping', 'delivery', 'when will', 'how long']):
                return self._handle_shipping_query(user_message)
            
            # Return queries
            elif any(word in message_lower for word in ['return', 'refund', 'exchange']):
                return self._handle_return_query(user_message)
            
            # Cancellation queries  
            elif any(word in message_lower for word in ['cancel', 'cancellation', 'cancel order', 'cancel policy']):
                return self._handle_cancellation_query(user_message)
            
            # Sizing queries
            elif any(word in message_lower for word in ['size', 'fit', 'measurement']):
                return self._handle_sizing_query(user_message)
            
            # Payment queries
            elif any(word in message_lower for word in ['payment', 'pay', 'card', 'upi', 'cod']):
                return self._handle_payment_query(user_message)
            
            # Order tracking
            elif any(word in message_lower for word in ['order', 'track', 'status', 'where is']):
                return self._handle_order_query(user_message)
            
            # Cart queries
            elif any(word in message_lower for word in ['cart', 'my cart', 'show cart', 'cart items', 'what\'s in cart']):
                return self._handle_cart_query(user_message)
            
            # Wishlist queries  
            elif any(word in message_lower for word in ['wishlist', 'my wishlist', 'show wishlist', 'saved items', 'favorites']):
                return self._handle_wishlist_query(user_message)
            
            # My orders queries
            elif any(word in message_lower for word in ['my orders', 'show orders', 'order history', 'past orders']):
                return self._handle_my_orders_query(user_message)
            
            # General support
            elif any(word in message_lower for word in ['help', 'support', 'contact', 'problem']):
                return self._handle_support_query(user_message)
            
            # Stats and inventory
            elif any(word in message_lower for word in ['stats', 'statistics', 'inventory', 'total']):
                return self._get_inventory_stats()
            
            # Categories
            elif any(word in message_lower for word in ['categories', 'types', 'what do you have']):
                return self._get_available_categories()
            
            # Colors
            elif any(word in message_lower for word in ['colors', 'available colors']):
                return self._get_available_colors()
            
            # Default: friendly conversational response
            else:
                return self._handle_general_conversation(user_message)
                
        except Exception as e:
            self.logger.error(f"❌ Error in general e-commerce query: {e}")
            return self._get_default_help_response()
    
    def _handle_shipping_query(self, user_message: str) -> str:
        """Handle shipping-related queries - fetch from database"""
        try:
            # Try to get policy from database first
            policy_info = self._get_policy_from_database('shipping_policy')
            
            if policy_info:
                return policy_info
            
            # Fallback to default policy if not found in database
            response = f"📦 **Shipping Information:**\n\n"
            response += f"• **Standard Delivery:** 5-7 business days\n"
            response += f"• **Express Delivery:** 2-3 business days\n"
            response += f"• **Free Shipping:** On orders ₹500+\n\n"
            
            if 'cost' in user_message.lower() or 'charge' in user_message.lower():
                response += f"💰 **Shipping Costs:**\n"
                response += f"• Standard: ₹50 (Free on orders ₹500+)\n"
                response += f"• Express: ₹150\n"
                response += f"• Same Day: ₹250 (select cities)\n\n"
            
            response += f"📍 **Coverage:** Pan-India delivery available\n"
            response += f"📋 **Tracking:** SMS and email updates provided\n\n"
            response += f"Need help with a specific order? Share your order number! 📋"
            
            return response
            
        except Exception as e:
            self.logger.error(f"❌ Error in shipping query: {e}")
            return "I'm sorry, I cannot find policy details right now. Please try again later."
    
    def _handle_return_query(self, user_message: str) -> str:
        """Handle return and exchange queries - fetch from database"""
        try:
            # Try to get policy from database first
            policy_info = self._get_policy_from_database('return_policy')
            
            if policy_info:
                return policy_info
            
            # Fallback to default policy if not found in database
            response = f"🔄 **Returns & Exchanges:**\n\n"
            response += f"• **Return Window:** 7 days from delivery date\n"
            response += f"• **Condition:** Items must be unused with original tags\n"
            response += f"• **Process:** Contact customer service or use return portal\n"
            response += f"• **Size Exchanges:** Free exchanges within 7 days\n\n"
            
            response += f"📋 **Return Process:**\n"
            response += f"1. Contact customer service or use return portal\n"
            response += f"2. Schedule pickup or drop at nearest center\n"
            response += f"3. Refund processed within 5-7 business days\n\n"
            
            if 'refund' in user_message.lower():
                response += f"💰 **Refund Information:**\n"
                response += f"• Original payment method: 5-7 business days\n"
                response += f"• Store credit: Instant\n"
                response += f"• COD orders: Bank transfer within 7 days\n\n"
            
            response += f"Need help with a specific return? I'm here to assist! 😊"
            
            return response
            
        except Exception as e:
            self.logger.error(f"❌ Error in return query: {e}")
            return "I'm sorry, I cannot find policy details right now. Please try again later."
    
    def _handle_sizing_query(self, user_message: str) -> str:
        """Handle sizing and fit queries"""
        response = f"📏 **Sizing Help:**\n\n"
        response += f"• {self.ecommerce_knowledge['sizing']['guide']}\n"
        response += f"• {self.ecommerce_knowledge['sizing']['exchange']}\n\n"
        
        response += f"📐 **Size Guide Tips:**\n"
        response += f"• Measure yourself with a tape measure\n"
        response += f"• Check product-specific size charts\n"
        response += f"• Consider fabric stretch and fit preference\n"
        response += f"• Read customer reviews for fit feedback\n\n"
        
        response += f"👕 **Common Size Conversions:**\n"
        response += f"• XS: 32-34 | S: 34-36 | M: 36-38 | L: 38-40 | XL: 40-42\n\n"
        
        response += f"🔄 **Size Exchange:**\n"
        response += f"• Free exchanges within 15 days\n"
        response += f"• Same product, different size only\n"
        response += f"• Subject to availability\n\n"
        
        response += f"Need specific size advice? Tell me the product and your measurements! ✨"
        
        return response
    
    def _handle_payment_query(self, user_message: str) -> str:
        """Handle payment-related queries"""
        methods = ", ".join(self.ecommerce_knowledge['payment']['methods'])
        
        response = f"💳 **Payment Options:**\n\n"
        response += f"• **Available Methods:** {methods}\n"
        response += f"• **Security:** {self.ecommerce_knowledge['payment']['security']}\n\n"
        
        response += f"💰 **Payment Details:**\n"
        response += f"• **Credit/Debit Cards:** Visa, MasterCard, RuPay, Amex\n"
        response += f"• **UPI:** All major UPI apps supported\n"
        response += f"• **Net Banking:** 50+ banks supported\n"
        response += f"• **COD:** Available for orders under ₹5000\n\n"
        
        if 'fail' in user_message.lower() or 'problem' in user_message.lower():
            response += f"🔧 **Payment Issues:**\n"
            response += f"• Check internet connection\n"
            response += f"• Verify card details and limits\n"
            response += f"• Try different payment method\n"
            response += f"• Contact your bank if needed\n\n"
        
        response += f"🔒 **Security Features:**\n"
        response += f"• 256-bit SSL encryption\n"
        response += f"• PCI DSS compliant\n"
        response += f"• OTP verification for cards\n"
        response += f"• No card details stored\n\n"
        
        response += f"Having payment issues? Let me know the specific problem! 🔒"
        
        return response
    
    def _handle_order_query(self, user_message: str) -> str:
        """Handle order tracking and status queries"""
        response = f"📦 **Order Tracking:**\n\n"
        
        # Check if user provided order number
        import re
        order_pattern = r'#?FP\d+'
        order_match = re.search(order_pattern, user_message, re.IGNORECASE)
        
        if order_match:
            order_num = order_match.group()
            response += f"🔍 **Tracking Order {order_num}:**\n"
            response += f"I'd love to help track your order! For real-time tracking:\n\n"
            response += f"1. **Login to your account** on our website\n"
            response += f"2. **Go to 'My Orders'** section\n"
            response += f"3. **Click on order {order_num}** for details\n\n"
            response += f"Or contact customer service with your order number! 📞\n\n"
        else:
            response += f"To track your order, I'll need your:\n"
            response += f"• **Order number** (starts with #FP)\n"
            response += f"• **Registered email** or phone number\n\n"
        
        response += f"📋 **Order Status Guide:**\n"
        response += f"• **Confirmed:** Order received and being processed\n"
        response += f"• **Packed:** Order packed and ready for dispatch\n"
        response += f"• **Shipped:** Order dispatched from warehouse\n"
        response += f"• **Out for Delivery:** Order with delivery partner\n"
        response += f"• **Delivered:** Order successfully delivered\n\n"
        
        response += f"📱 **Tracking Updates:**\n"
        response += f"• SMS notifications at each stage\n"
        response += f"• Email updates with tracking links\n"
        response += f"• Real-time tracking on website\n\n"
        
        response += f"Need help with a specific order? Share your order number! 🚚"
        
        return response
    
    def _handle_support_query(self, user_message: str) -> str:
        """Handle general support queries"""
        response = f"💬 **Customer Support:**\n\n"
        response += f"• **Hours:** {self.ecommerce_knowledge['support']['hours']}\n"
        response += f"• **Response Time:** {self.ecommerce_knowledge['support']['response_time']}\n"
        response += f"• **Channels:** {', '.join(self.ecommerce_knowledge['support']['channels'])}\n\n"
        
        response += f"🛍️ **I can help you with:**\n"
        response += f"• Product searches & recommendations\n"
        response += f"• Order tracking & modifications\n"
        response += f"• Returns & exchanges\n"
        response += f"• Sizing guidance\n"
        response += f"• Payment support\n"
        response += f"• Shipping information\n\n"
        
        response += f"📞 **Contact Information:**\n"
        response += f"• **Email:** support@fashionpulse.com\n"
        response += f"• **Phone:** 1800-123-4567 (Toll-free)\n"
        response += f"• **Chat:** Available on website\n\n"
        
        response += f"🎯 **Quick Help:**\n"
        response += f"• \"Show me red dresses\" - Product search\n"
        response += f"• \"Track order #FP12345\" - Order tracking\n"
        response += f"• \"Return policy\" - Policy information\n"
        response += f"• \"Size guide\" - Sizing help\n\n"
        
        response += f"What would you like help with today? 😊"
        
        return response
    
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
            return self._show_random_products_with_help()
            
        except Exception as e:
            self.logger.error(f"❌ Error in broader search: {e}")
            return self.response_formatter.format_no_results_response(parsed_query)
    
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
    
    def _show_random_products_with_help(self) -> str:
        """Show random products with helpful suggestions"""
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
                
                response += "💡 **Try asking me:**\n"
                response += "• \"Show red dresses under ₹2000\"\n"
                response += "• \"What's your return policy?\"\n"
                response += "• \"How long does shipping take?\"\n"
                response += "• \"Help me with sizing\"\n"
                
                return response
            else:
                return self._get_default_help_response()
        except Exception as e:
            self.logger.error(f"❌ Error showing random products: {e}")
            return self._get_default_help_response()
    
    def _handle_greeting(self, user_message: str) -> str:
        """Handle greeting messages with friendly responses"""
        import random
        
        greetings = [
            "Hi there! 👋 I'm your FashionPulse style assistant. How can I help you today?",
            "Hello! 😊 Welcome to FashionPulse! I'm here to help you find amazing fashion pieces.",
            "Hey! 🌟 Great to see you! I'm your personal fashion assistant. What are you looking for?",
            "Hi! 👗 I'm excited to help you discover some fantastic fashion finds today!",
            "Hello there! ✨ I'm your FashionPulse assistant, ready to help with all your fashion needs!"
        ]
        
        message_lower = user_message.lower()
        
        # Time-based greetings
        if 'morning' in message_lower:
            return "Good morning! ☀️ Ready to start your day with some amazing fashion finds? How can I help you?"
        elif 'afternoon' in message_lower:
            return "Good afternoon! 🌤️ Hope you're having a great day! What fashion pieces are you looking for?"
        elif 'evening' in message_lower:
            return "Good evening! 🌙 Perfect time for some fashion browsing! How can I assist you?"
        
        return random.choice(greetings)
    
    def _handle_thanks(self) -> str:
        """Handle thank you messages"""
        import random
        
        thanks_responses = [
            "You're very welcome! 😊 Happy to help anytime!",
            "My pleasure! 🌟 Is there anything else I can help you with?",
            "Glad I could help! 💫 Feel free to ask me anything else!",
            "You're welcome! 👍 I'm always here if you need more assistance!",
            "Happy to help! ✨ Let me know if you need anything else!"
        ]
        
        return random.choice(thanks_responses)
    
    def _handle_goodbye(self) -> str:
        """Handle goodbye messages"""
        import random
        
        goodbye_responses = [
            "Goodbye! 👋 Thanks for visiting FashionPulse. Come back soon!",
            "See you later! 🌟 Hope you found what you were looking for!",
            "Bye! 💫 Have a wonderful day and happy shopping!",
            "Take care! 😊 Don't forget to check out our new arrivals!",
            "Goodbye! ✨ It was great helping you today!"
        ]
        
        return random.choice(goodbye_responses)
    
    def _handle_how_are_you(self) -> str:
        """Handle 'how are you' questions"""
        import random
        
        responses = [
            "I'm doing great, thank you for asking! 😊 I'm excited to help you find some amazing fashion pieces today!",
            "I'm fantastic! 🌟 Ready to help you discover your next favorite outfit. How are you doing?",
            "I'm wonderful, thanks! 💫 I love helping people find perfect fashion matches. What brings you here today?",
            "I'm doing excellent! ✨ Always happy when I get to help with fashion choices. How can I assist you?",
            "I'm great! 👗 Passionate about helping you find the perfect style. What are you looking for today?"
        ]
        
        return random.choice(responses)
    
    def _handle_positive_feedback(self) -> str:
        """Handle positive feedback"""
        import random
        
        responses = [
            "Thank you! 😊 I'm so glad you're happy! Is there anything else I can help you with?",
            "That's wonderful to hear! 🌟 I love making your shopping experience great!",
            "Awesome! 💫 I'm thrilled I could help. What else would you like to explore?",
            "So glad you think so! ✨ I'm here whenever you need fashion assistance!",
            "That makes my day! 👍 Happy to help you anytime with your fashion needs!"
        ]
        
        return random.choice(responses)
    
    def _handle_general_conversation(self, user_message: str) -> str:
        """Handle general conversation that doesn't fit other categories"""
        import random
        
        # Check for questions about the assistant
        message_lower = user_message.lower()
        
        if any(phrase in message_lower for phrase in ['who are you', 'what are you', 'tell me about yourself']):
            return ("I'm your FashionPulse AI assistant! 🤖✨ I'm here to help you:\n\n"
                   "👗 Find perfect fashion pieces\n"
                   "🛍️ Browse our amazing collection\n"
                   "📦 Track orders and handle returns\n"
                   "💡 Get style advice and recommendations\n"
                   "📏 Help with sizing and fit\n\n"
                   "I'm like having a personal fashion consultant right in your pocket! What would you like to explore?")
        
        if any(phrase in message_lower for phrase in ['what can you do', 'how can you help']):
            return self._handle_support_query(user_message)
        
        # General friendly responses
        friendly_responses = [
            "I'm here to help! 😊 Feel free to ask me about our fashion collection, orders, returns, or anything else!",
            "That's interesting! 🌟 Is there anything fashion-related I can help you with today?",
            "I'd love to help you with that! 💫 What specifically are you looking for?",
            "Absolutely! ✨ I'm here to make your fashion shopping experience amazing. How can I assist?",
            "I understand! 👍 Let me know if you need help finding clothes, tracking orders, or anything else!"
        ]
        
        return random.choice(friendly_responses)
    
    def _get_default_help_response(self) -> str:
        """Get default help response"""
        return f"Hi! I'm your FashionPulse assistant 👗 I can help you with:\n\n🛍️ **Product Search** - Find clothes by style, color, price\n📦 **Orders** - Track, modify, or cancel orders\n🔄 **Returns** - Return/exchange policies and process\n📏 **Sizing** - Size guides and fit recommendations\n💳 **Payments** - Payment methods and billing\n🚚 **Shipping** - Delivery times and tracking\n\nWhat would you like to know? Just ask me anything! 😊"
    
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
    
    def _get_policy_from_database(self, policy_type: str) -> str:
        """Fetch policy information from database"""
        try:
            conn = self.db_handler.connect()
            if not conn:
                return None
                
            cursor = conn.cursor()
            
            # Check if policies table exists
            cursor.execute("SHOW TABLES LIKE 'policies'")
            if not cursor.fetchone():
                conn.close()
                return None
            
            # Fetch policy from database
            cursor.execute("SELECT policy_content FROM policies WHERE policy_type = %s", (policy_type,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return result[0]
            else:
                return None
                
        except Exception as e:
            self.logger.error(f"❌ Error fetching policy from database: {e}")
            return None
    
    def _handle_cancellation_query(self, user_message: str) -> str:
        """Handle order cancellation queries - fetch from database"""
        try:
            # Try to get policy from database first
            policy_info = self._get_policy_from_database('cancellation_policy')
            
            if policy_info:
                return policy_info
            
            # Fallback to default policy if not found in database
            response = f"❌ **Order Cancellation Policy:**\n\n"
            response += f"• **Cancellation Window:** Before order is shipped\n"
            response += f"• **Time Limit:** Within 24 hours of placing order\n"
            response += f"• **Refund:** Full refund for cancelled orders\n"
            response += f"• **Processing Time:** 3-5 business days for refund\n\n"
            
            response += f"📋 **How to Cancel:**\n"
            response += f"1. Go to 'My Orders' in your account\n"
            response += f"2. Find your order and click 'Cancel'\n"
            response += f"3. Select cancellation reason\n"
            response += f"4. Confirm cancellation\n\n"
            
            response += f"⚠️ **Important Notes:**\n"
            response += f"• Orders cannot be cancelled once shipped\n"
            response += f"• COD orders: Refund via bank transfer\n"
            response += f"• Prepaid orders: Refund to original payment method\n\n"
            
            response += f"📞 **Need Help?** Contact support: 1800-123-4567"
            
            return response
            
        except Exception as e:
            self.logger.error(f"❌ Error in cancellation query: {e}")
            return "I'm sorry, I cannot find policy details right now. Please try again later."
    
    def _handle_cart_query(self, user_message: str) -> str:
        """Handle cart-related queries - show cart contents"""
        try:
            # This will be handled by the frontend to pass cart data
            # Return a special response type that frontend can intercept
            return {
                'type': 'cart_request',
                'reply': "Let me show you what's in your cart! 🛒",
                'action': 'show_cart'
            }
        except Exception as e:
            self.logger.error(f"❌ Error in cart query: {e}")
            return "I'd love to show you your cart! Please make sure you're logged in and try again."
    
    def _handle_wishlist_query(self, user_message: str) -> str:
        """Handle wishlist-related queries - show wishlist contents"""
        try:
            # This will be handled by the frontend to pass wishlist data
            return {
                'type': 'wishlist_request', 
                'reply': "Here are your saved items! ❤️",
                'action': 'show_wishlist'
            }
        except Exception as e:
            self.logger.error(f"❌ Error in wishlist query: {e}")
            return "I'd love to show you your wishlist! Please make sure you're logged in and try again."
    
    def _handle_my_orders_query(self, user_message: str) -> str:
        """Handle my orders queries - show order history"""
        try:
            # This will be handled by the frontend to pass orders data
            return {
                'type': 'orders_request',
                'reply': "Here's your order history! 📦",
                'action': 'show_orders'
            }
        except Exception as e:
            self.logger.error(f"❌ Error in orders query: {e}")
            return "I'd love to show you your orders! Please make sure you're logged in and try again."
    
    def get_llm_status(self) -> Dict[str, Any]:
        """Get LLM integration status (lightweight version)"""
        return {
            "model_loaded": False,
            "model_name": "Lightweight Rule-Based Agent",
            "device": "cpu",
            "torch_available": False,
            "fallback_mode": True,
            "description": "Fast, lightweight chat agent with comprehensive e-commerce support"
        }
    
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