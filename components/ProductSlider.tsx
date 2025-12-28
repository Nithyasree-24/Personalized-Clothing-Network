"use client";

import { useState } from "react";
import ProductCard from "./ProductCard";

type Product = {
  id: string | number;
  title: string;
  price: number;
  img?: any;
  imageUrl: string;
};

type ProductSliderProps = {
  products: Product[];
  onAdd: (product: Product) => void;
  onBuy: (product: Product) => void;
  isWishlisted: (id: string | number) => boolean;
  onToggleWishlist: (product: Product) => void;
  getQty: (id: string | number) => number;
  onIncrease: (id: string | number) => void;
  onDecrease: (id: string | number) => void;
  onProductClick?: (product: Product) => void;
};

export default function ProductSlider({
  products,
  onAdd,
  onBuy,
  isWishlisted,
  onToggleWishlist,
  getQty,
  onIncrease,
  onDecrease,
  onProductClick,
}: ProductSliderProps) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const itemsPerSlide = 4;
  const maxIndex = Math.max(0, products.length - itemsPerSlide);

  const handlePrev = () => {
    setCurrentIndex((prev) => Math.max(0, prev - 1));
  };

  const handleNext = () => {
    setCurrentIndex((prev) => Math.min(maxIndex, prev + 1));
  };

  return (
    <div className="relative group">
      <div className="overflow-hidden">
        <div
          className="flex gap-6 transition-transform duration-500 ease-out"
          style={{
            transform: `translateX(-${currentIndex * (320 + 24)}px)`, // 320px width + 24px gap
          }}
        >
          {products.map((product) => (
            <div key={String(product.id)} className="flex-shrink-0 w-80">
              <ProductCard
                productId={String(product.id)}
                title={product.title}
                price={product.price}
                img={product.img}
                onAdd={() => onAdd(product)}
                onBuy={() => onBuy(product)}
                isWishlisted={isWishlisted(product.id)}
                onToggleWishlist={() => onToggleWishlist(product)}
                qty={getQty(product.id)}
                onIncrease={() => onIncrease(product.id)}
                onDecrease={() => onDecrease(product.id)}
                onClick={onProductClick ? () => onProductClick(product) : undefined}
              />
            </div>
          ))}
        </div>
      </div>

      {/* Navigation Arrows */}
      {currentIndex > 0 && (
        <button
          onClick={handlePrev}
          className="absolute left-2 top-1/2 -translate-y-1/2 bg-gradient-to-r from-pink-400 to-pink-500 hover:from-pink-500 hover:to-pink-600 text-white rounded-full p-3 shadow-lg opacity-90 group-hover:opacity-100 transition-all z-10"
          aria-label="Previous"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
      )}

      {currentIndex < maxIndex && (
        <button
          onClick={handleNext}
          className="absolute right-2 top-1/2 -translate-y-1/2 bg-gradient-to-r from-pink-400 to-pink-500 hover:from-pink-500 hover:to-pink-600 text-white rounded-full p-3 shadow-lg opacity-90 group-hover:opacity-100 transition-all z-10"
          aria-label="Next"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      )}

      {/* Dots Indicator */}
      <div className="flex justify-center gap-2 mt-6">
        {Array.from({ length: maxIndex + 1 }).map((_, idx) => (
          <button
            key={idx}
            onClick={() => setCurrentIndex(idx)}
            className={`w-2 h-2 rounded-full transition-all ${
              idx === currentIndex ? "bg-gradient-to-r from-pink-500 to-pink-600 w-8" : "bg-pink-300"
            }`}
            aria-label={`Go to slide ${idx + 1}`}
          />
        ))}
      </div>
    </div>
  );
}
