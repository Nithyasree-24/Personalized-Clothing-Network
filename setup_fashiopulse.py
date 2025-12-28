#!/usr/bin/env python3
"""
FashionPulse Complete Setup Script
This script will:
1. Install required Python packages
2. Test database connection
3. Start the backend server
4. Provide instructions for frontend
"""
import subprocess
import sys
import os
import time

def install_packages():
    """Install required Python packages"""
    print("📦 Installing required packages...")
    packages = [
        "flask",
        "flask-cors", 
        "pymysql",
        "python-dotenv",
        "pyjwt",
        "requests"
    ]
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install"
        ] + packages)
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install packages")
        return False

def test_database():
    """Test database connection"""
    print("\n🔍 Testing database connection...")
    
    # Add backend to path
    sys.path.append('backend')
    
    try:
        from backend.db import execute_query
        from backend.config import Config
        
        # Test connection
        result = execute_query("SELECT COUNT(*) as count FROM clothing", fetch=True)
        if result:
            count = result[0]['count']
            print(f"✅ Database connected! Found {count} products in clothing table")
            return True
        else:
            print("❌ Database connection failed")
            return False
            
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def start_backend_server():
    """Start the Flask backend server"""
    print("\n🚀 Starting FashionPulse Backend Server...")
    print("📍 Server URL: http://localhost:5000")
    print("🔗 API Base: http://localhost:5000/api")
    print("📊 Database: fashiopulse (MySQL)")
    print("\n" + "="*60)
    print("🎯 Backend is now ready to serve products to frontend!")
    print("="*60)
    
    # Change to backend directory
    os.chdir("backend")
    
    try:
        # Start Flask app
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped")

def main():
    """Main setup function"""
    print("🎨 FashionPulse Setup & Connection Script")
    print("="*50)
    
    # Step 1: Install packages
    if not install_packages():
        return
    
    # Step 2: Test database
    if not test_database():
        print("\n🔧 Database Connection Issues:")
        print("1. Make sure MySQL/XAMPP is running")
        print("2. Check if 'fashiopulse' database exists")
        print("3. Verify the clothing table has data")
        print("4. Check database credentials in backend/config.py")
        return
    
    # Step 3: Show connection info
    print("\n🔗 Connection Summary:")
    print("Frontend (Next.js) ➡️  Backend (Flask) ➡️  Database (MySQL)")
    print("     localhost:3000  ➡️   localhost:5000  ➡️   fashiopulse")
    
    print("\n📋 Next Steps:")
    print("1. Keep this terminal open (backend server)")
    print("2. Open a new terminal")
    print("3. Run: npm run dev (to start frontend)")
    print("4. Visit: http://localhost:3000")
    
    # Step 4: Start backend
    input("\n⏳ Press Enter to start the backend server...")
    start_backend_server()

if __name__ == "__main__":
    main()