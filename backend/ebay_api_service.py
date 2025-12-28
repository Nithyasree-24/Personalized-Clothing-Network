import requests
import json
import os
from datetime import datetime
from db import execute_query
from config import Config

class EbayAPIService:
    def __init__(self):
        self.rapidapi_key = Config.RAPIDAPI_KEY_EBAY or Config.RAPIDAPI_KEY
        self.ebay_search_url = "https://ebay32.p.rapidapi.com/search"
        self.ebay_product_url = "https://ebay32.p.rapidapi.com/product"
        self.ebay_api_host = "ebay32.p.rapidapi.com"
        self.country = "india"
        self.country_code = "in"
        
        # Sample product IDs for testing (will be replaced with search results)
        self.sample_product_ids = [
            "195499451557",  # Example from your curl
        ]
    
    def get_product_by_id(self, product_id):
        """
        Get single product details from eBay
        
        Args:
            product_id: eBay product ID
        
        Returns:
            Product dictionary or None
        """
        try:
            headers = {
                "x-rapidapi-host": self.ebay_api_host,
                "x-rapidapi-key": self.rapidapi_key
            }
            
            params = {
                "country": self.country,
                "country_code": self.country_code
            }
            
            url = f"{self.ebay_product_url}/{product_id}"
            print(f"🔄 Calling eBay API for product: {product_id} (India)")
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Parse product data
                product = {
                    'product_id': data.get('item_id', product_id),
                    'title': data.get('title', ''),
                    'price': self._parse_price(data.get('price', {})),
                    'image_url': data.get('images', [{}])[0].get('url', '') if data.get('images') else '',
                    'product_url': data.get('url', ''),
                    'rating': data.get('rating', 0),
                    'description': data.get('description', ''),
                    'category': 'fashion',
                    'gender': self._detect_gender(data.get('title', '')),
                    'source': 'ebay'
                }
                
                print(f"✅ Fetched product from eBay API")
                return product
            else:
                print(f"❌ eBay API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error calling eBay API: {e}")
            return None
    
    def load_product_ids(self):
        """Load product IDs from JSON file"""
        try:
            json_path = os.path.join(os.path.dirname(__file__), 'ebay_product_ids.json')
            with open(json_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Could not load product IDs: {e}")
            return {"women": [], "men": [], "kids": []}
    
    def search_products(self, query, limit=50):
        """
        Fetch products from eBay by category
        Since eBay API doesn't have search endpoint, we fetch by product IDs
        
        Args:
            query: Search query (e.g., "women", "men", "kids", "clothing")
            limit: Number of results to fetch
        
        Returns:
            List of product dictionaries
        """
        try:
            # Load product IDs
            product_ids_data = self.load_product_ids()
            
            # Determine category from query
            query_lower = query.lower()
            category = 'women'  # default
            
            if 'men' in query_lower and 'women' not in query_lower:
                category = 'men'
            elif 'kid' in query_lower or 'child' in query_lower:
                category = 'kids'
            elif 'women' in query_lower or 'ladies' in query_lower:
                category = 'women'
            
            product_ids = product_ids_data.get(category, [])
            
            if not product_ids:
                print(f"⚠️  No product IDs found for category: {category}")
                return []
            
            print(f"🔄 Fetching {min(len(product_ids), limit)} eBay products for: {category} (India)")
            
            products = []
            for product_id in product_ids[:limit]:
                product = self.get_product_by_id(product_id)
                if product:
                    products.append(product)
            
            print(f"✅ Fetched {len(products)} products from eBay API")
            return products
                
        except Exception as e:
            print(f"❌ Error fetching eBay products: {e}")
            return []
    
    def _parse_price(self, price_data):
        """Parse price from eBay response"""
        try:
            if isinstance(price_data, dict):
                value = price_data.get('value', 0)
                # Convert to INR if needed (assuming USD to INR ~83)
                currency = price_data.get('currency', 'USD')
                if currency == 'USD':
                    return float(value) * 83
                return float(value)
            return float(price_data) if price_data else 0
        except:
            return 0
    
    def _detect_gender(self, title):
        """Detect gender from product title"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['women', 'womens', 'ladies', 'female', 'girl']):
            return 'women'
        elif any(word in title_lower for word in ['men', 'mens', 'male', 'boy']):
            return 'men'
        elif any(word in title_lower for word in ['kid', 'kids', 'child', 'children', 'baby']):
            return 'kids'
        
        return 'unisex'
    
    def store_products_in_cache(self, products):
        """Store eBay products in database cache"""
        stored_count = 0
        
        for product in products:
            try:
                # Check if product already exists
                existing = execute_query(
                    "SELECT id FROM api_cache WHERE product_id = %s AND source = 'ebay'",
                    (product['product_id'],),
                    fetch=True
                )
                
                if not existing:
                    # Insert new product
                    execute_query(
                        """INSERT INTO api_cache 
                           (product_id, title, price, image_url, product_url, rating, description, category, gender, source) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        (
                            product['product_id'],
                            product['title'],
                            product['price'],
                            product['image_url'],
                            product['product_url'],
                            product['rating'],
                            product['description'],
                            product['category'],
                            product['gender'],
                            product['source']
                        )
                    )
                    stored_count += 1
            except Exception as e:
                print(f"Error storing product: {e}")
                continue
        
        print(f"💾 Stored {stored_count} new eBay products in cache")
        return stored_count

# Create singleton instance
ebay_api_service = EbayAPIService()
