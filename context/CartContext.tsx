"use client";

import React, { createContext, useContext, useEffect, useState } from "react";

export type CartItem = {
  id: string | number;
  title: string;
  price: number;
  qty: number;
  image?: string;
};

export type WishlistItem = {
  id: string | number;
  title: string;
  image?: string;
  price?: number;
};

interface CartContextType {
  cart: CartItem[];
  wishlist: WishlistItem[];
  addToCart: (item: CartItem) => void;
  removeFromCart: (id: string | number) => void;
  incrementQuantity: (id: string | number) => void;
  decrementQuantity: (id: string | number) => void;
  toggleWishlist: (item: WishlistItem) => void;
  removeFromWishlist: (id: string | number) => void;
  clearCart: () => void;
  cartCount: number;
  cartTotal: number;
  showNotification: boolean;
  lastAddedProduct: string;
  hideNotification: () => void;
}

const CartContext = createContext<CartContextType | undefined>(undefined);

export function CartProvider({ children }: { children: React.ReactNode }) {
  const [cart, setCart] = useState<CartItem[]>([]);
  const [wishlist, setWishlist] = useState<WishlistItem[]>([]);
  const [isHydrated, setIsHydrated] = useState(false);
  const [showNotification, setShowNotification] = useState(false);
  const [lastAddedProduct, setLastAddedProduct] = useState("");

  // Load from localStorage on mount
  useEffect(() => {
    try {
      const savedCart = localStorage.getItem("cart");
      if (savedCart) setCart(JSON.parse(savedCart));
    } catch {
      // Ignore parse errors
    }

    try {
      const savedWishlist = localStorage.getItem("wishlist");
      if (savedWishlist) setWishlist(JSON.parse(savedWishlist));
    } catch {
      // Ignore parse errors
    }

    setIsHydrated(true);
  }, []);

  // Save cart to localStorage whenever it changes
  useEffect(() => {
    if (isHydrated) {
      try {
        localStorage.setItem("cart", JSON.stringify(cart));
      } catch {
        // Ignore storage errors
      }
    }
  }, [cart, isHydrated]);

  // Save wishlist to localStorage whenever it changes
  useEffect(() => {
    if (isHydrated) {
      try {
        localStorage.setItem("wishlist", JSON.stringify(wishlist));
      } catch {
        // Ignore storage errors
      }
    }
  }, [wishlist, isHydrated]);

  const addToCart = (item: CartItem) => {
    setCart((prev) => {
      const found = prev.find((it) => it.id === item.id);
      if (found) {
        return prev.map((it) => (it.id === item.id ? { ...it, qty: it.qty + item.qty } : it));
      }
      return [...prev, item];
    });
    
    // Show notification
    setLastAddedProduct(item.title);
    setShowNotification(true);
  };

  const hideNotification = () => {
    setShowNotification(false);
  };

  const removeFromCart = (id: string | number) => {
    setCart((prev) => prev.filter((it) => it.id !== id));
  };

  const incrementQuantity = (id: string | number) => {
    setCart((prev) => prev.map((it) => (it.id === id ? { ...it, qty: it.qty + 1 } : it)));
  };

  const decrementQuantity = (id: string | number) => {
    setCart((prev) => {
      const found = prev.find((it) => it.id === id);
      if (!found) return prev;
      if (found.qty <= 1) {
        return prev.filter((it) => it.id !== id);
      }
      return prev.map((it) => (it.id === id ? { ...it, qty: it.qty - 1 } : it));
    });
  };

  const toggleWishlist = (item: WishlistItem) => {
    setWishlist((prev) => {
      const exists = prev.find((it) => it.id === item.id);
      if (exists) {
        return prev.filter((it) => it.id !== item.id);
      }
      return [...prev, item];
    });
  };

  const removeFromWishlist = (id: string | number) => {
    setWishlist((prev) => prev.filter((it) => it.id !== id));
  };

  const clearCart = () => {
    setCart([]);
  };

  const cartCount = cart.reduce((sum, item) => sum + item.qty, 0);
  const cartTotal = cart.reduce((sum, item) => sum + (item.price || 0) * item.qty, 0);

  return (
    <CartContext.Provider
      value={{
        cart,
        wishlist,
        addToCart,
        removeFromCart,
        incrementQuantity,
        decrementQuantity,
        toggleWishlist,
        removeFromWishlist,
        clearCart,
        cartCount,
        cartTotal,
        showNotification,
        lastAddedProduct,
        hideNotification,
      }}
    >
      {children}
    </CartContext.Provider>
  );
}

export function useCart() {
  const context = useContext(CartContext);
  if (context === undefined) {
    throw new Error("useCart must be used within a CartProvider");
  }
  return context;
}
