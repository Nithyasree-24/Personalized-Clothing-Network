#!/usr/bin/env python3
"""
Create Mock Products Script
Creates sample products for testing when RapidAPI is not available
"""

import mysql.connector
from datetime import datetime
import json

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'fashiopulse'
}

def create_mock_products():
    """Create mock products for testing"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Mock products data
        mock_products = [
            # Women's Products
            {
                'id': 'W001',
                'title': 'Elegant Pink Dress',
                'price': 49.99,
                'imageUrl': 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400',
                'category': 'fashion',
                'gender': 'women',
                'description': 'Beautiful pink dress perfect for any occasion',
                'rating': 4.5,
                'reviews_count': 128
            },
            {
                'id': 'W002',
                'title': 'Casual White Top',
                'price': 29.99,
                'imageUrl': 'https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=400',
                'category': 'fashion',
                'gender': 'women',
                'description': 'Comfortable white top for everyday wear',
                'rating': 4.2,
                'reviews_count': 89
            },
            {
                'id': 'W003',
                'title': 'Blue Denim Jeans',
                'price': 59.99,
                'imageUrl': 'https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=400',
                'category': 'fashion',
                'gender': 'women',
                'description': 'Classic blue denim jeans with perfect fit',
                'rating': 4.7,
                'reviews_count': 203
            },
            {
                'id': 'W004',
                'title': 'Pink Sneakers',
                'price': 79.99,
                'imageUrl': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400',
                'category': 'fashion',
                'gender': 'women',
                'description': 'Stylish pink sneakers for active lifestyle',
                'rating': 4.4,
                'reviews_count': 156
            },
            {
                'id': 'W005',
                'title': 'Floral Summer Dress',
                'price': 39.99,
                'imageUrl': 'https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=400',
                'category': 'fashion',
                'gender': 'women',
                'description': 'Light floral dress perfect for summer',
                'rating': 4.6,
                'reviews_count': 174
            },
            
            # Men's Products
            {
                'id': 'M001',
                'title': 'Classic White Shirt',
                'price': 45.99,
                'imageUrl': 'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400',
                'category': 'fashion',
                'gender': 'men',
                'description': 'Professional white dress shirt',
                'rating': 4.3,
                'reviews_count': 92
            },
            {
                'id': 'M002',
                'title': 'Dark Blue Jeans',
                'price': 69.99,
                'imageUrl': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400',
                'category': 'fashion',
                'gender': 'men',
                'description': 'Premium dark blue denim jeans',
                'rating': 4.5,
                'reviews_count': 167
            },
            {
                'id': 'M003',
                'title': 'Black Leather Jacket',
                'price': 129.99,
                'imageUrl': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400',
                'category': 'fashion',
                'gender': 'men',
                'description': 'Stylish black leather jacket',
                'rating': 4.8,
                'reviews_count': 234
            },
            {
                'id': 'M004',
                'title': 'Brown Dress Shoes',
                'price': 89.99,
                'imageUrl': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400',
                'category': 'fashion',
                'gender': 'men',
                'description': 'Classic brown leather dress shoes',
                'rating': 4.4,
                'reviews_count': 145
            },
            {
                'id': 'M005',
                'title': 'Casual T-Shirt',
                'price': 24.99,
                'imageUrl': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400',
                'category': 'fashion',
                'gender': 'men',
                'description': 'Comfortable casual t-shirt',
                'rating': 4.1,
                'reviews_count': 78
            },
            
            # Kids Products
            {
                'id': 'K001',
                'title': 'Colorful Kids Dress',
                'price': 34.99,
                'imageUrl': 'https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=400',
                'category': 'fashion',
                'gender': 'kids',
                'description': 'Bright and colorful dress for kids',
                'rating': 4.6,
                'reviews_count': 112
            },
            {
                'id': 'K002',
                'title': 'Kids Superhero T-Shirt',
                'price': 19.99,
                'imageUrl': 'https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=400',
                'category': 'fashion',
                'gender': 'kids',
                'description': 'Fun superhero themed t-shirt',
                'rating': 4.7,
                'reviews_count': 89
            },
            {
                'id': 'K003',
                'title': 'Kids Denim Overalls',
                'price': 42.99,
                'imageUrl': 'https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=400',
                'category': 'fashion',
                'gender': 'kids',
                'description': 'Cute denim overalls for kids',
                'rating': 4.5,
                'reviews_count': 67
            },
            {
                'id': 'K004',
                'title': 'Colorful Kids Sneakers',
                'price': 39.99,
                'imageUrl': 'https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=400',
                'category': 'fashion',
                'gender': 'kids',
                'description': 'Bright and fun sneakers for active kids',
                'rating': 4.4,
                'reviews_count': 95
            },
            {
                'id': 'K005',
                'title': 'Kids Winter Jacket',
                'price': 54.99,
                'imageUrl': 'https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=400',
                'category': 'fashion',
                'gender': 'kids',
                'description': 'Warm winter jacket for kids',
                'rating': 4.8,
                'reviews_count': 143
            }
        ]
        
        # Insert products
        insert_query = """
        INSERT IGNORE INTO products 
        (id, title, price, imageUrl, category, gender, description, rating, reviews_count, cached_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        for product in mock_products:
            cursor.execute(insert_query, (
                product['id'],
                product['title'],
                product['price'],
                product['imageUrl'],
                product['category'],
                product['gender'],
                product['description'],
                product['rating'],
                product['reviews_count'],
                datetime.now()
            ))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✅ Successfully added {len(mock_products)} mock products to database!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating mock products: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Creating Mock Products...")
    print("=" * 40)
    
    if create_mock_products():
        print("\n✅ Mock products created successfully!")
        print("\n📊 Next steps:")
        print("   1. Start your Flask backend: python backend/app.py")
        print("   2. Start your Next.js frontend: npm run dev")
        print("   3. Visit http://localhost:3000 to see your products")
    else:
        print("\n❌ Failed to create mock products")

if __name__ == "__main__":
    main()