"use client";

import React, { useEffect, useState } from "react";

interface CartNotificationProps {
  show: boolean;
  productName: string;
  onHide: () => void;
}

export default function CartNotification({ show, productName, onHide }: CartNotificationProps) {
  useEffect(() => {
    if (show) {
      const timer = setTimeout(() => {
        onHide();
      }, 3000); // Hide after 3 seconds

      return () => clearTimeout(timer);
    }
  }, [show, onHide]);

  if (!show) return null;

  return (
    <div className="fixed top-20 right-4 z-50 animate-slideInRight">
      <div className="bg-white border-2 border-green-400 rounded-lg shadow-lg p-4 max-w-sm">
        <div className="flex items-center gap-3">
          <div className="flex-shrink-0">
            <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
              <span className="text-green-600 text-xl">✓</span>
            </div>
          </div>
          <div className="flex-1">
            <h4 className="text-sm font-semibold text-gray-900">Added to Cart!</h4>
            <p className="text-xs text-gray-600 mt-1 line-clamp-2">{productName}</p>
          </div>
          <button
            onClick={onHide}
            className="flex-shrink-0 text-gray-400 hover:text-gray-600 text-lg"
          >
            ✕
          </button>
        </div>
        
        <div className="mt-3 flex gap-2">
          <button
            onClick={onHide}
            className="flex-1 bg-gray-100 text-gray-700 text-xs py-2 px-3 rounded-md hover:bg-gray-200 transition-colors"
          >
            Continue Shopping
          </button>
          <button
            onClick={() => {
              window.location.href = '/cart';
            }}
            className="flex-1 bg-pink-500 text-white text-xs py-2 px-3 rounded-md hover:bg-pink-600 transition-colors"
          >
            View Cart
          </button>
        </div>
      </div>
    </div>
  );
}