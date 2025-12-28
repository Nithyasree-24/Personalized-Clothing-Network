# How to Start MySQL and Display Products

## 🔍 Current Issue
Products are not displaying because MySQL database is not running.

## 📋 Step-by-Step Solution

### Option 1: If you have XAMPP installed

1. **Open XAMPP Control Panel**
   - Search for "XAMPP" in Windows Start menu
   - Click on "XAMPP Control Panel"

2. **Start MySQL**
   - Find "MySQL" in the list
   - Click the "Start" button next to MySQL
   - Wait for it to turn green

3. **Verify MySQL is Running**
   - You should see "Running" status
   - Port should show 3306

4. **Refresh Your Browser**
   - Go to http://localhost:3000/home
   - Products should now load

### Option 2: If you have MySQL installed as Windows Service

1. **Open Command Prompt as Administrator**
   - Press `Win + X`
   - Select "Command Prompt (Admin)" or "PowerShell (Admin)"

2. **Try these commands one by one:**
   ```cmd
   net start MySQL
   net start MySQL80
   net start MySQL57
   net start MYSQL
   ```

3. **If successful, you'll see:**
   ```
   The MySQL service is starting.
   The MySQL service was started successfully.
   ```

### Option 3: If MySQL is not installed

You need to install MySQL first:

#### Quick Install with XAMPP (Recommended)
1. Download XAMPP from: https://www.apachefriends.org/
2. Install XAMPP
3. Open XAMPP Control Panel
4. Start MySQL
5. Follow Option 1 above

#### Or Install MySQL Standalone
1. Download MySQL from: https://dev.mysql.com/downloads/installer/
2. Run the installer
3. Choose "Developer Default"
4. Set root password (remember it!)
5. Complete installation
6. MySQL should start automatically

## 🔧 After Starting MySQL

### 1. Verify Backend is Running
Check if Flask backend is running on port 5000:
- Open browser: http://localhost:5000/api/products/search?query=clothing
- You should see JSON data with products

### 2. Check Database Connection
The backend logs should show:
```
✅ Database connected successfully
```

Instead of:
```
❌ Error connecting to database: Can't connect to MySQL server
```

### 3. Refresh Your Website
- Go to: http://localhost:3000/home
- Products should now display in the grid

## 🎯 Quick Test

Run this command to test if MySQL is accessible:
```bash
mysql -u root -p
```

If it asks for password, MySQL is running!
If it says "command not found", MySQL is not installed or not in PATH.

## 📊 Expected Result

Once MySQL is running, you should see:
- ✅ 359 products in the database
- ✅ Products displayed on home page
- ✅ Categories working (Men, Women, Kids)
- ✅ Search functionality working
- ✅ Cart and Wishlist working

## 🆘 Still Not Working?

### Check Backend Logs
Look at the terminal where Flask is running:
```
python backend/app.py
```

You should see:
```
✅ Connected to MySQL database: shopping
✅ Found 359 products in cache
```

### Check Frontend Console
Open browser DevTools (F12) and check Console tab:
- Should see successful API calls
- No "Failed to fetch" errors

### Restart Everything
1. Stop Flask backend (Ctrl+C)
2. Start MySQL
3. Start Flask backend: `python backend/app.py`
4. Refresh browser

## 💡 Pro Tips

1. **Set MySQL to Auto-Start**
   - Open Services (Win + R → `services.msc`)
   - Find MySQL service
   - Right-click → Properties
   - Set "Startup type" to "Automatic"

2. **Check MySQL Port**
   - Default port is 3306
   - Make sure nothing else is using this port

3. **Verify Database Exists**
   ```sql
   mysql -u root -p
   SHOW DATABASES;
   USE shopping;
   SHOW TABLES;
   SELECT COUNT(*) FROM products;
   ```

## 🎨 What You'll See After Fix

Your home page will display:
- 🔥 Top Deals (20 products)
- ☀️ Summer Collection (16 products)
- ❄️ Winter Collection (16 products)
- ✨ New In (20 products)

All in beautiful pink gradient theme! 🎨

---

**Need more help?** Check the backend terminal for specific error messages.
