"""
Hugging Face Falcon 7B E-commerce LLM Integration
Integrates the SHJ622/falcon_7b_ecommerce_ai_chatbot_n100 model with FashionPulse
"""
import logging
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from typing import Dict, Any, Optional, List
import json
import re
from config import ChatAgentConfig

class FalconEcommerceLLM:
    def __init__(self):
        self.config = ChatAgentConfig()
        self.logger = logging.getLogger(__name__)
        self.model = None
        self.tokenizer = None
        self.pipeline = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # E-commerce knowledge base
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
        
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the Falcon 7B e-commerce model"""
        try:
            model_name = "SHJ622/falcon_7b_ecommerce_ai_chatbot_n100"
            
            self.logger.info(f"🤖 Loading Falcon 7B E-commerce model: {model_name}")
            
            # Try to load the model with different configurations
            try:
                # First attempt: Direct loading
                self.tokenizer = AutoTokenizer.from_pretrained(
                    model_name,
                    trust_remote_code=True,
                    padding_side="left"
                )
                
                # Add pad token if not present
                if self.tokenizer.pad_token is None:
                    self.tokenizer.pad_token = self.tokenizer.eos_token
                
                # Load model with optimizations
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_name,
                    trust_remote_code=True,
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                    device_map="auto" if self.device == "cuda" else None,
                    low_cpu_mem_usage=True
                )
                
            except Exception as e1:
                self.logger.warning(f"⚠️ Primary model loading failed: {e1}")
                self.logger.info("🔄 Trying alternative Falcon 7B model...")
                
                # Fallback to base Falcon 7B Instruct model
                fallback_model = "tiiuae/falcon-7b-instruct"
                
                self.tokenizer = AutoTokenizer.from_pretrained(
                    fallback_model,
                    trust_remote_code=True,
                    padding_side="left"
                )
                
                if self.tokenizer.pad_token is None:
                    self.tokenizer.pad_token = self.tokenizer.eos_token
                
                self.model = AutoModelForCausalLM.from_pretrained(
                    fallback_model,
                    trust_remote_code=True,
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                    device_map="auto" if self.device == "cuda" else None,
                    low_cpu_mem_usage=True
                )
                
                self.logger.info(f"✅ Loaded fallback model: {fallback_model}")
            
            # Create text generation pipeline
            self.pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if self.device == "cuda" else -1,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                max_new_tokens=512,
                repetition_penalty=1.1
            )
            
            self.logger.info(f"✅ Falcon 7B model loaded successfully on {self.device}")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to load Falcon 7B model: {e}")
            self.logger.info("🔄 Falling back to rule-based responses")
            self.model = None
            self.tokenizer = None
            self.pipeline = None
    
    def generate_response(self, user_query: str, context: Dict[str, Any] = None) -> str:
        """
        Generate response using Falcon 7B model with e-commerce context
        
        Args:
            user_query (str): User's question
            context (Dict): Additional context (products, user info, etc.)
            
        Returns:
            str: Generated response
        """
        try:
            # Check if model is available
            if not self.pipeline:
                return self._fallback_response(user_query, context)
            
            # Build prompt with e-commerce context
            prompt = self._build_ecommerce_prompt(user_query, context)
            
            # Generate response
            response = self.pipeline(
                prompt,
                max_new_tokens=256,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            # Extract and clean response
            generated_text = response[0]['generated_text']
            clean_response = self._extract_response(generated_text, prompt)
            
            # Post-process for e-commerce context
            final_response = self._post_process_response(clean_response, user_query, context)
            
            return final_response
            
        except Exception as e:
            self.logger.error(f"❌ Error generating LLM response: {e}")
            return self._fallback_response(user_query, context)
    
    def _build_ecommerce_prompt(self, user_query: str, context: Dict[str, Any] = None) -> str:
        """Build a comprehensive e-commerce prompt"""
        
        # Base system prompt
        system_prompt = """You are FashionPulse AI, an expert e-commerce assistant for a fashion retail platform. You help customers with:

🛍️ PRODUCT QUERIES: Search, recommendations, details, availability
📦 ORDER SUPPORT: Tracking, modifications, cancellations  
🔄 RETURNS & EXCHANGES: Policies, process, refunds
📏 SIZING HELP: Size guides, fit recommendations
💳 PAYMENT SUPPORT: Methods, security, billing issues
🚚 SHIPPING INFO: Delivery times, costs, tracking
💬 GENERAL SUPPORT: Policies, account help, complaints

