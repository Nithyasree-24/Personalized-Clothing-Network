#!/usr/bin/env python3
"""
Create Realistic Clothing Database
Creates a comprehensive database of realistic clothing products with Amazon-like structure
"""

import mysql.connector
import random
import json
from datetime import datetime
import hashlib

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'fashiopulse'
}

def create_realistic_clothing_products():
    """Create realistic clothing products with Amazon-like data"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Clear existing products
        cursor.execute("DELETE FROM products")
        conn.commit()
        print("🗑️  Cleared existing products")
        
        # Realistic clothing data with Amazon-style information
        clothing_products = []
        
        # Women's Clothing
        womens_items = [
            # Dresses
            {
                'title': 'PRETTYGARDEN Women\'s Summer Wrap Maxi Dress Casual V Neck Short Sleeve',
                'price': 32.99,
                'brand': 'PRETTYGARDEN',
                'category': 'dress',
                'image': 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400',
                'description': 'Lightweight summer maxi dress with wrap design, perfect for casual occasions',
                'asin': 'B08XQJK9M7'
            },
            {
                'title': 'Lark & Ro Women\'s Classic Long Sleeve Wrap Dress',
                'price': 45.99,
                'brand': 'Lark & Ro',
                'category': 'dress',
                'image': 'https://images.unsplash.com/photo-1566479179817-c0ae8e4b4b3d?w=400',
                'description': 'Elegant wrap dress suitable for work and evening occasions',
                'asin': 'B07XQJK8N6'
            },
            {
                'title': 'Floerns Women\'s Floral Print Short Sleeve A Line Swing Dress',
                'price': 28.99,
                'brand': 'Floerns',
                'category': 'dress',
                'image': 'https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=400',
                'description': 'Cute floral A-line dress with short sleeves, perfect for spring and summer',
                'asin': 'B08YQJK7L5'
            },
            
            # Tops & Blouses
            {
                'title': 'Amazon Essentials Women\'s Classic-Fit Long-Sleeve Crewneck T-Shirt',
                'price': 12.99,
                'brand': 'Amazon Essentials',
                'category': 'top',
                'image': 'https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=400',
                'description': 'Basic long-sleeve crewneck tee in soft cotton blend',
                'asin': 'B07MQJK6P4'
            },
            {
                'title': 'ANRABESS Women Casual Batwing Sleeve Loose Plain Maxi Dresses',
                'price': 24.99,
                'brand': 'ANRABESS',
                'category': 'top',
                'image': 'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=400',
                'description': 'Comfortable loose-fit top with batwing sleeves',
                'asin': 'B08RQJK5M3'
            },
            {
                'title': 'Hanes Women\'s V-Neck T-Shirt, Cotton Tee for Women',
                'price': 8.99,
                'brand': 'Hanes',
                'category': 'top',
                'image': 'https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=400',
                'description': 'Classic cotton V-neck tee, available in multiple colors',
                'asin': 'B01NQJK4R2'
            },
            
            # Bottoms
            {
                'title': 'Levi\'s Women\'s 711 Skinny Jeans',
                'price': 59.99,
                'brand': 'Levi\'s',
                'category': 'pants',
                'image': 'https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=400',
                'description': 'Classic skinny fit jeans with stretch for comfort',
                'asin': 'B01PQJK3N1'
            },
            {
                'title': 'Lee Women\'s Relaxed Fit Straight Leg Jean',
                'price': 34.99,
                'brand': 'Lee',
                'category': 'pants',
                'image': 'https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=400',
                'description': 'Comfortable straight leg jeans with relaxed fit',
                'asin': 'B07SQJK2M8'
            },
            {
                'title': 'GRACE KARIN Women High Waist Pleated A-Line Midi Skirt',
                'price': 22.99,
                'brand': 'GRACE KARIN',
                'category': 'skirt',
                'image': 'https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=400',
                'description': 'Elegant pleated midi skirt with high waist design',
                'asin': 'B08TQJK1L7'
            },
            
            # Shoes
            {
                'title': 'Adidas Women\'s Cloudfoam Pure Running Shoe',
                'price': 65.99,
                'brand': 'Adidas',
                'category': 'shoes',
                'image': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400',
                'description': 'Comfortable running shoes with cloudfoam cushioning',
                'asin': 'B07UQJK0K6'
            },
            {
                'title': 'Steve Madden Women\'s Daisie Pump',
                'price': 79.99,
                'brand': 'Steve Madden',
                'category': 'shoes',
                'image': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400',
                'description': 'Classic pointed toe pump with block heel',
                'asin': 'B08VQJK9J5'
            }
        ]
        
        # Men's Clothing
        mens_items = [
            # Shirts
            {
                'title': 'Amazon Essentials Men\'s Regular-Fit Long-Sleeve Solid Oxford Shirt',
                'price': 18.99,
                'brand': 'Amazon Essentials',
                'category': 'shirt',
                'image': 'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400',
                'description': 'Classic oxford shirt in regular fit, perfect for business casual',
                'asin': 'B06WQJK8H4'
            },
            {
                'title': 'Goodthreads Men\'s Standard-Fit Short-Sleeve Chambray Shirt',
                'price': 25.99,
                'brand': 'Goodthreads',
                'category': 'shirt',
                'image': 'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400',
                'description': 'Casual chambray shirt with standard fit and short sleeves',
                'asin': 'B07RQJK7G3'
            },
            {
                'title': 'Van Heusen Men\'s Dress Shirt Regular Fit Flex Collar Stretch',
                'price': 32.99,
                'brand': 'Van Heusen',
                'category': 'shirt',
                'image': 'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400',
                'description': 'Professional dress shirt with flex collar and stretch fabric',
                'asin': 'B08SQJK6F2'
            },
            
            # T-Shirts
            {
                'title': 'Hanes Men\'s Short Sleeve Beefy-T',
                'price': 7.99,
                'brand': 'Hanes',
                'category': 'tshirt',
                'image': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400',
                'description': 'Classic heavyweight cotton t-shirt, pre-shrunk',
                'asin': 'B00MQJK5E1'
            },
            {
                'title': 'Gildan Men\'s Heavy Cotton T-Shirt, Style G5000',
                'price': 5.99,
                'brand': 'Gildan',
                'category': 'tshirt',
                'image': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400',
                'description': 'Heavy cotton t-shirt with seamless collar',
                'asin': 'B077QJKD0'
            },
            
            # Pants
            {
                'title': 'Levi\'s Men\'s 511 Slim Jeans',
                'price': 49.99,
                'brand': 'Levi\'s',
                'category': 'pants',
                'image': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400',
                'description': 'Slim fit jeans with slight stretch for comfort',
                'asin': 'B00PQJKC9'
            },
            {
                'title': 'Dockers Men\'s Alpha Khaki Slim Tapered Flat Front Pant',
                'price': 39.99,
                'brand': 'Dockers',
                'category': 'pants',
                'image': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400',
                'description': 'Slim tapered khaki pants with flat front design',
                'asin': 'B07TQJKB8'
            },
            {
                'title': 'Wrangler Authentics Men\'s Classic Relaxed Fit Jean',
                'price': 24.99,
                'brand': 'Wrangler',
                'category': 'pants',
                'image': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400',
                'description': 'Classic relaxed fit jeans with authentic styling',
                'asin': 'B08UQJKA7'
            },
            
            # Outerwear
            {
                'title': 'Amazon Essentials Men\'s Lightweight Water-Resistant Packable Puffer Jacket',
                'price': 45.99,
                'brand': 'Amazon Essentials',
                'category': 'jacket',
                'image': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400',
                'description': 'Lightweight packable puffer jacket, water-resistant',
                'asin': 'B07VQJK96'
            },
            {
                'title': 'Carhartt Men\'s Loose Fit Heavyweight Long-Sleeve Pocket T-Shirt',
                'price': 19.99,
                'brand': 'Carhartt',
                'category': 'hoodie',
                'image': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400',
                'description': 'Heavy-duty long sleeve pocket tee for work and casual wear',
                'asin': 'B08WQJK85'
            },
            
            # Shoes
            {
                'title': 'Nike Men\'s Air Monarch IV Cross Trainer',
                'price': 64.99,
                'brand': 'Nike',
                'category': 'shoes',
                'image': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400',
                'description': 'Classic cross training shoe with durable leather upper',
                'asin': 'B00XQJK74'
            },
            {
                'title': 'Clarks Men\'s Desert Boot Chukka Boot',
                'price': 89.99,
                'brand': 'Clarks',
                'category': 'shoes',
                'image': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400',
                'description': 'Classic desert boot with suede upper and crepe sole',
                'asin': 'B09YQJK63'
            }
        ]
        
        # Kids Clothing
        kids_items = [
            {
                'title': 'Simple Joys by Carter\'s Girls\' 3-Pack Short-Sleeve Tee',
                'price': 12.99,
                'brand': 'Simple Joys by Carter\'s',
                'category': 'tshirt',
                'image': 'https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=400',
                'description': 'Pack of 3 colorful t-shirts for girls, 100% cotton',
                'asin': 'B07ZQJK52'
            },
            {
                'title': 'Amazon Essentials Boys\' Fleece Pullover Hoodie',
                'price': 16.99,
                'brand': 'Amazon Essentials',
                'category': 'hoodie',
                'image': 'https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=400',
                'description': 'Comfortable fleece hoodie for boys, perfect for layering',
                'asin': 'B08AQJK41'
            },
            {
                'title': 'Levi\'s Kids\' 511 Slim Fit Jeans',
                'price': 29.99,
                'brand': 'Levi\'s',
                'category': 'pants',
                'image': 'https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=400',
                'description': 'Kids version of the classic 511 slim fit jeans',
                'asin': 'B09BQJK30'
            },
            {
                'title': 'Disney Girls\' Frozen Elsa Dress Up Costume',
                'price': 24.99,
                'brand': 'Disney',
                'category': 'dress',
                'image': 'https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=400',
                'description': 'Official Disney Frozen Elsa costume dress for girls',
                'asin': 'B08CQJK29'
            },
            {
                'title': 'Converse Kids\' Chuck Taylor All Star Low Top Sneaker',
                'price': 35.99,
                'brand': 'Converse',
                'category': 'shoes',
                'image': 'https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=400',
                'description': 'Classic Chuck Taylor sneakers sized for kids',
                'asin': 'B07DQJK18'
            }
        ]
        
        # Process all items
        all_items = []
        
        # Add women's items
        for item in womens_items:
            item['gender'] = 'women'
            all_items.append(item)
        
        # Add men's items  
        for item in mens_items:
            item['gender'] = 'men'
            all_items.append(item)
            
        # Add kids items
        for item in kids_items:
            item['gender'] = 'kids'
            all_items.append(item)
        
        # Generate additional variations
        expanded_items = []
        colors = ['Black', 'White', 'Navy', 'Gray', 'Blue', 'Red', 'Green', 'Pink', 'Purple', 'Brown']
        sizes = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
        
        for base_item in all_items:
            # Add base item
            expanded_items.append(base_item.copy())
            
            # Add 2-3 color variations
            for i, color in enumerate(random.sample(colors, 3)):
                if i >= 2:  # Limit to 2 additional variations
                    break
                    
                variant = base_item.copy()
                variant['title'] = f"{base_item['title']} - {color}"
                variant['asin'] = f"{base_item['asin']}__{color.lower()}"
                variant['price'] = round(base_item['price'] + random.uniform(-5, 10), 2)
                expanded_items.append(variant)
        
        # Save to database
        insert_sql = """
        INSERT INTO products 
        (id, title, price, imageUrl, category, gender, description, rating, 
         reviews_count, brand, source, asin, sizes, colors, cached_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        saved_count = 0
        for i, item in enumerate(expanded_items):
            try:
                product_id = item['asin'] or f"clothing_{i+1:04d}"
                
                # Generate realistic ratings and reviews
                rating = round(random.uniform(3.5, 4.9), 1)
                reviews = random.randint(10, 2500)
                
                # Generate sizes and colors JSON
                available_sizes = json.dumps(random.sample(sizes, random.randint(3, 6)))
                available_colors = json.dumps(random.sample(colors, random.randint(2, 5)))
                
                cursor.execute(insert_sql, (
                    product_id,
                    item['title'],
                    item['price'],
                    item['image'],
                    'fashion',
                    item['gender'],
                    item['description'],
                    rating,
                    reviews,
                    item['brand'],
                    'amazon_realistic',
                    item['asin'],
                    available_sizes,
                    available_colors,
                    datetime.now()
                ))
                
                saved_count += 1
                
                if saved_count % 20 == 0:
                    print(f"   💾 Saved {saved_count} products...")
                
            except Exception as e:
                print(f"   ⚠️  Error saving product {i}: {e}")
                continue
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"\n🎉 Successfully created {saved_count} realistic clothing products!")
        
        return saved_count > 0
        
    except Exception as e:
        print(f"❌ Error creating realistic clothing products: {e}")
        return False

