"""
Test API endpoints to verify everything is working
"""
import requests
import json

API_URL = "http://localhost:5000/api"

def test_endpoint(name, url, method="GET", data=None):
    """Test a single endpoint"""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"URL: {url}")
    print(f"{'='*60}")
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=5)
        else:
            response = requests.post(url, json=data, timeout=5)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS")
            
            # Show relevant data
            if 'cached_products' in data:
                print(f"   Cached Products: {data['cached_products']}")
            elif 'products' in data:
                print(f"   Products Returned: {len(data['products'])}")
                if len(data['products']) > 0:
                    print(f"   First Product: {data['products'][0].get('title', 'N/A')[:50]}")
            elif 'count' in data:
                print(f"   Count: {data['count']}")
            
            return True
        else:
            print(f"❌ FAILED: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "="*60)
    print("API Endpoint Testing")
    print("="*60)
    
    tests = [
        ("Cache Count", f"{API_URL}/cache/count"),
        ("Usage Stats", f"{API_URL}/usage/stats"),
        ("Search Products (clothing)", f"{API_URL}/products/search?query=clothing&category=fashion"),
        ("Search Products (women)", f"{API_URL}/products/search?query=women&category=fashion"),
        ("Search Products (men)", f"{API_URL}/products/search?query=men&category=fashion"),
        ("Category Products (women)", f"{API_URL}/products/category/fashion?gender=women&limit=20"),
        ("Category Products (men)", f"{API_URL}/products/category/fashion?gender=men&limit=20"),
    ]
    
    passed = 0
    failed = 0
    
    for name, url in tests:
        if test_endpoint(name, url):
            passed += 1
        else:
            failed += 1
    
    print("\n" + "="*60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("="*60)
    
    if failed == 0:
        print("\n✅ All API endpoints are working correctly!")
        print("🌐 Frontend should be able to load products.")
        print("\nIf products still not showing:")
        print("  1. Check browser console for errors (F12)")
        print("  2. Check Network tab for failed requests")
        print("  3. Clear browser cache and hard refresh (Ctrl+Shift+R)")
        print("  4. Visit: http://localhost:3000/home")
    else:
        print("\n⚠️  Some endpoints failed. Check the errors above.")
