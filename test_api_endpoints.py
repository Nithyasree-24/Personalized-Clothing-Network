#!/usr/bin/env python3
"""
Test API endpoints to ensure backend is working
"""
import requests
import json
import time

def test_endpoint(url, description):
    """Test a single API endpoint"""
    try:
        print(f"🔍 Testing: {description}")
        print(f"📍 URL: {url}")
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'products' in data:
                count = len(data['products'])
                print(f"✅ Success! Found {count} products")
                
                # Show sample product
                if count > 0:
                    sample = data['products'][0]
                    print(f"   📦 Sample: {sample.get('title', 'N/A')[:50]} - ₹{sample.get('price', 0)}")
            else:
                print(f"✅ Success! Response: {str(data)[:100]}")
        else:
            print(f"❌ Failed: HTTP {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection Error: Backend server not running")
    except requests.exceptions.Timeout:
        print(f"❌ Timeout: Server took too long to respond")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("-" * 60)

def main():
    """Test all API endpoints"""
    print("🧪 FashionPulse API Endpoint Tests")
    print("="*60)
    
    base_url = "http://localhost:5000/api"
    
    # Test endpoints
    endpoints = [
        (f"{base_url}/products/search?query=clothing", "Search all products"),
        (f"{base_url}/products/category/fashion", "Get fashion products"),
        (f"{base_url}/products/category/women", "Get women's products"),
        (f"{base_url}/products/category/men", "Get men's products"),
        (f"{base_url}/cache/count", "Get product count"),
        (f"{base_url}/usage/stats", "Get usage statistics"),
    ]
    
    print("⏳ Starting tests in 3 seconds...")
    time.sleep(3)
    
    for url, description in endpoints:
        test_endpoint(url, description)
        time.sleep(1)  # Small delay between requests
    
    print("🎉 API testing complete!")
    print("\n📋 If all tests passed:")
    print("1. Your backend is working correctly")
    print("2. Database connection is successful") 
    print("3. Frontend should be able to fetch products")
    print("\n🚀 Start frontend with: npm run dev")

if __name__ == "__main__":
    main()