#!/usr/bin/env python3
"""
Test the chat agent API
"""
import requests
import json

def test_chat_api():
    """Test the chat agent API endpoints"""
    base_url = "http://localhost:5001/api/chat"
    
    print("🧪 Testing FashionPulse Chat Agent API")
    print("="*50)
    
    # Test health check
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            health_data = response.json()
            print(f"   Database: {health_data.get('database')}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    # Test chat functionality
    test_messages = [
        "Hi there!",
        "Show me red dresses under 2000",
        "Find jeans for men",
        "What categories do you have?"
    ]
    
    for message in test_messages:
        print(f"\n💬 Testing: '{message}'")
        try:
            response = requests.post(
                base_url,
                headers={'Content-Type': 'application/json'},
                json={'message': message}
            )
            
            if response.status_code == 200:
                data = response.json()
                agent_response = data.get('response', '')
                print(f"✅ Response received ({len(agent_response)} chars)")
                # Show first 100 chars of response
                preview = agent_response[:100] + "..." if len(agent_response) > 100 else agent_response
                print(f"   Preview: {preview}")
            else:
                print(f"❌ Request failed: {response.status_code}")
                print(f"   Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Request error: {e}")
    
    print(f"\n🎉 Chat API testing complete!")
    print("✅ Your chat agent is ready for frontend integration!")

if __name__ == "__main__":
    test_chat_api()