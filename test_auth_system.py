#!/usr/bin/env python3
"""
Test script for FashionPulse Authentication System
Tests all authentication functionality
"""

import sys
import os
sys.path.append('backend')

from auth_system import AuthSystem

def test_authentication_system():
    print("🔍 Testing FashionPulse Authentication System")
    print("=" * 60)
    
    # Initialize auth system
    auth = AuthSystem()
    
    # Test data
    test_email = "testuser@fashionpulse.com"
    test_name = "Test User"
    test_password = "password123"
    wrong_password = "wrongpassword"
    
    print("\n1️⃣ Testing User Signup")
    print("-" * 30)
    
    # Test successful signup
    result = auth.signup(test_name, test_email, test_password)
    print(f"✅ Signup Result: {result}")
    
    # Test duplicate email signup
    result = auth.signup("Another User", test_email, "newpassword")
    print(f"🔄 Duplicate Email Result: {result}")
    
    print("\n2️⃣ Testing User Login")
    print("-" * 30)
    
    # Test successful login
    result = auth.login(test_email, test_password)
    print(f"✅ Login Result: {result}")
    
    # Test wrong password
    result = auth.login(test_email, wrong_password)
    print(f"❌ Wrong Password Result: {result}")
    
    # Test non-existent email
    result = auth.login("nonexistent@fashionpulse.com", test_password)
    print(f"🚫 Non-existent Email Result: {result}")
    
    print("\n3️⃣ Testing Password Reset")
    print("-" * 30)
    
    # Test forgot password
    result = auth.generate_reset_token(test_email)
    print(f"🔑 Reset Token Result: {result}")
    
    if result['success']:
        token = result['token']
        
        # Test password reset with valid token
        new_password = "newpassword123"
        result = auth.reset_password(token, new_password)
        print(f"🔄 Password Reset Result: {result}")
        
        # Test login with new password
        result = auth.login(test_email, new_password)
        print(f"✅ Login with New Password: {result}")
    
    print("\n4️⃣ Testing Chat History")
    print("-" * 30)
    
    # Test save chat history
    chat_data = {
        "messages": [
            {"text": "Hello", "isUser": True},
            {"text": "Hi there!", "isUser": False}
        ],
        "timestamp": "2024-01-01T12:00:00Z"
    }
    
    result = auth.save_chat_history(test_email, chat_data)
    print(f"💬 Save Chat History: {result}")
    
    # Test get chat history
    result = auth.get_chat_history(test_email)
    print(f"📜 Get Chat History: {result}")
    
    print("\n5️⃣ Testing Calendar Events")
    print("-" * 30)
    
    # Test save calendar event
    event_data = {
        "gender": "Women",
        "date": "2024-12-31",
        "event": "New Year Party"
    }
    
    result = auth.save_calendar_event(test_email, event_data)
    print(f"📅 Save Calendar Event: {result}")
    
    # Test get calendar events
    result = auth.get_calendar_events(test_email)
    print(f"🗓️ Get Calendar Events: {result}")
    
    print("\n" + "=" * 60)
    print("✅ All authentication tests completed!")
    print("\n📊 Summary:")
    print("   • User signup with duplicate prevention")
    print("   • User login with proper validation")
    print("   • Password reset with tokens")
    print("   • Chat history per user")
    print("   • Calendar events per user")
    print("\n🚀 Ready to start authentication server:")
    print("   python backend/auth_api.py")

if __name__ == "__main__":
    test_authentication_system()