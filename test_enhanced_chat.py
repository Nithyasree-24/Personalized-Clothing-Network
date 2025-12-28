#!/usr/bin/env python3
"""
Test the enhanced chat agent
"""
import requests
import json

def test_enhanced_chat():
    """Test the enhanced chat agent with various queries"""
    base_url = "http://localhost:5001/api/chat"
    
    print("🧪 Testing Enhanced FashionPulse Chat Agent")
    print("="*60)
    
    test_messages = [
        "show mens shirts",
        "find red dresses",
        "womens tops under 2000",
        "blue jeans for men",
        "ethnic wear for women",
        "hi there",
        "what do you have?",
        "cheap clothes",
        "expensive items"
    ]
    
    for message in test_messages:
        print(f"\n💬 User: '{message}'")
        print("-" * 50)
        
        try:
            response = requests.post(
                base_url,
                headers={'Content-Type': 'application/json'},
                json={'message': message}
            )
            
            if response.status_code == 200:
                data = response.json()
                agent_response = data.get('response', '')
                
                # Show first 200 chars of response
                preview = agent_response[:200] + "..." if len(agent_response) > 200 else agent_response
                print(f"🤖 Agent: {preview}")
                
                # Check if it contains product data
                if any(keyword in agent_response.lower() for keyword in ['₹', 'price', 'stock', 'product']):
                    print("✅ Contains product data from database")
                else:
                    print("⚠️ Generic response (no product data)")
                    
            else:
                print(f"❌ Request failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Request error: {e}")
    
    print(f"\n🎉 Enhanced chat testing complete!")

if __name__ == "__main__":
    test_enhanced_chat()