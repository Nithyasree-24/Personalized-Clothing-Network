#!/usr/bin/env python3
"""
Test Database Connection and Products
"""

import mysql.connector

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'fashiopulse'
}

def test_database():
    """Test database connection and check products"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # Check if products table exists
        cursor.execute("SHOW TABLES LIKE 'products'")
        table_exists = cursor.fetchone()
        print(f"Products table exists: {table_exists is not None}")
        
        if table_exists:
            # Check table structure
            cursor.execute("DESCRIBE products")
            columns = cursor.fetchall()
            print("\nTable structure:")
            for col in columns:
                print(f"  {col['Field']} - {col['Type']}")
            
            # Count products
            cursor.execute("SELECT COUNT(*) as count FROM products")
            count = cursor.fetchone()
            print(f"\nTotal products: {count['count']}")
            
            # Get sample products
            cursor.execute("SELECT * FROM products LIMIT 5")
            products = cursor.fetchall()
            print(f"\nSample products:")
            for product in products:
                print(f"  ID: {product['id']}, Title: {product['title']}, Price: {product['price']}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Database error: {e}")

if __name__ == "__main__":
    test_database()