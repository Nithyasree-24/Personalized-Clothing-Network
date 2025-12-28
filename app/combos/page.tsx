"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import Header from "../../components/Header";
import { useCart } from "../../context/CartContext";

interface ComboProduct {
  id: string;
  name: string;
  price: number;
  originalPrice: number;
  discount: number;
  image: string;
  items: string[];
  category: string;
  description: string;
}

export default function CombosPage() {
  const router = useRouter();
  const { wishlist, toggleWishlist, addToCart, cart, cartTotal, removeFromCart, incrementQuantity, decrementQuantity, removeFromWishlist, cartCount } = useCart();
  const [userName, setUserName] = useState<string | null>(null);
  const [combos, setCombos] = useState<ComboProduct[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState<string>("All");

  useEffect(() => {
    const user = localStorage.getItem("user");
    if (user) {
      try {
        const userData = JSON.parse(user);
        setUserName(userData.name || "Guest");
      } catch {}
    }
    
    // Load combo products
    loadCombos();
  }, []);

  const loadCombos = () => {
    // Sample combo data - in real app, this would come from API
    const sampleCombos: ComboProduct[] = [
      {
        id: "combo-1",
        name: "Summer Casual Combo",
        price: 1299,
        originalPrice: 1899,
        discount: 32,
        image: "/assets/tshirt.jpg",
        items: ["Cotton T-Shirt", "Denim Jeans", "Canvas Sneakers"],
        category: "Casual",
        description: "Perfect summer casual outfit with comfortable cotton t-shirt, stylish denim jeans, and trendy canvas sneakers."
      },
      {
        id: "combo-2",
        name: "Office Professional Combo",
        price: 2499,
        originalPrice: 3299,
        discount: 24,
        image: "/assets/dress.svg",
        items: ["Formal Shirt", "Dress Pants", "Leather Shoes", "Belt"],
        category: "Formal",
        description: "Complete professional look with formal shirt, dress pants, leather shoes, and matching belt."
      },
      {
        id: "combo-3",
        name: "Party Night Combo",
        price: 1899,
        originalPrice: 2599,
        discount: 27,
        image: "/assets/hoodie.jpg",
        items: ["Party Dress", "High Heels", "Clutch Bag"],
        category: "Party",
        description: "Stunning party outfit with elegant dress, stylish high heels, and matching clutch bag."
      },
      {
        id: "combo-4",
        name: "Gym Workout Combo",
        price: 999,
        originalPrice: 1399,
        discount: 29,
        image: "/assets/tshirt.jpg",
        items: ["Sports T-Shirt", "Track Pants", "Running Shoes"],
        category: "Sports",
        description: "Complete workout gear with moisture-wicking t-shirt, comfortable track pants, and performance running shoes."
      },
      {
        id: "combo-5",
        name: "Winter Warm Combo",
        price: 2199,
        originalPrice: 2899,
        discount: 24,
        image: "/assets/hoodie.jpg",
        items: ["Wool Sweater", "Warm Jeans", "Winter Boots", "Scarf"],
        category: "Winter",
        description: "Stay warm and stylish with wool sweater, warm jeans, winter boots, and cozy scarf."
      },
      {
        id: "combo-6",
        name: "Beach Holiday Combo",
        price: 1599,
        originalPrice: 2199,
        discount: 27,
        image: "/assets/dress.svg",
        items: ["Beach Dress", "Sandals", "Sun Hat", "Beach Bag"],
        category: "Casual",
        description: "Perfect beach vacation outfit with flowy dress, comfortable sandals, sun hat, and spacious beach bag."
      }
    ];
    
    setCombos(sampleCombos);
    setLoading(false);
  };

  const handleLogout = () => {
    localStorage.removeItem("user");
    setUserName(null);
  };

  const handleAddToCart = (combo: ComboProduct) => {
    addToCart({
      id: combo.id,
      title: combo.name,
      price: combo.price,
      qty: 1,
      image: combo.image
    });
  };

  const categories = ["All", "Casual", "Formal", "Party", "Sports", "Winter"];
  
  const filteredCombos = selectedCategory === "All" 
    ? combos 
    : combos.filter(combo => combo.category === selectedCategory);

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 to-white">
      <Header
        cartCount={cartCount}
        cartTotal={cartTotal}
        cartItems={cart}
        onRemoveFromCart={removeFromCart}
        onIncreaseQty={incrementQuantity}
        onDecreaseQty={decrementQuantity}
        onAddToCart={addToCart}
        wishlistItems={wishlist}
        onRemoveFromWishlist={removeFromWishlist}
        userName={userName}
        onLogout={handleLogout}
      />
      
      <div className="p-4 sm:p-8">
        <div className="mx-auto max-w-7xl">
          {/* Header */}
          <div className="mb-8 text-center">
            <h1 className="text-4xl font-bold bg-gradient-to-r from-pink-600 to-pink-800 bg-clip-text text-transparent mb-4">
              Fashion Combos
            </h1>
            <p className="text-gray-600 text-lg max-w-2xl mx-auto">
              Discover perfectly curated outfit combinations at amazing prices. Save more when you buy complete looks!
            </p>
          </div>

          {/* Category Filter */}
          <div className="mb-8 flex flex-wrap justify-center gap-3">
            {categories.map((category) => (
              <button
                key={category}
                onClick={() => setSelectedCategory(category)}
                className={`px-6 py-3 rounded-full font-medium transition-all ${
                  selectedCategory === category
                    ? "bg-gradient-to-r from-pink-500 to-pink-600 text-white shadow-lg"
                    : "bg-white text-gray-700 border-2 border-pink-200 hover:border-pink-400 hover:text-pink-600"
                }`}
              >
                {category}
              </button>
            ))}
          </div>

          {/* Loading State */}
          {loading ? (
            <div className="flex justify-center items-center py-20">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-pink-500"></div>
            </div>
          ) : (
            /* Combos Grid */
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {filteredCombos.map((combo) => (
                <div
                  key={combo.id}
                  className="bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 overflow-hidden group"
                >
                  {/* Image */}
                  <div className="relative h-64 bg-gradient-to-br from-pink-50 to-pink-100">
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    <img
                      src={combo.image}
                      alt={combo.name}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                    
                    {/* Discount Badge */}
                    <div className="absolute top-4 left-4 bg-gradient-to-r from-red-500 to-red-600 text-white px-3 py-1 rounded-full text-sm font-bold">
                      {combo.discount}% OFF
                    </div>
                    
                    {/* Wishlist Button */}
                    <button
                      onClick={() => toggleWishlist({
                        id: combo.id,
                        title: combo.name,
                        price: combo.price,
                        image: combo.image
                      })}
                      className="absolute top-4 right-4 bg-white rounded-full p-2 shadow-md hover:shadow-lg transition-all"
                    >
                      <span className={`text-xl ${
                        wishlist.some(item => item.id === combo.id) ? "text-red-500" : "text-gray-400"
                      }`}>
                        ❤️
                      </span>
                    </button>
                  </div>

                  {/* Content */}
                  <div className="p-6">
                    {/* Category */}
                    <div className="text-sm text-pink-600 font-medium mb-2">
                      {combo.category} Combo
                    </div>
                    
                    {/* Title */}
                    <h3 className="text-xl font-bold text-gray-800 mb-3">
                      {combo.name}
                    </h3>
                    
                    {/* Items Included */}
                    <div className="mb-4">
                      <p className="text-sm text-gray-600 font-medium mb-2">Includes:</p>
                      <ul className="text-sm text-gray-600 space-y-1">
                        {combo.items.map((item, index) => (
                          <li key={index} className="flex items-center">
                            <span className="w-2 h-2 bg-pink-400 rounded-full mr-2"></span>
                            {item}
                          </li>
                        ))}
                      </ul>
                    </div>
                    
                    {/* Description */}
                    <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                      {combo.description}
                    </p>
                    
                    {/* Price */}
                    <div className="flex items-center justify-between mb-4">
                      <div>
                        <span className="text-2xl font-bold text-pink-600">₹{combo.price}</span>
                        <span className="text-gray-400 line-through ml-2">₹{combo.originalPrice}</span>
                      </div>
                      <div className="text-green-600 font-medium text-sm">
                        Save ₹{combo.originalPrice - combo.price}
                      </div>
                    </div>
                    
                    {/* Actions */}
                    <div className="flex gap-3">
                      <button
                        onClick={() => handleAddToCart(combo)}
                        className="flex-1 bg-gradient-to-r from-pink-500 to-pink-600 text-white py-3 px-4 rounded-lg font-medium hover:from-pink-600 hover:to-pink-700 transition-all shadow-md hover:shadow-lg"
                      >
                        Add to Cart
                      </button>
                      <button className="px-4 py-3 border-2 border-pink-200 text-pink-600 rounded-lg hover:border-pink-400 hover:bg-pink-50 transition-all">
                        View Details
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* No Results */}
          {!loading && filteredCombos.length === 0 && (
            <div className="text-center py-20">
              <div className="text-6xl mb-4">🛍️</div>
              <h3 className="text-2xl font-bold text-gray-800 mb-2">No combos found</h3>
              <p className="text-gray-600 mb-6">Try selecting a different category</p>
              <button
                onClick={() => setSelectedCategory("All")}
                className="bg-gradient-to-r from-pink-500 to-pink-600 text-white px-6 py-3 rounded-lg font-medium hover:from-pink-600 hover:to-pink-700 transition-all"
              >
                View All Combos
              </button>
            </div>
          )}

          {/* Benefits Section */}
          <div className="mt-16 bg-gradient-to-r from-pink-50 to-rose-50 rounded-2xl p-8">
            <h2 className="text-3xl font-bold text-center text-gray-800 mb-8">
              Why Choose Our Combos?
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="w-16 h-16 bg-pink-500 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl text-white">💰</span>
                </div>
                <h3 className="text-xl font-bold text-gray-800 mb-2">Save Money</h3>
                <p className="text-gray-600">Get up to 35% off when you buy complete outfits instead of individual items.</p>
              </div>
              <div className="text-center">
                <div className="w-16 h-16 bg-pink-500 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl text-white">👗</span>
                </div>
                <h3 className="text-xl font-bold text-gray-800 mb-2">Perfect Match</h3>
                <p className="text-gray-600">Expertly curated combinations that guarantee a coordinated and stylish look.</p>
              </div>
              <div className="text-center">
                <div className="w-16 h-16 bg-pink-500 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl text-white">⏰</span>
                </div>
                <h3 className="text-xl font-bold text-gray-800 mb-2">Save Time</h3>
                <p className="text-gray-600">No more mixing and matching. Get complete outfits ready for any occasion.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}