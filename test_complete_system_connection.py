#!/usr/bin/env python3
"""
Complete System Connection Test
Tests all connections: Database -> Backend -> Frontend -> Chat Agent
"""
import requests
import json
import time
from datetime import datetime

def print_header(title):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"🧪 {title}")
    print("="*60)

def test_endpoint(name, url, method="GET", data=None, timeout=10):
    """Test an endpoint and return result"""
    try:
        start_time = time.time()
        
        if method == "GET":
            response = requests.get(url, timeout=timeout)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=timeout)
        
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {name} - OK ({response_time:.2f}s)")
            return True, result
        else:
            print(f"❌ {name} - HTTP {response.status_code}")
            return False, None
            
    except requests.exceptions.ConnectionError:
        print(f"❌ {name} - Connection Failed (Server not running)")
        return False, None
    except Exception as e:
        print(f"❌ {name} - Error: {e}")
        return False, None

def main():
    """Run complete system test"""
    print_header("FASHIONPULSE COMPLETE SYSTEM CONNECTION TEST")
    print(f"🕒 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test 1: Backend Database Connection
    print_header("BACKEND DATABASE CONNECTION")
    
    backend_tests = [
        ("Database Product Count", "http://localhost:5000/api/cache/count"),
        ("Product Search", "http://localhost:5000/api/products/search?query=dress&limit=5"),
        ("Category Products", "http://localhost:5000/api/products/category/fashion?limit=5"),
        ("Product Detail", "http://localhost:5000/api/products/1"),
    ]
    
    backend_results = []
    for name, url in backend_tests:
        success, data = test_endpoint(name, url)
        backend_results.append(success)
        
        if success and data:
            if 'cached_products' in data:
                print(f"   📊 Products in database: {data['cached_products']}")
            elif 'products' in data:
                print(f"   🛍️ Products returned: {len(data['products'])}")
            elif 'product' in data:
                print(f"   📦 Product: {data['product'].get('title', 'Unknown')}")
    
    # Test 2: Chat Agent Connection
    print_header("CHAT AGENT CONNECTION")
    
    chat_tests = [
        ("Chat Health Check", "http://localhost:5001/api/chat/health"),
        ("LLM Status", "http://localhost:5001/api/chat/llm-status"),
        ("Product Query", "http://localhost:5001/api/chat", "POST", {"message": "show me red dresses"}),
        ("E-commerce Query", "http://localhost:5001/api/chat", "POST", {"message": "what is your return policy?"}),
    ]
    
    chat_results = []
    for name, url, *args in chat_tests:
        method = args[0] if args else "GET"
        data = args[1] if len(args) > 1 else None
        
        success, result = test_endpoint(name, url, method, data)
        chat_results.append(success)
        
        if success and result:
            if 'database' in result:
                print(f"   🗄️ Database status: {result['database']}")
            elif 'llm_info' in result:
                llm_info = result['llm_info']
                print(f"   🧠 LLM loaded: {llm_info.get('model_loaded', False)}")
                print(f"   🖥️ Device: {llm_info.get('device', 'unknown')}")
            elif 'response' in result:
                response_preview = result['response'][:100] + "..." if len(result['response']) > 100 else result['response']
                print(f"   💬 Response: {response_preview}")
                if result.get('products'):
                    print(f"   🛍️ Products found: {len(result['products'])}")
    
    # Test 3: Frontend Connection (if accessible)
    print_header("FRONTEND CONNECTION TEST")
    
    try:
        frontend_response = requests.get("http://localhost:3000", timeout=5)
        if frontend_response.status_code == 200:
            print("✅ Frontend - Accessible")
            frontend_ok = True
        else:
            print(f"❌ Frontend - HTTP {frontend_response.status_code}")
            frontend_ok = False
    except:
        print("❌ Frontend - Not accessible (may still be starting)")
        frontend_ok = False
    
    # Test 4: Database Direct Connection Test
    print_header("DATABASE DIRECT CONNECTION")
    
    try:
        # Test if we can connect to MySQL directly
        import mysql.connector
        from backend.config import Config
        
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) as count FROM clothing")
        result = cursor.fetchone()
        
        print(f"✅ Direct Database Connection - OK")
        print(f"   📊 Total products: {result['count']}")
        
        # Test sample product
        cursor.execute("SELECT product_id, product_name, price, product_category, gender FROM clothing LIMIT 1")
        sample = cursor.fetchone()
        if sample:
            print(f"   📦 Sample product: {sample['product_name']} (₹{sample['price']})")
        
        cursor.close()
        connection.close()
        db_direct_ok = True
        
    except Exception as e:
        print(f"❌ Direct Database Connection - Error: {e}")
        db_direct_ok = False
    
    # Summary
    print_header("TEST SUMMARY")
    
    backend_success = sum(backend_results)
    chat_success = sum(chat_results)
    
    print(f"📊 **Results Overview:**")
    print(f"   🔧 Backend Tests: {backend_success}/{len(backend_results)} passed")
    print(f"   💬 Chat Agent Tests: {chat_success}/{len(chat_results)} passed")
    print(f"   🌐 Frontend: {'✅ OK' if frontend_ok else '❌ Issues'}")
    print(f"   🗄️ Database Direct: {'✅ OK' if db_direct_ok else '❌ Issues'}")
    
    total_tests = len(backend_results) + len(chat_results) + 2  # +2 for frontend and db direct
    total_passed = backend_success + chat_success + (1 if frontend_ok else 0) + (1 if db_direct_ok else 0)
    
    print(f"\n🎯 **Overall Status:**")
    print(f"   ✅ Passed: {total_passed}/{total_tests}")
    print(f"   📈 Success Rate: {(total_passed/total_tests)*100:.1f}%")
    
    if total_passed == total_tests:
        print(f"\n🎉 **ALL SYSTEMS OPERATIONAL!**")
        print(f"   🔗 Backend: http://localhost:5000")
        print(f"   🌐 Frontend: http://localhost:3000")
        print(f"   💬 Chat Agent: http://localhost:5001")
        print(f"   🗄️ Database: fashiopulse.clothing ({result['count'] if 'result' in locals() else '285'} products)")
    elif total_passed >= total_tests * 0.8:
        print(f"\n👍 **SYSTEM MOSTLY OPERATIONAL**")
        print(f"   Most components are working. Check failed tests above.")
    else:
        print(f"\n⚠️ **SYSTEM ISSUES DETECTED**")
        print(f"   Multiple components have issues. Check server status and logs.")
    
    # Recommendations
    print(f"\n💡 **Quick Start Commands:**")
    print(f"   Backend: python start_backend.py")
    print(f"   Frontend: npm run dev")
    print(f"   Chat Agent: python chat_agent/api_server.py")
    
    print(f"\n🕒 Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()