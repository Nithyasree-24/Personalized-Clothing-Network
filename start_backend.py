#!/usr/bin/env python3
"""
Quick start script for the backend server
"""
import subprocess
import sys
import os

def check_requirements():
    """Check if required packages are installed"""
    try:
        import flask
        import flask_cors
        import pymysql
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Installing required packages...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "flask-cors", "pymysql", "python-dotenv", "pyjwt"])
            print("✅ Packages installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages")
            return False

def start_backend():
    """Start the backend server"""
    if not check_requirements():
        return
    
    # Change to backend directory
    os.chdir("backend")
    
    print("🚀 Starting FashionPulse Backend Server...")
    print("📍 Server will run on: http://localhost:5000")
    print("🔗 Frontend should connect to: http://localhost:5000/api")
    print("📊 Database: fashiopulse (MySQL)")
    print("\n" + "="*50)
    
    # Start the Flask app
    try:
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server error: {e}")

if __name__ == "__main__":
    start_backend()