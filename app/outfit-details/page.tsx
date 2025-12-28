"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

type OutfitItem = {
  id: string;
  type: string;
  emoji: string;
  productId: string;
  title: string;
  price: number;
  imageUrl: string;
};

export default function OutfitDetailsPage() {
  const router = useRouter();
  const [outfitItems, setOutfitItems] = useState<OutfitItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const storedOutfit = sessionStorage.getItem("currentOutfit");
    if (storedOutfit) {
      const parsed = JSON.parse(storedOutfit);
      // Check if it's the new format (from avatar builder) or old format
      if (parsed.products && Array.isArray(parsed.products)) {
        setOutfitItems(parsed.products);
      } else if (Array.isArray(parsed)) {
        setOutfitItems(parsed);
      }
    }
    setLoading(false);
  }, []);

  const totalPrice = Array.isArray(outfitItems) ? outfitItems.reduce((sum, item) => sum + (Number(item.price) || 0), 0) : 0;

  const handleAddAllToCart = () => {
    if (!Array.isArray(outfitItems) || outfitItems.length === 0) {
      alert("No items in outfit!");
      return;
    }

    // Add all items to cart
    outfitItems.forEach(item => {
      const cartItem = {
        id: item.id || item.productId,
        title: item.title,
        price: item.price,
        imageUrl: item.imageUrl,
        qty: 1,
      };
      
      // Get existing cart
      const existingCart = JSON.parse(localStorage.getItem("cart") || "[]");
      
      // Check if item already in cart
      const existingIndex = existingCart.findIndex((i: any) => i.id === (item.id || item.productId));
      if (existingIndex >= 0) {
        existingCart[existingIndex].qty += 1;
      } else {
        existingCart.push(cartItem);
      }
      
      localStorage.setItem("cart", JSON.stringify(existingCart));
    });

    alert("All items added to cart!");
    router.push("/cart");
  };

  const handleBuyNow = () => {
    handleAddAllToCart();
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-pink-50 via-purple-50 to-blue-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-pink-300 border-t-pink-600"></div>
          <p className="mt-4 text-gray-600">Loading outfit...</p>
        </div>
      </div>
    );
  }

  if (outfitItems.length === 0) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-pink-50 via-purple-50 to-blue-50">
        <div className="max-w-4xl mx-auto px-4 py-12 text-center">
          <div className="text-6xl mb-4">😕</div>
          <h2 className="text-2xl font-bold text-gray-700 mb-4">No Outfit Found</h2>
          <p className="text-gray-600 mb-8">Please create an outfit first in the Avatar Builder.</p>
          <Link
            href="/avatar-builder"
            className="inline-block bg-gradient-to-r from-pink-500 to-pink-600 text-white px-8 py-3 rounded-lg font-semibold hover:shadow-xl transition-all"
          >
            Go to Avatar Builder
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-purple-50 to-blue-50">
      {/* Header */}
      <div className="bg-white shadow-sm sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <button
              onClick={() => router.back()}
              className="text-pink-600 hover:text-pink-700 font-semibold"
            >
              ← Back to Avatar
            </button>
            <h1 className="text-2xl font-bold text-pink-600">Your Outfit</h1>
            <Link href="/home" className="text-pink-600 hover:text-pink-700 font-semibold">
              Home
            </Link>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header Section */}
        <div className="text-center mb-12">
          <div className="bg-gradient-to-r from-pink-500 to-pink-600 py-6 px-8 rounded-2xl shadow-lg inline-block mb-6">
            <h2 className="text-4xl font-bold text-white mb-2">
              🎉 Your Perfect Outfit!
            </h2>
          </div>
          <p className="text-xl text-gray-600">
            Here are all the items from your avatar's outfit
          </p>
        </div>

        {/* Outfit Summary */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-2xl font-bold text-gray-800">Outfit Items</h3>
            <div className="text-right">
              <p className="text-sm text-gray-600">Total Items</p>
              <p className="text-2xl font-bold text-pink-600">{Array.isArray(outfitItems) ? outfitItems.length : 0}</p>
            </div>
          </div>

          {/* Items Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
            {Array.isArray(outfitItems) && outfitItems.map((item) => (
              <div
                key={item.id}
                className="bg-gradient-to-br from-pink-50 to-purple-50 rounded-xl p-6 border-2 border-pink-200 hover:shadow-lg transition-all"
              >
                <div className="flex items-start gap-4">
                  <div className="text-5xl">{item.emoji}</div>
                  <div className="flex-1">
                    <h4 className="font-bold text-gray-800 mb-2">{item.title}</h4>
                    <p className="text-sm text-gray-600 mb-2 capitalize">
                      Type: {item.type}
                    </p>
                    <p className="text-xl font-bold text-pink-600">${(Number(item.price) || 0).toFixed(2)}</p>
                    <Link
                      href={`/products/${item.productId}`}
                      className="inline-block mt-3 text-sm text-pink-600 hover:text-pink-700 font-semibold underline"
                    >
                      View Details →
                    </Link>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Total Price */}
          <div className="border-t-2 border-pink-200 pt-6">
            <div className="flex items-center justify-between mb-6">
              <div>
                <p className="text-gray-600 mb-1">Complete Outfit Total</p>
                <p className="text-4xl font-bold text-pink-600">${totalPrice.toFixed(2)}</p>
              </div>
              <div className="text-right">
                <p className="text-sm text-green-600 font-semibold">✓ All items available</p>
                <p className="text-xs text-gray-500">Ready to purchase</p>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <button
                onClick={handleAddAllToCart}
                className="bg-white border-2 border-pink-500 text-pink-600 px-8 py-4 rounded-lg text-lg font-semibold hover:bg-pink-50 transition-all"
              >
                🛒 Add All to Cart
              </button>
              <button
                onClick={handleBuyNow}
                className="bg-gradient-to-r from-pink-500 to-pink-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:shadow-xl transition-all transform hover:scale-105"
              >
                💳 Buy Complete Outfit Now
              </button>
            </div>
          </div>
        </div>

        {/* Additional Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Link
            href="/avatar-builder"
            className="bg-white rounded-xl p-6 shadow-md hover:shadow-lg transition-all text-center border-2 border-pink-200"
          >
            <div className="text-4xl mb-3">🎨</div>
            <h4 className="font-bold text-gray-800 mb-2">Try Another Outfit</h4>
            <p className="text-sm text-gray-600">Create a new look</p>
          </Link>

          <Link
            href="/home"
            className="bg-white rounded-xl p-6 shadow-md hover:shadow-lg transition-all text-center border-2 border-pink-200"
          >
            <div className="text-4xl mb-3">🏠</div>
            <h4 className="font-bold text-gray-800 mb-2">Browse More</h4>
            <p className="text-sm text-gray-600">Explore our collection</p>
          </Link>

          <Link
            href="/cart"
            className="bg-white rounded-xl p-6 shadow-md hover:shadow-lg transition-all text-center border-2 border-pink-200"
          >
            <div className="text-4xl mb-3">🛍️</div>
            <h4 className="font-bold text-gray-800 mb-2">View Cart</h4>
            <p className="text-sm text-gray-600">Check your items</p>
          </Link>
        </div>
      </div>
    </div>
  );
}
