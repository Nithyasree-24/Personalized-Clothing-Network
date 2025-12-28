#!/usr/bin/env python3
"""
Test View All Products Functionality
"""
import requests
import json

def test_view_all_functionality():
    print('👀 Testing View All Products Functionality...')
    print('='*50)
    
    # Test product search that should return multiple products
    test_queries = [
        'show me products under ₹2000',
        'find dresses for women',
        'show me shirts',
        'products under 1500'
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f'\n{i}️⃣ Testing: "{query}"')
        
        try:
            response = requests.post('http://localhost:5001/api/chat', 
                json={'message': query}, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                products = data.get('products', [])
                response_text = data.get('response', '')
                
                print(f'   📦 Products returned: {len(products)}')
                print(f'   📝 Response preview: {response_text[:100]}...')
                
                if len(products) > 2:
                    print(f'   ✅ Perfect! {len(products)} products returned (more than 2)')
                    print(f'   🎯 Frontend will show 2 initially with "View All" button')
                    
                    # Show sample products
                    print(f'   📋 Sample products:')
                    for j, product in enumerate(products[:3], 1):
                        name = product.get('product_name', 'Unknown')[:30]
                        price = product.get('price', 0)
                        try:
                            price_int = int(float(price)) if price else 0
                            print(f'      {j}. {name}... - ₹{price_int}')
                        except (ValueError, TypeError):
                            print(f'      {j}. {name}... - ₹{price}')
                    
                    if len(products) > 3:
                        print(f'      ... and {len(products) - 3} more products')
                        
                elif len(products) == 2:
                    print(f'   ⚠️  Only 2 products returned (no "View All" needed)')
                elif len(products) == 1:
                    print(f'   ⚠️  Only 1 product returned')
                else:
                    print(f'   ❌ No products returned')
                    
            else:
                print(f'   ❌ HTTP {response.status_code}')
                
        except Exception as e:
            print(f'   ❌ Error: {e}')
    
    print('\n' + '='*50)
    print('🎯 View All Functionality Test Complete!')
    print('\n✅ Expected Frontend Behavior:')
    print('   • Show 2 products initially')
    print('   • Display "View All X Products" button if more than 2')
    print('   • Expand to show all products when clicked')
    print('   • Add "Show Less" button when expanded')
    print('   • Improved scrolling with smooth behavior')
    print('\n🚀 Test your chat now with: "show me products under ₹2000"')

if __name__ == '__main__':
    test_view_all_functionality()