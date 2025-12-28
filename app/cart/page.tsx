"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import Header from "../../components/Header";
import { useCart } from "../../context/CartContext";

export default function CartPage() {
  const router = useRouter();
  const { cart, cartTotal, removeFromCart, incrementQuantity, decrementQuantity, wishlist, addToCart, removeFromWishlist, cartCount } = useCart();
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

  const deliveryCharge = cartTotal > 999 ? 0 : 50;
  const totalAmount = cartTotal + deliveryCharge;

  return (
    <div className="min-h-screen bg-gray-50">
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
          <Link href="/home" className="text-indigo-600 hover:underline flex items-center gap-2 font-medium">
            <span>←</span>
            <span>Continue Shopping</span>
          </Link>
          <h1 className="text-3xl font-bold text-gray-800">Shopping Cart</h1>
          <div className="w-40"></div>
        </div>

        {cart.length === 0 ? (
          <div className="bg-white rounded-xl p-12 shadow-md text-center">
            <div className="text-6xl mb-4">🛒</div>
            <h2 className="text-2xl font-bold text-gray-800 mb-2">Your cart is empty</h2>
            <p className="text-gray-600 mb-6">Add items to get started!</p>
            <Link
              href="/home"
              className="inline-block bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-6 py-3 rounded-lg font-bold hover:from-indigo-700 hover:to-purple-700 transition-all"
            >
              Start Shopping
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Cart Items */}
            <div className="lg:col-span-2 space-y-4">
              {cart.map((item) => (
                <div
                  key={String(item.id)}
                  className="bg-white rounded-xl p-4 shadow-md hover:shadow-lg transition-shadow"
                >
                  <div className="flex gap-4">
                    {/* Product Image */}
                    <Link href={`/products/${item.id}`}>
                      <div className="w-24 h-24 sm:w-32 sm:h-32 bg-gray-50 rounded-lg flex-shrink-0 flex items-center justify-center overflow-hidden cursor-pointer group">
                        {item.image ? (
                          // eslint-disable-next-line @next/next/no-img-element
                          <img
                            src={item.image}
                            alt={item.title}
                            className="w-full h-full object-contain mix-blend-multiply group-hover:scale-110 transition-transform duration-300"
                          />
                        ) : (
                          <span className="text-4xl">📦</span>
                        )}
                      </div>
                    </Link>

                    {/* Product Details */}
                    <div className="flex-1 flex flex-col justify-between">
                      <div>
                        <Link href={`/products/${item.id}`}>
                          <h3 className="text-lg font-semibold text-gray-800 hover:text-indigo-600 cursor-pointer line-clamp-2">
                            {item.title}
                          </h3>
                        </Link>
                        <div className="text-2xl font-bold text-indigo-600 mt-2">
                          ₹{item.price}
                        </div>
                      </div>

                      {/* Quantity Controls */}
                      <div className="flex items-center justify-between mt-4">
                        <div className="flex items-center gap-3 bg-gray-100 rounded-lg p-1">
                          <button
                            onClick={() => decrementQuantity(item.id)}
                            className="rounded-lg bg-white border border-gray-300 px-3 py-1.5 text-base font-bold hover:bg-gray-50 transition-colors"
                          >
                            −
                          </button>
                          <span className="text-base font-bold text-gray-800 min-w-[30px] text-center">
                            {item.qty}
                          </span>
                          <button
                            onClick={() => incrementQuantity(item.id)}
                            className="rounded-lg bg-white border border-gray-300 px-3 py-1.5 text-base font-bold hover:bg-gray-50 transition-colors"
                          >
                            +
                          </button>
                        </div>

                        <button
                          onClick={() => removeFromCart(item.id)}
                          className="text-red-500 hover:text-red-700 font-medium flex items-center gap-1 transition-colors"
                        >
                          <span>🗑️</span>
                          <span className="hidden sm:inline">Remove</span>
                        </button>
                      </div>
                    </div>

                    {/* Item Total */}
                    <div className="hidden sm:flex flex-col items-end justify-between">
                      <div className="text-xl font-bold text-gray-800">
                        ₹{item.price * item.qty}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Order Summary */}
            <div className="lg:col-span-1">
              <div className="bg-white rounded-xl p-6 shadow-md sticky top-4">
                <h2 className="text-xl font-bold text-gray-800 mb-4 pb-4 border-b">
                  Order Summary
                </h2>

                <div className="space-y-3 mb-4">
                  <div className="flex justify-between text-gray-700">
                    <span>Subtotal ({cart.reduce((sum, item) => sum + item.qty, 0)} items)</span>
                    <span className="font-semibold">₹{cartTotal}</span>
                  </div>
                  <div className="flex justify-between text-gray-700">
                    <span>Delivery Charges</span>
                    <span className="font-semibold">
                      {deliveryCharge === 0 ? (
                        <span className="text-green-600">FREE</span>
                      ) : (
                        `₹${deliveryCharge}`
                      )}
                    </span>
                  </div>
                  {cartTotal < 999 && (
                    <div className="text-xs text-green-600 bg-green-50 p-2 rounded">
                      Add ₹{999 - cartTotal} more for FREE delivery!
                    </div>
                  )}
                </div>

                <div className="border-t pt-4 mb-6">
                  <div className="flex justify-between text-xl font-bold text-gray-800">
                    <span>Total Amount</span>
                    <span className="text-indigo-600">₹{totalAmount}</span>
                  </div>
                </div>

                <button
                  onClick={() => router.push("/checkout")}
                  className="w-full bg-gradient-to-r from-orange-500 to-red-500 text-white py-3 rounded-lg font-bold hover:from-orange-600 hover:to-red-600 shadow-lg hover:shadow-xl transition-all mb-3"
                >
                  Proceed to Checkout
                </button>

                <div className="text-center text-xs text-gray-500 mt-4">
                  <p>🔒 Safe and Secure Payments</p>
                  <p className="mt-1">Easy Returns & Refunds</p>
                </div>
              </div>
            </div>
          </div>
        )}
        </div>
      </div>
    </div>
  );
}
