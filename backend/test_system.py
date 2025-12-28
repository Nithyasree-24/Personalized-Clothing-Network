"""
Test script to verify database and API caching system
"""
import mysql.connector
from config import Config
from api_cache_service import api_cache_service

def test_database_connection():
    """Test database connection"""
    print("\n" + "="*50)
    print("1. TESTING DATABASE CONNECTION")
    print("="*50)
    try:
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        print("✅ Database connection successful!")
        
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        print(f"\n📋 Tables in database '{Config.DB_NAME}':")
        for table in tables:
            print(f"   - {table[0]}")
        
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_tables_structure():
    """Test if all required tables exist with correct structure"""
    print("\n" + "="*50)
    print("2. TESTING TABLE STRUCTURES")
    print("="*50)
    try:
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        cursor = connection.cursor()
        
        # Check api_cache table
        cursor.execute("DESCRIBE api_cache")
        print("\n✅ api_cache table structure:")
        for row in cursor.fetchall():
            print(f"   {row[0]}: {row[1]}")
        
        # Check api_usage table
        cursor.execute("DESCRIBE api_usage")
        print("\n✅ api_usage table structure:")
        for row in cursor.fetchall():
            print(f"   {row[0]}: {row[1]}")
        
        # Check users table
        cursor.execute("DESCRIBE users")
        print("\n✅ users table structure:")
        for row in cursor.fetchall():
            print(f"   {row[0]}: {row[1]}")
        
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print(f"❌ Table structure test failed: {e}")
        return False

def test_api_usage_tracking():
    """Test API usage tracking"""
    print("\n" + "="*50)
    print("3. TESTING API USAGE TRACKING")
    print("="*50)
    try:
        stats = api_cache_service.get_usage_stats()
        print(f"\n📊 API Usage Statistics:")
        print(f"   Month: {stats['month_year']}")
        print(f"   Current Usage: {stats['current_usage']}/{stats['monthly_limit']}")
        print(f"   Remaining: {stats['remaining']}")
        print(f"   Percentage: {stats['percentage']:.1f}%")
        print(f"   Can Make Call: {'✅ Yes' if stats['can_make_call'] else '❌ No'}")
        return True
    except Exception as e:
        print(f"❌ API usage tracking test failed: {e}")
        return False

def test_cache_count():
    """Test cached products count"""
    print("\n" + "="*50)
    print("4. TESTING CACHED PRODUCTS")
    print("="*50)
    try:
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        cursor = connection.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM api_cache")
        count = cursor.fetchone()[0]
        print(f"\n💾 Total cached products: {count}")
        
        if count > 0:
            cursor.execute("SELECT category, COUNT(*) as count FROM api_cache GROUP BY category")
            print("\n📦 Products by category:")
            for row in cursor.fetchall():
                print(f"   {row[0]}: {row[1]} products")
            
            cursor.execute("SELECT gender, COUNT(*) as count FROM api_cache GROUP BY gender")
            print("\n👥 Products by gender:")
            for row in cursor.fetchall():
                print(f"   {row[0]}: {row[1]} products")
        
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print(f"❌ Cache count test failed: {e}")
        return False

def test_api_key_configured():
    """Test if RapidAPI key is configured"""
    print("\n" + "="*50)
    print("5. TESTING API KEY CONFIGURATION")
    print("="*50)
    if Config.RAPIDAPI_KEY and Config.RAPIDAPI_KEY != 'your-rapidapi-key-here':
        print(f"✅ RapidAPI Key configured: {Config.RAPIDAPI_KEY[:10]}...")
        return True
    else:
        print("⚠️  RapidAPI Key not configured!")
        print("   Please add your key to backend/.env file:")
        print("   RAPIDAPI_KEY=your-actual-key-here")
        return False

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 FASHIOPULSE SYSTEM TEST")
    print("="*60)
    
    results = []
    results.append(("Database Connection", test_database_connection()))
    results.append(("Table Structures", test_tables_structure()))
    results.append(("API Usage Tracking", test_api_usage_tracking()))
    results.append(("Cached Products", test_cache_count()))
    results.append(("API Key Configuration", test_api_key_configured()))
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! System is ready to use.")
        print("\n📝 Next steps:")
        print("   1. Add your RapidAPI key to backend/.env (if not done)")
        print("   2. Start the backend: python backend/app.py")
        print("   3. Test API endpoint: http://localhost:5000/api/products/search?query=shirt")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")

if __name__ == "__main__":
    run_all_tests()
