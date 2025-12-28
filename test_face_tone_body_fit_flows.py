#!/usr/bin/env python3
"""
Test Face Tone and Body Fit flows in FashionPulse Chat Agent
"""
import requests
import json
import time

def test_chat_endpoint():
    """Test basic chat endpoint"""
    url = "http://localhost:5001/api/chat"
    
    # Test basic greeting
    response = requests.post(url, json={"message": "hi"})
    print("✅ Basic greeting test:")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()['response'][:100]}...")
    print()

def test_face_tone_flow():
    """Test Face Tone flow"""
    url = "http://localhost:5001/api/chat"
    
    # Test Face Tone flow with Fair skin tone, Blue color, Women, Dresses
    flow_data = {
        "message": json.dumps({
            "type": "faceToneFlow",
            "color": "blue",
            "gender": "women",
            "category": "Dresses"
        })
    }
    
    response = requests.post(url, json=flow_data)
    print("✅ Face Tone Flow test:")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {data['response'][:100]}...")
        print(f"Products found: {len(data.get('products', []))}")
        if data.get('products'):
            print(f"First product: {data['products'][0]['product_name']}")
    else:
        print(f"Error: {response.text}")
    print()

def test_body_fit_flow():
    """Test Body Fit flow"""
    url = "http://localhost:5001/api/chat"
    
    # Test Body Fit flow with Men, Athletic, Shirts
    flow_data = {
        "message": json.dumps({
            "type": "bodyFitFlow",
            "gender": "men",
            "bodyType": "Athletic",
            "category": "Shirts"
        })
    }
    
    response = requests.post(url, json=flow_data)
    print("✅ Body Fit Flow test:")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {data['response'][:100]}...")
        print(f"Products found: {len(data.get('products', []))}")
        if data.get('products'):
            print(f"First product: {data['products'][0]['product_name']}")
    else:
        print(f"Error: {response.text}")
    print()

def test_regular_product_search():
    """Test regular product search still works"""
    url = "http://localhost:5001/api/chat"
    
    response = requests.post(url, json={"message": "show me red dresses"})
    print("✅ Regular product search test:")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {data['response'][:100]}...")
        print(f"Products found: {len(data.get('products', []))}")
    else:
        print(f"Error: {response.text}")
    print()

if __name__ == "__main__":
    print("🧪 Testing Face Tone and Body Fit Flows")
    print("=" * 50)
    
    try:
        # Wait a moment for servers to be ready
        time.sleep(2)
        
        test_chat_endpoint()
        test_face_tone_flow()
        test_body_fit_flow()
        test_regular_product_search()
        
        print("✅ All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - make sure chat agent server is running on port 5001")
        print("Run: python chat_agent/lightweight_api_server.py")
    except Exception as e:
        print(f"❌ Test error: {e}")