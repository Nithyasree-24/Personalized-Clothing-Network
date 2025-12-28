# Enable Real Virtual Try-On (AI-Powered)

## 🎯 Current Status
You're seeing the same input image because the system is in **Demo Mode**. To get real AI-powered virtual try-on where the garment is actually applied to your photo, follow these steps:

## 🚀 Quick Setup (5 Minutes)

### Step 1: Get Hugging Face API Key

1. **Go to Hugging Face**: https://huggingface.co/
2. **Sign up or log in** (it's free!)
3. **Go to Settings → Access Tokens**: https://huggingface.co/settings/tokens
4. **Click "New token"**
5. **Name it**: "FashioPulse-VirtualTryOn"
6. **Select permission**: "Read"
7. **Click "Generate token"**
8. **Copy the token** (starts with `hf_...`)

### Step 2: Add API Key to Backend

1. **Open file**: `backend/.env`
2. **Find this line**:
   ```
   HUGGINGFACE_API_KEY=your_huggingface_api_key_here
   ```
3. **Replace with your actual token**:
   ```
   HUGGINGFACE_API_KEY=hf_YourActualTokenHere
   ```
4. **Save the file**

### Step 3: Restart Backend Server

**Option A - If backend is running in terminal:**
```bash
# Press Ctrl+C to stop
# Then restart:
cd backend
python app.py
```

**Option B - If using the process manager:**
The backend should auto-reload when you save the .env file.

### Step 4: Test Real Virtual Try-On

1. Go to any product page
2. Click "👗 Virtual Try-On"
3. Upload your photo
4. Click "Try On Now"
5. Wait 10-30 seconds
6. See the AI-generated result with the garment on you! ✨

## 🎨 How It Works

### Demo Mode (Current):
```
Your Photo → Backend → Returns Same Photo
```

### Full Mode (With API Key):
```
Your Photo + Garment Image → Hugging Face AI → Photo with Garment Applied
```

## 📊 What to Expect

### With API Key:
- ✅ Real AI-powered virtual try-on
- ✅ Garment actually appears on your body
- ✅ Realistic fitting and draping
- ✅ Professional quality results
- ⏱️ Processing time: 10-30 seconds

### Free Tier Limits:
- 🆓 Free to use
- 📊 ~30 requests per hour
- ⚡ May have queue during peak times

## 🔍 Verify It's Working

After adding the API key, check the backend logs:

**You should see:**
```
Virtual Try-On request - Category: upper_body
Calling Hugging Face API...
```

**Instead of:**
```
Running in demo mode (no API key configured)
```

## 🐛 Troubleshooting

### Still Seeing Same Image?

**Check 1: API Key Format**
- Should start with `hf_`
- No quotes around it in .env file
- No extra spaces

**Check 2: Backend Restarted**
- Stop and restart the backend server
- Check logs for "Calling Hugging Face API..."

**Check 3: API Key Permissions**
- Make sure you selected "Read" permission
- Token should be active (not expired)

### "API Error" Message?

**Possible causes:**
1. Invalid API key
2. Hugging Face service down
3. Rate limit exceeded
4. Network issues

**Solution:**
- Verify API key is correct
- Check Hugging Face status: https://status.huggingface.co/
- Wait a few minutes and try again

## 💡 Alternative: Use Hugging Face Space Directly

If you want to test the AI model first:

1. Go to: https://huggingface.co/spaces/yisol/IDM-VTON
2. Upload your photo and garment image
3. See how it works
4. Then integrate into your website

## 🎯 Expected Results

### Good Results:
- Full-body, front-facing photo
- Good lighting
- Simple background
- Clear garment image
- Proper category (top/bottom/dress)

### May Need Adjustment:
- Side-facing photos
- Poor lighting
- Busy backgrounds
- Low-resolution images

## 📈 Upgrade Options

### Free Tier (Current):
- Cost: $0/month
- Limit: ~30 requests/hour
- Best for: Testing, low traffic

### Hugging Face Pro:
- Cost: $9/month
- Limit: Higher rate limits
- Best for: Production use

### Self-Hosted:
- Cost: $50-200/month (GPU server)
- Limit: Unlimited
- Best for: High traffic, full control

## 🎉 Success Checklist

- [ ] Created Hugging Face account
- [ ] Generated API token
- [ ] Added token to backend/.env
- [ ] Restarted backend server
- [ ] Tested virtual try-on
- [ ] Saw different result (not same image)
- [ ] Garment appeared on photo
- [ ] Downloaded result successfully

## 📞 Need Help?

**Backend logs show errors?**
- Check the terminal where backend is running
- Look for error messages
- Share the error for specific help

**Frontend shows error?**
- Check browser console (F12)
- Look for network errors
- Verify backend is running

**API not working?**
- Test API key at: https://huggingface.co/spaces/yisol/IDM-VTON
- Verify token permissions
- Check Hugging Face status

---

## 🚀 Quick Command Reference

**Check if backend is running:**
```bash
curl http://localhost:5000/api/usage/stats
```

**Restart backend:**
```bash
cd backend
python app.py
```

**Test virtual try-on endpoint:**
```bash
curl -X POST http://localhost:5000/api/virtual-tryon \
  -H "Content-Type: application/json" \
  -d '{"person_image":"test","garment_image":"test","category":"upper_body"}'
```

**Check backend logs:**
Look for:
- "Running in demo mode" = No API key
- "Calling Hugging Face API" = API key configured ✅

---

**Ready to see real virtual try-on? Get your API key now!** 🎉
