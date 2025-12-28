"""
Flask API Server for FashionPulse Chat Agent
Provides REST API endpoints for the chat functionality
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import json
import sys
import os
from datetime import datetime

# Add current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chat_agent import FashionPulseChatAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Initialize chat agent
chat_agent = FashionPulseChatAgent()

@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    """
    Main chat endpoint
    Expects: {"message": "user message"}
    Returns: {"response": "agent response", "timestamp": "ISO timestamp"}
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'error': 'Missing message in request body',
                'example': {'message': 'Show me red dresses under 2000'}
            }), 400
        
        user_message = data['message'].strip()
        
        if not user_message:
            return jsonify({
                'error': 'Empty message provided'
            }), 400
        
        # Process message with chat agent
        response = chat_agent.process_message(user_message)
        
        # Also get structured product data if it's a search query
        parsed_query = chat_agent.query_parser.parse_user_query(user_message)
        products = []
        
        if parsed_query['intent'] == 'search' or any([parsed_query['category'], parsed_query['color'], parsed_query['gender']]):
            products = chat_agent.db_handler.search_products(
                category=parsed_query['category'],
                color=parsed_query['color'],
                gender=parsed_query['gender'],
                max_price=parsed_query['max_price'],
                limit=5  # Limit for chat display
            )
        
        return jsonify({
            'response': response,
            'products': products,
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        })
        
    except Exception as e:
        logging.error(f"Chat endpoint error: {e}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/api/chat/product/<product_id>', methods=['GET'])
def get_product_details(product_id):
    """
    Get detailed product information
    Returns: {"response": "formatted product details", "timestamp": "ISO timestamp"}
    """
    try:
        response = chat_agent.get_product_details(product_id)
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        })
        
    except Exception as e:
        logging.error(f"Product details error: {e}")
        return jsonify({
            'error': 'Failed to fetch product details',
            'message': str(e)
        }), 500

@app.route('/api/chat/stats', methods=['GET'])
def get_chat_stats():
    """
    Get chat agent and database statistics
    """
    try:
        stats = chat_agent.db_handler.get_stats()
        
        return jsonify({
            'stats': stats,
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        })
        
    except Exception as e:
        logging.error(f"Stats endpoint error: {e}")
        return jsonify({
            'error': 'Failed to fetch statistics',
            'message': str(e)
        }), 500

@app.route('/api/chat/categories', methods=['GET'])
def get_categories():
    """
    Get all available product categories
    """
    try:
        categories = chat_agent.db_handler.get_categories()
        
        return jsonify({
            'categories': categories,
            'count': len(categories),
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        })
        
    except Exception as e:
        logging.error(f"Categories endpoint error: {e}")
        return jsonify({
            'error': 'Failed to fetch categories',
            'message': str(e)
        }), 500

@app.route('/api/chat/colors', methods=['GET'])
def get_colors():
    """
    Get all available colors
    """
    try:
        colors = chat_agent.db_handler.get_colors()
        
        return jsonify({
            'colors': colors,
            'count': len(colors),
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        })
        
    except Exception as e:
        logging.error(f"Colors endpoint error: {e}")
        return jsonify({
            'error': 'Failed to fetch colors',
            'message': str(e)
        }), 500

@app.route('/api/chat/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    try:
        # Test database connection
        test_query = chat_agent.db_handler.execute_query("SELECT 1 as test")
        db_status = "connected" if test_query else "disconnected"
        
        return jsonify({
            'status': 'healthy',
            'database': db_status,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0'
        })
        
    except Exception as e:
        logging.error(f"Health check error: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/chat/llm-status', methods=['GET'])
def get_llm_status():
    """
    Get LLM integration status and information
    """
    try:
        llm_info = chat_agent.get_llm_status()
        
        return jsonify({
            'llm_info': llm_info,
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        })
        
    except Exception as e:
        logging.error(f"LLM status endpoint error: {e}")
        return jsonify({
            'error': 'Failed to fetch LLM status',
            'message': str(e)
        }), 500

@app.route('/api/chat/help', methods=['GET'])
def get_help():
    """
    Get help information about the chat agent
    """
    help_info = {
        'description': 'FashionPulse Chat Agent - Your AI Fashion Assistant with Falcon 7B LLM',
        'capabilities': [
            'Search products by category (dress, jeans, shirt, etc.)',
            'Filter by color (red, blue, black, etc.)',
            'Filter by gender (men, women, kids)',
            'Filter by price range (under ₹2000, etc.)',
            'Get product details and recommendations',
            'Handle shipping and delivery queries',
            'Process return and exchange requests',
            'Provide sizing guidance and fit recommendations',
            'Answer payment and billing questions',
            'General e-commerce customer support',
            'Order tracking and status updates',
            'Policy information and store guidelines'
        ],
        'llm_enhanced': True,
        'model': 'SHJ622/falcon_7b_ecommerce_ai_chatbot_n100',
        'example_queries': [
            'Show me red dresses under ₹2000',
            'Find jeans for men',
            'Looking for ethnic wear for women',
            'Blue shirts under ₹1500',
            'What is your return policy?',
            'How long does shipping take?',
            'Can I exchange this for a different size?',
            'What payment methods do you accept?',
            'Track my order #FP12345',
            'I need help with sizing',
            'What categories do you have?',
            'Show me some popular items'
        ],
        'endpoints': {
            'POST /api/chat': 'Main chat interface with LLM support',
            'GET /api/chat/product/{id}': 'Get product details',
            'GET /api/chat/stats': 'Get database statistics',
            'GET /api/chat/categories': 'Get all categories',
            'GET /api/chat/colors': 'Get all colors',
            'GET /api/chat/llm-status': 'Get LLM integration status',
            'GET /api/chat/health': 'Health check',
            'GET /api/chat/help': 'This help information'
        }
    }
    
    return jsonify(help_info)

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint not found',
        'available_endpoints': [
            '/api/chat',
            '/api/chat/product/<id>',
            '/api/chat/stats',
            '/api/chat/categories',
            '/api/chat/colors',
            '/api/chat/health',
            '/api/chat/help'
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'message': 'Something went wrong on our end'
    }), 500

if __name__ == '__main__':
    print("🤖 Starting FashionPulse Chat Agent API Server...")
    print("📍 Server will run on: http://localhost:5001")
    print("🔗 Main chat endpoint: POST http://localhost:5001/api/chat")
    print("📚 Help endpoint: GET http://localhost:5001/api/chat/help")
    print("="*60)
    
    app.run(host='0.0.0.0', port=5001, debug=True)