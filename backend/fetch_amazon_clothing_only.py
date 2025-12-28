#!/usr/bin/env python3
"""
Amazon Clothing Data Fetcher - RapidAPI
Fetches ONLY clothing items from Amazon via RapidAPI, removes duplicates, saves to database
"""

import mysql.connector
import requests
import json
import time
import hashlib
from datetime import datetime
import re

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'fashiopulse'
}

# RapidAPI Configuration - Multiple endpoints to try
RAPIDAPI_ENDPOINTS = [
    {
        'name': 'Amazon Real Time Product Search',
        'url': 'https://real-time-amazon-data.p.rapidapi.com/search',
        'host': 'real-time-amazon-data.p.rapidapi.com',
        'key': '99de9f55f4msh3ff10d9c02adbb8p1d5a45jsn9651c5759bae'
    },
    {
        'name': 'Amazon Product Data',
        'url': 'https://amazon-product-data.p.rapidapi.com/products',
        'host': 'amazon-product-data.p.rapidapi.com', 
        'key': '99de9f55f4msh3ff10d9c02adbb8p1d5a45jsn9651c5759bae'
    },
    {
        'name': 'Amazon API v1',
        'url': 'https://amazon-api-v2.p.rapidapi.com/products/search',
        'host': 'amazon-api-v2.p.rapidapi.com',
        'key': '99de9f55f4msh3ff10d9c02adbb8p1d5a45jsn9651c5759bae'
    },
    {
        'name': 'Amazon Data Scraper',
        'url': 'https://amazon-scraper-api.p.rapidapi.com/products/search',
        'host': 'amazon-scraper-api.p.rapidapi.com',
        'key': '99de9f55f4msh3ff10d9c02adbb8p1d5a45jsn9651c5759bae'
    }
]

# Clothing-specific keywords for filtering
CLOTHING_KEYWORDS = [
    # Tops
    'shirt', 'blouse', 'top', 't-shirt', 'tshirt', 'tank', 'camisole', 'sweater', 
    'cardigan', 'hoodie', 'sweatshirt', 'polo', 'tunic', 'crop top', 'halter',
    
    # Bottoms  
    'pants', 'jeans', 'trousers', 'shorts', 'skirt', 'leggings', 'joggers',
    'chinos', 'slacks', 'capris', 'culottes', 'palazzo',
    
    # Dresses & Outerwear
    'dress', 'gown', 'frock', 'jacket', 'coat', 'blazer', 'vest', 'cardigan',
    'parka', 'windbreaker', 'bomber', 'denim jacket', 'leather jacket',
    
    # Footwear
    'shoes', 'sneakers', 'boots', 'sandals', 'heels', 'flats', 'loafers',
    'oxfords', 'pumps', 'wedges', 'clogs', 'moccasins', 'stilettos',
    
    # Undergarments & Sleepwear
    'bra', 'underwear', 'lingerie', 'panties', 'boxers', 'briefs', 'pajamas',
    'nightgown', 'robe', 'sleepwear', 'loungewear',
    
    # Accessories (clothing-related)
    'belt', 'scarf', 'tie', 'bow tie', 'suspenders', 'gloves', 'hat', 'cap',
    'beanie', 'headband', 'socks', 'stockings', 'tights',
    
    # General clothing terms
    'clothing', 'apparel', 'wear', 'fashion', 'garment', 'outfit', 'attire'
]

# Non-clothing keywords to exclude
EXCLUDE_KEYWORDS = [
    'phone', 'case', 'charger', 'cable', 'electronics', 'book', 'toy', 'game',
    'kitchen', 'home', 'garden', 'tool', 'automotive', 'beauty', 'makeup',
    'supplement', 'vitamin', 'food', 'snack', 'drink', 'coffee', 'tea',
    'furniture', 'decor', 'lamp', 'pillow', 'blanket', 'sheet', 'towel',
    'computer', 'laptop', 'tablet', 'mouse', 'keyboard', 'monitor', 'camera'
]

def is_clothing_item(title, description=""):
    """Check if item is clothing based on title and description"""
    text = f"{title} {description}".lower()
    
    # Check for exclude keywords first
    if any(exclude in text for exclude in EXCLUDE_KEYWORDS):
        return False
    
    # Check for clothing keywords
    return any(keyword in text for keyword in CLOTHING_KEYWORDS)

