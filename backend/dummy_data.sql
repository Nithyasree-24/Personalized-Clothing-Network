-- Use shopping database
USE shopping;

-- Insert dummy users (plain passwords - no hashing)
INSERT INTO users (name, email, password) VALUES
('John Doe', 'john@example.com', 'password123'),
('Jane Smith', 'jane@example.com', 'password123'),
('Mike Johnson', 'mike@example.com', 'password123'),
('Sarah Williams', 'sarah@example.com', 'password123'),
('David Brown', 'david@example.com', 'password123');

-- Insert dummy products
INSERT INTO products (title, description, price, image, category, gender) VALUES
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
('Cardigan', 'Soft knit cardigan', 799.00, 'hoodie.jpg', 'Outerwear', 'women');

-- Insert dummy orders
INSERT INTO orders (user_id, order_id, total_amount, status, shipping_address, payment_method) VALUES
(1, 'ORD12345678', 1494.00, 'completed', '123 Main St, City, State 12345', 'cod'),
(2, 'ORD12345679', 959.00, 'pending', '456 Oak Ave, Town, State 67890', 'online'),
(3, 'ORD12345680', 1351.00, 'completed', '789 Pine Rd, Village, State 11111', 'cod');

-- Insert dummy order items
INSERT INTO order_items (order_id, product_id, quantity, price) VALUES
(1, 1, 2, 745.00),
(2, 2, 1, 959.00),
(3, 3, 1, 747.00),
(3, 5, 1, 602.00);

-- Insert dummy wishlist items
INSERT INTO wishlist (user_id, product_id) VALUES
(1, 2),
(1, 4),
(2, 1),
(2, 5),
(3, 3);

-- Insert dummy cart items
INSERT INTO cart (user_id, product_id, quantity) VALUES
(1, 1, 2),
(2, 2, 1),
(3, 3, 1);

-- Show summary
SELECT 'Users' as Table_Name, COUNT(*) as Count FROM users
UNION ALL
SELECT 'Products', COUNT(*) FROM products
UNION ALL
SELECT 'Orders', COUNT(*) FROM orders
UNION ALL
SELECT 'Order Items', COUNT(*) FROM order_items
UNION ALL
SELECT 'Wishlist', COUNT(*) FROM wishlist
UNION ALL
SELECT 'Cart', COUNT(*) FROM cart;
