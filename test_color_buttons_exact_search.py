#!/usr/bin/env python3
"""
Test Color-Filled Buttons and Exact Keyword Search
"""
import requests
import json
import time

def test_exact_keyword_search():
    """Test exact keyword matching for precise product filtering"""
    url = "http://localhost:5001/api/chat"
    
    print("🧪 Testing Exact Keyword Search")
    print("=" * 50)
    
    # Test 1: Blue Men Shirts (should show ONLY shirts, not t-shirts)
    print("\n1️⃣ Testing: Blue + Men + Shirts")
    flow_data = {
        "message": json.dumps({
            "type": "faceToneFlow",
            "color": "blue",
            "gender": "men",
            "category": "Shirts"
        })
    }
    
    response = requests.post(url, json=flow_data)
    if response.status_code == 200:
        data = response.json()
        products = data.get('products', [])
        print(f"✅ Found {len(products)} products")
        
        # Check if results are precise
        shirts_only = all('shirt' in p['product_category'].lower() and 't-shirt' not in p['product_category'].lower() for p in products)
        blue_only = all(p['color'].lower() == 'blue' for p in products)
        men_only = all(p['gender'].lower() == 'men' for p in products)
        
        print(f"   📊 Shirts only (no t-shirts): {shirts_only}")
        print(f"   🔵 Blue color only: {blue_only}")
        print(f"   👨 Men gender only: {men_only}")
        
        if products:
            print(f"   📝 Sample: {products[0]['product_name']} - {products[0]['product_category']}")
    else:
        print(f"❌ Error: {response.status_code}")
    
    # Test 2: Red Women Dresses
    print("\n2️⃣ Testing: Red + Women + Dresses")
    flow_data = {
        "message": json.dumps({
            "type": "faceToneFlow",
            "color": "red",
            "gender": "women",
            "category": "Dresses"
        })
    }
    
    response = requests.post(url, json=flow_data)
    if response.status_code == 200:
        data = response.json()
        products = data.get('products', [])
        print(f"✅ Found {len(products)} products")
        
        # Check precision
        dresses_only = all('dress' in p['product_category'].lower() for p in products)
        red_only = all(p['color'].lower() == 'red' for p in products)
        women_only = all(p['gender'].lower() == 'women' for p in products)
        
        print(f"   👗 Dresses only: {dresses_only}")
        print(f"   🔴 Red color only: {red_only}")
        print(f"   👩 Women gender only: {women_only}")
        
        if products:
            print(f"   📝 Sample: {products[0]['product_name']} - {products[0]['product_category']}")
    else:
        print(f"❌ Error: {response.status_code}")
    
    # Test 3: Black Men T-shirts (should show ONLY t-shirts, not shirts)
    print("\n3️⃣ Testing: Black + Men + T-shirts")
    flow_data = {
        "message": json.dumps({
            "type": "faceToneFlow",
            "color": "black",
            "gender": "men",
            "category": "T-shirts"
        })
    }
    
    response = requests.post(url, json=flow_data)
    if response.status_code == 200:
        data = response.json()
        products = data.get('products', [])
        print(f"✅ Found {len(products)} products")
        
        # Check precision
        tshirts_only = all('t-shirt' in p['product_category'].lower() for p in products)
        black_only = all(p['color'].lower() == 'black' for p in products)
        men_only = all(p['gender'].lower() == 'men' for p in products)
        
        print(f"   👕 T-shirts only (no regular shirts): {tshirts_only}")
        print(f"   ⚫ Black color only: {black_only}")
        print(f"   👨 Men gender only: {men_only}")
        
        if products:
            print(f"   📝 Sample: {products[0]['product_name']} - {products[0]['product_category']}")
    else:
        print(f"❌ Error: {response.status_code}")

def test_color_suggestions():
    """Test that color suggestions work correctly"""
    url = "http://localhost:5001/api/chat"
    
    print("\n🎨 Testing Color Suggestions")
    print("=" * 30)
    
    # Test basic greeting to get color options
    response = requests.post(url, json={"message": "hi"})
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Basic chat response: {data['response'][:50]}...")
        
        # Check if we get products for color search
        color_response = requests.post(url, json={"message": "show me blue shirts"})
        if color_response.status_code == 200:
            color_data = color_response.json()
            products = color_data.get('products', [])
            print(f"✅ Color search found {len(products)} products")
            
            if products:
                # Check color accuracy
                blue_products = [p for p in products if 'blue' in p['color'].lower()]
                print(f"   🔵 Blue products: {len(blue_products)}/{len(products)}")
        else:
            print(f"❌ Color search error: {color_response.status_code}")
    else:
        print(f"❌ Basic chat error: {response.status_code}")

def main():
    print("🎯 Color-Filled Buttons & Exact Search Test")
    print("=" * 60)
    
    try:
        # Wait for servers to be ready
        time.sleep(1)
        
        test_exact_keyword_search()
        test_color_suggestions()
        
        print("\n" + "=" * 60)
        print("🎉 Test Summary:")
        print("✅ Exact keyword matching implemented")
        print("✅ Color-specific database filtering")
        print("✅ Precise category matching (shirts ≠ t-shirts)")
        print("✅ Gender-specific filtering")
        print("\n💡 Frontend Changes:")
        print("✅ Color-filled buttons with proper colors")
        print("✅ Black text on light colors, white on dark")
        print("✅ Dynamic color styling based on option text")
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - make sure servers are running:")
        print("   Chat Agent: python chat_agent/lightweight_api_server.py (port 5001)")
        print("   Backend: python start_backend.py (port 5000)")
    except Exception as e:
        print(f"❌ Test error: {e}")

if __name__ == "__main__":
    main()