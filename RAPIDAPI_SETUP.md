# RapidAPI Integration Setup Guide

## Overview
Your FashioPulse app now integrates with external clothing APIs from Amazon, Alibaba, and ASOS through RapidAPI.

## Features Added:
1. **Browse Page** (`/browse`) - Search and browse products from multiple sources
2. **External Product Cards** - Display products with source badges
3. **Category Filtering** - Filter by clothing categories
4. **Search Functionality** - Search across all platforms

## Setup Instructions:

### Step 1: Get RapidAPI Key

1. Go to [RapidAPI.com](https://rapidapi.com)
2. Sign up for a free account
3. Navigate to your profile and copy your API key

### Step 2: Subscribe to APIs

Subscribe to these free/freemium APIs on RapidAPI:

#### 1. Real-Time Amazon Data
- URL: https://rapidapi.com/letscrape-6bRBa3QguO5/api/real-time-amazon-data
- Free tier: 100 requests/month
- Search Amazon products

#### 2. Alibaba Product Search  
- URL: https://rapidapi.com/search/alibaba
- Search for wholesale products from Alibaba

#### 3. ASOS API
- URL: https://rapidapi.com/apidojo/api/asos2
- Free tier: 500 requests/month
- Fashion products from ASOS

### Step 3: Add API Key to Your Project

Create a `.env.local` file in your project root:

```env
NEXT_PUBLIC_RAPIDAPI_KEY=your-rapidapi-key-here
```

### Step 4: Restart Development Server

```bash
npm run dev
```

## Usage:

### Access the Browse Page:
- Click "🛍️ Browse" button in the header
- Or navigate to `/browse`

### Features:
- **Search**: Enter keywords to search across all platforms
- **Categories**: Click category buttons for filtered results
- **View Products**: Click "View Product" to open the product on the original site
- **Source Badges**: See which platform each product is from

## API Functions:

### Available Functions in `services/rapidapi.ts`:

```typescript
// Fetch from specific source
fetchAmazonProducts(query, category?)
fetchAlibabaProducts(query)
fetchAsosProducts(query, category?)

// Fetch from all sources
fetchAllProducts(query, category?)

// Search by category
searchProductsByCategory(category)

// Get trending products
getTrendingProducts()
```

## Alternative Free APIs:

If you want to use different APIs, here are alternatives:

1. **Etsy API** - Handmade and vintage items
2. **eBay API** - Auction and buy-it-now products
3. **Shopify API** - Products from Shopify stores
4. **Fake Store API** - Free mock data for testing

## Testing Without API Key:

The app will work without an API key but won't fetch real products. You'll see a setup notice on the browse page.

## Rate Limits:

- Amazon API: 100 requests/month (free tier)
- ASOS API: 500 requests/month (free tier)
- Consider caching results to reduce API calls

## Next Steps:

1. Add product caching to reduce API calls
2. Implement pagination for large result sets
3. Add filters (price range, ratings, etc.)
4. Save favorite external products
5. Compare prices across platforms

## Troubleshooting:

**Products not loading?**
- Check if API key is correctly set in `.env.local`
- Verify you've subscribed to the APIs on RapidAPI
- Check browser console for error messages
- Ensure you haven't exceeded rate limits

**CORS errors?**
- RapidAPI handles CORS, but ensure you're using the correct API endpoints
- Check that your API key is valid

**Images not displaying?**
- Some product images may have CORS restrictions
- The app includes fallback images for failed loads
