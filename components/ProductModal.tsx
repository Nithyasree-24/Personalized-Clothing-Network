"use client";

import { useState } from "react";

interface ProductModalProps {
  isOpen: boolean;
  onClose: () => void;
  product: {
    id: string | number;
    title: string;
    price: number;
    imageUrl?: string;
    description?: string;
  };
  onAddToCart: (product: any, size: string, color: string) => void;
  onBuyNow: (product: any, size: string, color: string) => void;
}

export default function ProductModal({
  isOpen,
  onClose,
  product,
  onAddToCart,
  onBuyNow,
}: ProductModalProps) {
  const [selectedSize, setSelectedSize] = useState("M");
  const [selectedColor, setSelectedColor] = useState("Black");
  const [quantity, setQuantity] = useState(1);

  const sizes = ["XS", "S", "M", "L", "XL", "XXL"];
  const colors = [
    { name: "Black", hex: "#000000" },
    { name: "White", hex: "#FFFFFF" },
    { name: "Navy", hex: "#001f3f" },
    { name: "Gray", hex: "#808080" },
    { name: "Beige", hex: "#D4A574" },
    { name: "Pink", hex: "#FFB6C1" },
  ];

  if (!isOpen) return null;

  const handleAddToCart = () => {
    onAddToCart({ ...product, qty: quantity }, selectedSize, selectedColor);
    onClose();
  };

  const handleBuyNow = () => {
    onBuyNow({ ...product, qty: quantity }, selectedSize, selectedColor);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
      <div className="bg-white rounded-2xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 bg-white rounded-full p-2 shadow-lg hover:bg-gray-100 transition-all z-10"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        <div className="grid md:grid-cols-2 gap-8 p-8">
          {/* Product Image */}
          <div className="relative">
            <div className="sticky top-0">
              <div className="bg-gray-100 rounded-xl overflow-hidden aspect-square">
                <img
                  src={product.imageUrl || "/placeholder.png"}
                  alt={product.title}
                  className="w-full h-full object-contain"
                />
              </div>
            </div>
          </div>

          {/* Product Details */}
          <div className="space-y-6">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-2">{product.title}</h2>
              <div className="flex items-center gap-2 mb-4">
                <div className="flex text-yellow-400">
                  {"★★★★☆"}
                </div>
                <span className="text-sm text-gray-600">(4.0 / 5)</span>
              </div>
              <div className="text-4xl font-bold text-[#8B6F47]">
                ₹{product.price.toLocaleString()}
              </div>
              <p className="text-sm text-green-600 mt-2">✓ In Stock</p>
            </div>

            {/* Description */}
            {product.description && (
              <div className="border-t border-gray-200 pt-4">
                <h3 className="font-semibold text-gray-900 mb-2">Description</h3>
                <p className="text-gray-600 text-sm">{product.description}</p>
              </div>
            )}

            {/* Size Selection */}
            <div className="border-t border-gray-200 pt-4">
              <h3 className="font-semibold text-gray-900 mb-3">Select Size</h3>
              <div className="flex flex-wrap gap-2">
                {sizes.map((size) => (
                  <button
                    key={size}
                    onClick={() => setSelectedSize(size)}
                    className={`px-4 py-2 rounded-lg border-2 font-semibold transition-all ${
                      selectedSize === size
                        ? "border-[#8B6F47] bg-[#8B6F47] text-white"
                        : "border-gray-300 hover:border-[#8B6F47] text-gray-700"
                    }`}
                  >
                    {size}
                  </button>
                ))}
              </div>
            </div>

            {/* Color Selection */}
            <div className="border-t border-gray-200 pt-4">
              <h3 className="font-semibold text-gray-900 mb-3">Select Color</h3>
              <div className="flex flex-wrap gap-3">
                {colors.map((color) => (
                  <button
                    key={color.name}
                    onClick={() => setSelectedColor(color.name)}
                    className={`flex items-center gap-2 px-4 py-2 rounded-lg border-2 transition-all ${
                      selectedColor === color.name
                        ? "border-[#8B6F47] bg-[#f5f1e8]"
                        : "border-gray-300 hover:border-[#8B6F47]"
                    }`}
                  >
                    <div
                      className="w-6 h-6 rounded-full border-2 border-gray-300"
                      style={{ backgroundColor: color.hex }}
                    />
                    <span className="text-sm font-medium">{color.name}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Quantity */}
            <div className="border-t border-gray-200 pt-4">
              <h3 className="font-semibold text-gray-900 mb-3">Quantity</h3>
              <div className="flex items-center gap-3">
                <button
                  onClick={() => setQuantity(Math.max(1, quantity - 1))}
                  className="w-10 h-10 rounded-lg border-2 border-gray-300 hover:border-[#8B6F47] font-bold text-lg"
                >
                  −
                </button>
                <span className="text-xl font-semibold w-12 text-center">{quantity}</span>
                <button
                  onClick={() => setQuantity(quantity + 1)}
                  className="w-10 h-10 rounded-lg border-2 border-gray-300 hover:border-[#8B6F47] font-bold text-lg"
                >
                  +
                </button>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="border-t border-gray-200 pt-6 space-y-3">
              <button
                onClick={handleAddToCart}
                className="w-full bg-[#FFD814] hover:bg-[#F7CA00] text-gray-900 font-bold py-4 rounded-lg transition-all shadow-md hover:shadow-lg"
              >
                🛒 Add to Cart
              </button>
              <button
                onClick={handleBuyNow}
                className="w-full bg-gradient-to-r from-[#FF6B35] to-[#FF8C42] hover:from-[#FF5722] hover:to-[#FF7B32] text-white font-bold py-4 rounded-lg transition-all shadow-md hover:shadow-lg"
              >
                ⚡ Buy Now
              </button>
            </div>

            {/* Additional Info */}
            <div className="border-t border-gray-200 pt-4 space-y-2 text-sm text-gray-600">
              <p className="flex items-center gap-2 text-green-600 font-medium">
                <span>🚚</span> 
                Delivery by {(() => {
                  const today = new Date();
                  const days = Math.floor(Math.random() * 5) + 3; // 3-7 days
                  const delivery = new Date();
                  delivery.setDate(today.getDate() + days);
                  const options = { weekday: 'short', month: 'short', day: 'numeric' };
                  return delivery.toLocaleDateString('en-IN', options);
                })()}
              </p>
              <p>✓ Free delivery on orders over ₹500</p>
              <p>✓ Easy 7-day returns</p>
              <p>✓ Secure payment options</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
