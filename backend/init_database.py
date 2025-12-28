import mysql.connector
from config import Config

def init_database():
    try:
        # Connect to MySQL server (without database)
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        )
        
        cursor = connection.cursor()
        
        # Create database if not exists
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.DB_NAME}")
        print(f"✓ Database '{Config.DB_NAME}' ready")
        
        cursor.close()
        connection.close()
        
        # Now connect to the database
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        
        cursor = connection.cursor()
        
        # Create api_cache table for storing Amazon products
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS api_cache (
                id INT AUTO_INCREMENT PRIMARY KEY,
                product_id VARCHAR(100) UNIQUE NOT NULL,
                title VARCHAR(500) NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                image_url TEXT,
                category VARCHAR(100),
                gender VARCHAR(20),
                source VARCHAR(50) DEFAULT 'amazon',
                product_url TEXT,
                rating DECIMAL(3, 2),
                description TEXT,
                cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_category (category),
                INDEX idx_gender (gender),
                INDEX idx_source (source)
            )
        """)
        print("✓ Created api_cache table")
        
        # Create api_usage table to track API calls
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS api_usage (
                id INT AUTO_INCREMENT PRIMARY KEY,
                api_name VARCHAR(50) NOT NULL,
                endpoint VARCHAR(200),
                request_count INT DEFAULT 1,
                last_request TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                month_year VARCHAR(7) NOT NULL,
                UNIQUE KEY unique_usage (api_name, month_year)
            )
        """)
        print("✓ Created api_usage table")
        
        # Create users table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)
        print("✓ Created users table")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print("\n✅ Database initialization complete!")
        print(f"Database: {Config.DB_NAME}")
        print("Tables: api_cache, api_usage, users")
        
    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")

if __name__ == "__main__":
    init_database()
