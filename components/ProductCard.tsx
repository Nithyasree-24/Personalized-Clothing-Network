"use client";

import Image from "next/image";
import Link from "next/link";
import React from "react";

type Props = {
  productId?: string;
  title: string;
  price?: number | string;
  img?: string | any;
  onAdd?: () => void;
  onBuy?: () => void;
  isWishlisted?: boolean;
  onToggleWishlist?: () => void;
  qty?: number;
  onIncrease?: () => void;
  onDecrease?: () => void;
  onClick?: () => void;
  deliveryDate?: string;
};

export default function ProductCard({ productId, title, price, img, onAdd, onBuy, isWishlisted, onToggleWishlist, qty = 0, onIncrease, onDecrease, onClick, deliveryDate }: Props) {
  const handleClick = () => {
    if (onClick) {
      onClick();
    }
  };

  const getDeliveryText = () => {
    if (!deliveryDate) {
      // Default delivery date - 3-7 days from now
      const days = Math.floor(Math.random() * 5) + 3; // 3-7 days
      const delivery = new Date();
      delivery.setDate(delivery.getDate() + days);
      return `Delivery by ${delivery.toLocaleDateString('en-IN', { month: 'short', day: 'numeric' })}`;
    }
    
    const delivery = new Date(deliveryDate);
    const today = new Date();
    const diffTime = delivery.getTime() - today.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays <= 1) return "Delivery by Tomorrow";
    if (diffDays <= 7) return `Delivery in ${diffDays} days`;
    return `Delivery by ${delivery.toLocaleDateString('en-IN', { month: 'short', day: 'numeric' })}`;
  };

  return (
    <div className="group relative rounded-lg border border-gray-200 bg-white p-4 hover:shadow-lg transition-shadow duration-200 flex flex-col h-full">
      {/* Clickable image and title area */}
      <div onClick={handleClick} className="cursor-pointer flex-1 flex flex-col">
        <div className="relative mb-4 w-full aspect-square flex items-center justify-center overflow-hidden rounded-lg bg-gray-50">
          {img ? (
            // img can be StaticImageData or a string path
            typeof img === "string" ? (
              // eslint-disable-next-line @next/next/no-img-element
              <img src={img} alt={title} className="h-full w-full object-cover group-hover:scale-110 transition-transform duration-300 ease-in-out" />
            ) : (
              <Image src={img} alt={title} className="h-full w-full object-cover group-hover:scale-110 transition-transform duration-300 ease-in-out" />
            )
          ) : (
            <div className="text-gray-400">No image</div>
          )}
        </div>
        <h4 className="text-sm font-medium text-gray-800 hover:text-indigo-600 line-clamp-2 mb-2 h-10">{title}</h4>
      </div>
      
      {/* Wishlist button - top right */}
      <button
        onClick={(e) => {
          e.preventDefault();
          e.stopPropagation();
          onToggleWishlist?.();
        }}
        aria-label="Toggle wishlist"
        className="absolute top-2 right-2 bg-white rounded-full p-2 shadow-md hover:shadow-lg transition-shadow z-10"
      >
        <span className="text-xl">{isWishlisted ? "❤️" : "🤍"}</span>
      </button>
      
      <div className="text-lg font-semibold text-black mb-2">₹{price ?? "-"}</div>

      {/* Action buttons - compact icon layout */}
      <div className="flex items-center gap-1.5">
        {/* Add to Cart / Decrease */}
        <button
          onClick={(e) => {
            e.preventDefault();
            e.stopPropagation();
            qty > 0 ? onDecrease?.() : onAdd?.();
          }}
          aria-label={qty > 0 ? "Decrease quantity" : "Add to cart"}
          className="flex-1 rounded-lg bg-gradient-to-br from-pink-500 to-pink-600 p-2 text-white hover:from-pink-600 hover:to-pink-700 font-bold shadow-md hover:shadow-lg transition-all flex items-center justify-center"
        >
          {qty > 0 ? <span className="text-base">−</span> : <span className="text-base">🛒</span>}
        </button>

        {/* Quantity Display / Increase */}
        {qty > 0 && (
          <>
            <div className="flex items-center justify-center bg-gradient-to-r from-pink-50 to-pink-100 rounded-lg px-2 py-2 shadow-inner min-w-[35px]">
              <span className="text-xs font-bold text-pink-700">{qty}</span>
            </div>
            <button
              onClick={(e) => {
                e.preventDefault();
                e.stopPropagation();
                onIncrease?.();
              }}
              aria-label="Increase quantity"
              className="flex-1 rounded-lg bg-gradient-to-br from-pink-500 to-pink-600 p-2 text-white hover:from-pink-600 hover:to-pink-700 font-bold shadow-md hover:shadow-lg transition-all flex items-center justify-center"
            >
              <span className="text-base">+</span>
            </button>
          </>
        )}

        {/* Buy Now */}
        <button
          onClick={(e) => {
            e.preventDefault();
            e.stopPropagation();
            onBuy?.();
          }}
          aria-label="Buy now"
          className="flex-1 rounded-lg bg-white border-2 border-gray-800 p-2 text-black hover:bg-gray-100 font-bold shadow-[0_3px_0_0_rgba(0,0,0,0.3)] hover:shadow-[0_4px_0_0_rgba(0,0,0,0.3)] active:shadow-[0_1px_0_0_rgba(0,0,0,0.3)] transition-all transform hover:-translate-y-0.5 active:translate-y-0.5 flex items-center justify-center"
        >
          <span className="text-base">💵</span>
        </button>
      </div>
    </div>
  );
}
