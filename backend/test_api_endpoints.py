#!/usr/bin/env python3
"""
Test API Endpoints
"""

import requests
import json

def test_endpoints():
    """Test various API endpoints"""
    base_url = "http://localhost:5000"
    
    endpoints = [
        "/api/products/search?query=clothing",
        "/api/products/search?query=women",
        "/api/products/search?query=men", 
        "/api/products/category/fashion",
        "/api/products/category/women",
        "/api/products/category/men",
        "/api/products/category/kids"
    ]
    
    for endpoint in endpoints:
        try:
            print(f"\n🔍 Testing: {endpoint}")
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                count = data.get('count', 0)
                print(f"   ✅ Status: {response.status_code}")
                print(f"   📦 Products: {count}")
                
                if count > 0:
                    # Show first product
                    products = data.get('products', [])
                    if products:
                        first = products[0]
                        print(f"   📝 Sample: {first.get('title', 'No title')[:40]}...")
                else:
                    print(f"   ⚠️  No products returned")
            else:
                print(f"   ❌ Status: {response.status_code}")
                print(f"   📄 Response: {response.text[:200]}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_endpoints()