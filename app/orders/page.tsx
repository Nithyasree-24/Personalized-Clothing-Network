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

export default function OrdersPage() {
  const router = useRouter();
  const { cart, cartTotal, removeFromCart, incrementQuantity, decrementQuantity, addToCart, wishlist, removeFromWishlist, cartCount } = useCart();
  const [orders, setOrders] = useState<OrderData[]>([]);
  const [userName, setUserName] = useState<string | null>(null);
  const [selectedOrder, setSelectedOrder] = useState<OrderData | null>(null);
  const [showReturnPolicy, setShowReturnPolicy] = useState(false);
  const [cancellingOrderId, setCancellingOrderId] = useState<string | null>(null);
  const [showCancelConfirm, setShowCancelConfirm] = useState<string | null>(null);

  useEffect(() => {
    const user = localStorage.getItem("user");
    if (user) {
      try {
        const userData = JSON.parse(user);
        setUserName(userData.name || "Guest");
      } catch {}
    }

    // Load orders from localStorage
    try {
      const savedOrders = localStorage.getItem("orders");
      if (savedOrders) {
        const parsedOrders = JSON.parse(savedOrders);
        setOrders(parsedOrders.reverse()); // Show newest first
      }
    } catch (e) {
      console.error("Failed to load orders", e);
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("user");
    setUserName(null);
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const getDeliveryStatus = (deliveryDate: string) => {
    const delivery = new Date(deliveryDate);
    const today = new Date();
    const diffTime = delivery.getTime() - today.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays < 0) return { text: "Delivered", color: "text-green-600", bg: "bg-green-100" };
    if (diffDays <= 1) return { text: "Arriving Tomorrow", color: "text-blue-600", bg: "bg-blue-100" };
    if (diffDays <= 7) return { text: `Arriving in ${diffDays} days`, color: "text-orange-600", bg: "bg-orange-100" };
    return { text: `Arriving ${formatDate(deliveryDate)}`, color: "text-gray-600", bg: "bg-gray-100" };
  };

  const handleCancelOrder = (orderId: string) => {
    setShowCancelConfirm(orderId);
  };

  const confirmCancelOrder = (orderId: string) => {
    setCancellingOrderId(orderId);
    
    // Simulate API call delay
    setTimeout(() => {
      const updatedOrders = orders.map(order => 
        order.id === orderId ? { ...order, status: 'cancelled' } : order
      );
      setOrders(updatedOrders);
      localStorage.setItem("orders", JSON.stringify(updatedOrders));
      setCancellingOrderId(null);
      setShowCancelConfirm(null);
      
      // Show success message
      alert("✅ Order cancelled successfully! Your refund will be processed within 5-7 business days.");
    }, 1500);
  };

  const handleReturnPolicy = () => {
    setShowReturnPolicy(true);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-white">
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
            <Link href="/home" className="text-blue-600 hover:underline flex items-center gap-2">
              <span>←</span>
              <span>Back to Shopping</span>
            </Link>
            <h1 className="text-3xl font-bold text-gray-800">My Orders</h1>
            <div className="w-32"></div>
          </div>

          {orders.length === 0 ? (
            <div className="bg-white rounded-xl p-12 shadow-md text-center">
              <div className="text-6xl mb-4">📦</div>
              <h2 className="text-2xl font-bold text-gray-800 mb-2">No orders yet</h2>
              <p className="text-gray-600 mb-6">Start shopping to see your orders here!</p>
              <Link
                href="/home"
                className="inline-block bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-lg font-bold hover:from-blue-700 hover:to-purple-700 transition-all"
              >
                Start Shopping
              </Link>
            </div>
          ) : (
            <div className="space-y-6">
              {orders.map((order) => {
                const deliveryStatus = getDeliveryStatus(order.deliveryDate);
                return (
                  <div key={order.id} className="bg-white rounded-xl shadow-lg overflow-hidden">
                    {/* Order Header */}
                    <div className="bg-gray-50 px-6 py-4 border-b">
                      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                        <div>
                          <h3 className="text-lg font-bold text-gray-800">Order #{order.id}</h3>
                          <p className="text-sm text-gray-600">Placed on {formatDate(order.date)}</p>
                        </div>
                        <div className="flex items-center gap-4">
                        <div className={`px-3 py-1 rounded-full text-sm font-medium ${
                          order.status === 'cancelled' 
                            ? 'bg-red-100 text-red-600' 
                            : `${deliveryStatus.bg} ${deliveryStatus.color}`
                        }`}>
                          {order.status === 'cancelled' ? 'Order Cancelled' : deliveryStatus.text}
                        </div>
                          <div className="text-right">
                            <div className="text-lg font-bold text-gray-800">₹{order.total}</div>
                            <div className="text-sm text-gray-600">{order.items.length} items</div>
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Order Items */}
                    <div className="p-6">
                      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-4">
                        {order.items.slice(0, 3).map((item, index) => (
                          <div key={index} className="flex gap-3 p-3 border border-gray-200 rounded-lg">
                            <div className="w-16 h-16 bg-gray-50 rounded-lg flex-shrink-0 flex items-center justify-center overflow-hidden">
                              {item.image ? (
                                // eslint-disable-next-line @next/next/no-img-element
                                <img
                                  src={item.image}
                                  alt={item.title}
                                  className="w-full h-full object-contain mix-blend-multiply"
                                />
                              ) : (
                                <span className="text-xl">📦</span>
                              )}
                            </div>
                            <div className="flex-1 min-w-0">
                              <h4 className="text-sm font-medium text-gray-800 line-clamp-2">{item.title}</h4>
                              <p className="text-xs text-gray-600 mt-1">Qty: {item.qty}</p>
                              <p className="text-sm font-semibold text-gray-800">₹{item.price * item.qty}</p>
                              <div className="text-xs text-green-600 mt-1">
                                📅 {getDeliveryStatus(item.deliveryDate).text}
                              </div>
                            </div>
                          </div>
                        ))}
                        {order.items.length > 3 && (
                          <div className="flex items-center justify-center p-3 border border-gray-200 rounded-lg bg-gray-50">
                            <span className="text-sm text-gray-600">+{order.items.length - 3} more items</span>
                          </div>
                        )}
                      </div>

                      {/* Action Buttons */}
                      <div className="flex flex-wrap gap-3 pt-4 border-t border-gray-200">
                        <button
                          onClick={() => setSelectedOrder(order)}
                          className="bg-blue-500 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-600 transition-colors"
                        >
                          View Details
                        </button>
                        
                        {order.status !== 'cancelled' && getDeliveryStatus(order.deliveryDate).text !== 'Delivered' && (
                          <button
                            onClick={() => handleCancelOrder(order.id)}
                            disabled={cancellingOrderId === order.id}
                            className="bg-red-500 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-red-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                          >
                            {cancellingOrderId === order.id ? (
                              <>
                                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                                Cancelling...
                              </>
                            ) : (
                              'Cancel Order'
                            )}
                          </button>
                        )}
                        
                        <button 
                          onClick={handleReturnPolicy}
                          className="bg-gray-500 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-600 transition-colors"
                        >
                          Return Policy
                        </button>
                        
                        <Link
                          href="/home"
                          className="bg-pink-500 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-pink-600 transition-colors"
                        >
                          Buy Again
                        </Link>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}

          {/* Return Policy Modal */}
          {selectedOrder && (
            <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
              <div className="bg-white rounded-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
                <div className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-xl font-bold text-gray-800">Order Details</h3>
                    <button
                      onClick={() => setSelectedOrder(null)}
                      className="text-gray-400 hover:text-gray-600 text-2xl"
                    >
                      ✕
                    </button>
                  </div>
                  
                  <div className="space-y-4">
                    <div>
                      <h4 className="font-semibold text-gray-800 mb-2">Order #{selectedOrder.id}</h4>
                      <p className="text-sm text-gray-600">Placed: {formatDate(selectedOrder.date)}</p>
                      <p className="text-sm text-gray-600">Expected Delivery: {formatDate(selectedOrder.deliveryDate)}</p>
                    </div>
                    
                    <div>
                      <h4 className="font-semibold text-gray-800 mb-2">Items ({selectedOrder.items.length})</h4>
                      <div className="space-y-2">
                        {selectedOrder.items.map((item, index) => (
                          <div key={index} className="flex gap-3 p-3 border border-gray-200 rounded-lg">
                            <div className="w-12 h-12 bg-gray-50 rounded flex-shrink-0 flex items-center justify-center overflow-hidden">
                              {item.image ? (
                                // eslint-disable-next-line @next/next/no-img-element
                                <img src={item.image} alt={item.title} className="w-full h-full object-contain" />
                              ) : (
                                <span className="text-lg">📦</span>
                              )}
                            </div>
                            <div className="flex-1">
                              <h5 className="text-sm font-medium text-gray-800">{item.title}</h5>
                              <p className="text-xs text-gray-600">Qty: {item.qty} × ₹{item.price}</p>
                            </div>
                            <div className="text-sm font-semibold text-gray-800">₹{item.qty * item.price}</div>
                          </div>
                        ))}
                      </div>
                    </div>
                    
                    <div className="bg-blue-50 p-4 rounded-lg">
                      <h4 className="font-semibold text-blue-800 mb-2">Return Policy</h4>
                      <ul className="text-sm text-blue-700 space-y-1">
                        <li>• 7-day return window from delivery date</li>
                        <li>• Items must be unused and in original packaging</li>
                        <li>• Free return pickup available</li>
                        <li>• Refund processed within 5-7 business days</li>
                        <li>• Exchange available for size/color issues</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Cancel Order Confirmation Modal */}
          {showCancelConfirm && (
            <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
              <div className="bg-white rounded-xl max-w-md w-full p-6">
                <div className="text-center">
                  <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <span className="text-2xl">⚠️</span>
                  </div>
                  <h3 className="text-xl font-bold text-gray-800 mb-2">Cancel Order?</h3>
                  <p className="text-gray-600 mb-6">
                    Are you sure you want to cancel this order? This action cannot be undone.
                  </p>
                  <div className="flex gap-3">
                    <button
                      onClick={() => setShowCancelConfirm(null)}
                      className="flex-1 bg-gray-200 text-gray-800 py-2 px-4 rounded-lg font-medium hover:bg-gray-300 transition-colors"
                    >
                      Keep Order
                    </button>
                    <button
                      onClick={() => confirmCancelOrder(showCancelConfirm)}
                      className="flex-1 bg-red-500 text-white py-2 px-4 rounded-lg font-medium hover:bg-red-600 transition-colors"
                    >
                      Yes, Cancel
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Return Policy Modal */}
          {showReturnPolicy && (
            <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
              <div className="bg-white rounded-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
                <div className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-xl font-bold text-gray-800">Return & Refund Policy</h3>
                    <button
                      onClick={() => setShowReturnPolicy(false)}
                      className="text-gray-400 hover:text-gray-600 text-2xl"
                    >
                      ✕
                    </button>
                  </div>
                  
                  <div className="space-y-6">
                    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                      <h4 className="font-semibold text-blue-800 mb-3 flex items-center gap-2">
                        <span>📋</span> Return Policy Overview
                      </h4>
                      <ul className="text-sm text-blue-700 space-y-2">
                        <li className="flex items-start gap-2">
                          <span className="text-green-600 mt-0.5">✓</span>
                          <span><strong>7-day return window</strong> from delivery date</span>
                        </li>
                        <li className="flex items-start gap-2">
                          <span className="text-green-600 mt-0.5">✓</span>
                          <span>Items must be <strong>unused and in original packaging</strong></span>
                        </li>
                        <li className="flex items-start gap-2">
                          <span className="text-green-600 mt-0.5">✓</span>
                          <span><strong>Free return pickup</strong> available</span>
                        </li>
                        <li className="flex items-start gap-2">
                          <span className="text-green-600 mt-0.5">✓</span>
                          <span>Refund processed within <strong>5-7 business days</strong></span>
                        </li>
                        <li className="flex items-start gap-2">
                          <span className="text-green-600 mt-0.5">✓</span>
                          <span><strong>Exchange available</strong> for size/color issues</span>
                        </li>
                      </ul>
                    </div>

                    <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                      <h4 className="font-semibold text-yellow-800 mb-3 flex items-center gap-2">
                        <span>⚠️</span> Important Notes
                      </h4>
                      <ul className="text-sm text-yellow-700 space-y-2">
                        <li>• Items must have original tags attached</li>
                        <li>• Undergarments and intimate wear are non-returnable</li>
                        <li>• Damaged or worn items will not be accepted</li>
                        <li>• Return shipping is free for defective items</li>
                      </ul>
                    </div>

                    <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                      <h4 className="font-semibold text-green-800 mb-3 flex items-center gap-2">
                        <span>📞</span> Need Help?
                      </h4>
                      <div className="text-sm text-green-700 space-y-2">
                        <p><strong>Customer Support:</strong> 1800-123-4567</p>
                        <p><strong>Email:</strong> returns@fashiopulse.com</p>
                        <p><strong>Hours:</strong> 9 AM - 9 PM IST (Mon-Sun)</p>
                      </div>
                    </div>
                  </div>

                  <div className="mt-6 pt-4 border-t border-gray-200">
                    <button
                      onClick={() => setShowReturnPolicy(false)}
                      className="w-full bg-blue-500 text-white py-3 rounded-lg font-semibold hover:bg-blue-600 transition-colors"
                    >
                      Got it, Thanks!
                    </button>
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