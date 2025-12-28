# Quick Start: Virtual Try-On Feature

## 🚀 Get Started in 3 Steps

### Step 1: Get Your Hugging Face API Key (2 minutes)

1. Visit: https://huggingface.co/settings/tokens
2. Click "New token"
3. Name it: "FashioPulse-VirtualTryOn"
4. Select "Read" permission
5. Click "Generate" and copy the token

### Step 2: Add API Key to Your Project (1 minute)

Open `.env.local` and replace the placeholder:

```bash
NEXT_PUBLIC_HUGGINGFACE_API_KEY=hf_YourActualTokenHere
```

### Step 3: Restart Your Server (30 seconds)

```bash
# Stop the current server (Ctrl+C)
# Then restart:
npm run dev
```

## ✅ Test It Out

1. Go to any product page: http://localhost:3000/products/[any-product-id]
2. Click the purple "👗 Virtual Try-On" button
3. Upload a full-body photo
4. Click "Try On Now"
5. Wait 10-30 seconds for the magic! ✨

## 📸 Photo Tips

For best results, use a photo that:
- Shows full body (head to feet)
- Person faces camera directly
- Has good lighting
- Simple background
- Clear and not blurry

## 🎯 Where It Works

The Virtual Try-On button appears on:
- ✅ Product detail pages (`/products/[id]`)
- 🔜 Can be added to: Home page, Category pages, Avatar Builder

## 🔧 How It Works

```
User Photo + Product Image → Hugging Face IDM-VTON API → Try-On Result
```

1. User uploads their photo
2. System fetches product image from your database
3. Both sent to AI model
4. AI generates realistic try-on image
5. User can download result

## 💡 Features

- ✅ Automatic category detection (tops, bottoms, dresses)
- ✅ Real product images from your database
- ✅ Download result image
- ✅ Try multiple outfits
- ✅ Mobile-friendly interface
- ✅ Loading states and error handling

## 🎨 Customization

### Change Button Color

In `app/products/[id]/page.tsx`:

```tsx
// Current: Purple gradient
className="bg-gradient-to-r from-purple-500 to-purple-600"

// Change to pink:
className="bg-gradient-to-r from-pink-500 to-pink-600"
```

### Add to Other Pages

Copy this code to any page:

```tsx
import VirtualTryOn from "../components/VirtualTryOn";

// Add state
const [showVirtualTryOn, setShowVirtualTryOn] = useState(false);

// Add button
<button onClick={() => setShowVirtualTryOn(true)}>
  👗 Virtual Try-On
</button>

// Add modal
{showVirtualTryOn && (
  <VirtualTryOn
    productImage={product.image_url}
    productTitle={product.title}
    onClose={() => setShowVirtualTryOn(false)}
  />
)}
```

## 📊 API Limits

**Free Tier (Current):**
- ~30 requests per hour
- 10-30 seconds per request
- Perfect for testing!

**Need More?**
- Hugging Face Pro: $9/month for higher limits
- Self-host: Unlimited but requires GPU server

## 🐛 Troubleshooting

**Button doesn't work?**
- Check if API key is set in `.env.local`
- Restart the server after adding API key

**"Failed to generate" error?**
- Verify API key is correct
- Check Hugging Face API status
- Try with a different photo

**Slow processing?**
- Normal: 10-30 seconds
- Free tier may have queues during peak times

**Poor quality result?**
- Use better quality photos
- Ensure full-body, front-facing photo
- Good lighting is essential

## 🎉 Next Steps

1. **Test with different products** - Try tops, pants, dresses
2. **Test with different photos** - See what works best
3. **Add to Avatar Builder** - Let users try on their avatar outfits
4. **Add to home page** - Quick try-on from product cards
5. **Collect feedback** - See what users think!

## 📚 More Information

- Full setup guide: `VIRTUAL_TRYON_SETUP.md`
- IDM-VTON model: https://huggingface.co/spaces/yisol/IDM-VTON
- Hugging Face docs: https://huggingface.co/docs

## 🎯 Integration with Avatar Builder

Want to add Virtual Try-On to your Avatar Builder? The outfit images are already in your database, so you can:

1. Add "Virtual Try-On" button in `components/avatar/ClothingLibrary.tsx`
2. Use the avatar's base image as the person photo
3. Apply the selected outfit image as the garment
4. Show the result in the avatar preview

This creates a seamless experience where users can:
- Build their avatar
- Try on clothes virtually
- See realistic results
- Purchase the items they like

---

**Ready to go? Get your API key and start trying on clothes! 👗✨**
