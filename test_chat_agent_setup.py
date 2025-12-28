#!/usr/bin/env python3
"""
Quick test for FashionPulse Chat Agent setup
"""
import sys
import os

# Add chat_agent to path
sys.path.append('chat_agent')

def test_imports():
    """Test if all modules can be imported"""
    print("🧪 Testing Chat Agent Imports...")
    
    try:
        from chat_agent.config import ChatAgentConfig
        print("✅ Config imported")
        
        from chat_agent.database import DatabaseHandler
        print("✅ Database handler imported")
        
        from chat_agent.query_parser import QueryParser
        print("✅ Query parser imported")
        
        from chat_agent.response_formatter import ResponseFormatter
        print("✅ Response formatter imported")
        
        from chat_agent.chat_agent import FashionPulseChatAgent
        print("✅ Chat agent imported")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_basic_functionality():
    """Test basic chat agent functionality"""
    print("\n🔍 Testing Basic Functionality...")
    
    try:
        from chat_agent.chat_agent import FashionPulseChatAgent
        
        # Initialize agent
        agent = FashionPulseChatAgent()
        
        # Test greeting
        response = agent.process_message("Hi")
        print(f"✅ Greeting test: {len(response)} chars response")
        
        # Test search query
        response = agent.process_message("show me dresses")
        print(f"✅ Search test: {len(response)} chars response")
        
        # Close agent
        agent.close()
        
        return True
    except Exception as e:
        print(f"❌ Functionality test error: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    print("\n🔌 Testing Database Connection...")
    
    try:
        from chat_agent.database import DatabaseHandler
        
        db = DatabaseHandler()
        if db.connect():
            print("✅ Database connection successful")
            
            # Test query
            result = db.execute_query("SELECT COUNT(*) as count FROM clothing")
            if result:
                count = result[0]['count']
                print(f"✅ Found {count} products in database")
            
            db.disconnect()
            return True
        else:
            print("❌ Database connection failed")
            return False
    except Exception as e:
        print(f"❌ Database test error: {e}")
        return False

def main():
    """Run all tests"""
    print("🤖 FashionPulse Chat Agent Setup Test")
    print("="*50)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed. Please install requirements:")
        print("pip install -r chat_agent/requirements.txt")
        return
    
    # Test database
    if not test_database_connection():
        print("\n❌ Database tests failed. Please check:")
        print("1. MySQL is running")
        print("2. fashiopulse database exists")
        print("3. clothing table has data")
        return
    
    # Test functionality
    if not test_basic_functionality():
        print("\n❌ Functionality tests failed")
        return
    
    print("\n🎉 All tests passed! Chat agent is ready to use!")
    print("\n🚀 Next steps:")
    print("1. Run: python start_chat_agent.py")
    print("2. Or start API server: cd chat_agent && python api_server.py")
    print("3. Test API: POST http://localhost:5001/api/chat")

if __name__ == "__main__":
    main()