def verify_clothing_database():
    """Verify the clothing database"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # Get counts
        cursor.execute("SELECT COUNT(*) as total FROM products")
        total = cursor.fetchone()['total']
        
        cursor.execute("SELECT gender, COUNT(*) as count FROM products GROUP BY gender")
        gender_counts = cursor.fetchall()
        
        cursor.execute("SELECT brand, COUNT(*) as count FROM products GROUP BY brand ORDER BY count DESC LIMIT 10")
        brand_counts = cursor.fetchall()
        
        cursor.execute("SELECT MIN(price) as min_price, MAX(price) as max_price, AVG(price) as avg_price FROM products")
        price_stats = cursor.fetchone()
        
        # Sample products
        cursor.execute("SELECT id, title, price, gender, brand FROM products ORDER BY RAND() LIMIT 8")
        samples = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        print(f"\n📊 Realistic Clothing Database Verification:")
        print(f"   Total products: {total}")
        print(f"   Price range: ${price_stats['min_price']:.2f} - ${price_stats['max_price']:.2f}")
        print(f"   Average price: ${price_stats['avg_price']:.2f}")
        
        print(f"\n👥 By gender:")
        for item in gender_counts:
            print(f"     {item['gender']}: {item['count']} items")
        
        print(f"\n🏷️  Top brands:")
        for brand in brand_counts:
            print(f"     {brand['brand']}: {brand['count']} items")
        
        print(f"\n🛍️  Sample products:")
        for product in samples:
            print(f"   {product['title'][:50]}... (${product['price']}) - {product['gender']} - {product['brand']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verifying database: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Creating Realistic Amazon-Style Clothing Database")
    print("=" * 55)
    print("🎯 Creating clothing products with real brand names")
    print("🔄 Including size and color variations")
    print("💾 Saving to phpMyAdmin database")
    print("=" * 55)
    
    if create_realistic_clothing_products():
        verify_clothing_database()
        
        print("\n" + "=" * 55)
        print("🎉 Realistic clothing database created successfully!")
        print("\n📊 Features:")
        print("   ✅ Real brand names (Nike, Adidas, Levi's, etc.)")
        print("   ✅ Authentic product titles and descriptions")
        print("   ✅ Realistic pricing ($5.99 - $89.99)")
        print("   ✅ Size and color variations")
        print("   ✅ Amazon-style ASINs")
        print("   ✅ Gender-specific categorization")
        
        print("\n📊 Next steps:")
        print("   1. Check phpMyAdmin: http://localhost/phpmyadmin")
        print("   2. View 'fashiopulse' → 'products' table")
        print("   3. Restart Flask backend: python backend/app.py")
        print("   4. Test API endpoints")
        print("   5. Browse products in frontend")
        print("   6. Use in Avatar Builder")
    else:
        print("\n❌ Failed to create realistic clothing database")

if __name__ == "__main__":
    main()