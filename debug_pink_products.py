#!/usr/bin/env python3
"""
Debug Pink Products Issue
"""
import requests
import json

def test_pink_products():
    print("🔍 Debugging Pink Products Issue")
    print("=" * 50)
    
    # Test what products are available for pink women tops
    print("Testing Pink Women Tops search...")
    response = requests.post('http://localhost:5001/api/chat', json={
        'message': json.dumps({
            'type': 'faceToneFlow',
            'color': 'pink',
            'gender': 'women',
            'category': 'Tops and Co-ord Sets'
        })
    })
    
    if response.status_code == 200:
        data = response.json()
        products = data.get('products', [])
        print(f"Found {len(products)} products for Pink + Women + Tops and Co-ord Sets")
        
        if products:
            for i, product in enumerate(products[:5]):
                print(f"{i+1}. {product['product_name']}")
                print(f"   Color: {product['color']}")
                print(f"   Category: {product['product_category']}")
                print(f"   Gender: {product['gender']}")
                print()
        else:
            print("❌ No products found!")
    else:
        print(f"❌ API Error: {response.status_code}")
        print(response.text)
    
    # Test general pink products
    print("\n" + "=" * 50)
    print("Testing general Pink products...")
    response = requests.post('http://localhost:5001/api/chat', json={
        'message': 'show me pink clothes'
    })
    
    if response.status_code == 200:
        data = response.json()
        products = data.get('products', [])
        print(f"Found {len(products)} general pink products")
        
        if products:
            for i, product in enumerate(products[:3]):
                print(f"{i+1}. {product['product_name']} - {product['color']}")
    
    # Test database directly
    print("\n" + "=" * 50)
    print("Testing database connection...")
    try:
        import sys
        sys.path.append('chat_agent')
        from database import DatabaseHandler
        
        db = DatabaseHandler()
        if db.connect():
            print("✅ Database connected")
            
            # Search for pink products
            pink_products = db.search_products(color='pink', limit=5)
            print(f"Direct DB search found {len(pink_products)} pink products")
            
            # Search for women products
            women_products = db.search_products(gender='women', limit=5)
            print(f"Direct DB search found {len(women_products)} women products")
            
            # Search for tops
            tops_products = db.search_products(category='Tops and Co-ord Sets', limit=5)
            print(f"Direct DB search found {len(tops_products)} tops products")
            
            # Combined search
            combined = db.search_products(color='pink', gender='women', category='Tops and Co-ord Sets', limit=5)
            print(f"Combined search found {len(combined)} products")
            
            if combined:
                print("Combined search results:")
                for product in combined:
                    print(f"  - {product['product_name']} ({product['color']}, {product['gender']}, {product['product_category']})")
            
        else:
            print("❌ Database connection failed")
            
    except Exception as e:
        print(f"❌ Database test error: {e}")

if __name__ == "__main__":
    test_pink_products()