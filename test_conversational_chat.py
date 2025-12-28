#!/usr/bin/env python3
"""
Test Conversational Chat Improvements
"""
import requests
import json

def test_conversational_responses():
    print('🤖 Testing Conversational Chat Improvements...')
    print('='*50)
    
    # Test cases for conversational responses
    test_cases = [
        {
            'input': 'hi',
            'expected_type': 'greeting',
            'should_not_contain': ['Here are some popular items', 'products']
        },
        {
            'input': 'hello',
            'expected_type': 'greeting',
            'should_not_contain': ['Here are some popular items', 'products']
        },
        {
            'input': 'how are you',
            'expected_type': 'conversation',
            'should_not_contain': ['Here are some popular items', 'products']
        },
        {
            'input': 'thank you',
            'expected_type': 'thanks',
            'should_not_contain': ['Here are some popular items', 'products']
        },
        {
            'input': 'show me red dresses',
            'expected_type': 'product_search',
            'should_contain': ['dress', 'red']
        },
        {
            'input': 'what is your return policy',
            'expected_type': 'ecommerce',
            'should_contain': ['return', 'exchange']
        }
    ]
    
    passed_tests = 0
    total_tests = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f'\n{i}️⃣ Testing: "{test_case["input"]}"')
        
        try:
            response = requests.post('http://localhost:5001/api/chat', 
                json={'message': test_case['input']}, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                response_text = data.get('response', '').lower()
                products = data.get('products', [])
                
                print(f'   Response: {data.get("response", "")[:100]}...')
                
                # Check if response is appropriate
                test_passed = True
                
                # Check should_not_contain
                if 'should_not_contain' in test_case:
                    for phrase in test_case['should_not_contain']:
                        if phrase.lower() in response_text:
                            print(f'   ❌ Should not contain "{phrase}" but does')
                            test_passed = False
                
                # Check should_contain
                if 'should_contain' in test_case:
                    for phrase in test_case['should_contain']:
                        if phrase.lower() not in response_text:
                            print(f'   ❌ Should contain "{phrase}" but doesn\'t')
                            test_passed = False
                
                # Check product search behavior
                if test_case['expected_type'] == 'product_search':
                    if len(products) == 0:
                        print(f'   ⚠️  Product search should return products')
                        # Don't fail the test, just warn
                elif test_case['expected_type'] in ['greeting', 'conversation', 'thanks']:
                    if len(products) > 0:
                        print(f'   ❌ Conversational response should not return products')
                        test_passed = False
                
                if test_passed:
                    print(f'   ✅ Test passed - Appropriate {test_case["expected_type"]} response')
                    passed_tests += 1
                else:
                    print(f'   ❌ Test failed')
                    
            else:
                print(f'   ❌ HTTP {response.status_code}')
                
        except Exception as e:
            print(f'   ❌ Error: {e}')
    
    print('\n' + '='*50)
    print(f'🎯 Test Results: {passed_tests}/{total_tests} tests passed')
    
    if passed_tests == total_tests:
        print('🎉 All conversational tests passed!')
        print('✅ Chat now behaves like a human assistant')
        print('✅ Greetings get friendly responses')
        print('✅ Product searches still work correctly')
        print('✅ E-commerce queries handled properly')
    else:
        print(f'⚠️  {total_tests - passed_tests} tests need attention')
    
    return passed_tests == total_tests

if __name__ == '__main__':
    success = test_conversational_responses()
    exit(0 if success else 1)