// Backend API service for fetching products from local MySQL database
const API_URL = 'http://localhost:5000/api';

export interface BackendProduct {
  id: number;
  product_id: string;
  title: string;
  price: number;
  image_url: string;
  category: string;
  gender: string;
  source: string;
  product_url?: string;
  rating: number;
  description: string;
  cached_at: string;
  color?: string;
  size?: string;
  stock?: number;
}

export interface UsageStats {
  current_usage: number;
  monthly_limit: number;
  remaining: number;
  percentage: number;
  month_year: string;
  can_make_call: boolean;
}

// Fetch products from backend (uses cache or API)
export async function searchProducts(query: string, category: string = 'fashion'): Promise<BackendProduct[]> {
  try {
    const response = await fetch(`${API_URL}/products/search?query=${encodeURIComponent(query)}&category=${category}`);
    if (!response.ok) {
      throw new Error('Failed to fetch products');
    }
    const data = await response.json();
    return data.products || [];
  } catch (error) {
    console.error('Error fetching products:', error);
    return [];
  }
}

// Fetch fresh products from Amazon API (increments counter)
export async function fetchFreshProducts(query: string, category: string = 'fashion'): Promise<BackendProduct[]> {
  try {
    const response = await fetch(`${API_URL}/products/fetch-fresh`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query, category }),
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to fetch products');
    }
    
    const data = await response.json();
    return data.products || [];
  } catch (error) {
    console.error('Error fetching fresh products:', error);
    return [];
  }
}

// Get products by category from cache
export async function getProductsByCategory(category: string, gender?: string, limit: number = 20): Promise<BackendProduct[]> {
  try {
    let url = `${API_URL}/products/category/${encodeURIComponent(category)}?limit=${limit}`;
    if (gender) {
      url += `&gender=${encodeURIComponent(gender)}`;
    }
    
    console.log('Fetching products from URL:', url);
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Failed to fetch products: ${response.status} ${response.statusText}`);
    }
    const data = await response.json();
    console.log('API Response:', data);
    return data.products || [];
  } catch (error) {
    console.error('Error fetching products by category:', error);
    return [];
  }
}

// Get API usage statistics
export async function getUsageStats(): Promise<UsageStats | null> {
  try {
    const response = await fetch(`${API_URL}/usage/stats`);
    if (!response.ok) {
      throw new Error('Failed to fetch usage stats');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching usage stats:', error);
    return null;
  }
}

// Get cached products count
export async function getCachedProductsCount(): Promise<number> {
  try {
    const response = await fetch(`${API_URL}/cache/count`);
    if (!response.ok) {
      throw new Error('Failed to fetch cache count');
    }
    const data = await response.json();
    return data.cached_products || 0;
  } catch (error) {
    console.error('Error fetching cache count:', error);
    return 0;
  }
}

// Fetch products from eBay API (India)
export async function fetchEbayProducts(query: string, limit: number = 50): Promise<BackendProduct[]> {
  try {
    const response = await fetch(`${API_URL}/products/fetch-ebay`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query, limit }),
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to fetch eBay products');
    }
    
    const data = await response.json();
    return data.products || [];
  } catch (error) {
    console.error('Error fetching eBay products:', error);
    return [];
  }
}

// Fetch products from both Amazon and eBay APIs
export async function fetchAllProducts(query: string): Promise<BackendProduct[]> {
  try {
    const response = await fetch(`${API_URL}/products/fetch-all`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query }),
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to fetch products');
    }
    
    const data = await response.json();
    return data.products || [];
  } catch (error) {
    console.error('Error fetching all products:', error);
    return [];
  }
}

// ============= PRODUCT DETAIL & REVIEWS =============

export interface Review {
  id: number;
  product_id: string;
  user_id: number;
  user_name: string;
  rating: number;
  comment: string;
  created_at: string;
}

// Get single product details
export async function getProductDetail(productId: string): Promise<BackendProduct | null> {
  try {
    const response = await fetch(`${API_URL}/products/${productId}`);
    if (!response.ok) {
      throw new Error('Failed to fetch product detail');
    }
    const data = await response.json();
    return data.product || null;
  } catch (error) {
    console.error('Error fetching product detail:', error);
    return null;
  }
}

// Get similar products
export async function getSimilarProducts(productId: string, limit: number = 8): Promise<BackendProduct[]> {
  try {
    const response = await fetch(`${API_URL}/products/${productId}/similar?limit=${limit}`);
    if (!response.ok) {
      throw new Error('Failed to fetch similar products');
    }
    const data = await response.json();
    return data.products || [];
  } catch (error) {
    console.error('Error fetching similar products:', error);
    return [];
  }
}

// Get reviews for a product
export async function getReviews(productId: string): Promise<Review[]> {
  try {
    const response = await fetch(`${API_URL}/reviews/${productId}`);
    if (!response.ok) {
      throw new Error('Failed to fetch reviews');
    }
    const data = await response.json();
    return data.reviews || [];
  } catch (error) {
    console.error('Error fetching reviews:', error);
    return [];
  }
}

// Add a review
export async function addReview(productId: string, userId: number, rating: number, comment: string): Promise<boolean> {
  try {
    const response = await fetch(`${API_URL}/reviews`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        product_id: productId,
        user_id: userId,
        rating,
        comment,
      }),
    });
    
    if (!response.ok) {
      throw new Error('Failed to add review');
    }
    
    return true;
  } catch (error) {
    console.error('Error adding review:', error);
    return false;
  }
}
