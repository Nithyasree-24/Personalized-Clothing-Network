#!/usr/bin/env python3
"""
Test a few products to see their descriptions and colors
"""
import requests
import json

def test_products():
    """Test multiple products to see variety of data"""
    product_ids = ["151", "1", "2", "3", "50", "100"]
    
    print("🧪 Testing Product Data for Frontend Display")
    print("="*60)
    
    for product_id in product_ids:
        try:
            url = f"http://localhost:5000/api/products/{product_id}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if 'product' in data:
                    product = data['product']
                    print(f"\n📦 Product ID: {product_id}")
                    print(f"   Title: {product.get('title', 'N/A')[:50]}...")
                    print(f"   Color: {product.get('color', 'N/A')}")
                    print(f"   Size: {product.get('size', 'N/A')}")
                    print(f"   Category: {product.get('category', 'N/A')}")
                    print(f"   Price: ₹{product.get('price', 0)}")
                    print(f"   Stock: {product.get('stock', 0)} units")
                    
                    # Show description preview
                    desc = product.get('description', '')
                    if desc:
                        desc_preview = desc.replace('\n', ' ').strip()[:100]
                        print(f"   Description: {desc_preview}...")
                    else:
                        print(f"   Description: No description available")
                    print("-" * 60)
            else:
                print(f"❌ Product {product_id}: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Product {product_id}: Error - {e}")
    
    print("\n🎉 Product data testing complete!")
    print("✅ Frontend should now display:")
    print("   • Actual product descriptions from database")
    print("   • Specific colors from database (not hardcoded)")
    print("   • Available sizes from database")
    print("   • Stock information")
    print("   • Product details section")

if __name__ == "__main__":
    test_products()