#!/usr/bin/env python3
"""
Startup script for FashionPulse Chat Agent
"""
import subprocess
import sys
import os

def install_requirements():
    """Install chat agent requirements"""
    print("📦 Installing chat agent requirements...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "-r", "chat_agent/requirements.txt"
        ])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        return False

def test_chat_agent():
    """Test the chat agent"""
    print("\n🧪 Testing chat agent...")
    try:
        # Add chat_agent to Python path
        sys.path.append('chat_agent')
        
        from chat_agent.test_chat_agent import test_database_connection
        test_database_connection()
        print("✅ Chat agent test passed!")
        return True
    except Exception as e:
        print(f"❌ Chat agent test failed: {e}")
        return False

def start_api_server():
    """Start the chat agent API server"""
    print("\n🚀 Starting FashionPulse Chat Agent API Server...")
    print("📍 Server will run on: http://localhost:5001")
    print("🔗 Main endpoint: POST http://localhost:5001/api/chat")
    print("📚 Help: GET http://localhost:5001/api/chat/help")
    print("\n" + "="*60)
    
    try:
        # Change to chat_agent directory and run server
        os.chdir("chat_agent")
        subprocess.run([sys.executable, "api_server.py"])
    except KeyboardInterrupt:
        print("\n🛑 Chat agent server stopped")
    except Exception as e:
        print(f"❌ Server error: {e}")

def main():
    """Main startup function"""
    print("🤖 FashionPulse Chat Agent Startup")
    print("="*50)
    
    # Step 1: Install requirements
    if not install_requirements():
        return
    
    # Step 2: Test chat agent
    if not test_chat_agent():
        print("\n⚠️ Tests failed, but you can still try running the server...")
    
    # Step 3: Show usage info
    print("\n📋 Chat Agent Features:")
    print("• Natural language product search")
    print("• Live database integration")
    print("• Smart query understanding")
    print("• Fashion-focused responses")
    print("• REST API for frontend integration")
    
    print("\n💬 Example Queries:")
    print("• 'Show me red dresses under ₹2000'")
    print("• 'Find jeans for men'")
    print("• 'Looking for ethnic wear for women'")
    print("• 'Blue shirts under ₹1500'")
    
    # Step 4: Start server
    input("\n⏳ Press Enter to start the chat agent API server...")
    start_api_server()

if __name__ == "__main__":
    main()