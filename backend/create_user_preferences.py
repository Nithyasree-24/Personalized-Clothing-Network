import mysql.connector
from config import Config

def create_user_preferences_table():
    """Create user_preferences table for storing style preferences"""
    try:
        conn = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        cursor = conn.cursor()
        
        # Create user_preferences table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                style_casual BOOLEAN DEFAULT FALSE,
                style_formal BOOLEAN DEFAULT FALSE,
                style_sporty BOOLEAN DEFAULT FALSE,
                style_ethnic BOOLEAN DEFAULT FALSE,
                style_trendy BOOLEAN DEFAULT FALSE,
                style_classic BOOLEAN DEFAULT FALSE,
                preferred_colors TEXT,
                price_range VARCHAR(50),
                favorite_categories TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                UNIQUE KEY unique_user_pref (user_id)
            )
        """)
        
        print("✅ user_preferences table created successfully")
        
        # Create user_behavior table for tracking interactions
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_behavior (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                product_id VARCHAR(100) NOT NULL,
                action_type ENUM('view', 'cart', 'wishlist', 'purchase') NOT NULL,
                action_count INT DEFAULT 1,
                last_action_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                INDEX idx_user_product (user_id, product_id),
                INDEX idx_action_type (action_type)
            )
        """)
        
        print("✅ user_behavior table created successfully")
        
        # Create avatar_data table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS avatar_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                gender ENUM('men', 'women', 'kids') NOT NULL,
                skin_tone VARCHAR(20),
                hair_style VARCHAR(50),
                hair_color VARCHAR(20),
                face_shape VARCHAR(20),
                body_type VARCHAR(20),
                avatar_json TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                UNIQUE KEY unique_user_avatar (user_id)
            )
        """)
        
        print("✅ avatar_data table created successfully")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n🎉 All tables created successfully!")
        
    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")

if __name__ == "__main__":
    create_user_preferences_table()
