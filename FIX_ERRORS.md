# Fix Current Errors

## ✅ Fixed Issues

1. **@next/swc-win32-x64-msvc module** - ✅ Installed successfully
2. **Backend Flask server** - ✅ Running on port 5000

## ❌ Current Issue: MySQL Not Running

### Error Message:
```
Error connecting to database: 2003 (HY000): Can't connect to MySQL server on 'localhost:3306' (10061)
```

### Solution:

#### Option 1: Start MySQL Service (Recommended)
```bash
# Open Command Prompt as Administrator and run:
net start MySQL80

# Or if you have a different MySQL version:
net start MySQL
```

#### Option 2: Start MySQL from Services
1. Press `Win + R`
2. Type `services.msc` and press Enter
3. Find "MySQL80" or "MySQL" in the list
4. Right-click and select "Start"

#### Option 3: Start MySQL from XAMPP/WAMP
If you're using XAMPP or WAMP:
1. Open XAMPP/WAMP Control Panel
2. Click "Start" next to MySQL

### Verify MySQL is Running
```bash
# Check if MySQL is listening on port 3306
netstat -ano | findstr :3306
```

You should see output like:
```
TCP    0.0.0.0:3306           0.0.0.0:0              LISTENING       12345
```

## 🔄 After Starting MySQL

1. **Refresh the browser** - The page should now load products
2. **Check backend logs** - Should see successful database connections
3. **Verify products load** - Home page should show products

## 🎯 Quick Test

Once MySQL is running, test the API:
```bash
# Open browser and go to:
http://localhost:5000/api/products/search?query=clothing&category=fashion
```

You should see JSON data with products.

## 📊 Current System Status

✅ **Frontend**: Running on http://localhost:3000
✅ **Backend**: Running on http://localhost:5000  
❌ **MySQL**: Not running (needs to be started)

## 🚀 Next Steps After MySQL Starts

1. Refresh the home page
2. Products should load automatically
3. You can then:
   - Browse products
   - Add to cart
   - Add to wishlist
   - View product details

## 💡 Pro Tip

To avoid this issue in the future, set MySQL to start automatically:
1. Open `services.msc`
2. Find MySQL service
3. Right-click → Properties
4. Set "Startup type" to "Automatic"
5. Click OK

---

**Need Help?** 
- Check if MySQL is installed: `mysql --version`
- Check MySQL status: `sc query MySQL80`
- View MySQL logs: Check `C:\ProgramData\MySQL\MySQL Server 8.0\Data\` folder