GUIDELINES:
- Be helpful, friendly, and professional
- Provide specific, actionable information
- Use emojis appropriately for better engagement
- If you don't know something, admit it and offer to connect with human support
- Always prioritize customer satisfaction

STORE INFO:
- Free shipping on orders ₹1500+
- 7-day return policy
- Size exchanges within 15 days
- Customer support: 9 AM - 9 PM IST
- Payment methods: Cards, UPI, Net Banking, COD"""

        # Add product context if available
        product_context = ""
        if context and context.get('products'):
            products = context['products'][:3]  # Limit to 3 products
            product_context = "\n\nAVAILABLE PRODUCTS:\n"
            for i, product in enumerate(products, 1):
                product_context += f"{i}. {product.get('product_name', 'Unknown')} - ₹{product.get('price', 0)} ({product.get('color', 'N/A')} for {product.get('gender', 'All')})\n"
        
        # Add user query context
        query_context = f"\n\nCUSTOMER QUERY: {user_query}\n\nRESPONSE:"
        
        return system_prompt + product_context + query_context
    
    def _extract_response(self, generated_text: str, prompt: str) -> str:
        """Extract the actual response from generated text"""
        try:
            # Remove the prompt from generated text
            if prompt in generated_text:
                response = generated_text.replace(prompt, "").strip()
            else:
                response = generated_text.strip()
            
            # Clean up common artifacts
            response = re.sub(r'^(RESPONSE:|Response:|Assistant:|AI:)', '', response, flags=re.IGNORECASE).strip()
            response = re.sub(r'\n+', '\n', response)  # Remove excessive newlines
            response = response.strip()
            
            return response if response else "I'm here to help! Could you please rephrase your question?"
            
        except Exception as e:
            self.logger.error(f"Error extracting response: {e}")
            return "I'm here to help! Could you please rephrase your question?"
    
    def _post_process_response(self, response: str, user_query: str, context: Dict[str, Any] = None) -> str:
        """Post-process response with additional e-commerce information"""
        
        # Add relevant policy information based on query type
        query_lower = user_query.lower()
        
        # Shipping queries
        if any(word in query_lower for word in ['shipping', 'delivery', 'when will', 'how long']):
            if 'free shipping' not in response.lower():
                response += f"\n\n📦 **Shipping Info:**\n• Free shipping on orders ₹{self.ecommerce_knowledge['shipping']['free_shipping_threshold']}+\n• Standard: {self.ecommerce_knowledge['shipping']['standard']}\n• Express: {self.ecommerce_knowledge['shipping']['express']}"
        
        # Return queries
        elif any(word in query_lower for word in ['return', 'refund', 'exchange', 'cancel']):
            if 'return policy' not in response.lower():
                response += f"\n\n🔄 **Return Policy:**\n• {self.ecommerce_knowledge['returns']['window']} return window\n• Items must be {self.ecommerce_knowledge['returns']['condition']}\n• Process: {self.ecommerce_knowledge['returns']['process']}"
        
        # Sizing queries
        elif any(word in query_lower for word in ['size', 'fit', 'measurement']):
            if 'size' not in response.lower():
                response += f"\n\n📏 **Sizing Help:**\n• {self.ecommerce_knowledge['sizing']['guide']}\n• {self.ecommerce_knowledge['sizing']['exchange']}"
        
        # Payment queries
        elif any(word in query_lower for word in ['payment', 'pay', 'card', 'upi', 'cod']):
            if 'payment' not in response.lower():
                methods = ", ".join(self.ecommerce_knowledge['payment']['methods'])
                response += f"\n\n💳 **Payment Options:**\n• Available: {methods}\n• Security: {self.ecommerce_knowledge['payment']['security']}"
        
        # Add contact info for complex queries
        if any(word in query_lower for word in ['help', 'support', 'contact', 'problem', 'issue']):
            response += f"\n\n💬 **Need More Help?**\n• Support Hours: {self.ecommerce_knowledge['support']['hours']}\n• Response Time: {self.ecommerce_knowledge['support']['response_time']}\n• Channels: {', '.join(self.ecommerce_knowledge['support']['channels'])}"
        
        return response
    
    def _fallback_response(self, user_query: str, context: Dict[str, Any] = None) -> str:
        """Fallback response when LLM is not available"""
        query_lower = user_query.lower()
        
        # Product-related queries
        if any(word in query_lower for word in ['product', 'dress', 'shirt', 'jeans', 'show me', 'find']):
            if context and context.get('products'):
                return "I found some products that match your search! Let me show you the details above. 🛍️"
            else:
                return "I'd love to help you find products! Could you be more specific about what you're looking for? For example: 'Show me red dresses under ₹2000' 👗"
        
        # Shipping queries
        elif any(word in query_lower for word in ['shipping', 'delivery', 'when will']):
            return f"📦 **Shipping Information:**\n\n• **Standard Delivery:** {self.ecommerce_knowledge['shipping']['standard']}\n• **Express Delivery:** {self.ecommerce_knowledge['shipping']['express']}\n• **Free Shipping:** On orders ₹{self.ecommerce_knowledge['shipping']['free_shipping_threshold']}+\n\nNeed tracking info? Please share your order number! 📋"
        
        # Return queries
        elif any(word in query_lower for word in ['return', 'refund', 'exchange']):
            return f"🔄 **Returns & Exchanges:**\n\n• **Return Window:** {self.ecommerce_knowledge['returns']['window']}\n• **Condition:** Items must be {self.ecommerce_knowledge['returns']['condition']}\n• **Process:** {self.ecommerce_knowledge['returns']['process']}\n• **Size Exchanges:** {self.ecommerce_knowledge['sizing']['exchange']}\n\nNeed help with a specific return? I'm here to assist! 😊"
        
        # Sizing queries
        elif any(word in query_lower for word in ['size', 'fit', 'measurement']):
            return f"📏 **Sizing Help:**\n\n• {self.ecommerce_knowledge['sizing']['guide']}\n• {self.ecommerce_knowledge['sizing']['exchange']}\n\nFor specific size recommendations, please share:\n• Your usual size in other brands\n• The product you're interested in\n• Your measurements (optional)\n\nI'll help you find the perfect fit! ✨"
        
        # Payment queries
        elif any(word in query_lower for word in ['payment', 'pay', 'card', 'upi', 'cod']):
            methods = ", ".join(self.ecommerce_knowledge['payment']['methods'])
            return f"💳 **Payment Options:**\n\n• **Available Methods:** {methods}\n• **Security:** {self.ecommerce_knowledge['payment']['security']}\n\nHaving payment issues? Let me know the specific problem and I'll help resolve it! 🔒"
        
        # Order tracking
        elif any(word in query_lower for word in ['order', 'track', 'status', 'where is']):
            return "📦 **Order Tracking:**\n\nTo track your order, I'll need your:\n• Order number (starts with #FP)\n• Registered email or phone number\n\nOnce you provide these details, I can check your order status and delivery updates! 🚚"
        
        # General support
        elif any(word in query_lower for word in ['help', 'support', 'contact', 'problem']):
            return f"💬 **Customer Support:**\n\n• **Hours:** {self.ecommerce_knowledge['support']['hours']}\n• **Response Time:** {self.ecommerce_knowledge['support']['response_time']}\n• **Channels:** {', '.join(self.ecommerce_knowledge['support']['channels'])}\n\nI'm here to help with:\n🛍️ Product searches & recommendations\n📦 Order tracking & modifications\n🔄 Returns & exchanges\n📏 Sizing guidance\n💳 Payment support\n\nWhat can I assist you with today? 😊"
        
        # Default response
        else:
            return "Hi! I'm your FashionPulse assistant 👗 I can help you with:\n\n🛍️ **Product Search** - Find clothes by style, color, price\n📦 **Orders** - Track, modify, or cancel orders\n🔄 **Returns** - Return/exchange policies and process\n📏 **Sizing** - Size guides and fit recommendations\n💳 **Payments** - Payment methods and billing\n🚚 **Shipping** - Delivery times and tracking\n\nWhat would you like to know? Just ask me anything! 😊"
    
    def is_model_loaded(self) -> bool:
        """Check if the LLM model is successfully loaded"""
        return self.pipeline is not None
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model"""
        return {
            "model_loaded": self.is_model_loaded(),
            "model_name": "SHJ622/falcon_7b_ecommerce_ai_chatbot_n100",
            "device": self.device,
            "torch_available": torch.cuda.is_available(),
            "fallback_mode": not self.is_model_loaded()
        }