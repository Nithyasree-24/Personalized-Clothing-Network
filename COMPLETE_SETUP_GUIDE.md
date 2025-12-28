# 🎉 FashioPulse - Complete Setup & Verification Guide

## ✅ System Status

Your FashioPulse e-commerce platform is **READY**! Here's what's been set up:

### 📊 Database Status
- ✅ Database `shopping` created
- ✅ Table `api_cache` - Stores Amazon products locally
- ✅ Table `api_usage` - Tracks monthly API usage (0/100 calls used)
- ✅ Table `users` - User authentication
- ✅ Additional tables: cart, wishlist, orders, order_items, products

### 🔧 Backend Status
- ✅ Flask API server configured
- ✅ API caching service implemented
- ✅ Smart rate limiting (100 calls/month)
- ✅ Database integration working
- ✅ All dependencies installed

---

## 🚀 Quick Start Guide

### Step 1: Add Your RapidAPI Key

1. Go to [RapidAPI](https://rapidapi.com/)
2. Sign up/Login and subscribe to **Real-Time Amazon Data API**
3. Copy your API key
4. Open `backend/.env` file
5. Replace `your-rapidapi-key-here` with your actual key:

```env
RAPIDAPI_KEY=your-actual-rapidapi-key-here
```

### Step 2: Start the Backend Server

```bash
cd backend
python app.py
```

You should see:
```
* Running on http://0.0.0.0:5000
```

### Step 3: Start the Frontend

Open a new terminal:

```bash
npm run dev
```

Visit: http://localhost:3000

---

## 🧪 Testing the System

### Test 1: Verify Database Setup

```bash
cd backend
python test_system.py
```

Expected output: **4/5 tests passed** (5/5 after adding API key)

### Test 2: Test API Endpoints

**Check API Usage:**
```bash
curl http://localhost:5000/api/usage/stats
```

**Search Products (will use cache or API):**
```bash
curl "http://localhost:5000/api/products/search?query=shirt&category=fashion"
```

**Get Cached Products Count:**
```bash
curl http://localhost:5000/api/cache/count
```

**Fetch Fresh Products from Amazon:**
```bash
curl -X POST http://localhost:5000/api/products/fetch-fresh \
  -H "Content-Type: application/json" \
  -d '{"query": "men shirt", "category": "fashion"}'
```

---

## 📋 Available API Endpoints

### Authentication
- `POST /api/signup` - Create new user
- `POST /api/login` - User login
- `GET /api/verify` - Verify JWT token
- `GET /api/user/<id>` - Get user details

### Products
- `GET /api/products/search?query=shirt&category=fashion` - Search products
- `GET /api/products/category/<category>?gender=men&limit=20` - Get by category
- `POST /api/products/fetch-fresh` - Force fetch from Amazon API
- `GET /api/usage/stats` - Get API usage statistics
- `GET /api/cache/count` - Get cached products count

---

## 🎯 How the Smart Caching Works

### Flow Diagram:
```
User Request → Backend API
                    ↓
            Check Cache First
                    ↓
         ┌──────────┴──────────┐
         ↓                     ↓
    Cache Found          Cache Empty
         ↓                     ↓
   Return Cache      Check API Limit
                            ↓
                    ┌───────┴───────┐
                    ↓               ↓
              Under Limit      Limit Reached
                    ↓               ↓
            Call Amazon API   Return Cache
                    ↓
            Store in Database
                    ↓
            Return Products
```

### Key Features:
1. **First Request**: Calls Amazon API, stores products in database
2. **Subsequent Requests**: Returns from cache (instant, no API calls)
3. **API Limit Protection**: Automatically switches to cache when limit reached
4. **Monthly Reset**: Usage counter resets each month
5. **100 Calls/Month**: Free tier limit tracking

---

## 📊 Database Schema

### api_cache Table
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
```sql
- id (Primary Key)
- api_name (e.g., 'amazon')
- endpoint
- request_count (current month)
- last_request (timestamp)
- month_year (e.g., '2025-11')
```

---

## 🔍 Monitoring & Debugging

### Check Current API Usage:
```bash
cd backend
python -c "from api_cache_service import api_cache_service; print(api_cache_service.get_usage_stats())"
```

### Check Cached Products:
```bash
mysql -u root shopping -e "SELECT COUNT(*) as total, category, gender FROM api_cache GROUP BY category, gender;"
```

### View Recent API Calls:
```bash
mysql -u root shopping -e "SELECT * FROM api_usage ORDER BY last_request DESC LIMIT 5;"
```

---

## 🎨 Frontend Integration

The frontend automatically uses the backend API. Update `services/api.ts` if needed:

```typescript
const API_URL = 'http://localhost:5000/api';

// Search products
export async function searchProducts(query: string, category: string) {
  const response = await fetch(
    `${API_URL}/products/search?query=${query}&category=${category}`
  );
  return response.json();
}

// Get usage stats
export async function getUsageStats() {
  const response = await fetch(`${API_URL}/usage/stats`);
  return response.json();
}
```

---

## 🐛 Troubleshooting

### Issue: "Database connection failed"
**Solution:** 
- Ensure MySQL is running
- Check credentials in `backend/.env`
- Run: `python backend/init_database.py`

### Issue: "API limit reached"
**Solution:**
- System automatically uses cache
- Wait for next month for reset
- Or upgrade RapidAPI plan

### Issue: "No products returned"
**Solution:**
- Check if API key is configured
- Verify API key is valid on RapidAPI
- Check backend logs for errors
- Try fetching fresh: `POST /api/products/fetch-fresh`

### Issue: "CORS errors"
**Solution:**
- Ensure backend is running on port 5000
- Check Flask-CORS is installed
- Verify frontend is calling correct URL

---

## 📈 Usage Examples

### Example 1: Fetch Men's Shirts
```bash
curl -X POST http://localhost:5000/api/products/fetch-fresh \
  -H "Content-Type: application/json" \
  -d '{"query": "men shirt", "category": "fashion"}'
```

### Example 2: Get Cached Women's Dresses
```bash
curl "http://localhost:5000/api/products/category/fashion?gender=women&limit=10"
```

### Example 3: Check System Status
```bash
# API Usage
curl http://localhost:5000/api/usage/stats

# Cache Count
curl http://localhost:5000/api/cache/count
```

---

## 🎯 Next Steps

1. ✅ Database created and verified
2. ✅ Backend API ready
3. ⚠️  **Add RapidAPI key to `backend/.env`**
4. 🚀 Start backend: `python backend/app.py`
5. 🚀 Start frontend: `npm run dev`
6. 🧪 Test the system
7. 🎉 Start shopping!

---

## 📞 Support

If you encounter any issues:
1. Run `python backend/test_system.py` to diagnose
2. Check backend logs for errors
3. Verify all environment variables are set
4. Ensure MySQL is running

---

## 🎉 Summary

Your FashioPulse platform includes:
- ✅ Complete e-commerce frontend (React/Next.js)
- ✅ Python Flask backend with RESTful APIs
- ✅ MySQL database with smart caching
- ✅ Amazon product integration via RapidAPI
- ✅ Intelligent rate limiting (100 calls/month)
- ✅ User authentication system
- ✅ Shopping cart & wishlist
- ✅ Body shape analyzer
- ✅ AI chatbot assistant

**Everything is ready! Just add your RapidAPI key and start the servers!** 🚀
