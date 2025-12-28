#!/usr/bin/env python3
"""
Create Comprehensive Product Database
Creates a large set of realistic fashion products for the e-commerce site
"""

import mysql.connector
import random
from datetime import datetime

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'fashiopulse'
}

def create_comprehensive_products():
    """Create a comprehensive set of fashion products"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Clear existing products
        cursor.execute("DELETE FROM products")
        conn.commit()
        print("🗑️  Cleared existing products")
        
        # Comprehensive product data
        products = []
        
        # Women's Products
        womens_products = [
            # Dresses
            {'title': 'Elegant Floral Summer Dress', 'price': 45.99, 'category': 'dress', 'image': 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400'},
            {'title': 'Black Evening Cocktail Dress', 'price': 79.99, 'category': 'dress', 'image': 'https://images.unsplash.com/photo-1566479179817-c0ae8e4b4b3d?w=400'},
            {'title': 'Casual Midi Wrap Dress', 'price': 52.99, 'category': 'dress', 'image': 'https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=400'},
            {'title': 'Bohemian Maxi Dress', 'price': 68.99, 'category': 'dress', 'image': 'https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=400'},
            {'title': 'Professional Sheath Dress', 'price': 89.99, 'category': 'dress', 'image': 'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=400'},
            
            # Tops & Blouses
            {'title': 'Casual White Cotton Blouse', 'price': 32.99, 'category': 'top', 'image': 'https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=400'},
            {'title': 'Silk Button-Up Shirt', 'price': 65.99, 'category': 'top', 'image': 'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=400'},
            {'title': 'Striped Long Sleeve Top', 'price': 28.99, 'category': 'top', 'image': 'https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=400'},
            {'title': 'Lace Trim Camisole', 'price': 24.99, 'category': 'top', 'image': 'https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=400'},
            {'title': 'Cropped Denim Jacket', 'price': 55.99, 'category': 'jacket', 'image': 'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=400'},
            
            # Bottoms
            {'title': 'High-Waisted Blue Jeans', 'price': 59.99, 'category': 'pants', 'image': 'https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=400'},
            {'title': 'Black Skinny Fit Jeans', 'price': 54.99, 'category': 'pants', 'image': 'https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=400'},
            {'title': 'Wide Leg Trousers', 'price': 72.99, 'category': 'pants', 'image': 'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=400'},
            {'title': 'Pleated Mini Skirt', 'price': 38.99, 'category': 'skirt', 'image': 'https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=400'},
            {'title': 'A-Line Midi Skirt', 'price': 42.99, 'category': 'skirt', 'image': 'https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=400'},
            
            # Shoes
            {'title': 'Classic Black Heels', 'price': 89.99, 'category': 'shoes', 'image': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400'},
            {'title': 'White Leather Sneakers', 'price': 75.99, 'category': 'shoes', 'image': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400'},
            {'title': 'Ankle Boots', 'price': 95.99, 'category': 'shoes', 'image': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400'},
            {'title': 'Ballet Flats', 'price': 45.99, 'category': 'shoes', 'image': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400'},
            {'title': 'Strappy Sandals', 'price': 52.99, 'category': 'shoes', 'image': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400'},
        ]
        
        # Men's Products
        mens_products = [
            # Shirts
            {'title': 'Classic White Dress Shirt', 'price': 42.99, 'category': 'shirt', 'image': 'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400'},
            {'title': 'Blue Oxford Button-Down', 'price': 38.99, 'category': 'shirt', 'image': 'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400'},
            {'title': 'Striped Casual Shirt', 'price': 35.99, 'category': 'shirt', 'image': 'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400'},
            {'title': 'Flannel Plaid Shirt', 'price': 45.99, 'category': 'shirt', 'image': 'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400'},
            {'title': 'Polo Shirt Navy', 'price': 29.99, 'category': 'shirt', 'image': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400'},
            
            # T-Shirts
            {'title': 'Basic White T-Shirt', 'price': 19.99, 'category': 'tshirt', 'image': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400'},
            {'title': 'Graphic Print Tee', 'price': 24.99, 'category': 'tshirt', 'image': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400'},
            {'title': 'V-Neck Cotton Tee', 'price': 22.99, 'category': 'tshirt', 'image': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400'},
            {'title': 'Long Sleeve Henley', 'price': 32.99, 'category': 'tshirt', 'image': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400'},
            
            # Pants
            {'title': 'Dark Blue Slim Fit Jeans', 'price': 65.99, 'category': 'pants', 'image': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400'},
            {'title': 'Black Chino Pants', 'price': 49.99, 'category': 'pants', 'image': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400'},
            {'title': 'Khaki Cargo Pants', 'price': 55.99, 'category': 'pants', 'image': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400'},
            {'title': 'Straight Leg Jeans', 'price': 59.99, 'category': 'pants', 'image': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400'},
            {'title': 'Dress Pants Charcoal', 'price': 75.99, 'category': 'pants', 'image': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400'},
            
            # Outerwear
            {'title': 'Black Leather Biker Jacket', 'price': 125.99, 'category': 'jacket', 'image': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400'},
            {'title': 'Navy Blue Blazer', 'price': 89.99, 'category': 'jacket', 'image': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400'},
            {'title': 'Denim Jacket', 'price': 65.99, 'category': 'jacket', 'image': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400'},
            {'title': 'Wool Peacoat', 'price': 145.99, 'category': 'jacket', 'image': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400'},
            {'title': 'Casual Hoodie', 'price': 39.99, 'category': 'hoodie', 'image': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400'},
            
            # Shoes
            {'title': 'Brown Leather Dress Shoes', 'price': 89.99, 'category': 'shoes', 'image': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400'},
            {'title': 'White Canvas Sneakers', 'price': 65.99, 'category': 'shoes', 'image': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400'},
            {'title': 'Black Combat Boots', 'price': 95.99, 'category': 'shoes', 'image': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400'},
            {'title': 'Casual Loafers', 'price': 75.99, 'category': 'shoes', 'image': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400'},
        ]
        
        # Kids Products
        kids_products = [
            # Girls
            {'title': 'Colorful Rainbow Dress', 'price': 34.99, 'category': 'dress', 'image': 'https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=400'},
            {'title': 'Pink Princess Dress', 'price': 39.99, 'category': 'dress', 'image': 'https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=400'},
            {'title': 'Denim Overall Dress', 'price': 32.99, 'category': 'dress', 'image': 'https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=400'},
            {'title': 'Floral Summer Top', 'price': 22.99, 'category': 'top', 'image': 'https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=400'},
            {'title': 'Unicorn Graphic Tee', 'price': 18.99, 'category': 'tshirt', 'image': 'https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=400'},
            
            # Boys
            {'title': 'Superhero Graphic T-Shirt', 'price': 19.99, 'category': 'tshirt', 'image': 'https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=400'},
            {'title': 'Striped Long Sleeve Shirt', 'price': 24.99, 'category': 'shirt', 'image': 'https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=400'},
            {'title': 'Dinosaur Print Hoodie', 'price': 29.99, 'category': 'hoodie', 'image': 'https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=400'},
            {'title': 'Cargo Shorts Khaki', 'price': 25.99, 'category': 'shorts', 'image': 'https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=400'},
            {'title': 'Denim Jeans Kids', 'price': 35.99, 'category': 'pants', 'image': 'https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=400'},
            
            # Unisex Kids
            {'title': 'Colorful Sneakers', 'price': 39.99, 'category': 'shoes', 'image': 'https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=400'},
            {'title': 'Winter Puffer Jacket', 'price': 54.99, 'category': 'jacket', 'image': 'https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=400'},
            {'title': 'School Backpack', 'price': 29.99, 'category': 'accessory', 'image': 'https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=400'},
        ]
        
        # Brands for variety
        brands = ['Fashion Co', 'Style Plus', 'Urban Fit', 'Denim Works', 'Business Attire', 
                 'Leather Craft', 'Kids Fashion', 'Hero Kids', 'Trendy Wear', 'Classic Style',
                 'Modern Look', 'Comfort Zone', 'Elite Fashion', 'Street Style', 'Casual Chic']
        
        # Process women's products
        for i, product in enumerate(womens_products):
            product_id = f"women_{i+1:03d}"
            rating = round(random.uniform(3.8, 4.9), 1)
            reviews = random.randint(25, 300)
            brand = random.choice(brands)
            
            products.append({
                'id': product_id,
                'title': product['title'],
                'price': product['price'],
                'imageUrl': product['image'],
                'category': 'fashion',
                'gender': 'women',
                'description': f"High quality {product['title'].lower()} perfect for any occasion. Made with premium materials for comfort and style.",
                'rating': rating,
                'reviews_count': reviews,
                'brand': brand,
                'source': 'comprehensive'
            })
        
        # Process men's products
        for i, product in enumerate(mens_products):
            product_id = f"men_{i+1:03d}"
            rating = round(random.uniform(3.7, 4.8), 1)
            reviews = random.randint(20, 250)
            brand = random.choice(brands)
            
            products.append({
                'id': product_id,
                'title': product['title'],
                'price': product['price'],
                'imageUrl': product['image'],
                'category': 'fashion',
                'gender': 'men',
                'description': f"Premium {product['title'].lower()} designed for modern men. Combines style with functionality.",
                'rating': rating,
                'reviews_count': reviews,
                'brand': brand,
                'source': 'comprehensive'
            })
        
        # Process kids products
        for i, product in enumerate(kids_products):
            product_id = f"kids_{i+1:03d}"
            rating = round(random.uniform(4.0, 4.9), 1)
            reviews = random.randint(15, 150)
            brand = random.choice(['Kids Fashion', 'Hero Kids', 'Little Style', 'Fun Wear', 'Tiny Trends'])
            
            products.append({
                'id': product_id,
                'title': product['title'],
                'price': product['price'],
                'imageUrl': product['image'],
                'category': 'fashion',
                'gender': 'kids',
                'description': f"Fun and comfortable {product['title'].lower()} for kids. Safe materials and vibrant designs.",
                'rating': rating,
                'reviews_count': reviews,
                'brand': brand,
                'source': 'comprehensive'
            })
        
        # Insert all products
        insert_sql = """
        INSERT INTO products 
        (id, title, price, imageUrl, category, gender, description, rating, 
         reviews_count, brand, source, cached_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        for product in products:
            cursor.execute(insert_sql, (
                product['id'],
                product['title'],
                product['price'],
                product['imageUrl'],
                product['category'],
                product['gender'],
                product['description'],
                product['rating'],
                product['reviews_count'],
                product['brand'],
                product['source'],
                datetime.now()
            ))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✅ Successfully created {len(products)} comprehensive products!")
        
        # Print summary
        women_count = len(womens_products)
        men_count = len(mens_products)
        kids_count = len(kids_products)
        
        print(f"\n📊 Product Summary:")
        print(f"   Women's products: {women_count}")
        print(f"   Men's products: {men_count}")
        print(f"   Kids products: {kids_count}")
        print(f"   Total products: {len(products)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating comprehensive products: {e}")
        return False

def verify_database():
    """Verify the products in database"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # Count products by gender
        cursor.execute("SELECT gender, COUNT(*) as count FROM products GROUP BY gender")
        gender_counts = cursor.fetchall()
        
        # Get total count
        cursor.execute("SELECT COUNT(*) as total FROM products")
        total = cursor.fetchone()['total']
        
        # Get sample products from each gender
        cursor.execute("SELECT id, title, price, gender FROM products ORDER BY gender, id LIMIT 15")
        samples = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        print(f"\n📊 Database Verification:")
        print(f"   Total products: {total}")
        print(f"   By gender:")
        for item in gender_counts:
            print(f"     {item['gender']}: {item['count']} products")
        
        print(f"\n📝 Sample products:")
        for product in samples:
            print(f"   {product['id']}: {product['title'][:35]}... (${product['price']}) - {product['gender']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verifying database: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Creating Comprehensive Fashion Product Database")
    print("=" * 55)
    
    if create_comprehensive_products():
        verify_database()
        
        print("\n" + "=" * 55)
        print("🎉 Comprehensive product database created successfully!")
        print("\n📊 Next steps:")
        print("   1. Open phpMyAdmin: http://localhost/phpmyadmin")
        print("   2. Check 'fashiopulse' database -> 'products' table")
        print("   3. Restart Flask backend: python backend/app.py")
        print("   4. Test API: curl http://localhost:5000/api/products/search?query=clothing")
        print("   5. Start frontend and browse products")
        print("   6. Test Avatar Builder with new products")
    else:
        print("\n❌ Failed to create comprehensive products")

if __name__ == "__main__":
    main()