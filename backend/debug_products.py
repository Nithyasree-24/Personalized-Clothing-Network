#!/usr/bin/env python3
"""
Debug Products - Check what's in the database and test queries
"""

import mysql.connector

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'fashiopulse'
}

def debug_products():
    """Debug products in database"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # Test 1: Count all products
        cursor.execute("SELECT COUNT(*) as count FROM products")
        count = cursor.fetchone()
        print(f"Total products in database: {count['count']}")
        
        # Test 2: Show all products with their categories and genders
        cursor.execute("SELECT id, title, category, gender, price FROM products LIMIT 10")
        products = cursor.fetchall()
        print(f"\nFirst 10 products:")
        for product in products:
            print(f"  ID: {product['id']}, Title: {product['title'][:30]}..., Category: {product['category']}, Gender: {product['gender']}, Price: ${product['price']}")
        
        # Test 3: Test the exact query used by get_cached_products
        print(f"\n--- Testing get_cached_products query ---")
        
        # Test without filters
        query = "SELECT id as product_id, title, price, imageUrl as image_url, category, gender, description, rating FROM products WHERE 1=1"
        cursor.execute(query)
        results = cursor.fetchall()
        print(f"Query without filters returned: {len(results)} products")
        
        # Test with category filter
        query = "SELECT id as product_id, title, price, imageUrl as image_url, category, gender, description, rating FROM products WHERE 1=1 AND (LOWER(category) LIKE %s OR LOWER(title) LIKE %s)"
        cursor.execute(query, ('%fashion%', '%fashion%'))
        results = cursor.fetchall()
        print(f"Query with category 'fashion' returned: {len(results)} products")
        
        # Test with gender filter
        query = "SELECT id as product_id, title, price, imageUrl as image_url, category, gender, description, rating FROM products WHERE 1=1 AND LOWER(gender) = %s"
        cursor.execute(query, ('women',))
        results = cursor.fetchall()
        print(f"Query with gender 'women' returned: {len(results)} products")
        
        # Test with both filters
        query = "SELECT id as product_id, title, price, imageUrl as image_url, category, gender, description, rating FROM products WHERE 1=1 AND (LOWER(category) LIKE %s OR LOWER(title) LIKE %s) AND LOWER(gender) = %s"
        cursor.execute(query, ('%fashion%', '%fashion%', 'women'))
        results = cursor.fetchall()
        print(f"Query with category 'fashion' AND gender 'women' returned: {len(results)} products")
        
        # Show sample result
        if results:
            print(f"\nSample result:")
            sample = results[0]
            for key, value in sample.items():
                print(f"  {key}: {value}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Database error: {e}")

if __name__ == "__main__":
    debug_products()