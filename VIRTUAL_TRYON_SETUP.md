# Virtual Try-On Setup Guide

This guide will help you set up the Virtual Try-On feature using the IDM-VTON model from Hugging Face.

## Overview

The Virtual Try-On feature allows users to:
- Upload their photo
- See how clothing items from your database look on them
- Download the result image
- Try multiple outfits

## Technology Stack

- **Model**: IDM-VTON (Image-based Virtual Try-On)
- **Source**: Hugging Face Space by yisol
- **Model URL**: https://huggingface.co/spaces/yisol/IDM-VTON
- **API**: Hugging Face Inference API

## Setup Steps

### 1. Get Hugging Face API Key

1. Go to https://huggingface.co/
2. Create an account or log in
3. Go to Settings → Access Tokens: https://huggingface.co/settings/tokens
4. Click "New token"
5. Give it a name (e.g., "FashioPulse Virtual Try-On")
6. Select "Read" permission
7. Click "Generate token"
8. Copy the token

### 2. Configure Environment Variable

1. Open `.env.local` file in your project root
2. Add your Hugging Face API key:
   ```
   NEXT_PUBLIC_HUGGINGFACE_API_KEY=hf_your_actual_token_here
   ```
3. Save the file
4. Restart your Next.js development server

### 3. Test the Feature

1. Navigate to any product detail page
2. Click the "👗 Virtual Try-On" button
3. Upload a full-body photo
4. Click "Try On Now"
5. Wait 10-30 seconds for the AI to generate the result

## How It Works

### Frontend Flow

1. **User uploads photo**: User selects a full-body photo from their device
2. **Product selection**: The garment image is automatically taken from your database
3. **Category detection**: System automatically detects if it's upper_body, lower_body, or dresses
4. **API call**: Both images are sent to Hugging Face IDM-VTON API
5. **Result display**: The generated try-on image is displayed
6. **Download option**: User can download the result

### Backend Integration

The system integrates with your existing product database:

```typescript
// Fetches product from your backend
GET http://localhost:5000/api/products/{productId}

// Uses product.image_url as garment image
// Determines category from product.title
```

### Category Mapping

The system automatically maps products to IDM-VTON categories:

- **upper_body**: Shirts, tops, t-shirts, blouses, jackets, coats, sweaters
- **lower_body**: Pants, jeans, shorts, skirts, trousers
- **dresses**: Dresses, gowns

## Files Created

### 1. `services/virtualTryOn.ts`
- Core service for virtual try-on functionality
- Handles API communication with Hugging Face
- Image processing utilities
- Category detection logic

### 2. `components/VirtualTryOn.tsx`
- React component for the virtual try-on UI
- Image upload interface
- Result display
- Loading states and error handling

### 3. Updated Files
- `app/products/[id]/page.tsx` - Added Virtual Try-On button
- `.env.local` - Added Hugging Face API key configuration

## Usage in Code

### Basic Usage

```typescript
import { performVirtualTryOn } from '../services/virtualTryOn';

const result = await performVirtualTryOn({
  personImage: "base64_or_url",
  garmentImage: "base64_or_url",
  category: "upper_body"
});

if (result.success) {
  console.log("Result image:", result.resultImage);
}
```

### With Product from Database

```typescript
import { virtualTryOnWithProduct } from '../services/virtualTryOn';

const result = await virtualTryOnWithProduct(
  personImageBase64,
  productId
);
```

## Tips for Best Results

### Photo Requirements

1. **Full-body photo**: Include entire body from head to feet
2. **Front-facing**: Person should face the camera directly
3. **Good lighting**: Well-lit photo with clear details
4. **Simple background**: Avoid busy patterns or cluttered backgrounds
5. **Fitted clothing**: Wear fitted clothes for more accurate results
6. **High resolution**: Use clear, high-quality images

### Garment Images

Your product images should:
- Show the garment clearly
- Have good contrast
- Be on a clean background (white/transparent preferred)
- Show the full garment

## API Limits

### Hugging Face Free Tier

- **Rate limit**: ~30 requests per hour
- **Processing time**: 10-30 seconds per request
- **Image size**: Max 10MB per image

### Upgrading

For production use, consider:
1. Hugging Face Pro subscription for higher limits
2. Self-hosting the IDM-VTON model
3. Implementing request queuing
4. Adding user authentication to prevent abuse

## Troubleshooting

### Common Issues

**1. "Failed to generate try-on result"**
- Check if API key is correctly set
- Verify API key has proper permissions
- Check Hugging Face API status

**2. "Image size should be less than 10MB"**
- Compress images before upload
- Implement client-side image compression

**3. Slow processing**
- Normal processing time is 10-30 seconds
- Hugging Face free tier may have queues
- Consider upgrading for faster processing

**4. Poor quality results**
- Ensure person photo is full-body and front-facing
- Use high-quality, well-lit images
- Avoid busy backgrounds

### Debug Mode

Enable console logging to debug:

```typescript
// In services/virtualTryOn.ts
console.log("Request:", request);
console.log("Response:", response);
```

## Alternative Approaches

### 1. Self-Hosted Model

For better performance and no API limits:
- Clone IDM-VTON repository
- Set up GPU server
- Deploy model locally
- Update API endpoint in `virtualTryOn.ts`

### 2. Other Virtual Try-On Models

Alternative models to consider:
- **VITON-HD**: High-resolution virtual try-on
- **HR-VITON**: High-resolution with better quality
- **ClothingGAN**: GAN-based approach

### 3. Commercial APIs

For production-ready solutions:
- **Vue.ai**: Commercial virtual try-on API
- **Metail**: Enterprise virtual fitting room
- **3DLOOK**: Body measurement and virtual try-on

## Future Enhancements

Potential improvements:
1. **Body measurement**: Detect user's body measurements
2. **Size recommendation**: Suggest best size based on measurements
3. **Multiple angles**: Generate front, side, and back views
4. **Outfit combinations**: Try multiple items together
5. **AR try-on**: Real-time augmented reality try-on
6. **Social sharing**: Share try-on results on social media
7. **Saved try-ons**: Save favorite try-on results to profile

## Security Considerations

1. **Image privacy**: User photos are sent to Hugging Face API
2. **Data retention**: Check Hugging Face's data retention policy
3. **User consent**: Add terms of service for photo uploads
4. **Rate limiting**: Implement to prevent API abuse
5. **Authentication**: Consider requiring login for try-on feature

## Cost Estimation

### Free Tier (Current Setup)
- Cost: $0/month
- Limit: ~30 requests/hour
- Best for: Testing and low-traffic sites

### Hugging Face Pro
- Cost: $9/month
- Limit: Higher rate limits
- Best for: Small to medium traffic

### Self-Hosted
- Cost: $50-200/month (GPU server)
- Limit: Unlimited
- Best for: High traffic, full control

## Support

For issues or questions:
1. Check Hugging Face documentation: https://huggingface.co/docs
2. IDM-VTON model page: https://huggingface.co/spaces/yisol/IDM-VTON
3. Hugging Face community: https://discuss.huggingface.co/

## License

IDM-VTON model license: Check the model page for specific license terms
Hugging Face API: Subject to Hugging Face Terms of Service
