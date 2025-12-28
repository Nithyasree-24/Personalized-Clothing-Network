"""
Test script to verify eBay API connectivity and find valid product IDs for India
"""
import requests
import json
from config import Config

def test_ebay_product(product_id, country="india", country_code="in"):
    """Test fetching a single product from eBay API"""
    
    url = f"https://ebay32.p.rapidapi.com/product/{product_id}"
    
    headers = {
        "x-rapidapi-host": "ebay32.p.rapidapi.com",
        "x-rapidapi-key": Config.RAPIDAPI_KEY
    }
    
    params = {
        "country": country,
        "country_code": country_code
    }
    
    print(f"\n{'='*60}")
    print(f"Testing eBay Product ID: {product_id}")
    print(f"Country: {country} ({country_code})")
    print(f"{'='*60}")
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS! Product found:")
            print(f"   Title: {data.get('title', 'N/A')}")
            print(f"   Price: {data.get('price', 'N/A')}")
            print(f"   Item ID: {data.get('item_id', 'N/A')}")
            print(f"   URL: {data.get('url', 'N/A')}")
            print(f"\nFull Response:")
            print(json.dumps(data, indent=2))
            return True
        else:
            print(f"❌ FAILED: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_multiple_countries(product_id):
    """Test the same product ID across different countries"""
    countries = [
        ("india", "in"),
        ("united states", "us"),
        ("united kingdom", "gb"),
        ("germany", "de"),
    ]
    
    print(f"\n{'='*60}")
    print(f"Testing Product ID {product_id} across multiple countries")
    print(f"{'='*60}")
    
    for country, code in countries:
        test_ebay_product(product_id, country, code)
        print()

if __name__ == "__main__":
    print("eBay API Test Script")
    print("="*60)
    print(f"API Key: {Config.RAPIDAPI_KEY[:20]}...")
    
    # Test the example product ID from your curl command
    test_product_id = "195499451557"
    
    # Test with India first
    print("\n\n🇮🇳 Testing with India region:")
    test_ebay_product(test_product_id, "india", "in")
    
    # Test with other countries to see if the product exists
    print("\n\n🌍 Testing same product across different countries:")
    test_multiple_countries(test_product_id)
    
    print("\n\n" + "="*60)
    print("IMPORTANT NOTES:")
    print("="*60)
    print("1. eBay API does NOT have a /search endpoint")
    print("2. You can ONLY fetch products by specific product IDs")
    print("3. Product IDs are region-specific")
    print("4. To get valid India product IDs:")
    print("   - Visit https://www.ebay.in/")
    print("   - Search for products (e.g., 'women dress', 'men shirt')")
    print("   - Copy product IDs from URLs (e.g., /itm/PRODUCT_ID)")
    print("   - Add them to backend/ebay_product_ids.json")
    print("\n5. Alternative: Focus on Amazon API only (204 products working)")
    print("="*60)
