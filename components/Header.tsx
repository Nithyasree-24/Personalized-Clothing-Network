"use client";

import React from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

type Props = {
  searchTerm?: string;
  onSearch?: (s: string) => void;
  cartCount?: number;
  cartTotal?: number;
  cartItems?: Array<{ id: string | number; title: string; price: number; qty: number; image?: string }>;
  onRemoveFromCart?: (id: string | number) => void;
  onIncreaseQty?: (id: string | number) => void;
  onDecreaseQty?: (id: string | number) => void;
  onAddToCart?: (item: { id: string | number; title: string; price: number; qty: number; image?: string }) => void;
  wishlistItems?: Array<{ id: string | number; title: string; image?: string; price?: number }>;
  onRemoveFromWishlist?: (id: string | number) => void;
  userName?: string | null;
  onLogout?: () => void;
  onAddNotification?: (notification: { title: string; message: string }) => void;
};

export default function Header({
  searchTerm = "",
  onSearch,
  cartCount = 0,
  cartTotal = 0,
  cartItems = [],
  onRemoveFromCart,
  onIncreaseQty,
  onDecreaseQty,
  onAddToCart,
  wishlistItems = [],
  onRemoveFromWishlist,
  userName = null,
  onLogout,
  onAddNotification,
}: Props) {
  const router = useRouter();
  const [showCart, setShowCart] = React.useState(false);
  const [showWishlist, setShowWishlist] = React.useState(false);
  const [showProfile, setShowProfile] = React.useState(false);
  const [showNotifications, setShowNotifications] = React.useState(false);
  const [profileEmail, setProfileEmail] = React.useState<string | null>(null);
  const [orders, setOrders] = React.useState<Array<any>>([]);
  
  const [notifications, setNotifications] = React.useState<Array<{id: number; title: string; message: string; time: string; read: boolean}>>([]);

  // Load notifications from localStorage on mount
  React.useEffect(() => {
    try {
      const raw = localStorage.getItem("user");
      if (raw) {
        const u = JSON.parse(raw);
        setProfileEmail(u.email || null);
      }
    } catch {
      setProfileEmail(null);
    }
    try {
      const o = localStorage.getItem("orders");
      if (o) setOrders(JSON.parse(o));
    } catch {}
    
    // Load notifications from localStorage
    try {
      const savedNotifs = localStorage.getItem("notifications");
      if (savedNotifs) {
        setNotifications(JSON.parse(savedNotifs));
      } else {
        // Set default notifications only if none exist
        const defaultNotifs = [
          { id: 1, title: "Welcome to FashioPulse!", message: "Explore our latest collection", time: "2 hours ago", read: false },
          { id: 2, title: "Flash Sale Alert!", message: "Up to 50% off on selected items", time: "5 hours ago", read: false },
        ];
        setNotifications(defaultNotifs);
        localStorage.setItem("notifications", JSON.stringify(defaultNotifs));
      }
    } catch {}
  }, []);

  // Save notifications to localStorage whenever they change
  React.useEffect(() => {
    if (notifications.length > 0) {
      localStorage.setItem("notifications", JSON.stringify(notifications));
    }
  }, [notifications]);

  const markAllAsRead = () => {
    const updatedNotifs = notifications.map(n => ({ ...n, read: true }));
    setNotifications(updatedNotifs);
  };

  const addNotification = React.useCallback((title: string, message: string) => {
    const newNotif = {
      id: Date.now(),
      title,
      message,
      time: "Just now",
      read: false,
    };
    setNotifications(prev => {
      const updated = [newNotif, ...prev];
      localStorage.setItem("notifications", JSON.stringify(updated));
      return updated;
    });
  }, []);

  React.useEffect(() => {
    (window as any).addNotification = addNotification;
  }, [addNotification]);

  const handleLogoutClick = () => {
    onLogout?.();
    setShowProfile(false);
    router.push("/login");
  };

  return (
    <header className="flex items-center justify-between gap-4 px-4 sm:px-6 lg:px-8 py-4 max-w-7xl mx-auto">
      <div className="flex items-center gap-4 flex-1">
        <Link href="/home" className="text-4xl bg-gradient-to-r from-pink-600 to-pink-800 bg-clip-text text-transparent whitespace-nowrap font-[family-name:var(--font-great-vibes)] pr-2" style={{ fontWeight: 600, textShadow: '0 0 1px rgba(236, 64, 122, 0.3)' }}>
          FashioPulse
        </Link>
        <div className="flex-1 max-w-2xl">
          <div className="relative">
            <input
              value={searchTerm}
              onChange={(e) => onSearch?.(e.target.value)}
              className="w-full rounded-full border-2 border-pink-300 pl-12 pr-4 py-2.5 text-sm text-black focus:border-pink-500 focus:outline-none transition-colors bg-white"
              placeholder="Search for products, brands and more..."
            />
            <span className="absolute left-4 top-1/2 -translate-y-1/2 text-pink-400 text-lg">🔍</span>
          </div>
        </div>
      </div>

      <div className="flex items-center gap-4">
        {/* Home button */}
        <div className="hidden sm:flex">
          <Link
            href="/"
            className="inline-flex items-center justify-center rounded-lg bg-white p-2 text-sm shadow-sm text-black hover:shadow-md transition-shadow"
            title="Home"
          >
            <span className="text-xl">🏠</span>
          </Link>
        </div>
        {/* Combos button */}
        <div className="hidden sm:flex">
          <Link
            href="/combos"
            className="inline-flex items-center gap-2 rounded-lg bg-gradient-to-r from-pink-500 to-pink-700 px-3 py-2 text-sm shadow-md text-white hover:shadow-lg transition-shadow font-semibold hover:from-pink-600 hover:to-pink-800"
            title="Combos"
          >
            <span className="text-lg">🎯</span>
            <span>Combos</span>
          </Link>
        </div>

        {/* Notification button */}
        <div className="hidden sm:flex relative">
          <button
            onClick={() => setShowNotifications(!showNotifications)}
            className="inline-flex items-center justify-center rounded-lg bg-white p-2.5 text-sm shadow-md hover:shadow-lg transition-all"
            title="Notifications"
          >
            <svg className="w-6 h-6" viewBox="0 0 24 24" fill="none">
              <defs>
                <linearGradient id="bellGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" style={{ stopColor: '#FFD700', stopOpacity: 1 }} />
                  <stop offset="100%" style={{ stopColor: '#FFA500', stopOpacity: 1 }} />
                </linearGradient>
              </defs>
              <path d="M12 2C11.172 2 10.5 2.672 10.5 3.5V4.1C8.53 4.56 7 6.24 7 8.25V14L5.29 15.71C5.11 15.89 5 16.14 5 16.41V17C5 17.55 5.45 18 6 18H18C18.55 18 19 17.55 19 17V16.41C19 16.14 18.89 15.89 18.71 15.71L17 14V8.25C17 6.24 15.47 4.56 13.5 4.1V3.5C13.5 2.672 12.828 2 12 2ZM10 19C10 20.1 10.9 21 12 21C13.1 21 14 20.1 14 19H10Z" fill="url(#bellGradient)"/>
            </svg>
            {notifications.filter(n => !n.read).length > 0 && (
              <span className="absolute -top-1 -right-1 bg-red-500 text-white rounded-full w-5 h-5 text-xs flex items-center justify-center font-bold">
                {notifications.filter(n => !n.read).length}
              </span>
            )}
          </button>
          {showNotifications && (
            <div className="absolute right-0 mt-2 w-80 rounded-md border bg-white p-3 shadow-lg z-50 top-full">
              <div className="flex items-center justify-between mb-3">
                <div className="text-sm font-semibold text-black">Notifications</div>
                <button
                  onClick={() => setShowNotifications(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  ✕
                </button>
              </div>
              <div className="space-y-2 max-h-96 overflow-auto">
                {notifications.length === 0 && (
                  <div className="text-sm text-gray-500 text-center py-4">No notifications</div>
                )}
                {notifications.map((notif) => (
                  <div
                    key={notif.id}
                    className={`p-3 rounded-lg border ${
                      notif.read ? 'bg-gray-50 border-gray-200' : 'bg-blue-50 border-blue-200'
                    } hover:shadow-sm transition-shadow cursor-pointer`}
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div className="flex-1">
                        <div className="text-sm font-semibold text-black">{notif.title}</div>
                        <div className="text-xs text-gray-600 mt-1">{notif.message}</div>
                        <div className="text-xs text-gray-400 mt-1">{notif.time}</div>
                      </div>
                      {!notif.read && (
                        <div className="w-2 h-2 bg-blue-500 rounded-full flex-shrink-0 mt-1"></div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
              <div className="mt-3 pt-3 border-t border-gray-200">
                <button 
                  onClick={markAllAsRead}
                  className="w-full text-center text-sm text-[#8B6F47] hover:text-[#7A5F3A] font-medium"
                >
                  Mark all as read
                </button>
              </div>
            </div>
          )}
        </div>
        {/* Wishlist button */}
        <div className="relative">
          <Link
            href="/wishlist"
            className="inline-flex items-center gap-2 rounded-lg bg-white px-3 py-2 text-sm shadow-sm text-black hover:shadow-md transition-shadow"
          >
            <span className="text-lg">{wishlistItems.length > 0 ? "❤️" : "🤍"}</span>
            <span className="hidden sm:inline">Wishlist</span>
            {wishlistItems.length > 0 && (
              <span className="bg-red-500 text-white rounded-full px-2 text-xs font-bold">{wishlistItems.length}</span>
            )}
          </Link>
          {showWishlist && (
            <div className="absolute right-0 mt-2 w-80 rounded-md border bg-white p-3 shadow-lg z-50">
              <div className="text-sm font-semibold mb-3 text-black">Saved items</div>
              <div className="space-y-3 max-h-60 overflow-auto">
                {wishlistItems.length === 0 && <div className="text-sm text-zinc-500">No saved items</div>}
                {wishlistItems.map((it) => (
                  <div key={String(it.id)} className="flex gap-3 pb-3 border-b border-gray-100">
                    <div className="w-16 h-16 bg-gray-50 rounded flex-shrink-0 flex items-center justify-center overflow-hidden">
                      {it.image ? (
                        // eslint-disable-next-line @next/next/no-img-element
                        <img src={it.image} alt={it.title} className="w-full h-full object-contain mix-blend-multiply" />
                      ) : (
                        <span className="text-2xl">❤️</span>
                      )}
                    </div>
                    <div className="flex-1">
                      <div className="text-sm font-medium text-black line-clamp-1">{it.title}</div>
                      {it.price && (
                        <div className="text-sm font-semibold text-black mt-1">₹{it.price}</div>
                      )}
                      <div className="mt-2 flex items-center gap-2">
                        <button
                          onClick={() => {
                            // Add to cart from wishlist
                            if (it.price && onAddToCart) {
                              onAddToCart({
                                id: it.id,
                                title: it.title,
                                price: it.price,
                                qty: 1,
                                image: it.image
                              });
                              setShowWishlist(false);
                              setShowCart(true);
                            }
                          }}
                          className="rounded-lg bg-gradient-to-br from-blue-500 to-blue-700 text-white p-2 hover:from-blue-600 hover:to-blue-800 shadow-md hover:shadow-lg transition-all"
                          title="Add to cart"
                        >
                          <span className="text-base">🛒</span>
                        </button>
                        <button
                          onClick={() => onRemoveFromWishlist?.(it.id)}
                          className="rounded-lg bg-gradient-to-br from-red-500 to-red-600 text-white p-2 hover:from-red-600 hover:to-red-700 shadow-md hover:shadow-lg transition-all"
                          title="Remove from wishlist"
                        >
                          <span className="text-base">✕</span>
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Cart button + panel */}
        <div className="relative">
          <Link
            href="/cart"
            className="inline-flex items-center gap-2 rounded-lg bg-white px-3 py-2 text-sm shadow-sm text-black hover:shadow-md transition-shadow"
          >
            <span className="text-lg">🛒</span>
            <span className="hidden sm:inline">Cart</span>
            {cartCount > 0 && (
              <span className="bg-pink-500 text-black rounded-full px-2 text-xs font-bold">{cartCount}</span>
            )}
          </Link>
          {showCart && (
            <div className="absolute right-0 mt-2 w-80 rounded-md border bg-white p-3 shadow-lg z-50">
              <div className="text-sm font-semibold mb-2 text-black">Cart</div>
              <div className="space-y-3 max-h-60 overflow-auto">
                {cartItems.length === 0 && <div className="text-sm text-zinc-500">Your cart is empty</div>}
                {cartItems.map((it) => (
                  <div key={String(it.id)} className="flex gap-3 pb-3 border-b border-gray-100">
                    <div className="w-16 h-16 bg-gray-50 rounded flex-shrink-0 flex items-center justify-center overflow-hidden">
                      {it.image ? (
                        // eslint-disable-next-line @next/next/no-img-element
                        <img src={it.image} alt={it.title} className="w-full h-full object-contain mix-blend-multiply" />
                      ) : (
                        <span className="text-2xl">📦</span>
                      )}
                    </div>
                    <div className="flex-1">
                      <div className="text-sm font-medium text-black line-clamp-1">{it.title}</div>
                      <div className="text-sm font-semibold text-black mt-1">₹{(Number(it.price) || 0)}</div>
                      <div className="mt-2 flex items-center gap-2">
                        <button
                          onClick={() => onDecreaseQty?.(it.id)}
                          className="rounded-lg bg-gray-200 text-gray-800 px-2 py-1 text-xs font-bold hover:bg-gray-300"
                          aria-label={`Decrease quantity for ${it.title}`}
                        >
                          −
                        </button>
                        <span className="text-xs font-semibold text-gray-700 min-w-[20px] text-center">{it.qty}</span>
                        <button
                          onClick={() => onIncreaseQty?.(it.id)}
                          className="rounded-lg bg-gray-200 text-gray-800 px-2 py-1 text-xs font-bold hover:bg-gray-300"
                          aria-label={`Increase quantity for ${it.title}`}
                        >
                          +
                        </button>
                        <button
                          onClick={() => onRemoveFromCart?.(it.id)}
                          className="ml-auto text-xs text-red-500 hover:text-red-700 font-medium"
                        >
                          Remove
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
              <div className="mt-3 pt-3 border-t border-gray-200">
                <div className="flex items-center justify-between mb-3">
                  <div className="text-sm font-medium text-black">Subtotal</div>
                  <div className="text-sm font-semibold text-black">₹{cartTotal?.toFixed(2) ?? "0.00"}</div>
                </div>
                {cartItems.length > 0 && (
                  <button
                    onClick={() => {
                      setShowCart(false);
                      router.push("/checkout");
                    }}
                    className="w-full bg-gradient-to-r from-orange-500 to-red-500 text-white py-2 rounded-lg font-bold hover:from-orange-600 hover:to-red-600 transition-all"
                  >
                    Proceed to Checkout
                  </button>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Profile area (no top-level logout) */}
        <div className="relative">
          {userName && userName !== "Guest" ? (
            <>
              <button
                onClick={() => setShowProfile((s) => !s)}
                className="flex items-center gap-2 px-3 py-2 rounded-lg bg-gray-100"
              >
                <span className="text-2xl">👤</span>
              </button>
              {showProfile && (
                <div className="absolute right-0 mt-2 w-64 rounded-md border bg-white p-4 shadow-lg z-50">
                  <div className="text-sm font-medium mb-2">Account</div>
                  <div className="text-xs text-zinc-600 mb-3">
                    <div><span className="font-semibold">Email:</span> {profileEmail ?? "-"}</div>
                  </div>
                  
                  <Link
                    href="/orders"
                    className="block w-full bg-blue-500 text-white text-center py-2 rounded-lg text-sm font-medium hover:bg-blue-600 transition-colors mb-3"
                  >
                    My Orders
                  </Link>
                  
                  <div className="flex justify-end">
                    <button
                      onClick={handleLogoutClick}
                      className="rounded bg-red-500 px-3 py-1 text-sm text-white hover:bg-red-600"
                    >
                      Logout
                    </button>
                  </div>
                </div>
              )}
            </>
          ) : (
            <Link
              href="/login"
              className="rounded bg-gradient-to-r from-[#8B6F47] to-[#D4A574] px-4 py-2 text-sm text-white hover:from-[#7A5F3A] hover:to-[#C4956A] font-semibold transition-all"
            >
              Login
            </Link>
          )}
        </div>
      </div>
    </header>
  );
}
