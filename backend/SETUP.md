# Quick Setup Guide for Existing Shopping Database

## Step 1: Create Tables in Your Existing Database

1. Open phpMyAdmin (http://localhost/phpmyadmin)
2. Select your existing `shopping` database from the left sidebar
3. Click on the "SQL" tab
4. Copy and paste the contents of `create_tables.sql`
5. Click "Go" to execute

This will create these tables:
- `users` - For login/signup
- `products` - Product catalog
- `orders` - Order history
- `order_items` - Order details
- `wishlist` - User wishlists
- `cart` - Shopping cart

## Step 2: Setup Backend Environment

1. Create a `.env` file in the backend folder:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=shopping
JWT_SECRET=fashiopulse-secret-key-2024
PORT=5000
```

2. Install Python dependencies:
```bash
cd backend
pip install -r requirements.txt
```

## Step 3: Run the Backend Server

```bash
python app.py
```

Server will start at: http://localhost:5000

## Step 4: Test the API

### Test Signup:
```bash
curl -X POST http://localhost:5000/api/signup \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","password":"password123"}'
```

### Test Login:
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

## Step 5: Update Frontend

The frontend API service is already created in `services/api.ts`. 

To use it in your login/signup pages, import and use the functions:

```typescript
import { login, signup, saveToken, saveUser } from '../../services/api';

// In your login handler:
const response = await login({ email, password });
saveToken(response.token);
saveUser(response.user);
```

## Troubleshooting

- **Port already in use**: Change PORT in .env file
- **Database connection error**: Check XAMPP MySQL is running
- **CORS error**: Make sure Flask-CORS is installed
- **Import error**: Run `pip install -r requirements.txt` again
