# Fix: Display Products on Home Page

## 🔴 Current Problem
Products are not showing on the home page because **MySQL database is not running**.

## ✅ Quick Solution

### Step 1: Start MySQL

**If you have XAMPP:**
1. Open XAMPP Control Panel
2. Click "Start" next to MySQL
3. Wait for green "Running" status

**If you have MySQL Service:**
1. Open Command Prompt as Administrator
2. Run: `net start MySQL80` (or `net start MySQL`)

**If MySQL is not installed:**
- Install XAMPP from: https://www.apachefriends.org/
- Or install MySQL from: https://dev.mysql.com/downloads/

### Step 2: Verify Backend is Running
✅ Backend is already running on port 5000

### Step 3: Refresh Browser
Once MySQL starts, refresh http://localhost:3000/home

## 📊 What You Should See

After MySQL starts, your home page will display:
- **Top Deals**: 20 products
- **Summer Collection**: 16 products  
- **Winter Collection**: 16 products
- **New In**: 20 products

Total: **72 products** on home page
Database has: **359 products** total

## 🎨 Current Status

✅ **Frontend**: Running on port 3000
✅ **Backend**: Running on port 5000
❌ **MySQL**: Not running (needs to be started)

## 🔧 Backend Error

The backend is showing:
```
Error connecting to database: Can't connect to MySQL server on 'localhost:3306'
```

This means MySQL service is not running.

## 💡 After Fix

Once MySQL is running, you'll see:
1. Products load automatically
2. All categories work (Men, Women, Kids)
3. Search works
4. Cart and Wishlist work
5. Product details work

## 🆘 Need Help?

See `START_MYSQL_GUIDE.md` for detailed instructions.

---

**TL;DR**: Start MySQL → Refresh browser → Products will display! 🎉