def detect_gender_from_text(title, description=""):
    """Detect gender from title and description"""
    text = f"{title} {description}".lower()
    
    women_indicators = [
        'women', 'woman', 'ladies', 'female', 'girl', 'womens', "women's",
        'dress', 'blouse', 'skirt', 'bra', 'lingerie', 'heels', 'purse', 
        'handbag', 'maternity', 'plus size women', 'ladies'
    ]
    
    men_indicators = [
        'men', 'man', 'male', 'boy', 'mens', "men's", 'gentleman',
        'tie', 'suit', 'tuxedo', 'boxer', 'briefs', 'beard', 'masculine'
    ]
    
    kids_indicators = [
        'kid', 'child', 'baby', 'toddler', 'infant', 'youth', 'junior',
        'boys', 'girls', 'children', 'pediatric', 'school age'
    ]
    
    if any(indicator in text for indicator in women_indicators):
        return 'women'
    elif any(indicator in text for indicator in men_indicators):
        return 'men'
    elif any(indicator in text for indicator in kids_indicators):
        return 'kids'
    
    return 'unisex'

def normalize_price(price_data):
    """Extract and normalize price from various formats"""
    try:
        if isinstance(price_data, (int, float)):
            price = float(price_data)
        elif isinstance(price_data, dict):
            price = float(price_data.get('value', 0) or price_data.get('amount', 0) or 0)
        elif isinstance(price_data, str):
            # Extract numbers from price string
            numbers = re.findall(r'\d+\.?\d*', price_data.replace(',', ''))
            price = float(numbers[0]) if numbers else 0
        else:
            price = 0
        
        # Convert to reasonable USD range
        if price < 5:
            price = price * 10  # Convert if in different scale
        elif price > 1000:
            price = price / 100  # Convert from cents
        
        # Ensure reasonable clothing price range ($5-$300)
        if price < 5:
            price = 25.99
        elif price > 300:
            price = 149.99
            
        return round(price, 2)
        
    except:
        return 29.99

def normalize_rating(rating_data):
    """Extract and normalize rating (1-5 scale)"""
    try:
        if isinstance(rating_data, (int, float)):
            rating = float(rating_data)
        elif isinstance(rating_data, dict):
            rating = float(rating_data.get('value', 0) or rating_data.get('rating', 0) or 4.0)
        elif isinstance(rating_data, str):
            numbers = re.findall(r'\d+\.?\d*', rating_data)
            rating = float(numbers[0]) if numbers else 4.0
        else:
            rating = 4.0
            
        # Ensure 1-5 range
        rating = max(1.0, min(5.0, rating))
        return round(rating, 1)
        
    except:
        return 4.0

def generate_product_hash(title, price, brand=""):
    """Generate hash for duplicate detection"""
    # Normalize title for comparison
    normalized_title = re.sub(r'[^\w\s]', '', title.lower().strip())
    hash_string = f"{normalized_title}_{price}_{brand.lower()}"
    return hashlib.md5(hash_string.encode()).hexdigest()

