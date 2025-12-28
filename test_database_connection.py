#!/usr/bin/env python3
"""
Test database connection and display products
"""
import sys
import os

# Add backend directory to path
sys.path.append('backend')

try:
    from backend.db import execute_query
    from backend.config import Config
    
    print("🔍 Testing FashionPulse Database Connection...")
    print(f"📊 Database: {Config.DB_NAME}")
    print(f"🏠 Host: {Config.DB_HOST}")
    print(f"👤 User: {Config.DB_USER}")
    print("="*50)
    
    # Test basic connection
    result = execute_query("SELECT 1 as test", fetch=True)
    if result:
        print("✅ Database connection successful!")
    else:
        print("❌ Database connection failed!")
        sys.exit(1)
    
    # Check if clothing table exists
    tables = execute_query("SHOW TABLES LIKE 'clothing'", fetch=True)
    if tables:
        print("✅ Clothing table exists!")
    else:
        print("❌ Clothing table not found!")
        sys.exit(1)
    
    # Count products
    count_result = execute_query("SELECT COUNT(*) as count FROM clothing", fetch=True)
    if count_result:
        product_count = count_result[0]['count']
        print(f"📦 Total products in database: {product_count}")
    
    # Show sample products
    if product_count > 0:
        print("\n🛍️ Sample Products:")
        print("-" * 80)
        sample_products = execute_query(
            "SELECT product_id, product_name, price, product_category, gender FROM clothing LIMIT 5", 
            fetch=True
        )
        
        for product in sample_products:
            print(f"ID: {product['product_id']} | {product['product_name'][:40]:<40} | ₹{product['price']:<8} | {product['product_category']:<15} | {product['gender']}")
    
    print("\n" + "="*50)
    print("🎉 Database is ready for frontend connection!")
    print("🚀 You can now start the backend server with: python start_backend.py")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Installing required packages...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pymysql", "flask", "flask-cors", "python-dotenv", "pyjwt"])
    print("✅ Packages installed. Please run the script again.")
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n🔧 Troubleshooting:")
    print("1. Make sure MySQL is running")
    print("2. Check if 'fashiopulse' database exists")
    print("3. Verify database credentials in backend/config.py")
    print("4. Ensure clothing table has data")