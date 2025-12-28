"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import Header from "../../components/Header";
import { useCart } from "../../context/CartContext";

export default function WishlistPage() {
  const router = useRouter();
  const { wishlist, toggleWishlist, addToCart, cart, cartTotal, removeFromCart, incrementQuantity, decrementQuantity, removeFromWishlist, cartCount } = useCart();
  const [userName, setUserName] = useState<string | null>(null);

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

  const handleAddToCart = (item: any) => {
    if (item.price) {
      addToCart({
        id: item.id,
        title: item.title,
        price: item.price,
        qty: 1,
        image: item.image
      });
      router.push("/home");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-sky-50 to-white">
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
        <div className="mb-6 flex items-center justify-between">
          <Link href="/home" className="text-indigo-600 hover:underline flex items-center gap-2">
            <span>←</span>
            <span>Back to Shopping</span>
          </Link>
          <h1 className="text-3xl font-bold text-gray-800">My Wishlist</h1>
          <div className="w-32"></div>
        </div>

        {/* Wishlist Items */}
        {wishlist.length === 0 ? (
          <div className="bg-white rounded-xl p-12 shadow-md text-center">
            <div className="text-6xl mb-4">💔</div>
            <h2 className="text-2xl font-bold text-gray-800 mb-2">Your wishlist is empty</h2>
            <p className="text-gray-600 mb-6">Start adding items you love!</p>
            <Link
              href="/home"
              className="inline-block bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-6 py-3 rounded-lg font-bold hover:from-indigo-700 hover:to-purple-700 transition-all"
            >
              Continue Shopping
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
            {wishlist.map((item) => (
              <div
                key={String(item.id)}
                className="bg-white rounded-xl p-4 shadow-md hover:shadow-xl transition-shadow duration-200 relative group"
              >
                {/* Remove button */}
                <button
                  onClick={() => toggleWishlist(item)}
                  className="absolute top-2 right-2 bg-white rounded-full p-2 shadow-md hover:shadow-lg transition-shadow z-10"
                  title="Remove from wishlist"
                >
                  <span className="text-xl">❤️</span>
                </button>

                {/* Product Image */}
                <Link href={`/products/${item.id}`}>
                  <div className="w-full h-48 bg-gray-50 rounded-lg mb-4 flex items-center justify-center overflow-hidden cursor-pointer">
                    {item.image ? (
                      // eslint-disable-next-line @next/next/no-img-element
                      <img
                        src={item.image}
                        alt={item.title}
                        className="w-full h-full object-contain mix-blend-multiply group-hover:scale-110 transition-transform duration-300"
                      />
                    ) : (
                      <span className="text-4xl">❤️</span>
                    )}
                  </div>
                </Link>

                {/* Product Info */}
                <Link href={`/products/${item.id}`}>
                  <h3 className="text-sm font-medium text-gray-800 line-clamp-2 mb-2 cursor-pointer hover:text-indigo-600">
                    {item.title}
                  </h3>
                </Link>

                {item.price && (
                  <div className="text-lg font-bold text-indigo-600 mb-3">₹{item.price}</div>
                )}

                {/* Action Buttons */}
                <div className="flex gap-2">
                  <button
                    onClick={() => handleAddToCart(item)}
                    className="flex-1 rounded-lg bg-gradient-to-br from-blue-500 to-blue-700 text-white py-2 px-3 text-sm font-bold hover:from-blue-600 hover:to-blue-800 shadow-md hover:shadow-lg transition-all flex items-center justify-center gap-2"
                  >
                    <span>🛒</span>
                    <span>Add to Cart</span>
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Wishlist Summary */}
        {wishlist.length > 0 && (
          <div className="mt-8 bg-white rounded-xl p-6 shadow-md">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-xl font-bold text-gray-800">
                  {wishlist.length} {wishlist.length === 1 ? 'item' : 'items'} in your wishlist
                </h3>
                <p className="text-gray-600 mt-1">Keep shopping to find more items you love!</p>
              </div>
              <Link
                href="/home"
                className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-6 py-3 rounded-lg font-bold hover:from-indigo-700 hover:to-purple-700 transition-all"
              >
                Continue Shopping
              </Link>
            </div>
          </div>
        )}
        </div>
      </div>
    </div>
  );
}