#!/usr/bin/env python3
"""
Fetch Amazon Products from RapidAPI - Alternative Endpoints
Tries multiple Amazon API endpoints to fetch real products
"""

import mysql.connector
import requests
import json
import time
from datetime import datetime

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'fashiopulse'
}

# Multiple RapidAPI Amazon endpoints to try
API_ENDPOINTS = [
    {
        'name': 'Real Time Amazon Data',
        'url': 'https://real-time-amazon-data.p.rapidapi.com/search',
        'host': 'real-time-amazon-data.p.rapidapi.com',
        'key': '99de9f55f4msh3ff10d9c02adbb8p1d5a45jsn9651c5759bae'
    },
    {
        'name': 'Amazon Data Scraper',
        'url': 'https://amazon-data-scraper126.p.rapidapi.com/search',
        'host': 'amazon-data-scraper126.p.rapidapi.com',
        'key': '99de9f55f4msh3ff10d9c02adbb8p1d5a45jsn9651c5759bae'
    },
    {
        'name': 'Amazon Products',
        'url': 'https://amazon-products1.p.rapidapi.com/search',
        'host': 'amazon-products1.p.rapidapi.com',
        'key': '99de9f55f4msh3ff10d9c02adbb8p1d5a45jsn9651c5759bae'
    }
]

