#!/usr/bin/env python3
"""
Check Clothing Table Structure
"""

import mysql.connector

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'fashiopulse'
}

def check_clothing_table():
    """Check the clothing table structure and data"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        print("🔍 Checking clothing table structure...")
        
        # Check if clothing table exists
        cursor.execute("SHOW TABLES LIKE 'clothing'")
        table_exists = cursor.fetchone()
        
        if not table_exists:
            print("❌ 'clothing' table does not exist")
            
            # Check what tables exist
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"\n📋 Available tables:")
            for table in tables:
                table_name = list(table.values())[0]
                print(f"   - {table_name}")
            
            cursor.close()
            conn.close()
            return False
        
        print("✅ 'clothing' table exists")
        
        # Get table structure
        cursor.execute("DESCRIBE clothing")
        columns = cursor.fetchall()
        
        print(f"\n📊 Table structure:")
        for col in columns:
            print(f"   {col['Field']} - {col['Type']} - {col['Null']} - {col['Key']}")
        
        # Count records
        cursor.execute("SELECT COUNT(*) as count FROM clothing")
        count = cursor.fetchone()
        print(f"\n📦 Total records: {count['count']}")
        
        # Get sample data
        cursor.execute("SELECT * FROM clothing LIMIT 5")
        samples = cursor.fetchall()
        
        if samples:
            print(f"\n📝 Sample records:")
            for i, sample in enumerate(samples, 1):
                print(f"\n   Record {i}:")
                for key, value in sample.items():
                    print(f"     {key}: {value}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    check_clothing_table()