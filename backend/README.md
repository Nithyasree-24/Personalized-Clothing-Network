# FashioPulse Backend API

Smart e-commerce backend with Amazon product caching and intelligent rate limiting.

---

## ✅ Quick Status Check

Run this to verify everything is working:
```bash
python test_system.py
```

Expected: **4/5 tests passed** (5/5 after adding API key)

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Setup Database
```bash
python init_database.py
```

This creates:
- Database: `shopping`
- Tables: `api_cache`, `api_usage`, `users`

### 3. Configure API Key

Edit `.env` file and add your RapidAPI key:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=shopping
JWT_SECRET=fashiopulse-secret-key-2024
PORT=5000
RAPIDAPI_KEY=your-actual-rapidapi-key-here
```

Get your key from: https://rapidapi.com/

### 4. Test the System
```bash
python quick_test.py
```

This will:
- Check database connection
- Verify API key
- Show current usage (0/100)
- Optionally fetch test products

### 5. Start the Server
```bash
python app.py
```

Server runs on: **http://localhost:5000**

---

## 📋 API Endpoints

### Products API

#### GET /api/products/search
Search products (uses cache or API)
```bash
curl "http://localhost:5000/api/products/search?query=shirt&category=fashion"
```

#### POST /api/products/fetch-fresh
Force fetch from Amazon API
```bash
curl -X POST http://localhost:5000/api/products/fetch-fresh \
  -H "Content-Type: application/json" \
  -d '{"query": "men shirt", "category": "fashion"}'
```

#### GET /api/products/category/:category
Get products by category
```bash
curl "http://localhost:5000/api/products/category/fashion?gender=men&limit=20"
```

#### GET /api/usage/stats
Get API usage statistics
```bash
curl http://localhost:5000/api/usage/stats
```

Response:
```json
{
  "current_usage": 5,
  "monthly_limit": 100,
  "remaining": 95,
  "percentage": 5.0,
  "month_year": "2025-11",
  "can_make_call": true
}
```

#### GET /api/cache/count
Get cached products count
```bash
curl http://localhost:5000/api/cache/count
```

### Authentication API

#### POST /api/signup
Register new user
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123"
}
```

#### POST /api/login
User login
```json
{
  "email": "john@example.com",
  "password": "password123"
}
```

#### GET /api/verify
Verify JWT token (send token in Authorization header)

#### GET /api/user/:id
Get user details by ID

---

## 🎯 How the Smart Caching Works

### Flow:
```
User Request
    ↓
Check Cache First
    ↓
┌───────┴───────┐
↓               ↓
Found       Not Found
↓               ↓
Return      Check API Limit
Cache           ↓
            ┌───┴───┐
            ↓       ↓
        Under   Over
        Limit   Limit
            ↓       ↓
        Call    Return
        API     Cache
            ↓
        Store in DB
            ↓
        Return Products
```

### Features:
- ✅ **First search:** Calls API + stores in database
- ✅ **Future searches:** Returns from cache (instant!)
- ✅ **API protection:** Auto-switches to cache when limit reached
- ✅ **Monthly reset:** Usage counter resets each month
- ✅ **100 calls/month:** Free tier tracking

---

## 📊 Database Schema

### api_cache Table
Stores Amazon products locally
```sql
- id (Primary Key)
- product_id (Unique)
- title
- price
- image_url
- category
- gender (men/women/kids/unisex)
- source (amazon)
- product_url
- rating
- description
- cached_at (timestamp)
```

### api_usage Table
Tracks monthly API calls
```sql
- id (Primary Key)
- api_name (e.g., 'amazon')
- endpoint
- request_count (current month)
- last_request (timestamp)
- month_year (e.g., '2025-11')
```

### users Table
User authentication
```sql
- id (Primary Key)
- name
- email (Unique)
- password
- created_at
- updated_at
```

---

## 🧪 Testing

### Full System Test
```bash
python test_system.py
```

Checks:
- Database connection
- Table structures
- API usage tracking
- Cached products
- API key configuration

### Quick Product Test
```bash
python quick_test.py
```

Interactive test that:
- Verifies API key
- Shows current usage
- Optionally fetches products
- Displays sample results

### Manual API Tests
```bash
# Check usage
curl http://localhost:5000/api/usage/stats

# Search products
curl "http://localhost:5000/api/products/search?query=shirt"

# Fetch fresh
curl -X POST http://localhost:5000/api/products/fetch-fresh \
  -H "Content-Type: application/json" \
  -d '{"query": "dress", "category": "fashion"}'

# Check cache
curl http://localhost:5000/api/cache/count
```

---

## 🔍 Monitoring

### Check API Usage
```bash
python -c "from api_cache_service import api_cache_service; print(api_cache_service.get_usage_stats())"
```

### Check Cached Products
```bash
mysql -u root shopping -e "SELECT COUNT(*) as total, category FROM api_cache GROUP BY category;"
```

### View Recent API Calls
```bash
mysql -u root shopping -e "SELECT * FROM api_usage ORDER BY last_request DESC;"
```

---

## 🐛 Troubleshooting

### Database Connection Failed
```bash
# Re-initialize database
python init_database.py

# Check MySQL is running
# Start XAMPP/MySQL service
```

### API Key Not Working
```bash
# Verify key in .env
cat .env | grep RAPIDAPI_KEY

# Test with quick_test.py
python quick_test.py
```

### No Products Returned
```bash
# Check if products are cached
curl http://localhost:5000/api/cache/count

# Force fetch fresh
curl -X POST http://localhost:5000/api/products/fetch-fresh \
  -H "Content-Type: application/json" \
  -d '{"query": "shirt", "category": "fashion"}'
```

---

## 📦 Dependencies

- Flask 3.0.0 - Web framework
- Flask-CORS 4.0.0 - CORS support
- mysql-connector-python 8.2.0 - MySQL driver
- PyJWT 2.8.0 - JWT authentication
- python-dotenv 1.0.0 - Environment variables
- requests 2.31.0 - HTTP client

---

## 🎉 Summary

Your backend includes:
- ✅ RESTful API with Flask
- ✅ MySQL database integration
- ✅ Smart product caching system
- ✅ Amazon API integration
- ✅ Rate limiting (100 calls/month)
- ✅ JWT authentication
- ✅ Automatic cache fallback

**Ready to use! Just add your RapidAPI key and start the server.**
