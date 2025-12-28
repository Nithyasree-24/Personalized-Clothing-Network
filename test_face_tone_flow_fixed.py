#!/usr/bin/env python3
"""
Test Face Tone Flow - Fixed Version
"""
import requests
import json

def test_face_tone_flow_complete():
    print("🎨 Testing Complete Face Tone Flow")
    print("=" * 50)
    
    # Test the exact scenario user mentioned: Pink + Women + Tops and Co-ord Sets
    print("Testing: Pink + Women + Tops and Co-ord Sets")
    
    response = requests.post('http://localhost:5001/api/chat', json={
        'message': json.dumps({
            'type': 'faceToneFlow',
            'color': 'Pink',
            'gender': 'women',
            'category': 'Tops and Co-ord Sets'
        })
    })
    
    if response.status_code == 200:
        data = response.json()
        products = data.get('products', [])
        response_text = data.get('response', '')
        
        print(f"✅ API Response: {response.status_code}")
        print(f"📝 Response Text: {response_text}")
        print(f"🛍️ Products Found: {len(products)}")
        
        if products:
            print("\n🎯 Product Details:")
            for i, product in enumerate(products[:3], 1):
                print(f"{i}. {product['product_name']}")
                print(f"   Color: {product['color']}")
                print(f"   Gender: {product['gender']}")
                print(f"   Category: {product['product_category']}")
                print(f"   Price: ₹{product['price']}")
                print()
            
            # Verify all products match criteria
            all_match = True
            for product in products:
                if (product['color'].lower() != 'pink' or 
                    product['gender'].lower() != 'women' or 
                    product['product_category'] != 'Tops and Co-ord Sets'):
                    all_match = False
                    print(f"❌ Mismatch: {product['product_name']} - {product['color']}, {product['gender']}, {product['product_category']}")
            
            if all_match:
                print("✅ All products match the search criteria!")
            else:
                print("❌ Some products don't match criteria")
        else:
            print("❌ No products found!")
    else:
        print(f"❌ API Error: {response.status_code}")
        print(response.text)
    
    print("\n" + "=" * 50)
    
    # Test Body Fit Flow too
    print("Testing Body Fit Flow: Women + Athletic + Dresses")
    
    response = requests.post('http://localhost:5001/api/chat', json={
        'message': json.dumps({
            'type': 'bodyFitFlow',
            'gender': 'women',
            'bodyType': 'Athletic',
            'category': 'Dresses'
        })
    })
    
    if response.status_code == 200:
        data = response.json()
        products = data.get('products', [])
        response_text = data.get('response', '')
        
        print(f"✅ Body Fit API Response: {response.status_code}")
        print(f"📝 Response Text: {response_text}")
        print(f"🛍️ Products Found: {len(products)}")
        
        if products:
            print(f"✅ Body Fit flow working! Found {len(products)} dresses for women")
        else:
            print("❌ No products found for Body Fit flow")
    else:
        print(f"❌ Body Fit API Error: {response.status_code}")

if __name__ == "__main__":
    test_face_tone_flow_complete()