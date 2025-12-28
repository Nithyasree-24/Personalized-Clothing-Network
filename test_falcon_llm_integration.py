#!/usr/bin/env python3
"""
Test script for Falcon 7B LLM integration with FashionPulse Chat Agent
Tests both product search and general e-commerce queries
"""
import requests
import json
import time
from datetime import datetime

# Configuration
CHAT_API_URL = "http://localhost:5001/api/chat"
LLM_STATUS_URL = "http://localhost:5001/api/chat/llm-status"
HEALTH_URL = "http://localhost:5001/api/chat/health"

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"🧪 {title}")
    print("="*60)

def print_test_result(test_name, success, response_time=None):
    """Print test result with formatting"""
    status = "✅ PASS" if success else "❌ FAIL"
    time_str = f" ({response_time:.2f}s)" if response_time else ""
    print(f"{status} {test_name}{time_str}")

def test_chat_query(query, expected_keywords=None):
    """Test a chat query and return response"""
    try:
        start_time = time.time()
        
        response = requests.post(
            CHAT_API_URL,
            json={"message": query},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            
            # Check if response contains expected keywords
            success = True
            if expected_keywords:
                response_text = data.get('response', '').lower()
                success = any(keyword.lower() in response_text for keyword in expected_keywords)
            
            print_test_result(f"Query: '{query}'", success, response_time)
            
            # Print response preview
            response_preview = data.get('response', '')[:200]
            if len(data.get('response', '')) > 200:
                response_preview += "..."
            print(f"   📝 Response: {response_preview}")
            
            # Print product count if available
            if data.get('products'):
                print(f"   🛍️ Products found: {len(data['products'])}")
            
            return data, True
        else:
            print_test_result(f"Query: '{query}'", False, response_time)
            print(f"   ❌ HTTP {response.status_code}: {response.text}")
            return None, False
            
    except Exception as e:
        print_test_result(f"Query: '{query}'", False)
        print(f"   ❌ Error: {e}")
        return None, False

def test_llm_status():
    """Test LLM status endpoint"""
    try:
        response = requests.get(LLM_STATUS_URL, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            llm_info = data.get('llm_info', {})
            
            print_test_result("LLM Status Check", True)
            print(f"   🧠 Model Loaded: {llm_info.get('model_loaded', False)}")
            print(f"   🖥️ Device: {llm_info.get('device', 'unknown')}")
            print(f"   🔄 Fallback Mode: {llm_info.get('fallback_mode', True)}")
            print(f"   📦 Model: {llm_info.get('model_name', 'N/A')}")
            
            return llm_info, True
        else:
            print_test_result("LLM Status Check", False)
            return None, False
            
    except Exception as e:
        print_test_result("LLM Status Check", False)
        print(f"   ❌ Error: {e}")
        return None, False

def test_health_check():
    """Test health check endpoint"""
    try:
        response = requests.get(HEALTH_URL, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print_test_result("Health Check", True)
            print(f"   🏥 Status: {data.get('status', 'unknown')}")
            print(f"   🗄️ Database: {data.get('database', 'unknown')}")
            return data, True
        else:
            print_test_result("Health Check", False)
            return None, False
            
    except Exception as e:
        print_test_result("Health Check", False)
        print(f"   ❌ Error: {e}")
        return None, False

def main():
    """Run comprehensive LLM integration tests"""
    print_header("FALCON 7B LLM INTEGRATION TEST SUITE")
    print(f"🕒 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test 1: Health and Status Checks
    print_header("SYSTEM STATUS TESTS")
    health_data, health_ok = test_health_check()
    llm_info, llm_ok = test_llm_status()
    
    if not health_ok:
        print("\n❌ Chat server is not responding. Please start the server:")
        print("   python chat_agent/api_server.py")
        return
    
    # Test 2: Product Search Queries (Database + LLM)
    print_header("PRODUCT SEARCH TESTS (Database + LLM Enhancement)")
    
    product_queries = [
        ("show me red dresses under 2000", ["red", "dress", "₹"]),
        ("find jeans for men", ["jeans", "men"]),
        ("looking for ethnic wear for women", ["women", "ethnic"]),
        ("blue shirts under 1500", ["blue", "shirt"]),
        ("show me some popular items", ["popular", "items"])
    ]
    
    product_results = []
    for query, keywords in product_queries:
        result, success = test_chat_query(query, keywords)
        product_results.append(success)
        time.sleep(1)  # Rate limiting
    
    # Test 3: General E-commerce Queries (LLM Enhanced)
    print_header("E-COMMERCE SUPPORT TESTS (LLM Enhanced)")
    
    ecommerce_queries = [
        ("what is your return policy", ["return", "policy", "days"]),
        ("how long does shipping take", ["shipping", "delivery", "days"]),
        ("what payment methods do you accept", ["payment", "card", "upi"]),
        ("can I exchange this for a different size", ["exchange", "size"]),
        ("track my order", ["order", "track"]),
        ("I need help with sizing", ["size", "help", "guide"]),
        ("what are your store hours", ["hours", "support"]),
        ("how do I contact customer service", ["contact", "support", "service"])
    ]
    
    ecommerce_results = []
    for query, keywords in ecommerce_queries:
        result, success = test_chat_query(query, keywords)
        ecommerce_results.append(success)
        time.sleep(1)  # Rate limiting
    
    # Test 4: Complex Mixed Queries
    print_header("COMPLEX QUERY TESTS")
    
    complex_queries = [
        ("I want to buy a red dress but need to know about returns", ["red", "dress", "return"]),
        ("show me jeans and tell me about shipping costs", ["jeans", "shipping"]),
        ("what sizes do you have for women's tops and what's your exchange policy", ["size", "women", "exchange"])
    ]
    
    complex_results = []
    for query, keywords in complex_queries:
        result, success = test_chat_query(query, keywords)
        complex_results.append(success)
        time.sleep(1)
    
    # Test Summary
    print_header("TEST SUMMARY")
    
    total_tests = len(product_results) + len(ecommerce_results) + len(complex_results) + 2  # +2 for health/llm status
    passed_tests = sum([health_ok, llm_ok] + product_results + ecommerce_results + complex_results)
    
    print(f"📊 **Overall Results:**")
    print(f"   ✅ Passed: {passed_tests}/{total_tests}")
    print(f"   ❌ Failed: {total_tests - passed_tests}/{total_tests}")
    print(f"   📈 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    print(f"\n📋 **Category Breakdown:**")
    print(f"   🏥 System Status: {sum([health_ok, llm_ok])}/2")
    print(f"   🛍️ Product Search: {sum(product_results)}/{len(product_results)}")
    print(f"   💬 E-commerce Support: {sum(ecommerce_results)}/{len(ecommerce_results)}")
    print(f"   🔀 Complex Queries: {sum(complex_results)}/{len(complex_results)}")
    
    # LLM Status Summary
    if llm_info:
        print(f"\n🧠 **LLM Integration Status:**")
        if llm_info.get('model_loaded'):
            print(f"   ✅ Falcon 7B model is loaded and active")
            print(f"   🖥️ Running on: {llm_info.get('device', 'unknown')}")
        else:
            print(f"   ⚠️ LLM model not loaded - using fallback responses")
            print(f"   💡 This is normal if you don't have GPU or model files")
    
    print(f"\n🎯 **Recommendations:**")
    if passed_tests == total_tests:
        print("   🎉 All tests passed! Your Falcon 7B integration is working perfectly.")
    elif passed_tests >= total_tests * 0.8:
        print("   👍 Most tests passed. System is functional with minor issues.")
    else:
        print("   ⚠️ Several tests failed. Check server logs and configuration.")
    
    if llm_info and not llm_info.get('model_loaded'):
        print("   💡 To enable full LLM features, ensure you have:")
        print("      - Sufficient GPU memory (8GB+ recommended)")
        print("      - All required packages installed")
        print("      - Stable internet connection for model download")
    
    print(f"\n🕒 Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()