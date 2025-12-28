#!/usr/bin/env python3
"""
Test the recent fixes
"""
import requests
import json

def test_fixes():
    print('🔧 Testing Recent Fixes...')
    print('='*40)
    
    # Test 1: Check if stock is removed
    print('\n1️⃣ Testing stock removal...')
    try:
        response = requests.post('http://localhost:5001/api/chat', 
            json={'message': 'Show me red dresses'}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            products = data.get('products', [])
            if products:
                sample = products[0]
                if 'stock' in sample:
                    print(f'❌ Stock still present: {sample["stock"]}')
                else:
                    print('✅ Stock successfully removed from response')
                print(f'Sample product: {sample["product_name"]} - ₹{sample["price"]}')
        else:
            print(f'❌ HTTP {response.status_code}')
    except Exception as e:
        print(f'❌ Error: {e}')
    
    # Test 2: Check jeans search
    print('\n2️⃣ Testing jeans search...')
    try:
        response = requests.post('http://localhost:5001/api/chat', 
            json={'message': 'Show me jeans'}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            products = data.get('products', [])
            print(f'✅ Jeans search: {len(products)} products found')
            if products:
                print(f'   Sample: {products[0]["product_name"]}')
        else:
            print(f'❌ HTTP {response.status_code}')
    except Exception as e:
        print(f'❌ Error: {e}')
    
    # Test 3: Check ethnic wear search  
    print('\n3️⃣ Testing ethnic wear search...')
    try:
        response = requests.post('http://localhost:5001/api/chat', 
            json={'message': 'Looking for ethnic wear'}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            products = data.get('products', [])
            print(f'✅ Ethnic wear search: {len(products)} products found')
            if products:
                print(f'   Sample: {products[0]["product_name"]}')
        else:
            print(f'❌ HTTP {response.status_code}')
    except Exception as e:
        print(f'❌ Error: {e}')
    
    print('\n' + '='*40)
    print('🎯 Fix Testing Complete!')

if __name__ == '__main__':
    test_fixes()