def try_amazon_api_endpoint(endpoint, search_query, max_results=50):
    """Try fetching from a specific Amazon API endpoint"""
    try:
        headers = {
            'X-RapidAPI-Key': endpoint['key'],
            'X-RapidAPI-Host': endpoint['host']
        }
        
        # Different parameter formats for different APIs
        params = {
            'query': search_query,
            'country': 'US',
            'page': '1'
        }
        
        # Add category if supported
        if 'real-time-amazon' in endpoint['url']:
            params['category'] = 'fashion'
        
        print(f"   🔄 Trying {endpoint['name']}...")
        print(f"   📡 URL: {endpoint['url']}")
        print(f"   🔍 Query: {search_query}")
        
        response = requests.get(
            endpoint['url'],
            headers=headers,
            params=params,
            timeout=30
        )
        
        print(f"   📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   📦 Response keys: {list(data.keys()) if isinstance(data, dict) else 'List response'}")
            
            # Extract products from different response structures
            products = []
            
            if isinstance(data, list):
                products = data
            elif isinstance(data, dict):
                # Try different possible product keys
                for key in ['products', 'data', 'results', 'items']:
                    if key in data:
                        if isinstance(data[key], list):
                            products = data[key]
                            break
                        elif isinstance(data[key], dict):
                            # Check for nested products
                            nested_data = data[key]
                            for nested_key in ['products', 'results', 'items']:
                                if nested_key in nested_data and isinstance(nested_data[nested_key], list):
                                    products = nested_data[nested_key]
                                    break
                            if products:
                                break
            
            print(f"   📦 Found {len(products)} raw products")
            
            # Filter and process clothing items
            clothing_products = []
            seen_hashes = set()
            
            for product in products[:max_results]:
                try:
                    # Extract basic info
                    title = (
                        product.get('title') or 
                        product.get('product_title') or 
                        product.get('name') or 
                        product.get('product_name') or
                        ''
                    )
                    
                    description = (
                        product.get('description') or 
                        product.get('product_description') or
                        product.get('summary') or
                        ''
                    )
                    
                    # Skip if not clothing
                    if not title or not is_clothing_item(title, description):
                        continue
                    
                    # Extract other fields
                    asin = product.get('asin') or product.get('id') or product.get('product_id')
                    
                    price = normalize_price(
                        product.get('price') or 
                        product.get('product_price') or 
                        product.get('current_price') or
                        product.get('price_current')
                    )
                    
                    brand = (
                        product.get('brand') or 
                        product.get('manufacturer') or
                        'Fashion Brand'
                    )
                    
                    # Check for duplicates
                    product_hash = generate_product_hash(title, price, brand)
                    if product_hash in seen_hashes:
                        continue
                    seen_hashes.add(product_hash)
                    
                    image_url = (
                        product.get('image') or 
                        product.get('product_photo') or 
                        product.get('thumbnail') or 
                        product.get('image_url') or
                        product.get('main_image') or
                        'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400'
                    )
                    
                    rating = normalize_rating(
                        product.get('rating') or 
                        product.get('product_star_rating') or 
                        product.get('stars')
                    )
                    
                    reviews_count = int(
                        product.get('reviews_count') or 
                        product.get('review_count') or 
                        product.get('total_reviews') or
                        50
                    )
                    
                    product_url = (
                        product.get('product_url') or 
                        product.get('url') or 
                        f"https://amazon.com/dp/{asin}" if asin else ""
                    )
                    
                    gender = detect_gender_from_text(title, description)
                    
                    clothing_product = {
                        'asin': asin,
                        'title': title[:255],  # Limit title length
                        'price': price,
                        'image_url': image_url,
                        'rating': rating,
                        'reviews_count': min(reviews_count, 9999),  # Reasonable limit
                        'description': description[:500],  # Limit description
                        'product_url': product_url,
                        'brand': brand[:100],  # Limit brand length
                        'gender': gender,
                        'hash': product_hash
                    }
                    
                    clothing_products.append(clothing_product)
                    
                except Exception as e:
                    print(f"   ⚠️  Error processing product: {e}")
                    continue
            
            print(f"   ✅ Filtered to {len(clothing_products)} clothing items")
            return clothing_products
            
        elif response.status_code == 429:
            print(f"   ⏳ Rate limited - waiting 10 seconds...")
            time.sleep(10)
            return None
        elif response.status_code == 403:
            print(f"   ❌ Access forbidden - API key issue")
            return None
        else:
            print(f"   ❌ API Error {response.status_code}: {response.text[:200]}")
            return None
            
    except Exception as e:
        print(f"   ❌ Request failed: {e}")
        return None

