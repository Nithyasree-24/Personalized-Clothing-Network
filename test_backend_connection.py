#!/usr/bin/env python3
"""
Test Backend Connection and Database Integration
Tests all backend services and database connections
"""

import requests
import json

def test_main_backend():
    """Test main backend API"""
    print("🔍 Testing Main Backend API (Port 5000)")
    print("-" * 40)
    
    try:
        # Test products endpoint
        response = requests.get('http://localhost:5000/api/products/search?query=clothing&category=fashion')
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Products API working: {len(data.get('products', []))} products found")
            
            # Show sample product
            if data.get('products'):
                sample = data['products'][0]
                print(f"📦 Sample product: {sample.get('product_name', 'N/A')} - ₹{sample.get('price', 'N/A')}")
        else:
            print(f"❌ Products API failed: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to main backend on port 5000")
        return False
    except Exception as e:
        print(f"❌ Error testing main backend: {e}")
        return False
    
    return True

def test_auth_backend():
    """Test authentication backend"""
    print("\n🔐 Testing Authentication Backend (Port 5002)")
    print("-" * 40)
    
    try:
        response = requests.get('http://localhost:5002/api/auth/test')
        if response.status_code == 200:
            print("✅ Authentication API working")
        else:
            print(f"❌ Authentication API failed: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to auth backend on port 5002")
        return False
    except Exception as e:
        print(f"❌ Error testing auth backend: {e}")
        return False
    
    return True

def test_chat_backend():
    """Test chat agent backend"""
    print("\n💬 Testing Chat Agent Backend (Port 5001)")
    print("-" * 40)
    
    try:
        response = requests.post('http://localhost:5001/api/chat', json={
            'message': 'show me red dresses'
        })
        if response.status_code == 200:
            data = response.json()
            print("✅ Chat Agent API working")
            print(f"📝 Sample response: {data.get('response', 'No response')[:100]}...")
        else:
            print(f"❌ Chat Agent API failed: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to chat agent on port 5001")
        return False
    except Exception as e:
        print(f"❌ Error testing chat agent: {e}")
        return False
    
    return True

def test_frontend_connection():
    """Test frontend connection"""
    print("\n🌐 Testing Frontend Connection (Port 3000)")
    print("-" * 40)
    
    try:
        response = requests.get('http://localhost:3000')
        if response.status_code == 200:
            print("✅ Frontend is accessible")
        else:
            print(f"❌ Frontend failed: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to frontend on port 3000")
        return False
    except Exception as e:
        print(f"❌ Error testing frontend: {e}")
        return False
    
    return True

def main():
    """Run complete backend connection test"""
    print("🧪 Complete Backend Connection Test")
    print("=" * 50)
    
    # Test all services
    main_backend = test_main_backend()
    auth_backend = test_auth_backend()
    chat_backend = test_chat_backend()
    frontend = test_frontend_connection()
    
    print("\n" + "=" * 50)
    print("📊 Connection Status Summary:")
    print(f"   • Main Backend (Products): {'✅ Working' if main_backend else '❌ Failed'}")
    print(f"   • Auth Backend (Users): {'✅ Working' if auth_backend else '❌ Failed'}")
    print(f"   • Chat Agent (AI): {'✅ Working' if chat_backend else '❌ Failed'}")
    print(f"   • Frontend (UI): {'✅ Working' if frontend else '❌ Failed'}")
    
    if all([main_backend, auth_backend, chat_backend, frontend]):
        print("\n🎉 All services are working perfectly!")
        print("\n🚀 Ready to use:")
        print("   • Visit: http://localhost:3000")
        print("   • Login/Signup with database authentication")
        print("   • Browse 285+ products from fashiopulse database")
        print("   • Use AI chat for product recommendations")
        print("   • Access combos page via header button")
        print("   • Use calendar feature in chat")
    else:
        print("\n⚠️ Some services need attention")
        print("💡 Make sure all servers are running:")
        print("   • python start_backend.py (port 5000)")
        print("   • python backend/auth_api.py (port 5002)")
        print("   • python chat_agent/lightweight_api_server.py (port 5001)")
        print("   • npm run dev (port 3000)")

if __name__ == "__main__":
    main()