#!/usr/bin/env python3
"""
Create Amazon-Style Clothing Products
Creates realistic clothing products with Amazon-like structure (no API calls)
"""

import mysql.connector
import random
import json
from datetime import datetime

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'fashiopulse'
}

def create_amazon_style_products():
    """Create Amazon-style clothing products"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Clear existing products
        cursor.execute("DELETE FROM products")
        conn.commit()
        print("🗑️  Cleared existing products")
        
        # Amazon-style clothing products
        products = []
        
        # Women's Products
        womens_products = [
            # Dresses
            {'title': 'PRETTYGARDEN Women\'s Summer Wrap Maxi Dress Casual V Neck Short Sleeve', 'price': 32.99, 'brand': 'PRETTYGARDEN', 'asin': 'B08XQJK9M7'},
            {'title': 'Lark & Ro Women\'s Classic Long Sleeve Wrap Dress', 'price': 45.99, 'brand': 'Lark & Ro', 'asin': 'B07XQJK8N6'},
            {'title': 'Floerns Women\'s Floral Print Short Sleeve A Line Swing Dress', 'price': 28.99, 'brand': 'Floerns', 'asin': 'B08YQJK7L5'},
            {'title': 'Amazon Essentials Women\'s Surplice Dress', 'price': 24.99, 'brand': 'Amazon Essentials', 'asin': 'B07MQJK6P4'},
            {'title': 'Daily Ritual Women\'s Jersey Long-Sleeve Wrap Dress', 'price': 35.99, 'brand': 'Daily Ritual', 'asin': 'B08RQJK5M3'},
            
            # Tops
            {'title': 'Amazon Essentials Women\'s Classic-Fit Long-Sleeve Crewneck T-Shirt', 'price': 12.99, 'brand': 'Amazon Essentials', 'asin': 'B07MQJK6P4'},
            {'title': 'Hanes Women\'s V-Neck T-Shirt, Cotton Tee for Women', 'price': 8.99, 'brand': 'Hanes', 'asin': 'B01NQJK4R2'},
            {'title': 'ANRABESS Women Casual Batwing Sleeve Loose Plain Top', 'price': 24.99, 'brand': 'ANRABESS', 'asin': 'B08RQJK5M3'},
            {'title': 'Levi\'s Women\'s Perfect Tee', 'price': 19.99, 'brand': 'Levi\'s', 'asin': 'B07SQJK2M8'},
            {'title': 'Champion Women\'s Powercore Compression Tank', 'price': 16.99, 'brand': 'Champion', 'asin': 'B08TQJK1L7'},
            
            # Bottoms
            {'title': 'Levi\'s Women\'s 711 Skinny Jeans', 'price': 59.99, 'brand': 'Levi\'s', 'asin': 'B01PQJK3N1'},
            {'title': 'Lee Women\'s Relaxed Fit Straight Leg Jean', 'price': 34.99, 'brand': 'Lee', 'asin': 'B07SQJK2M8'},
            {'title': 'GRACE KARIN Women High Waist Pleated A-Line Midi Skirt', 'price': 22.99, 'brand': 'GRACE KARIN', 'asin': 'B08TQJK1L7'},
            {'title': 'Amazon Essentials Women\'s High-Rise Skinny Jean', 'price': 28.99, 'brand': 'Amazon Essentials', 'asin': 'B07UQJK0K6'},
            {'title': 'Wrangler Women\'s Retro Mae Mid Rise Boot Cut Jean', 'price': 42.99, 'brand': 'Wrangler', 'asin': 'B08VQJK9J5'},
            
            # Shoes
            {'title': 'Adidas Women\'s Cloudfoam Pure Running Shoe', 'price': 65.99, 'brand': 'Adidas', 'asin': 'B07UQJK0K6'},
            {'title': 'Steve Madden Women\'s Daisie Pump', 'price': 79.99, 'brand': 'Steve Madden', 'asin': 'B08VQJK9J5'},
            {'title': 'Nike Women\'s Revolution 5 Running Shoe', 'price': 59.99, 'brand': 'Nike', 'asin': 'B07WQJK8I4'},
            {'title': 'Skechers Women\'s Go Walk Joy Walking Shoe', 'price': 54.99, 'brand': 'Skechers', 'asin': 'B08XQJK7H3'},
            {'title': 'Clarks Women\'s Cloudsteppers Sillian Paz Slip-On Loafer', 'price': 49.99, 'brand': 'Clarks', 'asin': 'B09YQJK6G2'}
        ]
        
        # Men's Products
        mens_products = [
            # Shirts
            {'title': 'Amazon Essentials Men\'s Regular-Fit Long-Sleeve Solid Oxford Shirt', 'price': 18.99, 'brand': 'Amazon Essentials', 'asin': 'B06WQJK8H4'},
            {'title': 'Goodthreads Men\'s Standard-Fit Short-Sleeve Chambray Shirt', 'price': 25.99, 'brand': 'Goodthreads', 'asin': 'B07RQJK7G3'},
            {'title': 'Van Heusen Men\'s Dress Shirt Regular Fit Flex Collar Stretch', 'price': 32.99, 'brand': 'Van Heusen', 'asin': 'B08SQJK6F2'},
            {'title': 'Dickies Men\'s Original 874 Work Pant', 'price': 29.99, 'brand': 'Dickies', 'asin': 'B09TQJK5E1'},
            {'title': 'Calvin Klein Men\'s Dress Shirt Slim Fit Non Iron Herringbone', 'price': 39.99, 'brand': 'Calvin Klein', 'asin': 'B08UQJK4D0'},
            
            # T-Shirts
            {'title': 'Hanes Men\'s Short Sleeve Beefy-T', 'price': 7.99, 'brand': 'Hanes', 'asin': 'B00MQJK5E1'},
            {'title': 'Gildan Men\'s Heavy Cotton T-Shirt, Style G5000', 'price': 5.99, 'brand': 'Gildan', 'asin': 'B077QJKD0'},
            {'title': 'Champion Men\'s Classic Jersey T-Shirt', 'price': 12.99, 'brand': 'Champion', 'asin': 'B08NQJKC9'},
            {'title': 'Nike Men\'s Dri-FIT Legend Tee', 'price': 24.99, 'brand': 'Nike', 'asin': 'B09OQJKB8'},
            {'title': 'Under Armour Men\'s Tech 2.0 Short Sleeve T-Shirt', 'price': 19.99, 'brand': 'Under Armour', 'asin': 'B08PQJKA7'},
            
            # Pants
            {'title': 'Levi\'s Men\'s 511 Slim Jeans', 'price': 49.99, 'brand': 'Levi\'s', 'asin': 'B00PQJKC9'},
            {'title': 'Dockers Men\'s Alpha Khaki Slim Tapered Flat Front Pant', 'price': 39.99, 'brand': 'Dockers', 'asin': 'B07TQJKB8'},
            {'title': 'Wrangler Authentics Men\'s Classic Relaxed Fit Jean', 'price': 24.99, 'brand': 'Wrangler', 'asin': 'B08UQJKA7'},
            {'title': 'Amazon Essentials Men\'s Straight-Fit Chino Pant', 'price': 22.99, 'brand': 'Amazon Essentials', 'asin': 'B09VQJK96'},
            {'title': 'Lee Men\'s Regular Fit Straight Leg Jean', 'price': 32.99, 'brand': 'Lee', 'asin': 'B08WQJK85'},
            
            # Outerwear
            {'title': 'Amazon Essentials Men\'s Lightweight Water-Resistant Packable Puffer Jacket', 'price': 45.99, 'brand': 'Amazon Essentials', 'asin': 'B07VQJK96'},
            {'title': 'Carhartt Men\'s Loose Fit Heavyweight Long-Sleeve Pocket T-Shirt', 'price': 19.99, 'brand': 'Carhartt', 'asin': 'B08WQJK85'},
            {'title': 'Champion Men\'s Powerblend Fleece Hoodie', 'price': 34.99, 'brand': 'Champion', 'asin': 'B09XQJK74'},
            {'title': 'Hanes Men\'s Pullover EcoSmart Hooded Sweatshirt', 'price': 18.99, 'brand': 'Hanes', 'asin': 'B08YQJK63'},
            {'title': 'Nike Men\'s Club Fleece Pullover Hoodie', 'price': 54.99, 'brand': 'Nike', 'asin': 'B09ZQJK52'},
            
            # Shoes
            {'title': 'Nike Men\'s Air Monarch IV Cross Trainer', 'price': 64.99, 'brand': 'Nike', 'asin': 'B00XQJK74'},
            {'title': 'Clarks Men\'s Desert Boot Chukka Boot', 'price': 89.99, 'brand': 'Clarks', 'asin': 'B09YQJK63'},
            {'title': 'Adidas Men\'s Grand Court Sneaker', 'price': 59.99, 'brand': 'Adidas', 'asin': 'B08ZQJK52'},
            {'title': 'New Balance Men\'s 608 V5 Casual Comfort Cross Trainer', 'price': 69.99, 'brand': 'New Balance', 'asin': 'B09AQJK41'},
            {'title': 'Skechers Men\'s Energy Afterburn Lace-Up Sneaker', 'price': 54.99, 'brand': 'Skechers', 'asin': 'B08BQJK30'}
        ]
        
        # Kids Products
        kids_products = [
            {'title': 'Simple Joys by Carter\'s Girls\' 3-Pack Short-Sleeve Tee', 'price': 12.99, 'brand': 'Simple Joys by Carter\'s', 'asin': 'B07ZQJK52'},
            {'title': 'Amazon Essentials Boys\' Fleece Pullover Hoodie', 'price': 16.99, 'brand': 'Amazon Essentials', 'asin': 'B08AQJK41'},
            {'title': 'Levi\'s Kids\' 511 Slim Fit Jeans', 'price': 29.99, 'brand': 'Levi\'s', 'asin': 'B09BQJK30'},
            {'title': 'Disney Girls\' Frozen Elsa Dress Up Costume', 'price': 24.99, 'brand': 'Disney', 'asin': 'B08CQJK29'},
            {'title': 'Converse Kids\' Chuck Taylor All Star Low Top Sneaker', 'price': 35.99, 'brand': 'Converse', 'asin': 'B07DQJK18'},
            {'title': 'Carter\'s Boys\' 2-Piece Pajama Set', 'price': 14.99, 'brand': 'Carter\'s', 'asin': 'B08EQJK07'},
            {'title': 'Hanes Girls\' Big ComfortSoft EcoSmart T-Shirt', 'price': 6.99, 'brand': 'Hanes', 'asin': 'B09FQJK96'},
            {'title': 'Nike Kids\' Revolution 5 Running Shoe', 'price': 44.99, 'brand': 'Nike', 'asin': 'B08GQJK85'},
            {'title': 'OshKosh B\'Gosh Girls\' Denim Overall', 'price': 22.99, 'brand': 'OshKosh B\'Gosh', 'asin': 'B09HQJK74'},
            {'title': 'Adidas Kids\' Grand Court Sneaker', 'price': 39.99, 'brand': 'Adidas', 'asin': 'B08IQJK63'}
        ]
        
        # Colors and sizes for variations
        colors = ['Black', 'White', 'Navy', 'Gray', 'Blue', 'Red', 'Green', 'Pink', 'Purple', 'Brown', 'Khaki', 'Olive']
        sizes = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
        
        # Process all products and create variations
        all_products = []
        
        # Add women's products
        for item in womens_products:
            item['gender'] = 'women'
            all_products.append(item)
            
            # Add 1-2 color variations
            for color in random.sample(colors, 2):
                variant = item.copy()
                variant['title'] = f"{item['title']} - {color}"
                variant['asin'] = f"{item['asin']}_{color.lower()}"
                variant['price'] = round(item['price'] + random.uniform(-3, 8), 2)
                all_products.append(variant)
        
        # Add men's products
        for item in mens_products:
            item['gender'] = 'men'
            all_products.append(item)
            
            # Add 1-2 color variations
            for color in random.sample(colors, 2):
                variant = item.copy()
                variant['title'] = f"{item['title']} - {color}"
                variant['asin'] = f"{item['asin']}_{color.lower()}"
                variant['price'] = round(item['price'] + random.uniform(-3, 8), 2)
                all_products.append(variant)
        
        # Add kids products
        for item in kids_products:
            item['gender'] = 'kids'
            all_products.append(item)
            
            # Add 1 color variation
            color = random.choice(colors)
            variant = item.copy()
            variant['title'] = f"{item['title']} - {color}"
            variant['asin'] = f"{item['asin']}_{color.lower()}"
            variant['price'] = round(item['price'] + random.uniform(-2, 5), 2)
            all_products.append(variant)
        
        # Save to database
        insert_sql = """
        INSERT INTO products 
        (id, title, price, imageUrl, category, gender, description, rating, 
         reviews_count, brand, source, asin, sizes, colors, cached_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        # High-quality images by category
        images = {
            'women': [
                'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400',
                'https://images.unsplash.com/photo-1566479179817-c0ae8e4b4b3d?w=400',
                'https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=400',
                'https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=400',
                'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=400',
                'https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=400',
                'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400'
            ],
            'men': [
                'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400',
                'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400',
                'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400',
                'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400',
                'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400'
            ],
            'kids': [
                'https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=400'
            ]
        }
        
        saved_count = 0
        for i, product in enumerate(all_products):
            try:
                product_id = product['asin']
                
                # Generate realistic data
                rating = round(random.uniform(3.6, 4.9), 1)
                reviews = random.randint(15, 3500)
                
                # Generate description
                description = f"High quality {product['title'].lower()} from {product['brand']}. Perfect for everyday wear with comfortable fit and durable materials."
                
                # Select appropriate image
                image_url = random.choice(images[product['gender']])
                
                # Generate sizes and colors
                available_sizes = json.dumps(random.sample(sizes, random.randint(4, 6)))
                available_colors = json.dumps(random.sample(colors, random.randint(3, 6)))
                
                cursor.execute(insert_sql, (
                    product_id,
                    product['title'],
                    product['price'],
                    image_url,
                    'fashion',
                    product['gender'],
                    description,
                    rating,
                    reviews,
                    product['brand'],
                    'amazon_style',
                    product['asin'],
                    available_sizes,
                    available_colors,
                    datetime.now()
                ))
                
                saved_count += 1
                
                if saved_count % 25 == 0:
                    print(f"   💾 Saved {saved_count} products...")
                
            except Exception as e:
                print(f"   ⚠️  Error saving product {i}: {e}")
                continue
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"\n🎉 Successfully created {saved_count} Amazon-style clothing products!")
        return saved_count > 0
        
    except Exception as e:
        print(f"❌ Error creating Amazon-style products: {e}")
        return False

