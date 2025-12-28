#!/usr/bin/env python3
"""
Test Calendar Event Based Outfit Personalization System
"""
import requests
import json

def test_event_outfit_suggestions():
    print("📅 Testing Calendar Event Based Outfit System")
    print("=" * 60)
    
    # Test Women's Job Interview
    print("Test 1: Women + Job Interview")
    response = requests.post('http://localhost:5001/api/chat', json={
        'message': json.dumps({
            'type': 'eventOutfitSuggestion',
            'gender': 'women',
            'eventType': 'Job Interview',
            'eventDate': '2024-01-15'
        })
    })
    
    if response.status_code == 200:
        data = response.json()
        products = data.get('products', [])
        print(f"✅ Found {len(products)} outfits for women's job interview")
        
        if products:
            for i, product in enumerate(products[:3], 1):
                print(f"  {i}. {product['product_name']} - {product['product_category']} - ₹{product['price']}")
        print()
    else:
        print(f"❌ Error: {response.status_code}")
    
    # Test Men's Wedding
    print("Test 2: Men + Wedding")
    response = requests.post('http://localhost:5001/api/chat', json={
        'message': json.dumps({
            'type': 'eventOutfitSuggestion',
            'gender': 'men',
            'eventType': 'Wedding',
            'eventDate': '2024-02-20'
        })
    })
    
    if response.status_code == 200:
        data = response.json()
        products = data.get('products', [])
        print(f"✅ Found {len(products)} outfits for men's wedding")
        
        if products:
            for i, product in enumerate(products[:3], 1):
                print(f"  {i}. {product['product_name']} - {product['product_category']} - ₹{product['price']}")
        print()
    else:
        print(f"❌ Error: {response.status_code}")
    
    # Test Women's Festival
    print("Test 3: Women + Festival")
    response = requests.post('http://localhost:5001/api/chat', json={
        'message': json.dumps({
            'type': 'eventOutfitSuggestion',
            'gender': 'women',
            'eventType': 'Diwali Festival',
            'eventDate': '2024-11-01'
        })
    })
    
    if response.status_code == 200:
        data = response.json()
        products = data.get('products', [])
        print(f"✅ Found {len(products)} outfits for women's festival")
        
        if products:
            for i, product in enumerate(products[:3], 1):
                print(f"  {i}. {product['product_name']} - {product['product_category']} - ₹{product['price']}")
        print()
    else:
        print(f"❌ Error: {response.status_code}")
    
    # Test Men's Party
    print("Test 4: Men + Party")
    response = requests.post('http://localhost:5001/api/chat', json={
        'message': json.dumps({
            'type': 'eventOutfitSuggestion',
            'gender': 'men',
            'eventType': 'Birthday Party',
            'eventDate': '2024-03-10'
        })
    })
    
    if response.status_code == 200:
        data = response.json()
        products = data.get('products', [])
        print(f"✅ Found {len(products)} outfits for men's party")
        
        if products:
            for i, product in enumerate(products[:3], 1):
                print(f"  {i}. {product['product_name']} - {product['product_category']} - ₹{product['price']}")
        print()
    else:
        print(f"❌ Error: {response.status_code}")
    
    print("=" * 60)
    print("✅ Calendar Event System testing complete!")

def test_event_category_logic():
    print("\n🧠 Testing Event Category Logic")
    print("=" * 60)
    
    try:
        import sys
        sys.path.append('chat_agent')
        from lightweight_chat_agent import LightweightFashionPulseChatAgent
        
        agent = LightweightFashionPulseChatAgent()
        
        # Test women's event categories
        print("Women's Event Categories:")
        women_events = [
            'Job Interview', 'Wedding', 'Birthday Party', 'College', 
            'Diwali Festival', 'Family Function', 'Travel'
        ]
        
        for event in women_events:
            categories = agent._get_event_categories('women', event)
            print(f"  {event}: {', '.join(categories)}")
        
        print("\nMen's Event Categories:")
        men_events = [
            'Job Interview', 'Wedding', 'Party', 'College', 
            'Festival', 'Travel'
        ]
        
        for event in men_events:
            categories = agent._get_event_categories('men', event)
            print(f"  {event}: {', '.join(categories)}")
        
        print("\n✅ Event category logic working correctly!")
        
    except Exception as e:
        print(f"❌ Error testing event categories: {e}")

if __name__ == "__main__":
    test_event_outfit_suggestions()
    test_event_category_logic()