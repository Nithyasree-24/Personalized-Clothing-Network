"use client";

import React from "react";

type Props = {
  id: string;
  title: string;
  price: number;
  image: string;
  source: 'amazon' | 'alibaba' | 'asos' | 'local';
  url?: string;
  rating?: number;
};

export default function ExternalProductCard({ id, title, price, image, source, url, rating }: Props) {
  const sourceColors = {
    amazon: { bg: 'bg-[#f5f1e8]', text: 'text-[#8B6F47]', label: 'Featured' },
    alibaba: { bg: 'bg-[#f5f1e8]', text: 'text-[#8B6F47]', label: 'Featured' },
    asos: { bg: 'bg-[#f5f1e8]', text: 'text-[#8B6F47]', label: 'Featured' },
    local: { bg: 'bg-[#f5f1e8]', text: 'text-[#8B6F47]', label: 'Featured' }
  };

  const sourceStyle = sourceColors[source];

  const handleViewProduct = () => {
    if (url) {
      window.open(url, '_blank', 'noopener,noreferrer');
    }
  };

  return (
    <div className="group relative rounded-lg border border-gray-200 bg-white p-4 hover:shadow-lg transition-shadow duration-200">
      {/* Source Badge */}
      <div className={`absolute top-2 right-2 ${sourceStyle.bg} ${sourceStyle.text} px-2 py-1 rounded-full text-xs font-semibold z-10`}>
        {sourceStyle.label}
      </div>

      {/* Product Image */}
      <div className="relative mb-4 h-48 w-full flex items-center justify-center cursor-pointer overflow-hidden rounded-lg bg-gray-50">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={image}
          alt={title}
          className="h-full w-full object-contain mix-blend-multiply group-hover:scale-110 transition-transform duration-300 ease-in-out"
          onError={(e) => {
            (e.target as HTMLImageElement).src = '/assets/tshirt.jpg';
          }}
        />
      </div>

      {/* Product Title */}
      <h4 className="text-sm font-medium text-gray-800 line-clamp-2 mb-2 min-h-[40px]">
        {title}
      </h4>

      {/* Rating */}
      {rating && (
        <div className="flex items-center gap-1 mb-2">
          <span className="text-yellow-500">⭐</span>
          <span className="text-sm text-gray-600">{rating.toFixed(1)}</span>
        </div>
      )}

      {/* Price */}
      <div className="text-lg font-semibold text-[#8B6F47] mb-3">
        ${price.toFixed(2)}
      </div>

      {/* View Product Button */}
      <button
        onClick={handleViewProduct}
        className="w-full rounded-lg bg-gradient-to-br from-[#8B6F47] to-[#D4A574] p-2 text-white hover:from-[#7A5F3A] hover:to-[#C4956A] font-bold shadow-[0_3px_0_0_rgba(139,111,71,0.8)] hover:shadow-[0_4px_0_0_rgba(139,111,71,0.8)] active:shadow-[0_1px_0_0_rgba(139,111,71,0.8)] transition-all transform hover:-translate-y-0.5 active:translate-y-0.5 flex items-center justify-center gap-2"
      >
        <span>View Product</span>
        <span>🔗</span>
      </button>
    </div>
  );
}
