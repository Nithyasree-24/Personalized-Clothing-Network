#!/usr/bin/env python3
"""
Test product detail API to see current data structure
"""
import requests
import json

def test_product_detail(product_id):
    """Test product detail endpoint"""
    try:
        url = f"http://localhost:5000/api/products/{product_id}"
        print(f"🔍 Testing product detail API: {url}")
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Success! Product data:")
            print(json.dumps(data, indent=2))
            
            if 'product' in data:
                product = data['product']
                print(f"\n📦 Product Summary:")
                print(f"   ID: {product.get('product_id')}")
                print(f"   Title: {product.get('title')}")
                print(f"   Price: ₹{product.get('price')}")
                print(f"   Description: {product.get('description', 'N/A')}")
                print(f"   Color: {product.get('color', 'N/A')}")
                print(f"   Size: {product.get('size', 'N/A')}")
                print(f"   Category: {product.get('category')}")
                print(f"   Gender: {product.get('gender')}")
        else:
            print(f"❌ Failed: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Test the product ID from the URL (151)
    test_product_detail("151")