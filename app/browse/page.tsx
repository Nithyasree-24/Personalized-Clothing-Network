"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import ExternalProductCard from "../../components/ExternalProductCard";
import { fetchAllProducts, searchProductsByCategory, Product } from "../../services/rapidapi";

export default function BrowsePage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);

  const [selectedGender, setSelectedGender] = useState<string>("all");

  const genderCategories = {
    all: ["All Clothing", "Dresses", "Shirts", "Pants", "Jackets", "Sportswear"],
    women: ["Women Dresses", "Women Tops", "Women Pants", "Women Jackets", "Women Activewear", "Women Skirts"],
    men: ["Men Shirts", "Men T-Shirts", "Men Pants", "Men Jeans", "Men Jackets", "Men Sportswear"],
    kids: ["Kids Clothing", "Boys Clothing", "Girls Clothing", "Kids Activewear", "Kids Jackets"]
  };

  const categories = genderCategories[selectedGender as keyof typeof genderCategories] || genderCategories.all;

  const loadProducts = async (query?: string, category?: string) => {
    setLoading(true);
    try {
      let fetchedProducts: Product[];
      
      if (category) {
        console.log('Fetching by category:', category);
        fetchedProducts = await searchProductsByCategory(category);
      } else if (query) {
        console.log('Fetching by query:', query);
        fetchedProducts = await fetchAllProducts(query);
      } else {
        console.log('Fetching default products');
        fetchedProducts = await fetchAllProducts("women dress");
      }
      
      console.log('Fetched products:', fetchedProducts.length);
      setProducts(fetchedProducts);
    } catch (error) {
      console.error("Error loading products:", error);
      setProducts([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProducts();
  }, []);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      setSelectedCategory(null);
      loadProducts(searchQuery);
    }
  };

  const handleCategoryClick = (category: string) => {
    setSelectedCategory(category);
    setSearchQuery("");
    loadProducts(undefined, category);
  };

  return (
    <div className="min-h-screen bg-[#fbfbec]">
      {/* Header */}
      <div className="bg-white shadow-sm sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <Link href="/home" className="text-pink-600 hover:text-pink-700 font-semibold">
              ← Back to Home
            </Link>
            <h1 className="text-2xl font-bold text-pink-600">Browse Products</h1>
            <div className="w-32"></div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Search Bar */}
        <div className="mb-8">
          <form onSubmit={handleSearch} className="max-w-2xl mx-auto">
            <div className="relative">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search for clothing, shoes, accessories..."
                className="w-full rounded-full border-2 border-pink-300 pl-12 pr-4 py-3 text-black focus:border-pink-500 focus:outline-none transition-colors"
              />
              <span className="absolute left-4 top-1/2 -translate-y-1/2 text-pink-600 text-xl">🔍</span>
              <button
                type="submit"
                className="absolute right-2 top-1/2 -translate-y-1/2 bg-gradient-to-r from-pink-500 to-pink-600 text-white px-6 py-2 rounded-full font-semibold hover:shadow-lg transition-all"
              >
                Search
              </button>
            </div>
          </form>
        </div>

        {/* Gender Filter */}
        <div className="mb-6">
          <h2 className="text-xl font-bold text-pink-600 mb-4">Shop By</h2>
          <div className="flex flex-wrap gap-3">
            {[
              { key: "all", label: "All", icon: "👥" },
              { key: "women", label: "Women", icon: "👩" },
              { key: "men", label: "Men", icon: "👨" },
              { key: "kids", label: "Kids", icon: "👧" }
            ].map((gender) => (
              <button
                key={gender.key}
                onClick={() => {
                  setSelectedGender(gender.key);
                  setSelectedCategory(null);
                }}
                className={`px-6 py-3 rounded-lg font-semibold transition-all flex items-center gap-2 ${
                  selectedGender === gender.key
                    ? "bg-gradient-to-r from-pink-500 to-pink-600 text-white shadow-lg scale-105"
                    : "bg-white text-pink-600 border-2 border-pink-300 hover:bg-pink-50"
                }`}
              >
                <span className="text-xl">{gender.icon}</span>
                <span>{gender.label}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Categories */}
        <div className="mb-8">
          <h2 className="text-xl font-bold text-pink-600 mb-4">Categories</h2>
          <div className="flex flex-wrap gap-3">
            {categories.map((category) => (
              <button
                key={category}
                onClick={() => handleCategoryClick(category)}
                className={`px-4 py-2 rounded-lg font-semibold transition-all ${
                  selectedCategory === category
                    ? "bg-gradient-to-r from-pink-500 to-pink-600 text-white shadow-lg"
                    : "bg-white text-pink-600 border-2 border-pink-300 hover:bg-pink-50"
                }`}
              >
                {category}
              </button>
            ))}
          </div>
        </div>

        {/* Products Count */}
        <div className="mb-6 bg-gradient-to-r from-[#f5f1e8] to-[#faf8f3] rounded-lg p-4 shadow-sm border-2 border-[#D4A574]">
          <div className="flex items-center gap-4 flex-wrap">
            <span className="text-sm text-gray-700 font-semibold">🛍️ Products Available:</span>
            <span className="bg-gradient-to-r from-pink-500 to-pink-600 text-white px-4 py-1.5 rounded-full text-sm font-bold shadow-md">
              {products.length} items
            </span>
          </div>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-[#D4A574] border-t-[#8B6F47]"></div>
            <p className="mt-4 text-[#8B6F47] font-semibold">Loading products...</p>
          </div>
        )}

        {/* Products Grid */}
        {!loading && products.length > 0 && (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {products.map((product) => (
              <ExternalProductCard
                key={`${product.source}-${product.id}`}
                id={product.id}
                title={product.title}
                price={product.price}
                image={product.image}
                source={product.source}
                url={product.url}
                rating={product.rating}
              />
            ))}
          </div>
        )}

        {/* No Results */}
        {!loading && products.length === 0 && (
          <div className="text-center py-12">
            <span className="text-6xl mb-4 block">🔍</span>
            <h3 className="text-xl font-bold text-[#8B6F47] mb-2">No products found</h3>
            <p className="text-gray-600">Try searching with different keywords or select a category</p>
          </div>
        )}

        {/* Test Button */}
        <div className="mt-8 text-center">
          <button
            onClick={() => loadProducts("women dress")}
            className="bg-gradient-to-r from-[#8B6F47] to-[#D4A574] text-white px-8 py-3 rounded-lg font-semibold hover:shadow-lg transition-all"
          >
            🔄 Load Women's Dresses
          </button>
        </div>

        {/* Info Notice */}
        <div className="mt-12 bg-gradient-to-r from-[#f5f1e8] to-[#faf8f3] border-2 border-[#D4A574] rounded-lg p-6">
          <h3 className="font-bold text-[#8B6F47] mb-2 flex items-center gap-2">
            <span>✨</span>
            <span>FashioPulse Collection</span>
          </h3>
          <p className="text-sm text-gray-700 mb-3">
            Browse thousands of clothing items for men, women, and kids from our curated collection.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
            <div className="bg-white rounded-lg p-3 border border-[#D4A574]">
              <div className="text-2xl mb-2">👩</div>
              <div className="font-semibold text-[#8B6F47]">Women's Fashion</div>
              <div className="text-xs text-gray-600">Dresses, tops, pants & more</div>
            </div>
            <div className="bg-white rounded-lg p-3 border border-[#D4A574]">
              <div className="text-2xl mb-2">👨</div>
              <div className="font-semibold text-[#8B6F47]">Men's Fashion</div>
              <div className="text-xs text-gray-600">Shirts, jeans, jackets & more</div>
            </div>
            <div className="bg-white rounded-lg p-3 border border-[#D4A574]">
              <div className="text-2xl mb-2">👧</div>
              <div className="font-semibold text-[#8B6F47]">Kids' Fashion</div>
              <div className="text-xs text-gray-600">Boys & girls clothing</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
