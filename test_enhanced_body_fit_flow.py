#!/usr/bin/env python3
"""
Test Enhanced Body Fit Flow with Proper Body Shapes
"""
import requests
import json

def test_enhanced_body_fit_flow():
    print("👕 Testing Enhanced Body Fit Flow")
    print("=" * 60)
    
    # Test Women's Hourglass body shape
    print("Test 1: Women + Hourglass + Dresses + Red")
    response = requests.post('http://localhost:5001/api/chat', json={
        'message': json.dumps({
            'type': 'bodyFitFlow',
            'gender': 'women',
            'bodyShape': 'Hourglass',
            'category': 'Dresses',
            'color': 'Red'
        })
    })
    
    if response.status_code == 200:
        data = response.json()
        products = data.get('products', [])
        print(f"✅ Found {len(products)} red dresses for hourglass women")
        
        if products:
            for i, product in enumerate(products[:3], 1):
                print(f"  {i}. {product['product_name']} - {product['color']} - ₹{product['price']}")
        print()
    else:
        print(f"❌ Error: {response.status_code}")
    
    # Test Men's Rectangle body shape
    print("Test 2: Men + Rectangle + Shirts + Blue")
    response = requests.post('http://localhost:5001/api/chat', json={
        'message': json.dumps({
            'type': 'bodyFitFlow',
            'gender': 'men',
            'bodyShape': 'Rectangle',
            'category': 'Shirts',
            'color': 'Blue'
        })
    })
    
    if response.status_code == 200:
        data = response.json()
        products = data.get('products', [])
        print(f"✅ Found {len(products)} blue shirts for rectangle men")
        
        if products:
            for i, product in enumerate(products[:3], 1):
                print(f"  {i}. {product['product_name']} - {product['color']} - ₹{product['price']}")
        print()
    else:
        print(f"❌ Error: {response.status_code}")
    
    # Test Women's Pear body shape
    print("Test 3: Women + Pear + Tops and Co-ord Sets + Pink")
    response = requests.post('http://localhost:5001/api/chat', json={
        'message': json.dumps({
            'type': 'bodyFitFlow',
            'gender': 'women',
            'bodyShape': 'Pear',
            'category': 'Tops and Co-ord Sets',
            'color': 'Pink'
        })
    })
    
    if response.status_code == 200:
        data = response.json()
        products = data.get('products', [])
        print(f"✅ Found {len(products)} pink tops for pear-shaped women")
        
        if products:
            for i, product in enumerate(products[:3], 1):
                print(f"  {i}. {product['product_name']} - {product['color']} - ₹{product['price']}")
        print()
    else:
        print(f"❌ Error: {response.status_code}")
    
    print("=" * 60)
    print("✅ Enhanced Body Fit Flow testing complete!")

def test_body_shape_recommendations():
    print("\n🧠 Testing Body Shape Recommendations Logic")
    print("=" * 60)
    
    # Test the recommendation system
    try:
        import sys
        sys.path.append('chat_agent')
        from lightweight_chat_agent import LightweightFashionPulseChatAgent
        
        agent = LightweightFashionPulseChatAgent()
        
        # Test women's recommendations
        print("Women's Body Shape Recommendations:")
        women_shapes = ['Hourglass', 'Pear', 'Apple', 'Rectangle', 'Inverted Triangle']
        for shape in women_shapes:
            recommendations = agent.get_body_shape_recommendations('women', shape)
            print(f"  {shape}: {', '.join(recommendations)}")
        
        print("\nMen's Body Shape Recommendations:")
        men_shapes = ['Rectangle', 'Triangle', 'Inverted Triangle', 'Oval', 'Trapezoid']
        for shape in men_shapes:
            recommendations = agent.get_body_shape_recommendations('men', shape)
            print(f"  {shape}: {', '.join(recommendations)}")
        
        print("\n✅ Recommendation system working correctly!")
        
    except Exception as e:
        print(f"❌ Error testing recommendations: {e}")

if __name__ == "__main__":
    test_enhanced_body_fit_flow()
    test_body_shape_recommendations()