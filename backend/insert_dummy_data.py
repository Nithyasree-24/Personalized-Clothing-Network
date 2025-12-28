import mysql.connector
from config import Config

def insert_dummy_data():
    try:
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        
        cursor = connection.cursor()
        print(f"Connected to database: {Config.DB_NAME}\n")
        
        # Insert dummy users
        users_data = [
            ('John Doe', 'john@example.com', 'password123'),
            ('Jane Smith', 'jane@example.com', 'password123'),
            ('Mike Johnson', 'mike@example.com', 'password123'),
            ('Sarah Williams', 'sarah@example.com', 'password123'),
            ('David Brown', 'david@example.com', 'password123'),
        ]
        
        for user in users_data:
            try:
                cursor.execute(
                    "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                    user
                )
            except mysql.connector.IntegrityError:
                print(f"User {user[1]} already exists, skipping...")
        
        print("✓ Inserted dummy users")
        
        # Insert dummy products
        products_data = [
            ('Classic T-Shirt', 'Comfortable cotton t-shirt', 745.00, 'tshirt.jpg', 'T-Shirts', 'men'),
            ('Summer Dress', 'Light and breezy summer dress', 959.00, 'smtshirt.jpg', 'Dresses', 'women'),
            ('Running Shoes', 'High-performance running shoes', 747.00, 'shoes.jpg', 'Sportswear', 'men'),
            ('Leather Handbag', 'Premium leather handbag', 604.00, 'handbag.jpg', 'Accessories', 'women'),
            ('Unisex Hoodie', 'Warm and cozy hoodie', 602.00, 'hoodie.jpg', 'Outerwear', 'men'),
            ('Denim Jeans', 'Classic blue denim jeans', 899.00, 'tshirt.jpg', 'Jeans', 'men'),
            ('Floral Top', 'Beautiful floral pattern top', 650.00, 'smtshirt.jpg', 'Tops', 'women'),
            ('Sports Jacket', 'Waterproof sports jacket', 1250.00, 'hoodie.jpg', 'Jackets', 'men'),
            ('Casual Pants', 'Comfortable casual pants', 799.00, 'tshirt.jpg', 'Pants', 'men'),
            ('Evening Gown', 'Elegant evening gown', 1899.00, 'smtshirt.jpg', 'Dresses', 'women'),
            ('Sneakers', 'Trendy casual sneakers', 850.00, 'shoes.jpg', 'Sportswear', 'women'),
            ('Polo Shirt', 'Classic polo shirt', 699.00, 'tshirt.jpg', 'Shirts', 'men'),
            ('Maxi Dress', 'Long flowing maxi dress', 1099.00, 'smtshirt.jpg', 'Dresses', 'women'),
            ('Leather Boots', 'Stylish leather boots', 1450.00, 'shoes.jpg', 'Footwear', 'women'),
            ('Cardigan', 'Soft knit cardigan', 799.00, 'hoodie.jpg', 'Outerwear', 'women'),
        ]
        
        for product in products_data:
            cursor.execute(
                "INSERT INTO products (title, description, price, image, category, gender) VALUES (%s, %s, %s, %s, %s, %s)",
                product
            )
        
        print("✓ Inserted dummy products")
        
        # Insert dummy orders
        orders_data = [
            (1, 'ORD12345678', 1494.00, 'completed', '123 Main St, City, State 12345', 'cod'),
            (2, 'ORD12345679', 959.00, 'pending', '456 Oak Ave, Town, State 67890', 'online'),
            (3, 'ORD12345680', 1351.00, 'completed', '789 Pine Rd, Village, State 11111', 'cod'),
        ]
        
        for order in orders_data:
            cursor.execute(
                "INSERT INTO orders (user_id, order_id, total_amount, status, shipping_address, payment_method) VALUES (%s, %s, %s, %s, %s, %s)",
                order
            )
        
        print("✓ Inserted dummy orders")
        
        # Insert dummy order items
        order_items_data = [
            (1, 1, 2, 745.00),  # Order 1: 2x Classic T-Shirt
            (2, 2, 1, 959.00),  # Order 2: 1x Summer Dress
            (3, 3, 1, 747.00),  # Order 3: 1x Running Shoes
            (3, 5, 1, 602.00),  # Order 3: 1x Hoodie
        ]
        
        for item in order_items_data:
            cursor.execute(
                "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
                item
            )
        
        print("✓ Inserted dummy order items")
        
        # Insert dummy wishlist items
        wishlist_data = [
            (1, 2),  # John likes Summer Dress
            (1, 4),  # John likes Handbag
            (2, 1),  # Jane likes T-Shirt
            (2, 5),  # Jane likes Hoodie
            (3, 3),  # Mike likes Running Shoes
        ]
        
        for item in wishlist_data:
            try:
                cursor.execute(
                    "INSERT INTO wishlist (user_id, product_id) VALUES (%s, %s)",
                    item
                )
            except mysql.connector.IntegrityError:
                pass
        
        print("✓ Inserted dummy wishlist items")
        
        # Insert dummy cart items
        cart_data = [
            (1, 1, 2),  # John has 2x T-Shirt in cart
            (2, 2, 1),  # Jane has 1x Summer Dress in cart
            (3, 3, 1),  # Mike has 1x Running Shoes in cart
        ]
        
        for item in cart_data:
            try:
                cursor.execute(
                    "INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, %s)",
                    item
                )
            except mysql.connector.IntegrityError:
                pass
        
        print("✓ Inserted dummy cart items")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print("\n✅ All dummy data inserted successfully!")
        print("\n📝 Test Login Credentials:")
        print("Email: john@example.com | Password: password123")
        print("Email: jane@example.com | Password: password123")
        print("Email: mike@example.com | Password: password123")
        print("Email: sarah@example.com | Password: password123")
        print("Email: david@example.com | Password: password123")
        
    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")

if __name__ == "__main__":
    insert_dummy_data()
