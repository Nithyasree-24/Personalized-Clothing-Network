import requests
from datetime import datetime
from db import execute_query, get_db_connection
from config import Config

class APICacheService:
    def __init__(self):
        self.rapidapi_key = Config.RAPIDAPI_KEY
        self.amazon_api_url = "https://real-time-amazon-data.p.rapidapi.com/search"
        self.amazon_api_host = "real-time-amazon-data.p.rapidapi.com"
        self.monthly_limit = 100
    
    def get_current_month_year(self):
        """Get current month-year string (e.g., '2024-11')"""
        return datetime.now().strftime('%Y-%m')
    
    def get_api_usage_count(self):
        """Get current month's API usage count"""
        month_year = self.get_current_month_year()
        result = execute_query(
            "SELECT request_count FROM api_usage WHERE api_name = 'amazon' AND month_year = %s",
            (month_year,),
            fetch=True
        )
        return result[0]['request_count'] if result else 0
    
    def increment_api_usage(self):
        """Increment API usage counter for current month"""
        month_year = self.get_current_month_year()
        
        # Check if record exists
        existing = execute_query(
            "SELECT id FROM api_usage WHERE api_name = 'amazon' AND month_year = %s",
            (month_year,),
            fetch=True
        )
        
        if existing:
            # Update existing record
            execute_query(
                "UPDATE api_usage SET request_count = request_count + 1, last_request = NOW() WHERE api_name = 'amazon' AND month_year = %s",
                (month_year,)
            )
        else:
            # Insert new record
            execute_query(
                "INSERT INTO api_usage (api_name, endpoint, request_count, month_year) VALUES (%s, %s, %s, %s)",
                ('amazon', self.amazon_api_url, 1, month_year)
            )
    
    def can_make_api_call(self):
        """Check if we can make an API call (under monthly limit)"""
        current_usage = self.get_api_usage_count()
        return current_usage < self.monthly_limit
    
    def fetch_from_amazon_api(self, query, category='fashion'):
        """Fetch products from Amazon RapidAPI"""
        try:
            # Check if we can make API call
            if not self.can_make_api_call():
                print(f"⚠️ API limit reached ({self.monthly_limit} calls/month)")
                return []
            
            # Add clothing-specific keywords
            clothing_query = f"{query} clothing apparel fashion"
            
            params = {
                'query': clothing_query,
                'page': '1',
                'country': 'US',
                'category': category
            }
            
            headers = {
                'X-RapidAPI-Key': self.rapidapi_key,
                'X-RapidAPI-Host': self.amazon_api_host
            }
            
            print(f"🔄 Calling Amazon API for: {query}")
            response = requests.get(self.amazon_api_url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                # Increment usage counter
                self.increment_api_usage()
                
                data = response.json()
                if data and 'data' in data and 'products' in data['data']:
                    products = self.parse_amazon_products(data['data']['products'], category)
                    print(f"✅ Fetched {len(products)} products from Amazon API")
                    
                    # Store products in cache
                    self.store_products_in_cache(products)
                    return products
                else:
                    print("⚠️ Unexpected API response structure")
                    return []
            else:
                print(f"❌ Amazon API error: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Error fetching from Amazon API: {e}")
            return []
    
    def parse_amazon_products(self, items, category):
        """Parse Amazon API response into product format"""
        products = []
        clothing_keywords = ['shirt', 'dress', 'pants', 'jeans', 'jacket', 'coat', 'sweater', 
                            'hoodie', 'top', 'blouse', 'skirt', 'shorts', 'suit', 'clothing',
                            'apparel', 'wear', 't-shirt', 'polo', 'cardigan', 'blazer']
        
        for item in items:
            try:
                title = (item.get('product_title') or item.get('title') or '').lower()
                
                # Filter only clothing items
                if not any(keyword in title for keyword in clothing_keywords):
                    continue
                
                product = {
                    'product_id': item.get('asin') or item.get('product_id') or str(hash(title)),
                    'title': item.get('product_title') or item.get('title') or 'Unknown Product',
                    'price': self.parse_price(item.get('product_price', '0')),
                    'image_url': item.get('product_photo') or item.get('image'),
                    'category': category,
                    'gender': self.detect_gender(title),
                    'source': 'amazon',
                    'product_url': item.get('product_url'),
                    'rating': self.parse_rating(item.get('product_star_rating')),
                    'description': item.get('product_description', '')[:500]  # Limit description length
                }
                products.append(product)
            except Exception as e:
                print(f"Error parsing product: {e}")
                continue
        
        return products
    
    def parse_price(self, price_str):
        """Extract numeric price from string and adjust to reasonable range (₹500-₹5000)"""
        try:
            if isinstance(price_str, (int, float)):
                price = float(price_str)
            else:
                price_clean = ''.join(c for c in str(price_str) if c.isdigit() or c == '.')
                price = float(price_clean) if price_clean else 0.0
            
            # Adjust price to reasonable range for Indian market
            if price < 500:
                # Low prices: adjust to ₹500-₹2000
                import random
                price = random.randint(500, 2000)
            elif price > 5000:
                # High prices: adjust to ₹2000-₹5000
                import random
                price = random.randint(2000, 5000)
            
            return round(price, 2)
        except:
            import random
            return random.randint(500, 2000)
    
    def parse_rating(self, rating_str):
        """Extract numeric rating from string"""
        try:
            if isinstance(rating_str, (int, float)):
                return float(rating_str)
            rating_clean = ''.join(c for c in str(rating_str) if c.isdigit() or c == '.')
            return float(rating_clean) if rating_clean else 0.0
        except:
            return 0.0
    
    def detect_gender(self, title):
        """Detect gender from product title"""
        title_lower = title.lower()
        if any(word in title_lower for word in ['women', 'woman', 'ladies', 'female', 'girl']):
            return 'women'
        elif any(word in title_lower for word in ['men', 'man', 'male', 'boy']):
            return 'men'
        elif any(word in title_lower for word in ['kid', 'child', 'baby', 'toddler']):
            return 'kids'
        return 'unisex'
    
    def store_products_in_cache(self, products):
        """Store products in database cache"""
        stored_count = 0
        for product in products:
            try:
                # Check if product already exists
                existing = execute_query(
                    "SELECT id FROM products WHERE id = %s",
                    (product['product_id'],),
                    fetch=True
                )
                
                if not existing:
                    # Insert new product
                    execute_query(
                        """INSERT INTO products 
                        (id, title, price, imageUrl, category, gender, description, rating)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                        (
                            product['product_id'],
                            product['title'],
                            product['price'],
                            product['image_url'],
                            product['category'],
                            product['gender'],
                            product['description'],
                            product['rating']
                        )
                    )
                    stored_count += 1
            except Exception as e:
                print(f"Error storing product: {e}")
                continue
        
        print(f"💾 Stored {stored_count} new products in cache")
        return stored_count
    
    def get_cached_products(self, category=None, gender=None, limit=100, search_query=None):
        """Get products from cache with flexible search"""
        try:
            query = "SELECT id as product_id, title, price, imageUrl as image_url, category, gender, description, rating FROM products WHERE 1=1"
            params = []
            
            # Flexible search across title, category, gender, description
            if search_query:
                search_terms = search_query.lower().split()
                search_conditions = []
                for term in search_terms:
                    search_conditions.append(
                        "(LOWER(title) LIKE %s OR LOWER(category) LIKE %s OR LOWER(gender) LIKE %s OR LOWER(description) LIKE %s)"
                    )
                    search_pattern = f"%{term}%"
                    params.extend([search_pattern, search_pattern, search_pattern, search_pattern])
                
                if search_conditions:
                    query += " AND (" + " OR ".join(search_conditions) + ")"
            
            # Apply filters only when no search query (for category endpoints)
            if not search_query:
                if category:
                    query += " AND (LOWER(category) LIKE %s OR LOWER(title) LIKE %s)"
                    params.extend([f"%{category.lower()}%", f"%{category.lower()}%"])
                
                if gender:
                    query += " AND LOWER(gender) = %s"
                    params.append(gender.lower())
            
            query += " ORDER BY created_at DESC LIMIT %s"
            params.append(limit)
            
            products = execute_query(query, tuple(params), fetch=True)
            
            return products or []
        except Exception as e:
            print(f"Database error in get_cached_products: {e}")
            return []
    
    def get_products(self, query, category='fashion', use_cache_first=True):
        """
        Get products - first try cache with search, then API if needed
        """
        # Try to get from cache first with search query - return ALL matching products
        if use_cache_first:
            # If query is generic (clothing, fashion), return ALL products
            if query.lower() in ['clothing fashion', 'fashion', 'clothing']:
                cached = self.get_cached_products(limit=500)  # Increased limit to get all products
                if cached:
                    print(f"📦 Returning ALL {len(cached)} products from cache")
                    return cached
            else:
                cached = self.get_cached_products(search_query=query, limit=500)  # Increased limit
                if cached:
                    print(f"📦 Returning {len(cached)} products from cache for query: {query}")
                    return cached
        
        # If cache is empty or use_cache_first is False, try API
        if self.can_make_api_call():
            api_products = self.fetch_from_amazon_api(query, category)
            if api_products:
                return api_products
        
        # Fallback to cache if API fails or limit reached
        cached = self.get_cached_products(search_query=query, limit=500)  # Increased limit
        if cached:
            print(f"📦 Fallback: Returning {len(cached)} products from cache")
            return cached
        
        # Final fallback: Load mock products from JSON file
        try:
            import json
            import os
            
            fallback_file = os.path.join(os.path.dirname(__file__), 'fallback_products.json')
            if os.path.exists(fallback_file):
                with open(fallback_file, 'r') as f:
                    mock_products = json.load(f)
                
                if mock_products:
                    print(f"🎭 Using {len(mock_products)} mock products (database not available)")
                    return mock_products
        except Exception as e:
            print(f"Error loading fallback products: {e}")
        
        print("⚠️ No products available")
        return []
    
    def get_usage_stats(self):
        """Get API usage statistics"""
        month_year = self.get_current_month_year()
        current_usage = self.get_api_usage_count()
        
        return {
            'current_usage': current_usage,
            'monthly_limit': self.monthly_limit,
            'remaining': self.monthly_limit - current_usage,
            'percentage': (current_usage / self.monthly_limit) * 100,
            'month_year': month_year,
            'can_make_call': self.can_make_api_call()
        }

# Singleton instance
api_cache_service = APICacheService()