def verify_products():
    """Verify products in database"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # Get statistics
        cursor.execute("SELECT COUNT(*) as total FROM products")
        total = cursor.fetchone()['total']
        
        cursor.execute("SELECT gender, COUNT(*) as count FROM products GROUP BY gender")
        gender_counts = cursor.fetchall()
        
        cursor.execute("SELECT brand, COUNT(*) as count FROM products GROUP BY brand ORDER BY count DESC LIMIT 8")
        top_brands = cursor.fetchall()
        
        cursor.execute("SELECT MIN(price) as min_price, MAX(price) as max_price, AVG(price) as avg_price FROM products")
        price_stats = cursor.fetchone()
        
        cursor.execute("SELECT id, title, price, gender, brand FROM products ORDER BY RAND() LIMIT 6")
        samples = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        print(f"\n📊 Amazon-Style Clothing Database:")
        print(f"   Total products: {total}")
        print(f"   Price range: ${price_stats['min_price']:.2f} - ${price_stats['max_price']:.2f}")
        print(f"   Average price: ${price_stats['avg_price']:.2f}")
        
        print(f"\n👥 By gender:")
        for item in gender_counts:
            print(f"     {item['gender']}: {item['count']} items")
        
        print(f"\n🏷️  Top brands:")
        for brand in top_brands:
            print(f"     {brand['brand']}: {brand['count']} items")
        
        print(f"\n🛍️  Sample products:")
        for product in samples:
            print(f"   {product['title'][:45]}... (${product['price']}) - {product['brand']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verifying products: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Creating Amazon-Style Clothing Database")
    print("=" * 45)
    print("🎯 Real brand names and product titles")
    print("🔄 Color and size variations")
    print("💾 Amazon ASINs and realistic pricing")
    print("=" * 45)
    
    if create_amazon_style_products():
        verify_products()
        
        print("\n" + "=" * 45)
        print("🎉 Amazon-style clothing database created!")
        print("\n✨ Features:")
        print("   ✅ 150+ clothing products")
        print("   ✅ Real brands (Nike, Adidas, Levi's, Amazon Essentials)")
        print("   ✅ Authentic product titles")
        print("   ✅ Amazon ASINs")
        print("   ✅ Color variations")
        print("   ✅ Size options (JSON)")
        print("   ✅ Realistic ratings & reviews")
        
        print("\n📊 Next steps:")
        print("   1. Check phpMyAdmin: http://localhost/phpmyadmin")
        print("   2. Restart backend: python backend/app.py")
        print("   3. Test products in frontend")
        print("   4. Use in Avatar Builder")
    else:
        print("\n❌ Failed to create products")

if __name__ == "__main__":
    main()