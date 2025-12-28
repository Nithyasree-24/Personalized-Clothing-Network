"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import Header from "../../components/Header";
import { useCart } from "../../context/CartContext";

export default function CheckoutPage() {
  const router = useRouter();
  const { cart, cartTotal, clearCart, wishlist, removeFromWishlist, addToCart, removeFromCart, incrementQuantity, decrementQuantity, cartCount } = useCart();
  const [step, setStep] = useState(1);
  const [userName, setUserName] = useState<string | null>(null);

  // Form states
  const [shippingInfo, setShippingInfo] = useState({
    fullName: "",
    mobile: "",
    pincode: "",
    address: "",
    locality: "",
    city: "",
    state: "",
  });

  const [paymentMethod, setPaymentMethod] = useState("cod");

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

  useEffect(() => {
    if (cart.length === 0) {
      router.push("/home");
    }
  }, [cart, router]);

  const deliveryCharge = cartTotal > 999 ? 0 : 50;
  const totalAmount = cartTotal + deliveryCharge;

  const handlePlaceOrder = () => {
    // Generate order ID
    const orderId = `ORD${Date.now().toString().slice(-8)}`;
    const orderDate = new Date().toISOString();
    const deliveryDate = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(); // 7 days from now
    
    // Create order object
    const orderData = {
      id: orderId,
      date: orderDate,
      deliveryDate: deliveryDate,
      total: totalAmount,
      items: cart.map(item => ({
        ...item,
        deliveryDate: deliveryDate
      })),
      shippingInfo: shippingInfo,
      paymentMethod: paymentMethod,
      status: 'confirmed'
    };
    
    // Save order to localStorage
    try {
      const existingOrders = JSON.parse(localStorage.getItem("orders") || "[]");
      existingOrders.push(orderData);
      localStorage.setItem("orders", JSON.stringify(existingOrders));
    } catch (e) {
      console.error("Failed to save order", e);
    }
    
    // Clear the cart
    clearCart();
    
    // Redirect to order success page with order data
    localStorage.setItem("lastOrder", JSON.stringify(orderData));
    router.push("/order-success");
  };

  if (cart.length === 0) {
    return null;
  }

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
        <div className="mx-auto max-w-6xl">
        {/* Header */}
        <div className="mb-6 flex items-center justify-between">
          <Link href="/home" className="text-indigo-600 hover:underline">
            ← Back to Shopping
          </Link>
          <h1 className="text-2xl font-bold text-gray-800">Checkout</h1>
        </div>

        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          {/* Left Section - Forms */}
          <div className="lg:col-span-2 space-y-4">
            {/* Step 1: Delivery Address */}
            <div className="bg-white rounded-xl p-6 shadow-md">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold text-gray-800 flex items-center gap-2">
                  <span className="bg-indigo-600 text-white rounded-full w-8 h-8 flex items-center justify-center text-sm">1</span>
                  Delivery Address
                </h2>
                {step > 1 && (
                  <button onClick={() => setStep(1)} className="text-indigo-600 text-sm hover:underline">
                    Change
                  </button>
                )}
              </div>

              {step === 1 ? (
                <div className="space-y-4">
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <input
                      type="text"
                      placeholder="Full Name"
                      value={shippingInfo.fullName}
                      onChange={(e) => setShippingInfo({ ...shippingInfo, fullName: e.target.value })}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-900 placeholder:text-gray-400"
                    />
                    <input
                      type="tel"
                      placeholder="Mobile Number"
                      value={shippingInfo.mobile}
                      onChange={(e) => setShippingInfo({ ...shippingInfo, mobile: e.target.value })}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-900 placeholder:text-gray-400"
                    />
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <input
                      type="text"
                      placeholder="Pincode"
                      value={shippingInfo.pincode}
                      onChange={(e) => setShippingInfo({ ...shippingInfo, pincode: e.target.value })}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-900 placeholder:text-gray-400"
                    />
                    <input
                      type="text"
                      placeholder="Locality"
                      value={shippingInfo.locality}
                      onChange={(e) => setShippingInfo({ ...shippingInfo, locality: e.target.value })}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-900 placeholder:text-gray-400"
                    />
                  </div>

                  <textarea
                    placeholder="Address (House No, Building, Street, Area)"
                    value={shippingInfo.address}
                    onChange={(e) => setShippingInfo({ ...shippingInfo, address: e.target.value })}
                    rows={3}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-900 placeholder:text-gray-400"
                  />

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <input
                      type="text"
                      placeholder="City"
                      value={shippingInfo.city}
                      onChange={(e) => setShippingInfo({ ...shippingInfo, city: e.target.value })}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-900 placeholder:text-gray-400"
                    />
                    <input
                      type="text"
                      placeholder="State"
                      value={shippingInfo.state}
                      onChange={(e) => setShippingInfo({ ...shippingInfo, state: e.target.value })}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-900 placeholder:text-gray-400"
                    />
                  </div>

                  <button
                    onClick={() => setStep(2)}
                    disabled={!shippingInfo.fullName || !shippingInfo.mobile || !shippingInfo.address}
                    className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 text-white py-3 rounded-lg font-bold hover:from-indigo-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                  >
                    Continue to Payment
                  </button>
                </div>
              ) : (
                <div className="bg-gray-50 p-4 rounded-lg">
                  <p className="font-medium text-gray-800">{shippingInfo.fullName}</p>
                  <p className="text-sm text-gray-600">{shippingInfo.mobile}</p>
                  <p className="text-sm text-gray-600 mt-2">
                    {shippingInfo.address}, {shippingInfo.locality}
                  </p>
                  <p className="text-sm text-gray-600">
                    {shippingInfo.city}, {shippingInfo.state} - {shippingInfo.pincode}
                  </p>
                </div>
              )}
            </div>

            {/* Step 2: Payment Method */}
            {step >= 2 && (
              <div className="bg-white rounded-xl p-6 shadow-md">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-xl font-bold text-gray-800 flex items-center gap-2">
                    <span className="bg-indigo-600 text-white rounded-full w-8 h-8 flex items-center justify-center text-sm">2</span>
                    Payment Method
                  </h2>
                </div>

                <div className="space-y-3">
                  <label className="flex items-center gap-3 p-4 border-2 border-gray-200 rounded-lg cursor-pointer hover:border-indigo-500 transition-colors">
                    <input
                      type="radio"
                      name="payment"
                      value="cod"
                      checked={paymentMethod === "cod"}
                      onChange={(e) => setPaymentMethod(e.target.value)}
                      className="w-5 h-5"
                    />
                    <div>
                      <p className="font-medium text-gray-800">Cash on Delivery</p>
                      <p className="text-sm text-gray-500">Pay when you receive</p>
                    </div>
                  </label>

                  <label className="flex items-center gap-3 p-4 border-2 border-gray-200 rounded-lg cursor-pointer hover:border-indigo-500 transition-colors">
                    <input
                      type="radio"
                      name="payment"
                      value="upi"
                      checked={paymentMethod === "upi"}
                      onChange={(e) => setPaymentMethod(e.target.value)}
                      className="w-5 h-5"
                    />
                    <div>
                      <p className="font-medium text-gray-800">UPI / QR Code</p>
                      <p className="text-sm text-gray-500">Google Pay, PhonePe, Paytm</p>
                    </div>
                  </label>

                  <label className="flex items-center gap-3 p-4 border-2 border-gray-200 rounded-lg cursor-pointer hover:border-indigo-500 transition-colors">
                    <input
                      type="radio"
                      name="payment"
                      value="card"
                      checked={paymentMethod === "card"}
                      onChange={(e) => setPaymentMethod(e.target.value)}
                      className="w-5 h-5"
                    />
                    <div>
                      <p className="font-medium text-gray-800">Credit / Debit Card</p>
                      <p className="text-sm text-gray-500">Visa, Mastercard, Rupay</p>
                    </div>
                  </label>

                  <label className="flex items-center gap-3 p-4 border-2 border-gray-200 rounded-lg cursor-pointer hover:border-indigo-500 transition-colors">
                    <input
                      type="radio"
                      name="payment"
                      value="netbanking"
                      checked={paymentMethod === "netbanking"}
                      onChange={(e) => setPaymentMethod(e.target.value)}
                      className="w-5 h-5"
                    />
                    <div>
                      <p className="font-medium text-gray-800">Net Banking</p>
                      <p className="text-sm text-gray-500">All major banks</p>
                    </div>
                  </label>
                </div>
              </div>
            )}
          </div>

          {/* Right Section - Order Summary */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl p-6 shadow-md sticky top-4">
              <h2 className="text-xl font-bold text-gray-800 mb-4">Order Summary</h2>

              {/* Cart Items */}
              <div className="space-y-3 mb-4 max-h-60 overflow-y-auto">
                {cart.map((item) => (
                  <div key={item.id} className="flex items-center gap-3 pb-3 border-b border-gray-100">
                    <div className="flex-1">
                      <p className="text-sm font-medium text-gray-800 line-clamp-1">{item.title}</p>
                      <p className="text-xs text-gray-500">Qty: {item.qty}</p>
                    </div>
                    <p className="text-sm font-semibold text-gray-800">₹{item.price * item.qty}</p>
                  </div>
                ))}
              </div>

              {/* Price Details */}
              <div className="space-y-2 border-t border-gray-200 pt-4">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Subtotal ({cart.reduce((sum, item) => sum + item.qty, 0)} items)</span>
                  <span className="font-medium text-gray-800">₹{cartTotal}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Delivery Charges</span>
                  <span className="font-medium text-gray-800">
                    {deliveryCharge === 0 ? (
                      <span className="text-green-600">FREE</span>
                    ) : (
                      `₹${deliveryCharge}`
                    )}
                  </span>
                </div>
                <div className="flex justify-between text-lg font-bold border-t border-gray-200 pt-3">
                  <span className="text-gray-800">Total Amount</span>
                  <span className="text-indigo-600">₹{totalAmount}</span>
                </div>
              </div>

              {/* Place Order Button */}
              {step >= 2 && (
                <button
                  onClick={handlePlaceOrder}
                  className="w-full mt-6 bg-gradient-to-r from-orange-500 to-red-500 text-white py-3 rounded-lg font-bold hover:from-orange-600 hover:to-red-600 shadow-lg hover:shadow-xl transition-all"
                >
                  Place Order
                </button>
              )}

              {/* Safe & Secure */}
              <div className="mt-4 text-center">
                <p className="text-xs text-gray-500">🔒 Safe and Secure Payments</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    </div>
  );
}
