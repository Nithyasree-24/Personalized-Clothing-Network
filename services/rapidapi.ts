// RapidAPI Configuration
const RAPIDAPI_KEY = process.env.NEXT_PUBLIC_RAPIDAPI_KEY || 'your-rapidapi-key-here';

// API endpoints
const APIS = {
  // Amazon Product Data API
  amazon: {
    url: 'https://real-time-amazon-data.p.rapidapi.com/search',
    host: 'real-time-amazon-data.p.rapidapi.com'
  },
  // Alibaba API
  alibaba: {
    url: 'https://alibaba-product-search.p.rapidapi.com/search',
    host: 'alibaba-product-search.p.rapidapi.com'
  },
  // ASOS API (Alternative fashion API)
  asos: {
    url: 'https://asos2.p.rapidapi.com/products/v2/list',
    host: 'asos2.p.rapidapi.com'
  }
};

export interface Product {
  id: string;
  title: string;
  price: number;
  image: string;
  category?: string;
  source: 'amazon' | 'alibaba' | 'asos' | 'local';
  url?: string;
  rating?: number;
}

// Fetch products from Amazon (Clothing only)
export async function fetchAmazonProducts(query: string, category?: string): Promise<Product[]> {
  try {
    // Add clothing-specific keywords to ensure we get clothing items
    const clothingQuery = `${query} clothing apparel fashion`;
    
    const params = new URLSearchParams({
      query: clothingQuery,
      page: '1',
      country: 'US',
      category: 'fashion'
    });

    console.log('Fetching from Amazon:', `${APIS.amazon.url}?${params}`);
    console.log('Using API Key:', RAPIDAPI_KEY?.substring(0, 10) + '...');

    const response = await fetch(`${APIS.amazon.url}?${params}`, {
      method: 'GET',
      headers: {
        'X-RapidAPI-Key': RAPIDAPI_KEY,
        'X-RapidAPI-Host': APIS.amazon.host
      }
    });

    console.log('Amazon API Response Status:', response.status);

    if (!response.ok) {
      const errorText = await response.text();
      console.error('Amazon API error:', response.status, response.statusText, errorText);
      return [];
    }

    const data = await response.json();
    console.log('Amazon API Response Data:', data);
    
    // Check if data exists and has the expected structure
    if (!data || !data.data || !data.data.products) {
      console.error('Unexpected API response structure:', data);
      return [];
    }
    
    // Filter to ensure only clothing items
    const products = data.data.products
      .filter((item: any) => {
        if (!item) return false;
        const title = (item.product_title || item.title || '').toLowerCase();
        const clothingKeywords = ['shirt', 'dress', 'pants', 'jeans', 'jacket', 'coat', 'sweater', 
                                  'hoodie', 'top', 'blouse', 'skirt', 'shorts', 'suit', 'clothing',
                                  'apparel', 'wear', 't-shirt', 'polo', 'cardigan', 'blazer'];
        return clothingKeywords.some(keyword => title.includes(keyword));
      })
      .map((item: any) => {
        try {
          return {
            id: item.asin || item.product_id || String(Math.random()),
            title: item.product_title || item.title || 'Unknown Product',
            price: parseFloat(item.product_price?.replace(/[^0-9.]/g, '') || '0'),
            image: item.product_photo || item.image || '/assets/tshirt.jpg',
            category: category || 'Clothing',
            source: 'amazon' as const,
            url: item.product_url || '#',
            rating: parseFloat(item.product_star_rating || '0')
          };
        } catch (err) {
          console.error('Error mapping product:', err, item);
          return null;
        }
      })
      .filter((p: any) => p !== null);
    
    console.log('Filtered clothing products:', products.length);
    return products;
  } catch (error) {
    console.error('Error fetching Amazon products:', error);
    return [];
  }
}

