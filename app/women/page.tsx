"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Header from "../../components/Header";
import ProductSlider from "../../components/ProductSlider";
import AIChatBox from "../../components/AIChatBox";
import AITryOnInterface from "../../components/AITryOnInterface";
import { useCart } from "../../context/CartContext";
import { searchProducts, BackendProduct } from "../../services/backendApi";

// Helper function to adjust prices
const adjustPrice = (price: number): number => {
  if (price < 500) return Math.floor(Math.random() * 1500) + 500;
  if (price > 5000) return Math.floor(Math.random() * 3000) + 2000;
  return Math.floor(price);
};

export default function WomenPage() {
  const router = useRouter();
  const [userName, setUserName] = useState<string | null>(null);
  const [allProducts, setAllProducts] = useState<BackendProduct[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState<string>("all");
  const [searchTerm, setSearchTerm] = useState<string>("");
  const [showAITryOn, setShowAITryOn] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState<BackendProduct | null>(null);

  const { cart, wishlist, addToCart, removeFromCart, incrementQuantity, decrementQuantity, toggleWishlist, cartCount, cartTotal } = useCart();

  const handleBuyNow = (productId: string | number, title: string, price: number, image?: string) => {
    addToCart({ id: productId, title, price, qty: 1, image });
    router.push("/checkout");
  };

  const handleProductClick = (product: any) => {
    const productId = product.product_id || product.id;
    if (productId) {
      router.push(`/products/${productId}`);
    }
  };

  useEffect(() => {
    const user = localStorage.getItem("user");
    if (user) {
      try {
        const userData = JSON.parse(user);
        setUserName(userData.name || "Guest");
      } catch {}
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("user");
    setUserName(null);
  };

  // Load women's products
  useEffect(() => {
    const loadProducts = async () => {
      setLoading(true);
      try {
        // Fetch ALL products from API with multiple search terms
        console.log("Fetching ALL products from API...");
        
        // Try multiple search queries to get more products
        const searchQueries = [
          "clothing fashion",
          "women dress shirt",
          "fashion apparel",
          "clothing wear",
          "fashion style"
        ];
        
        let allApiProducts: BackendProduct[] = [];
        
        for (const query of searchQueries) {
          try {
            const products = await searchProducts(query, "fashion");
            console.log(`Query "${query}" returned ${products.length} products`);
            allApiProducts = [...allApiProducts, ...products];
          } catch (err) {
            console.log(`Query "${query}" failed:`, err);
          }
        }
        
        // Remove duplicates based on product_id
        const uniqueProducts = allApiProducts.filter((product, index, self) => 
          index === self.findIndex(p => p.product_id === product.product_id)
        );
        
        console.log(`Total unique products from API: ${uniqueProducts.length}`);
        const products = uniqueProducts;
        console.log("Raw products received:", products.length, products);
        
        // Filter for women's products
        const womenProducts = products.filter(p => {
          const title = p.title.toLowerCase();
          const gender = p.gender?.toLowerCase() || '';
          
          // EXCLUDE men's products
          if (gender === 'men' || gender === 'male') return false;
          if (title.includes('men\'s') || title.includes(' mens ') || title.includes('mens ')) return false;
          
          // EXCLUDE kids products  
          if (gender === 'kids') return false;
          if (title.includes('kids') || title.includes('children') || title.includes('child')) return false;
          if (title.includes('baby') || title.includes('infant') || title.includes('toddler')) return false;
          if (title.includes('boys ') || title.includes('girls ')) return false;
          
          // INCLUDE women's products
          if (gender === 'women' || gender === 'female') return true;
          if (title.includes('women') || title.includes('womens') || title.includes('ladies')) return true;
          
          // Include typically women's items
          if (title.includes('dress') && !title.includes('address')) return true;
          if (title.includes('skirt') || title.includes('blouse')) return true;
          
          // If no specific gender markers, include it (for mock products)
          if (!gender || gender === 'unisex') {
            // Include if it's not clearly men's or kids
            if (!title.includes('men') && !title.includes('boy') && !title.includes('kid')) {
              return true;
            }
          }
          
          return false;
        });
        
        console.log(`Women's products: ${womenProducts.length} out of ${products.length}`);
        console.log("Filtered women's products:", womenProducts);
        
        // Load ALL available women's products from fallback data
        const fallbackProducts = [
          {
            id: 1,
            product_id: "W001",
            title: "Women's Elegant Black Dress - Long Sleeve Midi Dress",
            price: 1299,
            image_url: "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400",
            category: "fashion",
            gender: "women",
            source: "fallback",
            product_url: "#",
            rating: 4.5,
            description: "Elegant black midi dress perfect for office or evening wear",
            cached_at: "2024-12-10T08:00:00Z"
          },
          {
            id: 2,
            product_id: "W002",
            title: "Women's Casual Blue Jeans - High Waist Skinny Fit",
            price: 899,
            image_url: "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=400",
            category: "fashion",
            gender: "women",
            source: "fallback",
            product_url: "#",
            rating: 4.3,
            description: "Comfortable high-waist skinny jeans in classic blue",
            cached_at: "2024-12-10T08:00:00Z"
          },
          {
            id: 3,
            product_id: "W003",
            title: "Women's White Cotton Blouse - Professional Office Wear",
            price: 699,
            image_url: "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=400",
            category: "fashion",
            gender: "women",
            source: "fallback",
            product_url: "#",
            rating: 4.7,
            description: "Classic white cotton blouse perfect for professional settings",
            cached_at: "2024-12-10T08:00:00Z"
          },
          {
            id: 4,
            product_id: "W004",
            title: "Women's Pink Floral Summer Dress - Casual Day Wear",
            price: 1099,
            image_url: "https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=400",
            category: "fashion",
            gender: "women",
            source: "fallback",
            product_url: "#",
            rating: 4.4,
            description: "Beautiful floral summer dress in soft pink tones",
            cached_at: "2024-12-10T08:00:00Z"
          },
          {
            id: 13,
            product_id: "W005",
            title: "Women's Red Evening Gown - Elegant Party Dress",
            price: 1899,
            image_url: "https://images.unsplash.com/photo-1566479179817-c0ae2b4a4b5e?w=400",
            category: "fashion",
            gender: "women",
            source: "fallback",
            product_url: "#",
            rating: 4.8,
            description: "Stunning red evening gown for special occasions",
            cached_at: "2024-12-10T08:00:00Z"
          },
          {
            id: 14,
            product_id: "W006",
            title: "Women's Cozy Knit Sweater - Warm Winter Pullover",
            price: 999,
            image_url: "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=400",
            category: "fashion",
            gender: "women",
            source: "fallback",
            product_url: "#",
            rating: 4.6,
            description: "Soft and warm knit sweater perfect for winter",
            cached_at: "2024-12-10T08:00:00Z"
          }
        ];

        if (womenProducts.length === 0) {
          console.log("No women's products found from API, using fallback products");
          setAllProducts(fallbackProducts);
        } else {
          console.log(`Found ${womenProducts.length} women's products from API, combining with fallback`);
          // Combine API products with fallback products for better variety
          setAllProducts([...womenProducts, ...fallbackProducts]);
        }
      } catch (err) {
        console.error("Error loading products:", err);
        
        // Use ALL fallback products on error
        console.log("API error occurred, using all fallback products");
        const fallbackProducts = [
          {
            id: 1,
            product_id: "W001",
            title: "Women's Elegant Black Dress - Long Sleeve Midi Dress",
            price: 1299,
            image_url: "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400",
            category: "fashion",
            gender: "women",
            source: "fallback",
            product_url: "#",
            rating: 4.5,
            description: "Elegant black midi dress perfect for office or evening wear",
            cached_at: "2024-12-10T08:00:00Z"
          },
          {
            id: 2,
            product_id: "W002",
            title: "Women's Casual Blue Jeans - High Waist Skinny Fit",
            price: 899,
            image_url: "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=400",
            category: "fashion",
            gender: "women",
            source: "fallback",
            product_url: "#",
            rating: 4.3,
            description: "Comfortable high-waist skinny jeans in classic blue",
            cached_at: "2024-12-10T08:00:00Z"
          },
          {
            id: 3,
            product_id: "W003",
            title: "Women's White Cotton Blouse - Professional Office Wear",
            price: 699,
            image_url: "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=400",
            category: "fashion",
            gender: "women",
            source: "fallback",
            product_url: "#",
            rating: 4.7,
            description: "Classic white cotton blouse perfect for professional settings",
            cached_at: "2024-12-10T08:00:00Z"
          },
          {
            id: 4,
            product_id: "W004",
            title: "Women's Pink Floral Summer Dress - Casual Day Wear",
            price: 1099,
            image_url: "https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=400",
            category: "fashion",
            gender: "women",
            source: "fallback",
            product_url: "#",
            rating: 4.4,
            description: "Beautiful floral summer dress in soft pink tones",
            cached_at: "2024-12-10T08:00:00Z"
          },
          {
            id: 13,
            product_id: "W005",
            title: "Women's Red Evening Gown - Elegant Party Dress",
            price: 1899,
            image_url: "https://images.unsplash.com/photo-1566479179817-c0ae2b4a4b5e?w=400",
            category: "fashion",
            gender: "women",
            source: "fallback",
            product_url: "#",
            rating: 4.8,
            description: "Stunning red evening gown for special occasions",
            cached_at: "2024-12-10T08:00:00Z"
          },
          {
            id: 14,
            product_id: "W006",
            title: "Women's Cozy Knit Sweater - Warm Winter Pullover",
            price: 999,
            image_url: "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=400",
            category: "fashion",
            gender: "women",
            source: "fallback",
            product_url: "#",
            rating: 4.6,
            description: "Soft and warm knit sweater perfect for winter",
            cached_at: "2024-12-10T08:00:00Z"
          }
        ];
        setAllProducts(fallbackProducts);
      } finally {
        setLoading(false);
      }
    };
    loadProducts();
  }, []);

  // Women's categories
  const categories = [
    { id: "all", name: "All Women's", icon: "👗", keywords: [] },
    { id: "tops", name: "Tops & Shirts", icon: "👚", keywords: ["top", "shirt", "blouse", "tee", "t-shirt"] },
    { id: "dresses", name: "Dresses", icon: "👗", keywords: ["dress"] },
    { id: "sweaters", name: "Sweaters & Cardigans", icon: "🧶", keywords: ["sweater", "cardigan", "pullover", "knit"] },
    { id: "outerwear", name: "Jackets & Coats", icon: "🧥", keywords: ["jacket", "coat", "blazer", "outerwear"] },
    { id: "activewear", name: "Activewear", icon: "🏃‍♀️", keywords: ["sport", "active", "gym", "yoga", "athletic"] },
  ];

  // Filter products by category
  const filteredProducts = allProducts
    .map(p => ({ ...p, price: adjustPrice(p.price) }))
    .filter(p => {
      // Apply search filter
      if (searchTerm) {
        const query = searchTerm.toLowerCase();
        if (!p.title.toLowerCase().includes(query)) return false;
      }

      // Apply category filter
      if (selectedCategory === "all") return true;
      
      const category = categories.find(c => c.id === selectedCategory);
      if (!category) return true;
      
      return category.keywords.some(kw => p.title.toLowerCase().includes(kw));
    });

  const renderCategorySection = (category: typeof categories[0]) => {
    const categoryProducts = category.id === "all" 
      ? filteredProducts
      : filteredProducts.filter(p => 
          category.keywords.some(kw => p.title.toLowerCase().includes(kw))
        );

    if (categoryProducts.length === 0) return null;

    return (
      <section key={category.id} className="bg-white rounded-xl p-8 shadow-md">
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-3">
            <h2 className="text-3xl font-bold text-pink-600">
              {category.icon} {category.name}
            </h2>
          </div>
          <div className="text-sm text-gray-600">
            {categoryProducts.length} products
          </div>
        </div>
        
        {categoryProducts.length <= 4 ? (
          <ProductSlider
            products={categoryProducts.map((p) => ({
              id: p.product_id,
              title: p.title,
              price: p.price,
              img: p.image_url,
              imageUrl: p.image_url,
            }))}
            onAdd={(product) => addToCart({ id: product.id, title: product.title, price: product.price, qty: 1, image: product.imageUrl })}
            onBuy={(product) => handleBuyNow(product.id, product.title, product.price, product.imageUrl)}
            isWishlisted={(id) => !!wishlist.find((it) => it.id === id)}
            onToggleWishlist={(product) => toggleWishlist({ id: product.id, title: product.title, image: product.imageUrl, price: product.price })}
            getQty={(id) => cart.find((it) => it.id === id)?.qty ?? 0}
            onIncrease={incrementQuantity}
            onDecrease={decrementQuantity}
            onProductClick={handleProductClick}
          />
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {categoryProducts.map((p) => {
              const product = {
                id: p.product_id,
                title: p.title,
                price: p.price,
                img: p.image_url,
                imageUrl: p.image_url,
              };
              return (
                <div key={String(p.product_id)} className="w-full">
                  <div className="group relative rounded-lg border border-gray-200 bg-white p-4 hover:shadow-lg transition-shadow duration-200 flex flex-col h-full">
                    <div onClick={() => handleProductClick(p)} className="cursor-pointer flex-1 flex flex-col">
                      <div className="relative mb-4 w-full aspect-square flex items-center justify-center overflow-hidden rounded-lg bg-gray-50">
                        <img src={p.image_url} alt={p.title} className="h-full w-full object-cover group-hover:scale-110 transition-transform duration-300 ease-in-out" />
                      </div>
                      <h4 className="text-sm font-medium text-gray-800 hover:text-indigo-600 line-clamp-2 mb-2 h-10">{p.title}</h4>
                    </div>
                    
                    <button
                      onClick={(e) => {
                        e.preventDefault();
                        e.stopPropagation();
                        toggleWishlist({ id: product.id, title: product.title, image: product.imageUrl, price: product.price });
                      }}
                      className="absolute top-2 right-2 bg-white rounded-full p-2 shadow-md hover:shadow-lg transition-shadow z-10"
                    >
                      <span className="text-xl">{!!wishlist.find((it) => it.id === product.id) ? "❤️" : "🤍"}</span>
                    </button>
                    
                    <div className="text-lg font-semibold text-black mb-3">₹{p.price}</div>

                    <div className="flex items-center gap-1.5">
                      <button
                        onClick={(e) => {
                          e.preventDefault();
                          e.stopPropagation();
                          const qty = cart.find((it) => it.id === product.id)?.qty ?? 0;
                          qty > 0 ? decrementQuantity(product.id) : addToCart({ id: product.id, title: product.title, price: product.price, qty: 1, image: product.imageUrl });
                        }}
                        className="flex-1 rounded-lg bg-gradient-to-br from-pink-500 to-pink-700 p-2 text-white hover:from-pink-600 hover:to-pink-800 font-bold shadow-[0_3px_0_0_rgba(236,72,153,0.8)] hover:shadow-[0_4px_0_0_rgba(236,72,153,0.8)] active:shadow-[0_1px_0_0_rgba(236,72,153,0.8)] transition-all transform hover:-translate-y-0.5 active:translate-y-0.5 flex items-center justify-center"
                      >
                        {(cart.find((it) => it.id === product.id)?.qty ?? 0) > 0 ? <span className="text-base">−</span> : <span className="text-base">🛒</span>}
                      </button>

                      {(cart.find((it) => it.id === product.id)?.qty ?? 0) > 0 && (
                        <>
                          <div className="flex items-center justify-center bg-gradient-to-r from-pink-50 to-pink-100 rounded-lg px-2 py-2 shadow-inner min-w-[35px]">
                            <span className="text-xs font-bold text-pink-700">{cart.find((it) => it.id === product.id)?.qty ?? 0}</span>
                          </div>
                          <button
                            onClick={(e) => {
                              e.preventDefault();
                              e.stopPropagation();
                              incrementQuantity(product.id);
                            }}
                            className="flex-1 rounded-lg bg-gradient-to-br from-pink-500 to-pink-700 p-2 text-white hover:from-pink-600 hover:to-pink-800 font-bold shadow-[0_3px_0_0_rgba(236,72,153,0.8)] hover:shadow-[0_4px_0_0_rgba(236,72,153,0.8)] active:shadow-[0_1px_0_0_rgba(236,72,153,0.8)] transition-all transform hover:-translate-y-0.5 active:translate-y-0.5 flex items-center justify-center"
                          >
                            <span className="text-base">+</span>
                          </button>
                        </>
                      )}

                      <button
                        onClick={(e) => {
                          e.preventDefault();
                          e.stopPropagation();
                          handleBuyNow(product.id, product.title, product.price, product.imageUrl);
                        }}
                        className="flex-1 rounded-lg bg-white border-2 border-gray-800 p-2 text-black hover:bg-gray-100 font-bold shadow-[0_3px_0_0_rgba(0,0,0,0.3)] hover:shadow-[0_4px_0_0_rgba(0,0,0,0.3)] active:shadow-[0_1px_0_0_rgba(0,0,0,0.3)] transition-all transform hover:-translate-y-0.5 active:translate-y-0.5 flex items-center justify-center"
                      >
                        <span className="text-base">💵</span>
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </section>
    );
  };

  return (
    <div className="min-h-screen bg-[#fbfbec]">
      <div className="bg-white shadow-sm sticky top-0 z-40">
        <Header
          searchTerm={searchTerm}
          onSearch={setSearchTerm}
          cartCount={cartCount}
          cartTotal={cartTotal}
          cartItems={cart}
          onRemoveFromCart={removeFromCart}
          onIncreaseQty={incrementQuantity}
          onDecreaseQty={decrementQuantity}
          onAddToCart={addToCart}
          wishlistItems={wishlist}
          onRemoveFromWishlist={(id) => {
            const item = wishlist.find((it) => it.id === id);
            if (item) toggleWishlist(item);
          }}
          userName={userName}
          onLogout={handleLogout}
        />
      </div>

      <div className="mx-auto max-w-[1400px] px-6 sm:px-8 lg:px-10 py-8">
        {/* Back to Home Button */}
        <div className="mb-6">
          <Link
            href="/home"
            className="inline-flex items-center gap-2 bg-white border-2 border-pink-500 text-pink-600 px-6 py-3 rounded-lg font-semibold hover:bg-pink-50 transition-all shadow-sm"
          >
            <span>←</span>
            <span>Back to Home</span>
          </Link>
        </div>

        {/* Page Header */}
        <div className="bg-gradient-to-r from-pink-500 to-pink-600 rounded-xl p-8 mb-8 text-white shadow-lg">
          <h1 className="text-4xl font-bold mb-2">👩 Women's Fashion</h1>
          <p className="text-lg opacity-90">Discover the latest trends in women's clothing</p>
          <div className="mt-4 text-sm opacity-80">
            {allProducts.length} products available
          </div>
        </div>

        {/* Category Filter Buttons */}
        <div className="bg-white rounded-xl p-6 shadow-md mb-8">
          <h3 className="text-lg font-bold text-pink-600 mb-4">Shop by Category</h3>
          <div className="flex flex-wrap gap-3">
            {categories.map((category) => (
              <button
                key={category.id}
                onClick={() => setSelectedCategory(category.id)}
                className={`px-6 py-3 rounded-lg font-semibold transition-all flex items-center gap-2 ${
                  selectedCategory === category.id
                    ? "bg-gradient-to-r from-pink-500 to-pink-600 text-white shadow-lg scale-105"
                    : "bg-white text-pink-600 border-2 border-pink-300 hover:bg-pink-50"
                }`}
              >
                <span className="text-xl">{category.icon}</span>
                <span>{category.name}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Products */}
        <div className="space-y-6">
          {loading ? (
            <div className="text-center py-12 bg-white rounded-xl shadow-md">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-pink-300 border-t-pink-600"></div>
              <p className="mt-4 text-pink-600 font-semibold">Loading women's products...</p>
            </div>
          ) : filteredProducts.length === 0 ? (
            <div className="text-center py-12 bg-white rounded-xl shadow-md">
              <span className="text-6xl mb-4 block">🔍</span>
              <h3 className="text-xl font-bold text-pink-600 mb-2">No products found</h3>
              <p className="text-gray-600">Try selecting a different category or search term</p>
            </div>
          ) : selectedCategory === "all" ? (
            // Show all categories
            categories.map(category => renderCategorySection(category))
          ) : (
            // Show selected category only
            renderCategorySection(categories.find(c => c.id === selectedCategory)!)
          )}
        </div>
      </div>

      <AIChatBox />

      {/* AI Try-On Modal */}
      {showAITryOn && selectedProduct && (
        <AITryOnInterface
          productImage={selectedProduct.image_url}
          productType={selectedProduct.title.toLowerCase().includes('dress') ? 'dress' : 
                      selectedProduct.title.toLowerCase().includes('top') || selectedProduct.title.toLowerCase().includes('shirt') || selectedProduct.title.toLowerCase().includes('blouse') ? 'top' : 
                      selectedProduct.title.toLowerCase().includes('jean') || selectedProduct.title.toLowerCase().includes('pant') ? 'bottom' : 
                      selectedProduct.title.toLowerCase().includes('jacket') || selectedProduct.title.toLowerCase().includes('coat') || selectedProduct.title.toLowerCase().includes('sweater') ? 'outerwear' : 'top'}
          onClose={() => {
            setShowAITryOn(false);
            setSelectedProduct(null);
          }}
        />
      )}

      <footer className="bg-gray-900 text-white mt-12 py-8">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <h3 className="text-xl font-bold mb-4 bg-gradient-to-r from-pink-400 to-purple-400 bg-clip-text text-transparent">FashioPulse</h3>
              <p className="text-gray-400 text-sm">Your one-stop destination for fashion and lifestyle products.</p>
            </div>
            <div>
              <h4 className="font-semibold mb-3">Shop</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li><Link href="/home" className="hover:text-white transition-colors">Home</Link></li>
                <li><Link href="/women" className="hover:text-white transition-colors">Women</Link></li>
                <li><Link href="/home" className="hover:text-white transition-colors">Men</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-3">Customer Service</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Contact Us</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Track Order</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Returns</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-3">Follow Us</h4>
              <div className="flex gap-3 text-2xl">
                <a href="#" className="hover:scale-110 transition-transform">📘</a>
                <a href="#" className="hover:scale-110 transition-transform">📷</a>
                <a href="#" className="hover:scale-110 transition-transform">🐦</a>
              </div>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-6 text-center text-sm text-gray-400">
            <p>© 2024 FashioPulse. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