def fetch_amazon_clothing_data():
    """Fetch clothing data from Amazon APIs and save to database"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Clear existing products
        cursor.execute("DELETE FROM products")
        conn.commit()
        print("🗑️  Cleared existing products")
        
        # Clothing-specific search queries
        clothing_searches = [
            "women dress clothing fashion",
            "women tops shirts blouses", 
            "women jeans pants denim",
            "women shoes sneakers heels",
            "women jackets coats outerwear",
            "men shirts dress casual",
            "men pants jeans chinos",
            "men shoes sneakers boots",
            "men jackets blazers coats",
            "men t-shirts polo shirts",
            "kids clothing children apparel",
            "boys shirts pants clothing",
            "girls dresses tops clothing",
            "unisex clothing fashion wear",
            "athletic wear sportswear",
            "formal wear business attire"
        ]
        
        all_products = []
        global_seen_hashes = set()
        successful_apis = []
        
        for search_query in clothing_searches:
            print(f"\n🔍 Searching: {search_query}")
            
            products_found = False
            
            # Try each API endpoint
            for endpoint in RAPIDAPI_ENDPOINTS:
                products = try_amazon_api_endpoint(endpoint, search_query, max_results=30)
                
                if products and len(products) > 0:
                    # Remove global duplicates
                    unique_products = []
                    for product in products:
                        if product['hash'] not in global_seen_hashes:
                            global_seen_hashes.add(product['hash'])
                            unique_products.append(product)
                    
                    if unique_products:
                        all_products.extend(unique_products)
                        successful_apis.append(endpoint['name'])
                        products_found = True
                        print(f"   ✅ Added {len(unique_products)} unique clothing items")
                        break  # Move to next search query
                
                # Rate limiting between API attempts
                time.sleep(3)
            
            if not products_found:
                print(f"   ⚠️  No clothing items found for: {search_query}")
            
            # Rate limiting between searches
            time.sleep(2)
        
        # Save all products to database
        if all_products:
            print(f"\n💾 Saving {len(all_products)} unique clothing products to database...")
            
            insert_sql = """
            INSERT INTO products 
            (id, title, price, imageUrl, category, gender, description, rating, 
             reviews_count, brand, product_url, source, asin, cached_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            saved_count = 0
            for i, product in enumerate(all_products):
                try:
                    product_id = product['asin'] or f"amazon_clothing_{i+1:04d}"
                    
                    cursor.execute(insert_sql, (
                        product_id,
                        product['title'],
                        product['price'],
                        product['image_url'],
                        'fashion',
                        product['gender'],
                        product['description'],
                        product['rating'],
                        product['reviews_count'],
                        product['brand'],
                        product['product_url'],
                        'amazon_api',
                        product['asin'],
                        datetime.now()
                    ))
                    
                    saved_count += 1
                    if saved_count % 10 == 0:
                        print(f"   💾 Saved {saved_count} products...")
                    
                except Exception as e:
                    print(f"   ⚠️  Error saving product {i}: {e}")
                    continue
            
            conn.commit()
            cursor.close()
            conn.close()
            
            print(f"\n🎉 Successfully saved {saved_count} unique clothing products!")
            print(f"📡 Successful APIs: {list(set(successful_apis))}")
            
            return saved_count > 0
        else:
            print(f"\n⚠️  No clothing products found from any API")
            return False
        
    except Exception as e:
        print(f"❌ Error in fetch_amazon_clothing_data: {e}")
        return False

def verify_clothing_database():
    """Verify the clothing products in database"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # Get counts by gender
        cursor.execute("SELECT gender, COUNT(*) as count FROM products GROUP BY gender ORDER BY count DESC")
        gender_counts = cursor.fetchall()
        
        # Get total count
        cursor.execute("SELECT COUNT(*) as total FROM products")
        total = cursor.fetchone()['total']
        
        # Get sample products
        cursor.execute("SELECT id, title, price, gender, brand FROM products ORDER BY RAND() LIMIT 10")
        samples = cursor.fetchall()
        
        # Get price range
        cursor.execute("SELECT MIN(price) as min_price, MAX(price) as max_price, AVG(price) as avg_price FROM products")
        price_stats = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        print(f"\n📊 Clothing Database Verification:")
        print(f"   Total clothing products: {total}")
        print(f"   Price range: ${price_stats['min_price']:.2f} - ${price_stats['max_price']:.2f}")
        print(f"   Average price: ${price_stats['avg_price']:.2f}")
        
        print(f"\n👥 By gender:")
        for item in gender_counts:
            print(f"     {item['gender']}: {item['count']} items")
        
        print(f"\n🛍️  Sample clothing products:")
        for product in samples:
            print(f"   {product['id']}: {product['title'][:40]}... (${product['price']}) - {product['gender']} - {product['brand']}")
        
        return total > 0
        
    except Exception as e:
        print(f"❌ Error verifying database: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Amazon Clothing Data Fetcher - RapidAPI")
    print("=" * 50)
    print("🎯 Fetching ONLY clothing items from Amazon")
    print("🔄 Removing duplicates automatically")
    print("💾 Saving to phpMyAdmin database")
    print("=" * 50)
    
    success = fetch_amazon_clothing_data()
    
    if success:
        verify_clothing_database()
        
        print("\n" + "=" * 50)
        print("🎉 Amazon clothing data fetch completed!")
        print("\n📊 Next steps:")
        print("   1. Check phpMyAdmin: http://localhost/phpmyadmin")
        print("   2. View 'fashiopulse' → 'products' table")
        print("   3. Restart Flask backend: python backend/app.py")
        print("   4. Test API: curl http://localhost:5000/api/products/search?query=clothing")
        print("   5. Browse products in your frontend")
        print("   6. Use products in Avatar Builder")
    else:
        print("\n❌ Failed to fetch clothing data from Amazon APIs")
        print("💡 This might be due to API limits or subscription issues")

if __name__ == "__main__":
    main()