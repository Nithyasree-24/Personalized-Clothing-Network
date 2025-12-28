#!/usr/bin/env python3
"""
Check Exact Category Names
"""

import mysql.connector

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'fashiopulse'
}

def check_exact_categories():
    """Check exact category names and test filtering"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        print("🔍 Checking exact category names...")
        
        # Get exact categories with quotes
        cursor.execute("SELECT DISTINCT product_category FROM clothing ORDER BY product_category")
        categories = cursor.fetchall()
        
        print(f"\n📂 Exact Categories in Database:")
        for cat in categories:
            category_name = cat['product_category']
            
            # Count products for each category
            cursor.execute("SELECT COUNT(*) as count FROM clothing WHERE product_category = %s", (category_name,))
            count = cursor.fetchone()['count']
            
            # Test lowercase matching
            cursor.execute("SELECT COUNT(*) as count FROM clothing WHERE LOWER(product_category) = %s", (category_name.lower(),))
            lowercase_count = cursor.fetchone()['count']
            
            print(f'   "{category_name}" -> {count} products (lowercase: {lowercase_count})')
        
        print(f"\n🧪 Testing problematic categories:")
        
        # Test specific categories that might be failing
        test_categories = ['Western Wear', 'Ethnic Wear', 'Bottom Wear']
        
        for test_cat in test_categories:
            print(f"\n   Testing '{test_cat}':")
            
            # Exact match
            cursor.execute("SELECT COUNT(*) as count FROM clothing WHERE product_category = %s", (test_cat,))
            exact_count = cursor.fetchone()['count']
            print(f"     Exact match: {exact_count}")
            
            # Lowercase match
            cursor.execute("SELECT COUNT(*) as count FROM clothing WHERE LOWER(product_category) = %s", (test_cat.lower(),))
            lower_count = cursor.fetchone()['count']
            print(f"     Lowercase match: {lower_count}")
            
            # Case insensitive match
            cursor.execute("SELECT COUNT(*) as count FROM clothing WHERE LOWER(product_category) = LOWER(%s)", (test_cat,))
            case_insensitive_count = cursor.fetchone()['count']
            print(f"     Case insensitive: {case_insensitive_count}")
            
            # LIKE match
            cursor.execute("SELECT COUNT(*) as count FROM clothing WHERE product_category LIKE %s", (f"%{test_cat}%",))
            like_count = cursor.fetchone()['count']
            print(f"     LIKE match: {like_count}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    check_exact_categories()