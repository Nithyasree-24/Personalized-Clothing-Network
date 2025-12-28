from db import execute_query

def create_reviews_table():
    """Create reviews table if it doesn't exist"""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS reviews (
        id INT AUTO_INCREMENT PRIMARY KEY,
        product_id VARCHAR(255) NOT NULL,
        user_id INT NOT NULL,
        rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
        comment TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        INDEX idx_product_id (product_id),
        INDEX idx_user_id (user_id)
    )
    """
    
    try:
        execute_query(create_table_query)
        print("✅ Reviews table created successfully!")
        
        # Add some sample reviews
        sample_reviews = [
            ("B0CQK8N5VF", 1, 5, "Excellent quality! Fits perfectly and looks great."),
            ("B0CQK8N5VF", 1, 4, "Good product, fast delivery. Slightly expensive but worth it."),
            ("B0D91RDKLC", 1, 5, "Love this! Very comfortable and stylish."),
            ("B0D91RDKLC", 1, 3, "Decent product but color was slightly different from picture."),
        ]
        
        for product_id, user_id, rating, comment in sample_reviews:
            execute_query(
                "INSERT INTO reviews (product_id, user_id, rating, comment) VALUES (%s, %s, %s, %s)",
                (product_id, user_id, rating, comment)
            )
        
        print("✅ Sample reviews added!")
        
    except Exception as e:
        print(f"❌ Error creating reviews table: {e}")

if __name__ == "__main__":
    create_reviews_table()