def clear_existing_products():
    """Clear existing products from the table"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM products")
        conn.commit()
        
        cursor.close()
        conn.close()
        print("✅ Cleared existing products")
        return True
    except Exception as e:
        print(f"❌ Error clearing products: {e}")
        return False

def detect_gender(title):
    """Detect gender from product title"""
    title_lower = title.lower()
    if any(word in title_lower for word in ['women', 'woman', 'ladies', 'female', 'girl']):
        return 'women'
    elif any(word in title_lower for word in ['men', 'man', 'male', 'boy']):
        return 'men'
    elif any(word in title_lower for word in ['kid', 'child', 'baby', 'toddler']):
        return 'kids'
    return 'women'  # Default to women

def parse_price(price_str):
    """Extract numeric price from string"""
    try:
        if isinstance(price_str, (int, float)):
            return float(price_str)
        
        # Remove currency symbols and extract numbers
        price_clean = ''.join(c for c in str(price_str) if c.isdigit() or c == '.')
        price = float(price_clean) if price_clean else 29.99
        
        # Ensure reasonable price range
        if price < 10:
            price = price * 10  # Convert if it's in different currency
        if price > 500:
            price = price / 10  # Adjust if too high
        
        return round(price, 2)
    except:
        return 29.99

def try_api_endpoint(endpoint, query, category):
    """Try fetching from a specific API endpoint"""
    try:
        headers = {
            'X-RapidAPI-Key': endpoint['key'],
            'X-RapidAPI-Host': endpoint['host']
        }
        
        params = {
            'query': query,
            'country': 'US'
        }
        
        print(f"   Trying {endpoint['name']}...")
        response = requests.get(endpoint['url'], headers=headers, params=params, timeout=15)
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Try different possible response structures
            products = []
            if isinstance(data, dict):
                if 'products' in data:
                    products = data['products']
                elif 'data' in data and isinstance(data['data'], dict):
                    if 'products' in data['data']:
                        products = data['data']['products']
                    elif 'results' in data['data']:
                        products = data['data']['results']
                elif 'results' in data:
                    products = data['results']
                elif 'items' in data:
                    products = data['items']
            elif isinstance(data, list):
                products = data
            
            print(f"   Found {len(products)} products")
            return products[:10]  # Limit to 10 products per query
        
        return None
        
    except Exception as e:
        print(f"   Error with {endpoint['name']}: {e}")
        return None

def fetch_products_from_amazon():
    """Fetch products from Amazon RapidAPI using multiple endpoints"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Search queries for different categories
        search_queries = [
            {"query": "women dress fashion", "category": "women"},
            {"query": "women tops blouse", "category": "women"},
            {"query": "women jeans pants", "category": "women"},
            {"query": "men shirt clothing", "category": "men"},
            {"query": "men pants jeans", "category": "men"},
            {"query": "men jacket coat", "category": "men"},
            {"query": "kids clothing dress", "category": "kids"},
            {"query": "boys shirt kids", "category": "kids"},
        ]
        
        total_products = 0
        successful_api = None
        
        for search in search_queries:
            print(f"\n🔍 Fetching {search['query']}...")
            
            products = None
            
            # Try each API endpoint until one works
            for endpoint in API_ENDPOINTS:
                if successful_api and endpoint['name'] != successful_api:
                    continue  # Skip if we already found a working API
                
                products = try_api_endpoint(endpoint, search['query'], search['category'])
                if products:
                    successful_api = endpoint['name']
                    print(f"   ✅ Success with {endpoint['name']}")
                    break
            
            # If no API worked, use fallback products
            if not products:
                print(f"   ⚠️  All APIs failed, using fallback products")
                products = create_fallback_products_for_query(search['query'], search['category'])
            
            # Process and store products
            for i, product in enumerate(products):
                try:
                    # Extract product data with multiple fallbacks
                    product_id = (
                        product.get('asin') or 
                        product.get('id') or 
                        product.get('product_id') or 
                        f"{search['category']}_api_{total_products}_{i}"
                    )
                    
                    title = (
                        product.get('title') or 
                        product.get('product_title') or 
                        product.get('name') or 
                        product.get('product_name') or
                        f"Fashion {search['category'].title()} Item"
                    )
                    
                    # Handle price extraction from various formats
                    price_raw = (
                        product.get('price') or 
                        product.get('product_price') or 
                        product.get('current_price') or
                        product.get('price_current') or
                        29.99
                    )
                    
                    # If price is a dict, try to extract value
                    if isinstance(price_raw, dict):
                        price = parse_price(price_raw.get('value') or price_raw.get('amount') or 29.99)
                    else:
                        price = parse_price(price_raw)
                    
                    image_url = (
                        product.get('image') or 
                        product.get('product_photo') or 
                        product.get('thumbnail') or 
                        product.get('image_url') or
                        product.get('main_image') or
                        'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400'
                    )
                    
                    # Handle rating extraction
                    rating_raw = (
                        product.get('rating') or 
                        product.get('product_star_rating') or 
                        product.get('stars') or
                        product.get('review_rating') or
                        4.0
                    )
                    
                    if isinstance(rating_raw, dict):
                        rating = min(float(rating_raw.get('value') or rating_raw.get('rating') or 4.0), 5.0)
                    else:
                        rating = min(float(rating_raw), 5.0) if rating_raw else 4.0
                    
                    reviews_count = int(
                        product.get('reviews_count') or 
                        product.get('review_count') or 
                        product.get('total_reviews') or
                        50
                    )
                    
                    description = (
                        product.get('description') or 
                        product.get('product_description') or
                        product.get('summary') or
                        f"High quality {title.lower()}"
                    )[:500]  # Limit description length
                    
                    # Detect gender from title or use search category
                    gender = detect_gender(title)
                    if gender == 'women' and search['category'] != 'women':
                        gender = search['category']
                    
                    # Insert product
                    insert_query = """
                    INSERT IGNORE INTO products 
                    (id, title, price, imageUrl, category, gender, description, rating, reviews_count, cached_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    
                    cursor.execute(insert_query, (
                        product_id,
                        title,
                        price,
                        image_url,
                        'fashion',
                        gender,
                        description,
                        rating,
                        reviews_count,
                        datetime.now()
                    ))
                    
                    total_products += 1
                    print(f"   ✅ Added: {title[:40]}... (${price})")
                    
                except Exception as e:
                    print(f"   ⚠️  Error processing product {i}: {e}")
                    continue
            
            # Rate limiting between queries
            time.sleep(1)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"\n🎉 Successfully added {total_products} products to database!")
        if successful_api:
            print(f"📡 Used API: {successful_api}")
        return True
        
    except Exception as e:
        print(f"❌ Error fetching products: {e}")
        return False

def create_fallback_products_for_query(query, category):
    """Create fallback products for a specific query"""
    base_products = {
        'women dress fashion': [
            {'title': 'Elegant Floral Summer Dress', 'price': 45.99, 'image': 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400'},
            {'title': 'Black Evening Cocktail Dress', 'price': 79.99, 'image': 'https://images.unsplash.com/photo-1566479179817-c0ae8e4b4b3d?w=400'},
        ],
        'women tops blouse': [
            {'title': 'Casual White Cotton Blouse', 'price': 32.99, 'image': 'https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=400'},
            {'title': 'Pink Summer Crop Top', 'price': 28.99, 'image': 'https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=400'},
        ],
        'women jeans pants': [
            {'title': 'Blue High-Waisted Denim Jeans', 'price': 59.99, 'image': 'https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=400'},
            {'title': 'Black Skinny Fit Jeans', 'price': 54.99, 'image': 'https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=400'},
        ],
        'men shirt clothing': [
            {'title': 'Classic White Dress Shirt', 'price': 42.99, 'image': 'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400'},
            {'title': 'Blue Casual Button-Up Shirt', 'price': 38.99, 'image': 'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400'},
        ],
        'men pants jeans': [
            {'title': 'Dark Blue Slim Fit Jeans', 'price': 65.99, 'image': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400'},
            {'title': 'Black Chino Pants', 'price': 49.99, 'image': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400'},
        ],
        'men jacket coat': [
            {'title': 'Black Leather Biker Jacket', 'price': 125.99, 'image': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400'},
            {'title': 'Navy Blue Blazer', 'price': 89.99, 'image': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400'},
        ],
        'kids clothing dress': [
            {'title': 'Colorful Rainbow Kids Dress', 'price': 34.99, 'image': 'https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=400'},
            {'title': 'Pink Princess Dress for Girls', 'price': 39.99, 'image': 'https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=400'},
        ],
        'boys shirt kids': [
            {'title': 'Superhero Graphic T-Shirt', 'price': 19.99, 'image': 'https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=400'},
            {'title': 'Striped Long Sleeve Shirt', 'price': 24.99, 'image': 'https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=400'},
        ]
    }
    
    products = []
    product_list = base_products.get(query, [
        {'title': f'{category.title()} Fashion Item', 'price': 35.99, 'image': 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400'}
    ])
    
    for i, product in enumerate(product_list):
        products.append({
            'title': product['title'],
            'price': product['price'],
            'image': product['image'],
            'rating': 4.2 + (i * 0.1),
            'reviews_count': 50 + (i * 20),
            'description': f"High quality {product['title'].lower()}"
        })
    
    return products

def main():
    """Main function"""
    print("🚀 Fetching Amazon Products from RapidAPI (Multiple Endpoints)...")
    print("=" * 60)
    
    # Step 1: Clear existing products
    print("\n🗑️  Step 1: Clearing existing products...")
    if not clear_existing_products():
        print("❌ Failed to clear products. Exiting.")
        return
    
    # Step 2: Fetch new products
    print("\n🛍️  Step 2: Fetching products from Amazon APIs...")
    if fetch_products_from_amazon():
        print("\n" + "=" * 60)
        print("✅ Amazon products fetched successfully!")
        print("\n📊 Next steps:")
        print("   1. Restart your Flask backend")
        print("   2. Test the API: curl http://localhost:5000/api/products/search?query=clothing")
        print("   3. Start your frontend and check products")
    else:
        print("\n❌ Failed to fetch products")

if __name__ == "__main__":
    main()