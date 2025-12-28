# FashionPulse Backend-Frontend Connection Guide

## 🎯 Overview
This guide will help you connect your FashionPulse clothing database to the frontend so all products are displayed correctly.

## 🏗️ Architecture
```
Frontend (Next.js)  ➡️  Backend (Flask)  ➡️  Database (MySQL)
   localhost:3000    ➡️   localhost:5000   ➡️   fashiopulse
```

## 📋 Prerequisites
1. ✅ MySQL/XAMPP running
2. ✅ `fashiopulse` database exists
3. ✅ `clothing` table has product data
4. ✅ Node.js installed
5. ✅ Python installed

## 🚀 Quick Start (Automated)

### Option 1: Complete Setup Script
```bash
python setup_fashiopulse.py
```
This will:
- Install Python packages
- Test database connection
- Start backend server
- Provide frontend instructions

### Option 2: Step by Step

#### Step 1: Test Database Connection
```bash
python test_database_connection.py
```

#### Step 2: Start Backend Server
```bash
python start_backend.py
```

#### Step 3: Test API Endpoints
```bash
# In a new terminal
python test_api_endpoints.py
```

#### Step 4: Start Frontend
```bash
npm run dev
```

## 🔧 Manual Setup

### 1. Install Python Dependencies
```bash
pip install flask flask-cors pymysql python-dotenv pyjwt requests
```

### 2. Configure Database (backend/config.py)
```python
DB_HOST = "localhost"
DB_USER = "root" 
DB_PASSWORD = ""
DB_NAME = "fashiopulse"
```

### 3. Start Backend Server
```bash
cd backend
python app.py
```

### 4. Start Frontend
```bash
npm run dev
```

## 🌐 API Endpoints

### Products
- `GET /api/products/search?query=clothing` - Search all products
- `GET /api/products/category/women` - Women's products
- `GET /api/products/category/men` - Men's products
- `GET /api/products/category/fashion` - All fashion products

### Statistics
- `GET /api/cache/count` - Total product count
- `GET /api/usage/stats` - API usage statistics

### Product Details
- `GET /api/products/{id}` - Single product details
- `GET /api/products/{id}/similar` - Similar products

## 🔍 Troubleshooting

### Backend Issues
1. **Database Connection Failed**
   - Check if MySQL/XAMPP is running
   - Verify database name: `fashiopulse`
   - Check credentials in `backend/config.py`

2. **No Products Found**
   - Verify clothing table has data
   - Check table structure matches expected columns

3. **Port 5000 Already in Use**
   - Change port in `backend/config.py`
   - Update `API_URL` in `services/backendApi.ts`

### Frontend Issues
1. **CORS Errors**
   - Backend includes CORS headers
   - Check if backend is running on port 5000

2. **API Connection Failed**
   - Verify backend URL: `http://localhost:5000`
   - Check network/firewall settings

## 📊 Database Schema
The backend expects these columns in the `clothing` table:
```sql
- product_id (Primary Key)
- product_name (Product title)
- price (Product price)
- product_image (Image URL)
- product_category (Category)
- product_description (Description)
- color (Product color)
- size (Product size)
- gender (men/women/unisex)
- stock (Available quantity)
- created_at (Timestamp)
```

## ✅ Verification Steps

### 1. Check Database
```bash
python test_database_connection.py
```
Should show:
- ✅ Database connection successful
- ✅ Clothing table exists
- 📦 Total products: [count]

### 2. Check Backend API
```bash
python test_api_endpoints.py
```
Should show:
- ✅ All endpoints responding
- 📦 Products being returned

### 3. Check Frontend
Visit `http://localhost:3000` and verify:
- Products are loading
- Categories work
- Search functions
- Product details display

## 🎉 Success Indicators
When everything is working:
1. Backend shows: "Running on http://0.0.0.0:5000"
2. Frontend shows products from your database
3. Product count matches your database
4. Categories filter correctly
5. Search returns relevant results

## 📞 Support
If you encounter issues:
1. Check the console logs (both frontend and backend)
2. Verify database connection with phpMyAdmin
3. Test API endpoints individually
4. Check network connectivity between services

---
**Happy Shopping! 🛍️**