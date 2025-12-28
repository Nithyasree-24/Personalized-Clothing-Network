# 🚀 Quick Setup Guide - Get Products Showing

## ⚠️ Current Issue

The home page shows "No products found" because the RapidAPI key is not configured.

---

## ✅ Solution (5 Minutes)

### Step 1: Get RapidAPI Key

1. Go to https://rapidapi.com/
2. Sign up or log in
3. Search for **"Real-Time Amazon Data"**
4. Subscribe to the **FREE plan** (100 calls/month)
5. Copy your API key

### Step 2: Add API Key to Backend

1. Open `backend/.env` file
2. Replace this line:
   ```env
   RAPIDAPI_KEY=your-rapidapi-key-here
   ```
   
   With your actual key:
   ```env
   RAPIDAPI_KEY=abc123xyz456...
   ```

3. Save the file

### Step 3: Restart Backend

```bash
# Stop the current backend (Ctrl+C)
# Then restart:
cd backend
python app.py
```

### Step 4: Fetch Products

1. Go to http://localhost:3000/home
2. Click the **"Fetch Products from API"** button
3. Wait for products to load
4. Products will be saved to database
5. Future visits will load instantly from cache!

---

## 🎯 What Happens After Setup

### First Time:
```
Click "Fetch Products" button
        ↓
Backend calls Amazon API
        ↓
Uses 1 API call (99 remaining)
        ↓
Stores ~20 products in database
        ↓
Displays products on page
        ↓
Counter shows: 1/100
```

### Next Time:
```
Visit home page
        ↓
Backend checks database
        ↓
Finds cached products
        ↓
Returns instantly (NO API call)
        ↓
Displays products
        ↓
Counter still shows: 1/100
```

---

## 📊 Alternative: Use Test Data

If you don't want to use RapidAPI, you can manually add test products to the database:

```sql
-- Connect to MySQL
mysql -u root shopping

-- Insert test products
INSERT INTO api_cache (product_id, title, price, image_url, category, gender, source, product_url, rating, description) VALUES
('TEST001', 'Men Cotton T-Shirt', 29.99, 'https://via.placeholder.com/300', 'fashion', 'men', 'amazon', '#', 4.5, 'Comfortable cotton t-shirt'),
('TEST002', 'Women Summer Dress', 49.99, 'https://via.placeholder.com/300', 'fashion', 'women', 'amazon', '#', 4.8, 'Beautiful summer dress'),
('TEST003', 'Kids Casual Shirt', 19.99, 'https://via.placeholder.com/300', 'fashion', 'kids', 'amazon', '#', 4.3, 'Casual shirt for kids'),
('TEST004', 'Men Denim Jeans', 59.99, 'https://via.placeholder.com/300', 'fashion', 'men', 'amazon', '#', 4.6, 'Classic denim jeans'),
('TEST005', 'Women Handbag', 79.99, 'https://via.placeholder.com/300', 'fashion', 'women', 'amazon', '#', 4.7, 'Stylish handbag');

-- Verify
SELECT COUNT(*) FROM api_cache;
```

Then refresh the page - products will show!

---

## 🔍 Troubleshooting

### Issue: "Failed to fetch products"

**Check:**
1. Backend is running: http://localhost:5000/api/usage/stats
2. API key is in `backend/.env`
3. API key is valid (not expired)
4. MySQL is running

**Test Backend:**
```bash
curl http://localhost:5000/api/usage/stats
```

Should return:
```json
{
  "current_usage": 0,
  "monthly_limit": 100,
  "remaining": 100,
  "percentage": 0.0,
  "month_year": "2025-11",
  "can_make_call": true
}
```

### Issue: "API error 403"

**Cause:** Invalid or missing API key

**Solution:**
1. Check API key in `backend/.env`
2. Verify key is correct on RapidAPI
3. Make sure you subscribed to the API

### Issue: "API error 429"

**Cause:** Rate limit reached (100 calls used)

**Solution:**
- Wait for next month
- Or use cached products (they're already in database)
- Or upgrade RapidAPI plan

---

## ✅ Verification Checklist

- [ ] RapidAPI account created
- [ ] Subscribed to "Real-Time Amazon Data" API
- [ ] API key copied
- [ ] API key added to `backend/.env`
- [ ] Backend restarted
- [ ] Clicked "Fetch Products" button
- [ ] Products showing on page
- [ ] Counter showing usage (e.g., 1/100)

---

## 🎉 Success!

Once setup is complete, you'll see:

**Home Page:**
```
✨ New In (20 products)
[Product Slider with real products]
```

**Counter (Top-Right):**
```
● 1 / 100  🔄
▓░░░░░░░░░░░
API Requests
```

**Database:**
```
api_cache table: 20 products
api_usage table: 1 call recorded
```

---

## 📝 Quick Commands

```bash
# Check backend status
curl http://localhost:5000/api/usage/stats

# Check cached products
curl http://localhost:5000/api/cache/count

# Fetch fresh products
curl -X POST http://localhost:5000/api/products/fetch-fresh \
  -H "Content-Type: application/json" \
  -d '{"query": "clothing", "category": "fashion"}'

# Check database
mysql -u root shopping -e "SELECT COUNT(*) FROM api_cache;"
```

---

**Need help? Check the backend logs for detailed error messages!**
