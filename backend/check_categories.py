#!/usr/bin/env python3
"""
Check Categories in Clothing Table
"""

import mysql.connector

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'fashiopulse'
}

def check_categories():
    """Check unique categories and genders in clothing table"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        print("🔍 Checking categories in clothing table...")
        
        # Get unique categories
        cursor.execute("SELECT DISTINCT product_category FROM clothing ORDER BY product_category")
        categories = cursor.fetchall()
        
        print(f"\n📂 Unique Categories ({len(categories)} total):")
        for cat in categories:
            cursor.execute("SELECT COUNT(*) as count FROM clothing WHERE product_category = %s", (cat['product_category'],))
            count = cursor.fetchone()['count']
            print(f"   - {cat['product_category']} ({count} products)")
        
        # Get unique genders
        cursor.execute("SELECT DISTINCT gender FROM clothing ORDER BY gender")
        genders = cursor.fetchall()
        
        print(f"\n👥 Unique Genders ({len(genders)} total):")
        for gender in genders:
            cursor.execute("SELECT COUNT(*) as count FROM clothing WHERE gender = %s", (gender['gender'],))
            count = cursor.fetchone()['count']
            print(f"   - {gender['gender']} ({count} products)")
        
        # Get category breakdown by gender
        print(f"\n📊 Category Breakdown by Gender:")
        for gender in genders:
            print(f"\n   {gender['gender']}:")
            cursor.execute("""
                SELECT product_category, COUNT(*) as count 
                FROM clothing 
                WHERE gender = %s 
                GROUP BY product_category 
                ORDER BY count DESC
            """, (gender['gender'],))
            gender_categories = cursor.fetchall()
            
            for cat in gender_categories:
                print(f"     - {cat['product_category']}: {cat['count']} products")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    check_categories()