"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { BaseAvatar, AppliedSticker, ProductSticker } from "../../types/avatar";
import AvatarCanvas from "./AvatarCanvas";

type ClothingLibraryProps = {
  baseAvatar: BaseAvatar;
  onBack: () => void;
};

export default function ClothingLibrary({ baseAvatar, onBack }: ClothingLibraryProps) {
  const router = useRouter();
  const [appliedStickers, setAppliedStickers] = useState<AppliedSticker[]>([]);
  const [products, setProducts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState<string>("all");

  useEffect(() => {
    fetchProducts();
  }, [baseAvatar.gender, baseAvatar.ageGroup]);

  const fetchProducts = async () => {
    setLoading(true);
    try {
      // Determine gender filter based on avatar
      let genderFilter = "";
      if (baseAvatar.ageGroup === "kid") {
        genderFilter = "kids";
      } else {
        genderFilter = baseAvatar.gender === "male" ? "men" : "women";
      }

      // Fetch products from backend with gender filter
      const response = await fetch(`http://localhost:5000/api/products/search?query=clothing fashion&category=fashion`);
      
      if (response.ok) {
        const data = await response.json();
        let allProducts = data.products || [];
        
        // Filter products by gender
        const filteredProducts = allProducts.filter((p: any) => {
          const title = p.title.toLowerCase();
          const gender = p.gender?.toLowerCase() || '';
          
          if (genderFilter === "kids") {
            // Kids products
            if (gender === 'kids') return true;
            if (title.includes('kids') || title.includes('children') || title.includes('child')) return true;
            if (title.includes('baby') || title.includes('infant') || title.includes('toddler')) return true;
            if (title.includes('boys ') || title.includes('girls ') || title.includes('boy ') || title.includes('girl ')) return true;
            return false;
          } else if (genderFilter === "men") {
            // Men's products
            if (gender === 'men' || gender === 'male') return true;
            if (title.includes('men\'s') || title.includes(' mens ') || title.includes('mens ')) return true;
            // Exclude women's and kids
            if (gender === 'women' || gender === 'female' || gender === 'kids') return false;
            if (title.includes('women') || title.includes('ladies') || title.includes('kids')) return false;
            return true;
          } else {
            // Women's products
            if (gender === 'women' || gender === 'female') return true;
            if (title.includes('women') || title.includes('womens') || title.includes('ladies')) return true;
            if (title.includes('dress') && !title.includes('address')) return true;
            if (title.includes('skirt') || title.includes('blouse')) return true;
            // Exclude men's and kids
            if (gender === 'men' || gender === 'male' || gender === 'kids') return false;
            if (title.includes('men\'s') || title.includes('mens') || title.includes('kids')) return false;
            return false;
          }
        });
        
        console.log(`Fetched ${filteredProducts.length} products for ${genderFilter}`);
        setProducts(filteredProducts);
      }
    } catch (error) {
      console.error("Error fetching products:", error);
      setProducts([]);
    } finally {
      setLoading(false);
    }
  };

  const categories = [
    { id: "all", name: "All Items", icon: "👕", emoji: "🎨" },
    { id: "tops", name: "Tops", icon: "👔", emoji: "👔" },
    { id: "bottoms", name: "Bottoms", icon: "👖", emoji: "👖" },
    { id: "outerwear", name: "Outerwear", icon: "🧥", emoji: "🧥" },
    { id: "shoes", name: "Shoes", icon: "👟", emoji: "👟" },
    { id: "accessories", name: "Accessories", icon: "👜", emoji: "👜" },
  ];

  const getProductCategory = (title: string): "top" | "bottom" | "outerwear" | "shoes" | "accessory" => {
    const lower = title.toLowerCase();
    if (lower.includes("jacket") || lower.includes("coat") || lower.includes("sweater")) return "outerwear";
    if (lower.includes("pant") || lower.includes("jean") || lower.includes("short") || lower.includes("skirt")) return "bottom";
    if (lower.includes("shoe") || lower.includes("sneaker") || lower.includes("boot")) return "shoes";
    if (lower.includes("bag") || lower.includes("hat") || lower.includes("accessory") || lower.includes("watch")) return "accessory";
    return "top";
  };

  const getProductEmoji = (title: string): string => {
    const lower = title.toLowerCase();
    if (lower.includes("dress")) return "👗";
    if (lower.includes("shirt") || lower.includes("top") || lower.includes("blouse")) return "👔";
    if (lower.includes("pant") || lower.includes("jean")) return "👖";
    if (lower.includes("shoe") || lower.includes("sneaker")) return "👟";
    if (lower.includes("jacket") || lower.includes("coat")) return "🧥";
    if (lower.includes("bag")) return "👜";
    if (lower.includes("hat")) return "🧢";
    return "👕";
  };

  const handleApplySticker = (product: any) => {
    const category = getProductCategory(product.title);
    const emoji = getProductEmoji(product.title);
    const productId = product.product_id || product.id;
    
    const newSticker: AppliedSticker = {
      sticker_id: emoji,
      product_id: productId,
      category,
      position: { x: 50, y: category === "top" ? 35 : category === "bottom" ? 55 : category === "shoes" ? 85 : 25 },
      scale: 1,
      zIndex: appliedStickers.length + 1,
    };

    // Remove existing item of same category (except accessories)
    if (category !== "accessory") {
      setAppliedStickers(prev => [...prev.filter(s => s.category !== category), newSticker]);
    } else {
      setAppliedStickers(prev => [...prev, newSticker]);
    }
  };

  const handleRemoveSticker = (stickerId: string) => {
    setAppliedStickers(prev => prev.filter(s => s.sticker_id !== stickerId));
  };

  const handleGiveThisOutfit = () => {
    if (appliedStickers.length === 0) {
      alert("Please add some items to your avatar first!");
      return;
    }

    // Store outfit data
    const outfitData = {
      avatar: baseAvatar,
      stickers: appliedStickers,
      products: appliedStickers.map(sticker => 
        products.find(p => (p.product_id || p.id) === sticker.product_id)
      ).filter(Boolean),
    };

    sessionStorage.setItem("currentOutfit", JSON.stringify(outfitData));
    router.push("/outfit-details");
  };

  const filteredProducts = selectedCategory === "all"
    ? products
    : products.filter(p => {
        const cat = getProductCategory(p.title);
        if (selectedCategory === "tops") return cat === "top";
        if (selectedCategory === "bottoms") return cat === "bottom";
        if (selectedCategory === "outerwear") return cat === "outerwear";
        if (selectedCategory === "shoes") return cat === "shoes";
        if (selectedCategory === "accessories") return cat === "accessory";
        return true;
      });

  return (
    <div className="max-w-7xl mx-auto">
      <button onClick={onBack} className="mb-6 text-pink-600 hover:text-pink-700 font-semibold flex items-center gap-2">
        <span>←</span>
        <span>Back to Avatar Creator</span>
      </button>

      <div className="bg-white rounded-2xl shadow-xl p-6 mb-6">
        <h2 className="text-3xl font-bold text-pink-600 mb-2 text-center">
          Step 2: Try On Clothes
        </h2>
        <p className="text-gray-600 text-center mb-4">
          Click on clothing items to apply them to your avatar
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Avatar Preview */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-2xl shadow-xl p-6 sticky top-24">
            <h3 className="text-xl font-bold text-pink-600 mb-4 text-center">Your Avatar</h3>
            
            <div className="bg-gradient-to-br from-pink-100 to-purple-100 rounded-xl p-6 mb-4 flex justify-center">
              <AvatarCanvas avatar={baseAvatar} appliedStickers={appliedStickers} size={280} />
            </div>

            {/* Applied Items */}
            <div className="bg-gray-50 rounded-lg p-4 mb-4 max-h-48 overflow-y-auto">
              <h4 className="font-bold text-gray-700 mb-2 text-sm">Wearing:</h4>
              {appliedStickers.length === 0 ? (
                <p className="text-xs text-gray-500">No items yet. Click items below to try them on!</p>
              ) : (
                <div className="space-y-2">
                  {appliedStickers.map((sticker, idx) => {
                    const product = products.find(p => (p.product_id || p.id) === sticker.product_id);
                    return (
                      <div key={idx} className="flex items-center justify-between bg-white rounded p-2">
                        <div className="flex items-center gap-2 flex-1 min-w-0">
                          <span className="text-xl">{sticker.sticker_id}</span>
                          <span className="text-xs text-gray-600 truncate">{product?.title || "Item"}</span>
                        </div>
                        <button
                          onClick={() => handleRemoveSticker(sticker.sticker_id)}
                          className="ml-2 bg-red-500 text-white rounded-full w-5 h-5 text-xs hover:bg-red-600"
                        >
                          ✕
                        </button>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>

            {/* Give This Outfit Button */}
            <button
              onClick={handleGiveThisOutfit}
              disabled={appliedStickers.length === 0}
              className={`w-full py-3 rounded-lg font-semibold transition-all ${
                appliedStickers.length === 0
                  ? "bg-gray-300 text-gray-500 cursor-not-allowed"
                  : "bg-gradient-to-r from-pink-500 to-pink-600 text-white hover:shadow-xl transform hover:scale-105"
              }`}
            >
              🛍️ Give This Outfit
            </button>
          </div>
        </div>

        {/* Clothing Library */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-2xl shadow-xl p-6">
            <h3 className="text-2xl font-bold text-pink-600 mb-6">Clothing Library</h3>

            {/* Category Filter */}
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
                  <span className="mr-2">{cat.icon}</span>
                  {cat.name}
                </button>
              ))}
            </div>

            {/* Products Grid */}
            {loading ? (
              <div className="text-center py-12">
                <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-pink-300 border-t-pink-600"></div>
                <p className="mt-4 text-gray-600">Loading clothing items...</p>
              </div>
            ) : (
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
                {filteredProducts.map((product) => {
                  const imageUrl = product.image_url || product.imageUrl;
                  const productPrice = product.price || 0;
                  const productId = product.product_id || product.id;
                  
                  return (
                    <button
                      key={productId}
                      onClick={() => handleApplySticker({ ...product, id: productId })}
                      className="group relative bg-white rounded-xl overflow-hidden hover:shadow-xl transition-all transform hover:scale-105 border-2 border-pink-200 hover:border-pink-400"
                      title={`${product.title} - ₹${productPrice}`}
                    >
                      <div className="aspect-square bg-gray-100 relative overflow-hidden">
                        {imageUrl ? (
                          <img 
                            src={imageUrl} 
                            alt={product.title} 
                            className="w-full h-full object-cover"
                            onError={(e) => {
                              // Fallback to emoji if image fails to load
                              const target = e.currentTarget;
                              target.style.display = 'none';
                            }}
                          />
                        ) : null}
                        {!imageUrl && (
                          <div className="absolute inset-0 flex items-center justify-center text-6xl bg-gradient-to-br from-pink-50 to-purple-50">
                            {getProductEmoji(product.title)}
                          </div>
                        )}
                        <div className="absolute top-2 right-2 bg-white/90 rounded-full p-1 shadow-md text-xl">
                          {getProductEmoji(product.title)}
                        </div>
                      </div>
                      <div className="p-3 bg-gradient-to-br from-pink-50 to-purple-50">
                        <p className="text-xs text-gray-700 font-medium truncate mb-1" title={product.title}>
                          {product.title}
                        </p>
                        <p className="text-sm font-bold text-pink-600">₹{Math.round(productPrice)}</p>
                      </div>
                      <div className="absolute inset-0 bg-pink-600/90 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                        <span className="text-white font-bold text-sm">👆 Try On</span>
                      </div>
                    </button>
                  );
                })}
              </div>
            )}

            {filteredProducts.length === 0 && !loading && (
              <div className="text-center py-12">
                <p className="text-gray-500">No items found in this category.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