// Fetch products from Alibaba
export async function fetchAlibabaProducts(query: string): Promise<Product[]> {
  try {
    const params = new URLSearchParams({
      query: query,
      page: '1'
    });

    const response = await fetch(`${APIS.alibaba.url}?${params}`, {
      method: 'GET',
      headers: {
        'X-RapidAPI-Key': RAPIDAPI_KEY,
        'X-RapidAPI-Host': APIS.alibaba.host
      }
    });

    if (!response.ok) {
      throw new Error('Failed to fetch Alibaba products');
    }

    const data = await response.json();
    
    return data.result?.map((item: any) => ({
      id: item.id || item.productId,
      title: item.title || item.name,
      price: parseFloat(item.price?.min || item.price || '0'),
      image: item.image || item.imageUrl,
      category: 'Clothing',
      source: 'alibaba' as const,
      url: item.url || item.link
    })) || [];
  } catch (error) {
    console.error('Error fetching Alibaba products:', error);
    return [];
  }
}

// Fetch products from ASOS
export async function fetchAsosProducts(query: string, category?: string): Promise<Product[]> {
  try {
    const params = new URLSearchParams({
      q: query,
      store: 'US',
      offset: '0',
      limit: '20',
      ...(category && { categoryId: category })
    });

    const response = await fetch(`${APIS.asos.url}?${params}`, {
      method: 'GET',
      headers: {
        'X-RapidAPI-Key': RAPIDAPI_KEY,
        'X-RapidAPI-Host': APIS.asos.host
      }
    });

    if (!response.ok) {
      throw new Error('Failed to fetch ASOS products');
    }

    const data = await response.json();
    
    return data.products?.map((item: any) => ({
      id: item.id?.toString(),
      title: item.name,
      price: parseFloat(item.price?.current?.value || '0'),
      image: `https://${item.imageUrl}`,
      category: 'Clothing',
      source: 'asos' as const,
      url: `https://www.asos.com/${item.url}`
    })) || [];
  } catch (error) {
    console.error('Error fetching ASOS products:', error);
    return [];
  }
}

// Fetch products from Amazon only (clothing focused)
export async function fetchAllProducts(query: string, category?: string): Promise<Product[]> {
  try {
    // Only fetch from Amazon for clothing
    const amazonProducts = await fetchAmazonProducts(query, category);
    return amazonProducts;
  } catch (error) {
    console.error('Error fetching products:', error);
    return [];
  }
}

// Search products by category (clothing only)
export async function searchProductsByCategory(category: string): Promise<Product[]> {
  const categoryQueries: Record<string, string> = {
    // Women's categories
    'Women Dresses': 'women dress',
    'Women Tops': 'women top blouse',
    'Women Pants': 'women pants trousers',
    'Women Jackets': 'women jacket coat',
    'Women Activewear': 'women activewear sportswear',
    'Women Skirts': 'women skirt',
    
    // Men's categories
    'Men Shirts': 'men shirt',
    'Men T-Shirts': 'men t-shirt tee',
    'Men Pants': 'men pants trousers',
    'Men Jeans': 'men jeans denim',
    'Men Jackets': 'men jacket coat',
    'Men Sportswear': 'men sportswear athletic',
    
    // Kids categories
    'Kids Clothing': 'kids children clothing',
    'Boys Clothing': 'boys clothing',
    'Girls Clothing': 'girls clothing',
    'Kids Activewear': 'kids sportswear',
    'Kids Jackets': 'kids jacket',
    
    // General
    'All Clothing': 'clothing fashion apparel',
    'Dresses': 'dress',
    'Shirts': 'shirt',
    'Pants': 'pants',
    'Jackets': 'jacket',
    'Sportswear': 'sportswear'
  };

  const query = categoryQueries[category] || category;
  return fetchAllProducts(query);
}

// Get trending products
export async function getTrendingProducts(): Promise<Product[]> {
  const trendingQueries = [
    'trending fashion',
    'new arrival clothing',
    'popular dress'
  ];

  const randomQuery = trendingQueries[Math.floor(Math.random() * trendingQueries.length)];
  return fetchAllProducts(randomQuery);
}
