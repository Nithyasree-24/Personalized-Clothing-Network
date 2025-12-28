"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import CustomAvatar from "./CustomAvatar";

type AvatarDressUpProps = {
  avatarData: any;
  gender: "women" | "men" | "kids";
  onBack: () => void;
};

type OutfitItem = {
  id: string;
  type: "top" | "bottom" | "dress" | "shoes" | "accessory";
  emoji: string;
  productId: string;
  title: string;
  price: number;
  imageUrl: string;
};

export default function AvatarDressUp({ avatarData, gender, onBack }: AvatarDressUpProps) {
  const router = useRouter();
  const [products, setProducts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState<string>("all");
  const [wornItems, setWornItems] = useState<OutfitItem[]>([]);

  useEffect(() => {
    fetchProducts();
  }, [gender]);

  const fetchProducts = async () => {
    try {
      const searchQuery = gender === "women" ? "dress" : gender === "men" ? "shirt" : "kids clothing";
      const response = await fetch(`http://localhost:5000/api/products/search?query=${searchQuery}&limit=100`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const contentType = response.headers.get("content-type");
      if (!contentType || !contentType.includes("application/json")) {
        console.warn("Backend not returning JSON");
        setProducts([]);
        setLoading(false);
        return;
      }
      
      const data = await response.json();
      const filteredByGender = (data.products || []).filter((p: any) => {
        const genderField = p.gender?.toLowerCase() || "";
        return genderField.includes(gender);
      });
      
      setProducts(filteredByGender.length > 0 ? filteredByGender : data.products || []);
    } catch (error) {
      console.error("Error fetching products:", error);
      setProducts([]);
    } finally {
      setLoading(false);
    }
  };

  const categories = [
    { id: "all", name: "All Items", emoji: "👕" },
    { id: "tops", name: "Tops", emoji: "👔" },
    { id: "bottoms", name: "Bottoms", emoji: "👖" },
    { id: "dresses", name: "Dresses", emoji: "👗" },
    { id: "shoes", name: "Shoes", emoji: "👟" },
    { id: "accessories", name: "Accessories", emoji: "👜" },
  ];

  const getProductEmoji = (title: string): string => {
    const lowerTitle = title.toLowerCase();
    if (lowerTitle.includes("dress")) return "👗";
    if (lowerTitle.includes("shirt") || lowerTitle.includes("top") || lowerTitle.includes("blouse")) return "👔";
    if (lowerTitle.includes("pant") || lowerTitle.includes("jean") || lowerTitle.includes("trouser")) return "👖";
    if (lowerTitle.includes("shoe") || lowerTitle.includes("sneaker") || lowerTitle.includes("boot")) return "👟";
    if (lowerTitle.includes("bag") || lowerTitle.includes("purse")) return "👜";
    if (lowerTitle.includes("hat") || lowerTitle.includes("cap")) return "🧢";
    if (lowerTitle.includes("jacket") || lowerTitle.includes("coat")) return "🧥";
    if (lowerTitle.includes("skirt")) return "👗";
    return "👕";
  };

  const getProductType = (title: string): "top" | "bottom" | "dress" | "shoes" | "accessory" => {
    const lowerTitle = title.toLowerCase();
    if (lowerTitle.includes("dress") || lowerTitle.includes("skirt")) return "dress";
    if (lowerTitle.includes("pant") || lowerTitle.includes("jean") || lowerTitle.includes("trouser") || lowerTitle.includes("short")) return "bottom";
    if (lowerTitle.includes("shoe") || lowerTitle.includes("sneaker") || lowerTitle.includes("boot")) return "shoes";
    if (lowerTitle.includes("bag") || lowerTitle.includes("hat") || lowerTitle.includes("accessory")) return "accessory";
    return "top";
  };

  const handleTryOn = (product: any) => {
    const outfitItem: OutfitItem = {
      id: `${product.id}-${Date.now()}`,
      type: getProductType(product.title),
      emoji: getProductEmoji(product.title),
      productId: product.id,
      title: product.title,
      price: typeof product.price === 'number' ? product.price : parseFloat(product.price) || 0,
      imageUrl: product.imageUrl,
    };

    if (outfitItem.type !== "accessory") {
      setWornItems(prev => [...prev.filter(item => item.type !== outfitItem.type), outfitItem]);
    } else {
      setWornItems(prev => [...prev, outfitItem]);
    }
  };

  const handleRemoveItem = (itemId: string) => {
    setWornItems(prev => prev.filter(item => item.id !== itemId));
  };

  const handleGiveThisOutfit = () => {
    if (wornItems.length === 0) {
      alert("Please add some items to your avatar first!");
      return;
    }
    sessionStorage.setItem("currentOutfit", JSON.stringify(wornItems));
    router.push("/outfit-details");
  };

  const filteredProducts = selectedCategory === "all" 
    ? products 
    : products.filter(p => {
        const type = getProductType(p.title);
        if (selectedCategory === "tops") return type === "top";
        if (selectedCategory === "bottoms") return type === "bottom";
        if (selectedCategory === "dresses") return type === "dress";
        if (selectedCategory === "shoes") return type === "shoes";
        if (selectedCategory === "accessories") return type === "accessory";
        return true;
      });

  return (
    <div className="max-w-7xl mx-auto">
      <button onClick={onBack} className="mb-6 text-pink-600 hover:text-pink-700 font-semibold">
        ← Back to Customize Avatar
      </button>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-1">
          <div className="bg-white rounded-2xl shadow-xl p-6 sticky top-24">
            <h3 className="text-xl font-bold text-pink-600 mb-4 text-center">Your Avatar</h3>
            
            <div className="bg-gradient-to-br from-pink-100 to-purple-100 rounded-xl p-6 mb-4">
              <div className="text-center">
                <div className="relative inline-block">
                  <CustomAvatar config={avatarData} size={250} />
                  <div className="absolute bottom-10 left-1/2 transform -translate-x-1/2 flex flex-wrap justify-center gap-2">
                    {wornItems.map((item) => (
                      <div key={item.id} className="text-2xl bg-white rounded-full p-1 shadow-md">
                        {item.emoji}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
            
            <div className="bg-gray-50 rounded-lg p-3 mb-4 max-h-40 overflow-y-auto">
              <h4 className="font-bold text-gray-700 mb-2 text-sm">Wearing:</h4>
              {wornItems.length === 0 ? (
                <p className="text-xs text-gray-500">No items yet</p>
              ) : (
                <div className="space-y-1">
                  {wornItems.map((item) => (
                    <div key={item.id} className="flex items-center justify-between bg-white rounded p-2">
                      <div className="flex items-center gap-2 flex-1 min-w-0">
                        <span className="text-lg">{item.emoji}</span>
                        <span className="text-xs text-gray-600 truncate">{item.title}</span>
                        <span className="text-xs font-bold text-pink-600">${item.price.toFixed(2)}</span>
                      </div>
                      <button
                        onClick={() => handleRemoveItem(item.id)}
                        className="ml-2 bg-red-500 text-white rounded-full w-5 h-5 text-xs hover:bg-red-600 flex-shrink-0"
                      >
                        ✕
                      </button>
                    </div>
                  ))}
                  <div className="pt-2 border-t border-gray-200 text-center">
                    <p className="font-bold text-pink-600">
                      Total: ${wornItems.reduce((sum, item) => sum + (Number(item.price) || 0), 0).toFixed(2)}
                    </p>
                  </div>
                </div>
              )}
            </div>

            <button
              onClick={handleGiveThisOutfit}
              disabled={wornItems.length === 0}
              className={`w-full py-3 rounded-lg font-semibold transition-all ${
                wornItems.length === 0
                  ? "bg-gray-300 text-gray-500 cursor-not-allowed"
                  : "bg-gradient-to-r from-pink-500 to-pink-600 text-white hover:shadow-xl transform hover:scale-105"
              }`}
            >
              🛍️ Give This Outfit
            </button>
          </div>
        </div>

        <div className="lg:col-span-2">
          <div className="bg-white rounded-2xl shadow-xl p-6">
            <h3 className="text-2xl font-bold text-pink-600 mb-6">Try On Clothes</h3>

            <div className="flex flex-wrap gap-3 mb-6">
              {categories.map((cat) => (
                <button
                  key={cat.id}
                  onClick={() => setSelectedCategory(cat.id)}
                  className={`px-4 py-2 rounded-lg font-semibold transition-all ${
                    selectedCategory === cat.id
                      ? "bg-gradient-to-r from-pink-500 to-pink-600 text-white shadow-lg"
                      : "bg-gray-100 text-gray-700 hover:bg-pink-50"
                  }`}
                >
                  <span className="mr-2">{cat.emoji}</span>
                  {cat.name}
                </button>
              ))}
            </div>

            {loading ? (
              <div className="text-center py-12">
                <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-pink-300 border-t-pink-600"></div>
                <p className="mt-4 text-gray-600">Loading products...</p>
              </div>
            ) : (
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
                {filteredProducts.map((product) => (
                  <button
                    key={product.id}
                    onClick={() => handleTryOn(product)}
                    className="group relative bg-white rounded-xl overflow-hidden hover:shadow-xl transition-all transform hover:scale-105 border-2 border-pink-200 hover:border-pink-400"
                  >
                    <div className="aspect-square bg-gray-100 relative overflow-hidden">
                      {product.imageUrl && (
                        <img
                          src={product.imageUrl}
                          alt={product.title}
                          className="w-full h-full object-cover"
                        />
                      )}
                      {!product.imageUrl && (
                        <div className="absolute inset-0 flex items-center justify-center text-6xl bg-gradient-to-br from-pink-50 to-purple-50">
                          {getProductEmoji(product.title)}
                        </div>
                      )}
                      <div className="absolute top-2 right-2 bg-white rounded-full p-1 shadow-md text-xl">
                        {getProductEmoji(product.title)}
                      </div>
                    </div>
                    <div className="p-3 bg-gradient-to-br from-pink-50 to-purple-50">
                      <p className="text-xs text-gray-700 font-medium truncate mb-1" title={product.title}>
                        {product.title}
                      </p>
                      <p className="text-sm font-bold text-pink-600">
                        ${typeof product.price === 'number' ? product.price.toFixed(2) : parseFloat(product.price || 0).toFixed(2)}
                      </p>
                    </div>
                    <div className="absolute inset-0 bg-pink-600/90 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                      <span className="text-white font-bold text-sm">👆 Try On</span>
                    </div>
                  </button>
                ))}
              </div>
            )}

            {filteredProducts.length === 0 && !loading && (
              <div className="text-center py-12 bg-gradient-to-br from-pink-50 to-purple-50 rounded-xl p-8">
                <div className="text-6xl mb-4">😕</div>
                <h3 className="text-xl font-bold text-gray-700 mb-2">No Products Available</h3>
                <p className="text-gray-600 mb-4">
                  {products.length === 0 
                    ? "Please make sure the backend server is running on port 5000."
                    : "No products found in this category."}
                </p>
                {products.length === 0 && (
                  <div className="bg-white rounded-lg p-4 text-left max-w-md mx-auto">
                    <p className="text-sm text-gray-600 mb-2">To start the backend:</p>
                    <code className="block bg-gray-100 p-2 rounded text-xs">
                      python backend/app.py
                    </code>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
