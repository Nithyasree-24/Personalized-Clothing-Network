from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta
from config import Config
from db import execute_query
from api_cache_service import api_cache_service
from clothing_api_service import clothing_api_service
from ebay_api_service import ebay_api_service
from ai_tryon_api import ai_tryon_bp

app = Flask(__name__)
CORS(app)

# Register AI Try-On Blueprint
app.register_blueprint(ai_tryon_bp, url_prefix='/ai-tryon')

# Helper function to generate JWT token
def generate_token(user_id, email):
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, Config.JWT_SECRET, algorithm='HS256')

# Helper function to verify JWT token
def verify_token(token):
    try:
        payload = jwt.decode(token, Config.JWT_SECRET, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@app.route('/api/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        # Validation
        if not name or not email or not password:
            return jsonify({'error': 'All fields are required'}), 400
        
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        # Check if user already exists
        existing_user = execute_query(
            "SELECT id FROM users WHERE email = %s",
            (email,),
            fetch=True
        )
        
        if existing_user:
            return jsonify({'error': 'Email already registered'}), 400
        
        # Insert user (plain password - no hashing)
        user_id = execute_query(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, password)
        )
        
        if user_id:
            token = generate_token(user_id, email)
            return jsonify({
                'message': 'User created successfully',
                'token': token,
                'user': {
                    'id': user_id,
                    'name': name,
                    'email': email
                }
            }), 201
        else:
            return jsonify({'error': 'Failed to create user'}), 500
            
    except Exception as e:
        print(f"Signup error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        # Validation
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Get user from database
        users = execute_query(
            "SELECT id, name, email, password FROM users WHERE email = %s AND password = %s",
            (email, password),
            fetch=True
        )
        
        if not users:
            return jsonify({'error': 'Invalid email or password'}), 401
        
        user = users[0]
        token = generate_token(user['id'], user['email'])
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': user['id'],
                'name': user['name'],
                'email': user['email']
            }
        }), 200
            
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/verify', methods=['GET'])
def verify():
    try:
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'No token provided'}), 401
        
        # Remove 'Bearer ' prefix if present
        if token.startswith('Bearer '):
            token = token[7:]
        
        payload = verify_token(token)
        if payload:
            return jsonify({'valid': True, 'user_id': payload['user_id']}), 200
        else:
            return jsonify({'valid': False}), 401
            
    except Exception as e:
        print(f"Verify error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        users = execute_query(
            "SELECT id, name, email, created_at FROM users WHERE id = %s",
            (user_id,),
            fetch=True
        )
        
        if users:
            return jsonify(users[0]), 200
        else:
            return jsonify({'error': 'User not found'}), 404
            
    except Exception as e:
        print(f"Get user error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

# ============= PRODUCT API ENDPOINTS =============

@app.route('/api/products/search', methods=['GET'])
def search_products():
    """Search products from clothing table"""
    try:
        query = request.args.get('query', 'clothing')
        category = request.args.get('category', 'fashion')
        
        # Use clothing table instead of cache
        products = clothing_api_service.get_products(query, category)
        
        return jsonify({
            'success': True,
            'count': len(products),
            'products': products
        }), 200
        
    except Exception as e:
        print(f"Search products error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/products/category/<category>', methods=['GET'])
def get_products_by_category(category):
    """Get products by category from clothing table"""
    try:
        gender = request.args.get('gender')
        limit = int(request.args.get('limit', 100))
        
        print(f"DEBUG: Category endpoint called - category={category}, gender={gender}")
        
        # Handle different category types
        if category.lower() == 'fashion':
            # Get all products without any filter
            products = clothing_api_service.get_clothing_products(gender=gender, limit=limit)
        elif category.lower() in ['women', 'men']:
            # Gender-based filtering
            products = clothing_api_service.get_clothing_products(gender=category.lower(), limit=limit)
        else:
            # Specific category filtering (Western Wear, Dresses, etc.)
            products = clothing_api_service.get_clothing_products(category=category, gender=gender, limit=limit)
        
        return jsonify({
            'success': True,
            'count': len(products),
            'products': products
        }), 200
        
    except Exception as e:
        print(f"Get products by category error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/products/fetch-fresh', methods=['POST'])
def fetch_fresh_products():
    """Force fetch fresh products from Amazon API"""
    try:
        data = request.json
        query = data.get('query', 'clothing')
        category = data.get('category', 'fashion')
        
        # Check if we can make API call
        if not api_cache_service.can_make_api_call():
            return jsonify({
                'success': False,
                'error': 'API limit reached',
                'usage': api_cache_service.get_usage_stats()
            }), 429
        
        products = api_cache_service.fetch_from_amazon_api(query, category)
        
        return jsonify({
            'success': True,
            'count': len(products),
            'products': products,
            'source': 'amazon',
            'usage': api_cache_service.get_usage_stats()
        }), 200
        
    except Exception as e:
        print(f"Fetch fresh products error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/products/fetch-ebay', methods=['POST'])
def fetch_ebay_products():
    """Fetch products from eBay API (India)"""
    try:
        data = request.json
        query = data.get('query', 'clothing')
        limit = int(data.get('limit', 50))
        
        # Fetch from eBay
        products = ebay_api_service.search_products(query, limit)
        
        # Store in cache
        if products:
            ebay_api_service.store_products_in_cache(products)
        
        return jsonify({
            'success': True,
            'count': len(products),
            'products': products,
            'source': 'ebay'
        }), 200
        
    except Exception as e:
        print(f"Fetch eBay products error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/products/fetch-all', methods=['POST'])
def fetch_all_products():
    """Fetch products from both Amazon and eBay APIs"""
    try:
        data = request.json
        query = data.get('query', 'clothing')
        
        all_products = []
        sources_used = []
        
        # Try Amazon first (if under limit)
        if api_cache_service.can_make_api_call():
            amazon_products = api_cache_service.fetch_from_amazon_api(query, 'fashion')
            if amazon_products:
                all_products.extend(amazon_products)
                sources_used.append('amazon')
        
        # Fetch from eBay
        ebay_products = ebay_api_service.search_products(query, 50)
        if ebay_products:
            ebay_api_service.store_products_in_cache(ebay_products)
            all_products.extend(ebay_products)
            sources_used.append('ebay')
        
        return jsonify({
            'success': True,
            'count': len(all_products),
            'products': all_products,
            'sources': sources_used,
            'usage': api_cache_service.get_usage_stats()
        }), 200
        
    except Exception as e:
        print(f"Fetch all products error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/usage/stats', methods=['GET'])
def get_usage_stats():
    """Get API usage statistics"""
    try:
        stats = api_cache_service.get_usage_stats()
        return jsonify(stats), 200
    except Exception as e:
        print(f"Get usage stats error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/cache/count', methods=['GET'])
def get_cache_count():
    """Get total number of clothing products"""
    try:
        result = execute_query(
            "SELECT COUNT(*) as count FROM clothing",
            fetch=True
        )
        count = result[0]['count'] if result else 0
        
        return jsonify({
            'success': True,
            'cached_products': count
        }), 200
    except Exception as e:
        print(f"Get cache count error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

# ============= PRODUCT DETAIL & REVIEWS =============

@app.route('/api/products/<product_id>', methods=['GET'])
def get_product_detail(product_id):
    """Get single product details from clothing table"""
    try:
        products = execute_query(
            """SELECT 
                product_id,
                product_name as title,
                price,
                product_image as image_url,
                product_category as category,
                gender,
                product_description as description,
                color,
                size,
                stock,
                created_at
            FROM clothing WHERE product_id = %s""",
            (product_id,),
            fetch=True
        )
        
        if not products:
            return jsonify({'error': 'Product not found'}), 404
        
        product = products[0]
        # Transform to expected format
        transformed_product = {
            'product_id': str(product['product_id']),
            'id': product['product_id'],
            'title': product['title'],
            'price': float(product['price']),
            'image_url': product['image_url'],
            'category': product['category'],
            'gender': product['gender'].lower() if product['gender'] else 'unisex',
            'description': product['description'] or '',
            'color': product['color'] or '',
            'size': product['size'] or '',
            'stock': product['stock'] or 0,
            'rating': 4.5,  # Default rating
            'source': 'clothing_table',
            'cached_at': product['created_at'].isoformat() if product['created_at'] else ''
        }
        
        return jsonify({
            'success': True,
            'product': transformed_product
        }), 200
        
    except Exception as e:
        print(f"Get product detail error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/products/<product_id>/similar', methods=['GET'])
def get_similar_products(product_id):
    """Get similar products based on category and gender from clothing table"""
    try:
        # Get the original product
        products = execute_query(
            "SELECT product_category as category, gender FROM clothing WHERE product_id = %s",
            (product_id,),
            fetch=True
        )
        
        if not products:
            return jsonify({'error': 'Product not found'}), 404
        
        product = products[0]
        limit = int(request.args.get('limit', 8))
        
        # Get similar products (same category/gender, exclude current)
        similar = execute_query(
            """SELECT 
                product_id,
                product_name as title,
                price,
                product_image as image_url,
                product_category as category,
                gender,
                product_description as description,
                color,
                size,
                stock,
                created_at
            FROM clothing 
            WHERE product_category = %s 
            AND gender = %s 
            AND product_id != %s 
            ORDER BY RAND() 
            LIMIT %s""",
            (product.get('category', 'fashion'), product.get('gender', 'women'), product_id, limit),
            fetch=True
        )
        
        # Transform products to expected format
        transformed_products = []
        for p in similar:
            transformed_product = {
                'product_id': str(p['product_id']),
                'id': p['product_id'],
                'title': p['title'],
                'price': float(p['price']),
                'image_url': p['image_url'],
                'category': p['category'],
                'gender': p['gender'].lower() if p['gender'] else 'unisex',
                'description': p['description'] or '',
                'color': p['color'] or '',
                'size': p['size'] or '',
                'stock': p['stock'] or 0,
                'rating': 4.5,
                'source': 'clothing_table',
                'cached_at': p['created_at'].isoformat() if p['created_at'] else ''
            }
            transformed_products.append(transformed_product)
        
        return jsonify({
            'success': True,
            'count': len(transformed_products),
            'products': transformed_products
        }), 200
        
    except Exception as e:
        print(f"Get similar products error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/reviews/<product_id>', methods=['GET'])
def get_reviews(product_id):
    """Get reviews for a product"""
    try:
        reviews = execute_query(
            """SELECT r.*, u.name as user_name 
               FROM reviews r 
               JOIN users u ON r.user_id = u.id 
               WHERE r.product_id = %s 
               ORDER BY r.created_at DESC""",
            (product_id,),
            fetch=True
        )
        
        return jsonify({
            'success': True,
            'count': len(reviews),
            'reviews': reviews
        }), 200
        
    except Exception as e:
        print(f"Get reviews error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/reviews', methods=['POST'])
def add_review():
    """Add a review for a product"""
    try:
        data = request.json
        product_id = data.get('product_id')
        user_id = data.get('user_id')
        rating = data.get('rating')
        comment = data.get('comment', '')
        
        if not product_id or not user_id or not rating:
            return jsonify({'error': 'Product ID, User ID, and Rating are required'}), 400
        
        if not (1 <= rating <= 5):
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400
        
        review_id = execute_query(
            """INSERT INTO reviews (product_id, user_id, rating, comment) 
               VALUES (%s, %s, %s, %s)""",
            (product_id, user_id, rating, comment)
        )
        
        if review_id:
            return jsonify({
                'success': True,
                'message': 'Review added successfully',
                'review_id': review_id
            }), 201
        else:
            return jsonify({'error': 'Failed to add review'}), 500
            
    except Exception as e:
        print(f"Add review error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

# ============= VIRTUAL TRY-ON =============

@app.route('/api/virtual-tryon', methods=['POST'])
def virtual_tryon():
    """
    Virtual Try-On endpoint - Proxy to Hugging Face IDM-VTON API
    This avoids CORS issues and keeps API key secure
    """
    try:
        data = request.json
        person_image = data.get('person_image')
        garment_image = data.get('garment_image')
        category = data.get('category', 'upper_body')
        
        if not person_image or not garment_image:
            return jsonify({'error': 'Both person_image and garment_image are required'}), 400
        
        # Get Hugging Face API key from environment
        hf_api_key = Config.HUGGINGFACE_API_KEY if hasattr(Config, 'HUGGINGFACE_API_KEY') else None
        
        print(f"Virtual Try-On request - Category: {category}")
        
        # Check if API key is configured
        if not hf_api_key or hf_api_key == 'your_huggingface_api_key_here':
            # Demo mode - return person image
            print("Running in demo mode (no API key configured)")
            return jsonify({
                'success': True,
                'result_image': person_image,  # For demo, return person image
                'message': 'Virtual try-on feature is in demo mode. Configure Hugging Face API for full functionality.'
            }), 200
        
        # Full mode - call Hugging Face API
        try:
            import requests
            
            # Hugging Face API endpoint
            api_url = "https://api-inference.huggingface.co/models/yisol/IDM-VTON"
            
            headers = {
                "Authorization": f"Bearer {hf_api_key}"
            }
            
            # Prepare the request
            # Note: This is a simplified version. The actual API may require different format
            payload = {
                "inputs": {
                    "person_image": person_image,
                    "garment_image": garment_image,
                    "category": category
                }
            }
            
            print("Calling Hugging Face API...")
            response = requests.post(api_url, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                # Success - return the result
                result_image = response.content
                import base64
                result_base64 = base64.b64encode(result_image).decode('utf-8')
                return jsonify({
                    'success': True,
                    'result_image': f'data:image/png;base64,{result_base64}'
                }), 200
            else:
                print(f"Hugging Face API error: {response.status_code} - {response.text}")
                # Fallback to demo mode on API error
                return jsonify({
                    'success': True,
                    'result_image': person_image,
                    'message': f'API error (falling back to demo mode): {response.text}'
                }), 200
                
        except Exception as api_error:
            print(f"Hugging Face API call error: {api_error}")
            # Fallback to demo mode on error
            return jsonify({
                'success': True,
                'result_image': person_image,
                'message': f'API call failed (demo mode): {str(api_error)}'
            }), 200
        
    except Exception as e:
        print(f"Virtual try-on error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=Config.PORT, debug=True)
