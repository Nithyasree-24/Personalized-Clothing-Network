"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import Header from "../../components/Header";
import { useCart } from "../../context/CartContext";

interface OrderItem {
  id: string | number;
  title: string;
  price: number;
  qty: number;
  image?: string;
  deliveryDate: string;
}

interface OrderData {
  id: string;
  date: string;
  deliveryDate: string;
  total: number;
  items: OrderItem[];
  shippingInfo: any;
  paymentMethod: string;
  status: string;
}

export default function OrderSuccessPage() {
  const router = useRouter();
  const { cart, cartTotal, removeFromCart, incrementQuantity, decrementQuantity, addToCart, wishlist, removeFromWishlist, cartCount } = useCart();
  const [orderData, setOrderData] = useState<OrderData | null>(null);
  const [userName, setUserName] = useState<string | null>(null);

  useEffect(() => {
    const user = localStorage.getItem("user");
    if (user) {
      try {
        const userData = JSON.parse(user);
        setUserName(userData.name || "Guest");
      } catch {}
    }

    // Get order data from localStorage
    const lastOrder = localStorage.getItem("lastOrder");
    if (lastOrder) {
      try {
        const order = JSON.parse(lastOrder);
        setOrderData(order);
        // Clear the lastOrder data after displaying
        localStorage.removeItem("lastOrder");
      } catch (e) {
        console.error("Failed to parse order data", e);
        router.push("/home");
      }
    } else {
      // If no order data, redirect to home
      router.push("/home");
    }
  }, [router]);

  const handleLogout = () => {
    localStorage.removeItem("user");
    setUserName(null);
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const getDeliveryDateText = (deliveryDate: string) => {
    const delivery = new Date(deliveryDate);
    const today = new Date();
    const diffTime = delivery.getTime() - today.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays <= 1) return "Tomorrow";
    if (diffDays <= 7) return `${diffDays} days`;
    return formatDate(deliveryDate);
  };

  if (!orderData) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-50 to-white flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-16 w-16 border-4 border-green-300 border-t-green-600"></div>
          <p className="mt-4 text-green-700 font-semibold text-lg">Loading order details...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-white">
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
        <div className="mx-auto max-w-4xl">
          {/* Success Header */}
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-20 h-20 bg-green-100 rounded-full mb-4">
              <span className="text-4xl">✅</span>
            </div>
            <h1 className="text-3xl font-bold text-gray-800 mb-2">Order Placed Successfully!</h1>
            <p className="text-gray-600">Thank you for your purchase. Your order has been confirmed.</p>
          </div>

          {/* Order Details Card */}
          <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
            <div className="border-b border-gray-200 pb-4 mb-4">
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                <div>
                  <h2 className="text-xl font-bold text-gray-800">Order #{orderData.id}</h2>
                  <p className="text-sm text-gray-600">Placed on {formatDate(orderData.date)}</p>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold text-green-600">₹{orderData.total}</div>
                  <div className="text-sm text-gray-600">Total Amount</div>
                </div>
              </div>
            </div>

            {/* Delivery Information */}
            <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
              <div className="flex items-center gap-3 mb-2">
                <span className="text-2xl">🚚</span>
                <div>
                  <h3 className="font-semibold text-green-800">Expected Delivery</h3>
                  <p className="text-green-700">{formatDate(orderData.deliveryDate)}</p>
                  <p className="text-sm text-green-600">({getDeliveryDateText(orderData.deliveryDate)})</p>
                </div>
              </div>
            </div>

            {/* Shipping Address */}
            <div className="mb-6">
              <h3 className="font-semibold text-gray-800 mb-2">Shipping Address</h3>
              <div className="bg-gray-50 p-4 rounded-lg">
                <p className="font-medium text-gray-800">{orderData.shippingInfo.fullName}</p>
                <p className="text-sm text-gray-600">{orderData.shippingInfo.mobile}</p>
                <p className="text-sm text-gray-600 mt-1">
                  {orderData.shippingInfo.address}, {orderData.shippingInfo.locality}
                </p>
                <p className="text-sm text-gray-600">
                  {orderData.shippingInfo.city}, {orderData.shippingInfo.state} - {orderData.shippingInfo.pincode}
                </p>
              </div>
            </div>

            {/* Payment Method */}
            <div className="mb-6">
              <h3 className="font-semibold text-gray-800 mb-2">Payment Method</h3>
              <div className="bg-gray-50 p-4 rounded-lg">
                <p className="text-gray-700 capitalize">{orderData.paymentMethod.replace(/([A-Z])/g, ' $1').trim()}</p>
              </div>
            </div>
          </div>

          {/* Ordered Items */}
          <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
            <h3 className="text-xl font-bold text-gray-800 mb-4">Ordered Items ({orderData.items.length})</h3>
            <div className="space-y-4">
              {orderData.items.map((item, index) => (
                <div key={index} className="flex gap-4 p-4 border border-gray-200 rounded-lg">
                  <div className="w-20 h-20 bg-gray-50 rounded-lg flex-shrink-0 flex items-center justify-center overflow-hidden">
                    {item.image ? (
                      // eslint-disable-next-line @next/next/no-img-element
                      <img
                        src={item.image}
                        alt={item.title}
                        className="w-full h-full object-contain mix-blend-multiply"
                      />
                    ) : (
                      <span className="text-2xl">📦</span>
                    )}
                  </div>
                  <div className="flex-1">
                    <h4 className="font-medium text-gray-800 line-clamp-2">{item.title}</h4>
                    <div className="flex items-center justify-between mt-2">
                      <div className="text-sm text-gray-600">
                        Qty: {item.qty} × ₹{item.price} = ₹{item.qty * item.price}
                      </div>
                      <div className="text-sm text-green-600 font-medium">
                        📅 Delivery: {getDeliveryDateText(item.deliveryDate)}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/orders"
              className="bg-gradient-to-r from-blue-500 to-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:from-blue-600 hover:to-blue-700 transition-all text-center"
            >
              View All Orders
            </Link>
            <Link
              href="/home"
              className="bg-gradient-to-r from-pink-500 to-pink-600 text-white px-6 py-3 rounded-lg font-semibold hover:from-pink-600 hover:to-pink-700 transition-all text-center"
            >
              Continue Shopping
            </Link>
          </div>

          {/* Help Section */}
          <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6 text-center">
            <h3 className="font-semibold text-blue-800 mb-2">Need Help?</h3>
            <p className="text-blue-700 text-sm mb-3">
              If you have any questions about your order, feel free to contact us.
            </p>
            <div className="flex flex-col sm:flex-row gap-2 justify-center text-sm">
              <span className="text-blue-600">📞 Customer Support: 1800-123-4567</span>
              <span className="text-blue-600">📧 Email: support@fashiopulse.com</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}