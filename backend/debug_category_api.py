#!/usr/bin/env python3
"""
Debug Category API Issue
"""

import mysql.connector

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'fashiopulse'
}

def debug_category_issue():
    """Debug the category filtering issue"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        print("🔍 Debugging Category API Issue")
        print("=" * 40)
        
        # Test 1: Check total products
        cursor.execute("SELECT COUNT(*) as total FROM products")
        total = cursor.fetchone()
        print(f"Total products in database: {total['total']}")
        
        # Test 2: Check gender distribution
        cursor.execute("SELECT gender, COUNT(*) as count FROM products GROUP BY gender")
        genders = cursor.fetchall()
        print(f"\nGender distribution:")
        for g in genders:
            print(f"  {g['gender']}: {g['count']} products")
        
        # Test 3: Test the exact query used by get_cached_products for gender filtering
        print(f"\n🧪 Testing gender filtering queries:")
        
        for gender in ['women', 'men', 'kids']:
            query = "SELECT id as product_id, title, price, imageUrl as image_url, category, gender, description, rating FROM products WHERE 1=1 AND LOWER(gender) = %s ORDER BY created_at DESC LIMIT %s"
            cursor.execute(query, (gender, 20))
            results = cursor.fetchall()
            print(f"  {gender}: {len(results)} products")
            
            if results:
                print(f"    Sample: {results[0]['title'][:40]}...")
        
        # Test 4: Test fashion category (all products)
        print(f"\n🧪 Testing fashion category (all products):")
        query = "SELECT id as product_id, title, price, imageUrl as image_url, category, gender, description, rating FROM products WHERE 1=1 ORDER BY created_at DESC LIMIT %s"
        cursor.execute(query, (20,))
        results = cursor.fetchall()
        print(f"  All products: {len(results)} products")
        
        if results:
            print(f"    Sample: {results[0]['title'][:40]}...")
        
        # Test 5: Check sample product data
        print(f"\n📝 Sample product data:")
        cursor.execute("SELECT id, title, gender, category FROM products LIMIT 3")
        samples = cursor.fetchall()
        for sample in samples:
            print(f"  ID: {sample['id']}")
            print(f"  Title: {sample['title']}")
            print(f"  Gender: '{sample['gender']}'")
            print(f"  Category: '{sample['category']}'")
            print()
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    debug_category_issue()