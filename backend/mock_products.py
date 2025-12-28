#!/usr/bin/env python3
"""
Mock Products Generator
Creates sample products when database is not available
"""

import json
import random

def generate_mock_products():
    """Generate mock products for testing"""
    
    # Sample product data
    mock_products = [
        # Women's Products
        {
            "id": 1,
            "product_id": "W001",
            "title": "Women's Elegant Black Dress - Long Sleeve Midi Dress",
            "price": 1299,
            "image_url": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400",
            "category": "fashion",
            "gender": "women",
            "source": "mock",
            "product_url": "#",
            "rating": 4.5,
            "description": "Elegant black midi dress perfect for office or evening wear",
            "cached_at": "2024-12-10T08:00:00Z"
        },
        {
            "id": 2,
            "product_id": "W002",
            "title": "Women's Casual Blue Jeans - High Waist Skinny Fit",
            "price": 899,
            "image_url": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=400",
            "category": "fashion",
            "gender": "women",
            "source": "mock",
            "product_url": "#",
            "rating": 4.3,
            "description": "Comfortable high-waist skinny jeans in classic blue",
            "cached_at": "2024-12-10T08:00:00Z"
        },
        {
            "id": 3,
            "product_id": "W003",
            "title": "Women's White Cotton Blouse - Professional Office Wear",
            "price": 699,
            "image_url": "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=400",
            "category": "fashion",
            "gender": "women",
            "source": "mock",
            "product_url": "#",
            "rating": 4.7,
            "description": "Classic white cotton blouse perfect for professional settings",
            "cached_at": "2024-12-10T08:00:00Z"
        },
        {
            "id": 4,
            "product_id": "W004",
            "title": "Women's Pink Floral Summer Dress - Casual Day Wear",
            "price": 1099,
            "image_url": "https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=400",
            "category": "fashion",
            "gender": "women",
            "source": "mock",
            "product_url": "#",
            "rating": 4.4,
            "description": "Beautiful floral summer dress in soft pink tones",
            "cached_at": "2024-12-10T08:00:00Z"
        },
        
        # Men's Products
        {
            "id": 5,
            "product_id": "M001",
            "title": "Men's Navy Blue Formal Shirt - Cotton Blend Business Wear",
            "price": 799,
            "image_url": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400",
            "category": "fashion",
            "gender": "men",
            "source": "mock",
            "product_url": "#",
            "rating": 4.6,
            "description": "Professional navy blue shirt perfect for business meetings",
            "cached_at": "2024-12-10T08:00:00Z"
        },
        {
            "id": 6,
            "product_id": "M002",
            "title": "Men's Dark Wash Denim Jeans - Regular Fit Classic Style",
            "price": 1199,
            "image_url": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400",
            "category": "fashion",
            "gender": "men",
            "source": "mock",
            "product_url": "#",
            "rating": 4.5,
            "description": "Classic dark wash jeans with regular fit and comfort",
            "cached_at": "2024-12-10T08:00:00Z"
        },
        {
            "id": 7,
            "product_id": "M003",
            "title": "Men's Black Leather Jacket - Genuine Leather Biker Style",
            "price": 2499,
            "image_url": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400",
            "category": "fashion",
            "gender": "men",
            "source": "mock",
            "product_url": "#",
            "rating": 4.8,
            "description": "Premium black leather jacket with classic biker styling",
            "cached_at": "2024-12-10T08:00:00Z"
        },
        {
            "id": 8,
            "product_id": "M004",
            "title": "Men's White Cotton T-Shirt - Casual Everyday Comfort",
            "price": 499,
            "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400",
            "category": "fashion",
            "gender": "men",
            "source": "mock",
            "product_url": "#",
            "rating": 4.2,
            "description": "Comfortable white cotton t-shirt for everyday wear",
            "cached_at": "2024-12-10T08:00:00Z"
        },
        
        # Kids Products
        {
            "id": 9,
            "product_id": "K001",
            "title": "Kids Rainbow Striped T-Shirt - Colorful Cotton Tee",
            "price": 399,
            "image_url": "https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=400",
            "category": "fashion",
            "gender": "kids",
            "source": "mock",
            "product_url": "#",
            "rating": 4.6,
            "description": "Fun rainbow striped t-shirt perfect for active kids",
            "cached_at": "2024-12-10T08:00:00Z"
        },
        {
            "id": 10,
            "product_id": "K002",
            "title": "Kids Blue Denim Overalls - Comfortable Play Wear",
            "price": 699,
            "image_url": "https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=400",
            "category": "fashion",
            "gender": "kids",
            "source": "mock",
            "product_url": "#",
            "rating": 4.4,
            "description": "Durable denim overalls perfect for playtime",
            "cached_at": "2024-12-10T08:00:00Z"
        },
        {
            "id": 11,
            "product_id": "K003",
            "title": "Girls Pink Princess Dress - Party Wear with Sparkles",
            "price": 899,
            "image_url": "https://images.unsplash.com/photo-1518831959646-742c3a14ebf7?w=400",
            "category": "fashion",
            "gender": "kids",
            "source": "mock",
            "product_url": "#",
            "rating": 4.7,
            "description": "Beautiful pink princess dress with sparkly details",
            "cached_at": "2024-12-10T08:00:00Z"
        },
        {
            "id": 12,
            "product_id": "K004",
            "title": "Boys Superhero Graphic T-Shirt - Action Hero Design",
            "price": 449,
            "image_url": "https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=400",
            "category": "fashion",
            "gender": "kids",
            "source": "mock",
            "product_url": "#",
            "rating": 4.5,
            "description": "Cool superhero t-shirt that kids will love",
            "cached_at": "2024-12-10T08:00:00Z"
        },
        
        # Additional Women's Items
        {
            "id": 13,
            "product_id": "W005",
            "title": "Women's Red Evening Gown - Elegant Party Dress",
            "price": 1899,
            "image_url": "https://images.unsplash.com/photo-1566479179817-c0ae2b4a4b5e?w=400",
            "category": "fashion",
            "gender": "women",
            "source": "mock",
            "product_url": "#",
            "rating": 4.8,
            "description": "Stunning red evening gown for special occasions",
            "cached_at": "2024-12-10T08:00:00Z"
        },
        {
            "id": 14,
            "product_id": "W006",
            "title": "Women's Cozy Knit Sweater - Warm Winter Pullover",
            "price": 999,
            "image_url": "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=400",
            "category": "fashion",
            "gender": "women",
            "source": "mock",
            "product_url": "#",
            "rating": 4.6,
            "description": "Soft and warm knit sweater perfect for winter",
            "cached_at": "2024-12-10T08:00:00Z"
        },
        
        # Additional Men's Items
        {
            "id": 15,
            "product_id": "M005",
            "title": "Men's Gray Wool Suit Jacket - Professional Business Attire",
            "price": 2999,
            "image_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400",
            "category": "fashion",
            "gender": "men",
            "source": "mock",
            "product_url": "#",
            "rating": 4.9,
            "description": "Premium gray wool suit jacket for professional wear",
            "cached_at": "2024-12-10T08:00:00Z"
        },
        {
            "id": 16,
            "product_id": "M006",
            "title": "Men's Casual Hoodie - Comfortable Cotton Blend",
            "price": 899,
            "image_url": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400",
            "category": "fashion",
            "gender": "men",
            "source": "mock",
            "product_url": "#",
            "rating": 4.3,
            "description": "Comfortable hoodie perfect for casual wear",
            "cached_at": "2024-12-10T08:00:00Z"
        }
    ]
    
    return mock_products

def save_mock_products():
    """Save mock products to JSON file"""
    products = generate_mock_products()
    
    with open('fallback_products.json', 'w') as f:
        json.dump(products, f, indent=2)
    
    print(f"✅ Generated {len(products)} mock products")
    print("📁 Saved to fallback_products.json")
    return products

if __name__ == "__main__":
    save_mock_products()