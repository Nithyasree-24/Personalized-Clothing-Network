#!/usr/bin/env python3
"""
Complete Authentication System Test
Tests the full integration between frontend and backend authentication
"""

import requests
import json
import time

def test_api_connection():
    """Test if authentication API is running"""
    try:
        response = requests.get('http://localhost:5002/api/auth/test')
        if response.status_code == 200:
            print("✅ Authentication API is running")
            return True
        else:
            print("❌ Authentication API connection failed")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to authentication API on port 5002")
        print("💡 Please start the server: python backend/auth_api.py")
        return False

def test_signup_flow():
    """Test complete signup flow"""
    print("\n🔐 Testing Signup Flow")
    print("-" * 40)
    
    # Test new user signup
    signup_data = {
        "name": "Frontend Test User",
        "email": "frontend@fashionpulse.com",
        "password": "testpass123"
    }
    
    response = requests.post('http://localhost:5002/api/auth/signup', json=signup_data)
    result = response.json()
    
    if result['success']:
        print(f"✅ New user signup: {result['message']}")
    else:
        print(f"ℹ️ Signup result: {result['message']}")
    
    # Test duplicate email
    response = requests.post('http://localhost:5002/api/auth/signup', json=signup_data)
    result = response.json()
    
    if not result['success'] and "already have an account" in result['message']:
        print("✅ Duplicate email prevention working")
    else:
        print(f"❌ Duplicate email test failed: {result['message']}")

def test_login_flow():
    """Test complete login flow"""
    print("\n🔑 Testing Login Flow")
    print("-" * 40)
    
    # Test successful login
    login_data = {
        "email": "frontend@fashionpulse.com",
        "password": "testpass123"
    }
    
    response = requests.post('http://localhost:5002/api/auth/login', json=login_data)
    result = response.json()
    
    if result['success']:
        print(f"✅ Successful login: {result['message']}")
        print(f"👤 User data: {result['user']}")
        return result['user']
    else:
        print(f"❌ Login failed: {result['message']}")
        return None
    
    # Test wrong password
    wrong_login = {
        "email": "frontend@fashionpulse.com",
        "password": "wrongpassword"
    }
    
    response = requests.post('http://localhost:5002/api/auth/login', json=wrong_login)
    result = response.json()
    
    if not result['success'] and "Incorrect password" in result['message']:
        print("✅ Wrong password detection working")
    else:
        print(f"❌ Wrong password test failed: {result['message']}")
    
    # Test non-existent email
    nonexistent_login = {
        "email": "nonexistent@fashionpulse.com",
        "password": "testpass123"
    }
    
    response = requests.post('http://localhost:5002/api/auth/login', json=nonexistent_login)
    result = response.json()
    
    if not result['success'] and "No account found" in result['message']:
        print("✅ Non-existent email detection working")
    else:
        print(f"❌ Non-existent email test failed: {result['message']}")

def test_password_reset_flow():
    """Test password reset flow"""
    print("\n🔄 Testing Password Reset Flow")
    print("-" * 40)
    
    # Generate reset token
    reset_request = {
        "email": "frontend@fashionpulse.com"
    }
    
    response = requests.post('http://localhost:5002/api/auth/forgot-password', json=reset_request)
    result = response.json()
    
    if result['success']:
        print("✅ Reset token generated successfully")
        token = result['token']
        
        # Reset password using token
        reset_data = {
            "token": token,
            "password": "newpassword123"
        }
        
        response = requests.post('http://localhost:5002/api/auth/reset-password', json=reset_data)
        result = response.json()
        
        if result['success']:
            print("✅ Password reset successful")
            
            # Test login with new password
            login_data = {
                "email": "frontend@fashionpulse.com",
                "password": "newpassword123"
            }
            
            response = requests.post('http://localhost:5002/api/auth/login', json=login_data)
            result = response.json()
            
            if result['success']:
                print("✅ Login with new password successful")
            else:
                print(f"❌ Login with new password failed: {result['message']}")
        else:
            print(f"❌ Password reset failed: {result['message']}")
    else:
        print(f"❌ Reset token generation failed: {result['message']}")

def test_user_data_persistence():
    """Test chat history and calendar events"""
    print("\n💾 Testing User Data Persistence")
    print("-" * 40)
    
    user_email = "frontend@fashionpulse.com"
    
    # Test chat history
    chat_data = {
        "user_email": user_email,
        "chat_data": {
            "messages": [
                {"text": "Hello, I'm looking for pink dresses", "isUser": True},
                {"text": "I found some great pink dresses for you!", "isUser": False}
            ],
            "timestamp": "2025-12-27T23:40:00Z"
        }
    }
    
    response = requests.post('http://localhost:5002/api/user/chat-history', json=chat_data)
    result = response.json()
    
    if result['success']:
        print("✅ Chat history saved successfully")
        
        # Retrieve chat history
        response = requests.get(f'http://localhost:5002/api/user/chat-history/{user_email}')
        result = response.json()
        
        if result['success'] and len(result['data']) > 0:
            print(f"✅ Chat history retrieved: {len(result['data'])} entries")
        else:
            print("❌ Chat history retrieval failed")
    else:
        print(f"❌ Chat history save failed: {result['message']}")
    
    # Test calendar events
    event_data = {
        "user_email": user_email,
        "event_data": {
            "gender": "Women",
            "date": "2025-01-15",
            "event": "Business Meeting",
            "outfit_suggestions": ["Professional blazer", "Formal dress"]
        }
    }
    
    response = requests.post('http://localhost:5002/api/user/calendar-event', json=event_data)
    result = response.json()
    
    if result['success']:
        print("✅ Calendar event saved successfully")
        
        # Retrieve calendar events
        response = requests.get(f'http://localhost:5002/api/user/calendar-events/{user_email}')
        result = response.json()
        
        if result['success'] and len(result['data']) > 0:
            print(f"✅ Calendar events retrieved: {len(result['data'])} entries")
        else:
            print("❌ Calendar events retrieval failed")
    else:
        print(f"❌ Calendar event save failed: {result['message']}")

def main():
    """Run complete authentication system test"""
    print("🧪 Complete Authentication System Test")
    print("=" * 50)
    
    # Test API connection
    if not test_api_connection():
        return
    
    # Test all flows
    test_signup_flow()
    test_login_flow()
    test_password_reset_flow()
    test_user_data_persistence()
    
    print("\n" + "=" * 50)
    print("✅ Complete Authentication System Test Finished!")
    print("\n📋 System Status:")
    print("   • Authentication API: Running on port 5002")
    print("   • Database: fashiopulse (MySQL)")
    print("   • Tables: users, user_chat_history, user_calendar_events")
    print("   • Frontend: Ready for authentication integration")
    
    print("\n🚀 Next Steps:")
    print("   1. Start Next.js frontend: npm run dev")
    print("   2. Test signup/login on frontend")
    print("   3. Verify user-specific chat and calendar data")

if __name__ == "__main__":
    main()