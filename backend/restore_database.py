#!/usr/bin/env python3
"""
Database Restoration Script
Automatically creates database, tables, and fetches products from RapidAPI Amazon
"""

import mysql.connector
import requests
import json
import os
from datetime import datetime
import time

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Default XAMPP password is empty
    'database': 'fashiopulse'
}

# RapidAPI Configuration (from previous sessions)
RAPIDAPI_CONFIG = {
    'url': 'https://amazon-products1.p.rapidapi.com/search',
    'headers': {
        'X-RapidAPI-Key': '99de9f55f4msh3ff10d9c02adbb8p1d5a45jsn9651c5759bae',
        'X-RapidAPI-Host': 'amazon-products1.p.rapidapi.com'
    }
}

def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect without database first
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = conn.cursor()
        
        # Create database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        print(f"✅ Database '{DB_CONFIG['database']}' created/verified")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False

def create_tables():
    """Create all necessary tables"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Products table (enhanced with avatar sticker fields)
        products_table = """
        CREATE TABLE IF NOT EXISTS products (
            id VARCHAR(255) PRIMARY KEY,
            title TEXT NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            imageUrl TEXT,
            category VARCHAR(100),
            gender VARCHAR(50),
            description TEXT,
            rating DECIMAL(3,2),
            reviews_count INT DEFAULT 0,
            availability VARCHAR(50) DEFAULT 'in_stock',
            brand VARCHAR(100),
            sizes JSON,
            colors JSON,
            sticker_image VARCHAR(255),
            sticker_anchor VARCHAR(50) DEFAULT 'chest',
            sticker_position_x INT DEFAULT 50,
            sticker_position_y INT DEFAULT 50,
            cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        
        # User preferences table
        user_preferences_table = """
        CREATE TABLE IF NOT EXISTS user_preferences (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id VARCHAR(255) UNIQUE,
            style_preferences JSON,
            size_preferences JSON,
            color_preferences JSON,
            brand_preferences JSON,
            price_range JSON,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        
        # User behavior table
        user_behavior_table = """
        CREATE TABLE IF NOT EXISTS user_behavior (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id VARCHAR(255),
            action_type VARCHAR(100),
            product_id VARCHAR(255),
            category VARCHAR(100),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            metadata JSON
        )
        """
        
        # Avatar data table
        avatar_data_table = """
        CREATE TABLE IF NOT EXISTS avatar_data (
            id VARCHAR(255) PRIMARY KEY,
            user_id VARCHAR(255),
            avatar_config JSON,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        
        # Saved outfits table
        saved_outfits_table = """
        CREATE TABLE IF NOT EXISTS saved_outfits (
            id VARCHAR(255) PRIMARY KEY,
            user_id VARCHAR(255),
            name VARCHAR(255),
            avatar_data JSON,
            stickers JSON,
            total_price DECIMAL(10,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        # API usage tracking
        api_usage_table = """
        CREATE TABLE IF NOT EXISTS api_usage (
            id INT AUTO_INCREMENT PRIMARY KEY,
            endpoint VARCHAR(255),
            requests_count INT DEFAULT 0,
            last_request TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            daily_limit INT DEFAULT 100,
            monthly_limit INT DEFAULT 1000
        )
        """
        
        tables = [
            ("products", products_table),
            ("user_preferences", user_preferences_table),
            ("user_behavior", user_behavior_table),
            ("avatar_data", avatar_data_table),
            ("saved_outfits", saved_outfits_table),
            ("api_usage", api_usage_table)
        ]
        
        for table_name, table_sql in tables:
            cursor.execute(table_sql)
            print(f"✅ Table '{table_name}' created/verified")
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def fetch_products_from_rapidapi():
    """Fetch products from RapidAPI Amazon (based on previous sessions)"""
    
    # Check if API key is set
    if RAPIDAPI_CONFIG['headers']['X-RapidAPI-Key'] == 'YOUR_RAPIDAPI_KEY_HERE':
        print("⚠️  Please set your RapidAPI key in the script")
        print("   Update RAPIDAPI_CONFIG['headers']['X-RapidAPI-Key'] with your actual key")
        return False
    
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Search queries from previous sessions
        search_queries = [
            # Women's clothing
            {"query": "women dress", "category": "women", "limit": 20},
            {"query": "women tops", "category": "women", "limit": 15},
            {"query": "women jeans", "category": "women", "limit": 15},
            {"query": "women shoes", "category": "women", "limit": 10},
            
            # Men's clothing
            {"query": "men shirt", "category": "men", "limit": 20},
            {"query": "men pants", "category": "men", "limit": 15},
            {"query": "men shoes", "category": "men", "limit": 10},
            {"query": "men jacket", "category": "men", "limit": 10},
            
            # Kids clothing
            {"query": "kids clothing", "category": "kids", "limit": 15},
            {"query": "boys shirt", "category": "kids", "limit": 10},
            {"query": "girls dress", "category": "kids", "limit": 10},
        ]
        
        total_products = 0
        
        for search in search_queries:
            print(f"🔍 Fetching {search['query']}...")
            
            params = {
                'query': search['query'],
                'country': 'US',
                'category': 'fashion'
            }
            
            try:
                response = requests.get(
                    RAPIDAPI_CONFIG['url'],
                    headers=RAPIDAPI_CONFIG['headers'],
                    params=params,
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    products = data.get('products', [])
                    
                    for product in products[:search['limit']]:
                        try:
                            # Extract product data
                            product_id = product.get('asin', f"prod_{int(time.time())}_{total_products}")
                            title = product.get('title', 'Unknown Product')
                            price = float(product.get('price', {}).get('value', 29.99))
                            image_url = product.get('image', '')
                            rating = float(product.get('rating', {}).get('value', 4.0))
                            reviews = int(product.get('reviews_count', 0))
                            
                            # Insert product
                            insert_query = """
                            INSERT IGNORE INTO products 
                            (id, title, price, imageUrl, category, gender, rating, reviews_count, cached_at)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """
                            
                            cursor.execute(insert_query, (
                                product_id,
                                title,
                                price,
                                image_url,
                                'fashion',
                                search['category'],
                                rating,
                                reviews,
                                datetime.now()
                            ))
                            
                            total_products += 1
                            
                        except Exception as e:
                            print(f"   ⚠️  Error processing product: {e}")
                            continue
                    
                    print(f"   ✅ Added {len(products[:search['limit']])} products")
                    
                else:
                    print(f"   ❌ API Error: {response.status_code}")
                
                # Rate limiting
                time.sleep(1)
                
            except Exception as e:
                print(f"   ❌ Request error: {e}")
                continue
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"\n🎉 Successfully added {total_products} products to database!")
        return True
        
    except Exception as e:
        print(f"❌ Error fetching products: {e}")
        return False

def update_api_usage():
    """Update API usage tracking"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Insert or update API usage
        cursor.execute("""
            INSERT INTO api_usage (endpoint, requests_count, last_request)
            VALUES ('amazon_products', 1, %s)
            ON DUPLICATE KEY UPDATE
            requests_count = requests_count + 1,
            last_request = %s
        """, (datetime.now(), datetime.now()))
        
        conn.commit()
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"⚠️  Could not update API usage: {e}")

def main():
    """Main restoration process"""
    print("🚀 Starting Database Restoration Process...")
    print("=" * 50)
    
    # Step 1: Create database
    print("\n📁 Step 1: Creating Database...")
    if not create_database():
        print("❌ Failed to create database. Exiting.")
        return
    
    # Step 2: Create tables
    print("\n📋 Step 2: Creating Tables...")
    if not create_tables():
        print("❌ Failed to create tables. Exiting.")
        return
    
    # Step 3: Fetch products
    print("\n🛍️  Step 3: Fetching Products from RapidAPI...")
    if fetch_products_from_rapidapi():
        update_api_usage()
    else:
        print("⚠️  Product fetching failed, but database structure is ready")
    
    print("\n" + "=" * 50)
    print("✅ Database restoration completed!")
    print("\n📊 Next steps:")
    print("   1. Start your Flask backend: python backend/app.py")
    print("   2. Start your Next.js frontend: npm run dev")
    print("   3. Visit http://localhost:3000 to see your products")
    
    if RAPIDAPI_CONFIG['headers']['X-RapidAPI-Key'] == 'YOUR_RAPIDAPI_KEY_HERE':
        print("\n⚠️  Remember to set your RapidAPI key to fetch products!")

if __name__ == "__main__":
    main()