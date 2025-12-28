"use client";

import { useState, useRef } from "react";
import { performVirtualTryOn, determineGarmentCategory } from "../services/virtualTryOn";

type VirtualTryOnProps = {
  productImage: string;
  productTitle: string;
  onClose: () => void;
};

export default function VirtualTryOn({ productImage, productTitle, onClose }: VirtualTryOnProps) {
  const [personImage, setPersonImage] = useState<string | null>(null);
  const [resultImage, setResultImage] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Validate file type
    if (!file.type.startsWith("image/")) {
      setError("Please upload a valid image file");
      return;
    }

    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      setError("Image size should be less than 10MB");
      return;
    }

    const reader = new FileReader();
    reader.onloadend = () => {
      setPersonImage(reader.result as string);
      setError(null);
    };
    reader.readAsDataURL(file);
  };

  const handleTryOn = async () => {
    if (!personImage) {
      setError("Please upload your photo first");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const category = determineGarmentCategory(productTitle);
      
      const result = await performVirtualTryOn({
        personImage,
        garmentImage: productImage,
        category,
      });

      if (result.success && result.resultImage) {
        setResultImage(result.resultImage);
        
        // Show info message if in demo mode (when result is same as input)
        if (result.resultImage === personImage) {
          setError("ℹ️ Demo Mode: Configure Hugging Face API key for full virtual try-on. See VIRTUAL_TRYON_SETUP.md");
        }
      } else {
        setError(result.error || "Failed to generate try-on result. Make sure backend server is running.");
      }
    } catch (err) {
      setError("Connection error: Make sure the backend server is running on port 5000");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setPersonImage(null);
    setResultImage(null);
    setError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl max-w-6xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-gradient-to-r from-pink-500 to-pink-600 text-white p-6 rounded-t-2xl flex items-center justify-between">
          <div>
            <h2 className="text-3xl font-bold mb-2">👗 Virtual Try-On</h2>
            <p className="text-pink-100">See how this looks on you!</p>
          </div>
          <button
            onClick={onClose}
            className="bg-white/20 hover:bg-white/30 rounded-full p-2 transition-all"
          >
            <span className="text-2xl">✕</span>
          </button>
        </div>

        <div className="p-6">
          {/* Instructions */}
          <div className="bg-pink-50 border-2 border-pink-200 rounded-xl p-4 mb-6">
            <h3 className="font-bold text-pink-700 mb-2 flex items-center gap-2">
              <span>ℹ️</span>
              <span>How to use:</span>
            </h3>
            <ol className="list-decimal list-inside space-y-1 text-sm text-gray-700">
              <li>Upload a full-body photo of yourself (front-facing works best)</li>
              <li>Click "Try On" to see how the garment looks on you</li>
              <li>Wait for the AI to generate your virtual try-on result</li>
            </ol>
          </div>

          {/* Error Message */}
          {error && (
            <div className="bg-red-50 border-2 border-red-200 rounded-xl p-4 mb-6">
              <p className="text-red-700 font-semibold flex items-center gap-2">
                <span>⚠️</span>
                <span>{error}</span>
              </p>
            </div>
          )}

          {/* Main Content */}
          <div className="grid md:grid-cols-3 gap-6">
            {/* Upload Section */}
            <div className="space-y-4">
              <h3 className="font-bold text-gray-800 text-lg">1. Your Photo</h3>
              <div className="border-2 border-dashed border-pink-300 rounded-xl p-4 bg-pink-50">
                {personImage ? (
                  <div className="relative">
                    <img
                      src={personImage}
                      alt="Your photo"
                      className="w-full h-64 object-contain rounded-lg"
                    />
                    <button
                      onClick={handleReset}
                      className="absolute top-2 right-2 bg-red-500 text-white rounded-full p-2 hover:bg-red-600 transition-all shadow-lg"
                    >
                      <span className="text-sm">🗑️</span>
                    </button>
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <span className="text-6xl mb-4 block">📸</span>
                    <p className="text-gray-600 mb-4">Upload your photo</p>
                    <input
                      ref={fileInputRef}
                      type="file"
                      accept="image/*"
                      onChange={handleImageUpload}
                      className="hidden"
                      id="person-image-upload"
                    />
                    <label
                      htmlFor="person-image-upload"
                      className="inline-block bg-gradient-to-r from-pink-500 to-pink-600 text-white px-6 py-3 rounded-lg font-semibold cursor-pointer hover:shadow-lg transition-all"
                    >
                      Choose Photo
                    </label>
                  </div>
                )}
              </div>
            </div>

            {/* Garment Section */}
            <div className="space-y-4">
              <h3 className="font-bold text-gray-800 text-lg">2. Garment</h3>
              <div className="border-2 border-pink-300 rounded-xl p-4 bg-white">
                <img
                  src={productImage}
                  alt={productTitle}
                  className="w-full h-64 object-contain rounded-lg mb-3"
                />
                <p className="text-sm text-gray-700 font-medium text-center line-clamp-2">
                  {productTitle}
                </p>
              </div>
            </div>

            {/* Result Section */}
            <div className="space-y-4">
              <h3 className="font-bold text-gray-800 text-lg">3. Result</h3>
              <div className="border-2 border-pink-300 rounded-xl p-4 bg-gradient-to-br from-pink-50 to-purple-50">
                {loading ? (
                  <div className="flex flex-col items-center justify-center h-64">
                    <div className="animate-spin rounded-full h-16 w-16 border-4 border-pink-300 border-t-pink-600 mb-4"></div>
                    <p className="text-pink-700 font-semibold">Generating your try-on...</p>
                    <p className="text-sm text-gray-600 mt-2">This may take 10-30 seconds</p>
                  </div>
                ) : resultImage ? (
                  <div className="relative">
                    <img
                      src={resultImage}
                      alt="Try-on result"
                      className="w-full h-64 object-contain rounded-lg"
                    />
                    <div className="mt-4 flex gap-2">
                      <a
                        href={resultImage}
                        download="virtual-tryon-result.png"
                        className="flex-1 bg-gradient-to-r from-green-500 to-green-600 text-white px-4 py-2 rounded-lg font-semibold text-center hover:shadow-lg transition-all"
                      >
                        💾 Download
                      </a>
                      <button
                        onClick={handleReset}
                        className="flex-1 bg-gray-500 text-white px-4 py-2 rounded-lg font-semibold hover:bg-gray-600 transition-all"
                      >
                        🔄 Try Again
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="flex flex-col items-center justify-center h-64 text-gray-400">
                    <span className="text-6xl mb-4">✨</span>
                    <p className="text-center">Your result will appear here</p>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Action Button */}
          {!resultImage && (
            <div className="mt-6 text-center">
              <button
                onClick={handleTryOn}
                disabled={!personImage || loading}
                className={`px-12 py-4 rounded-xl font-bold text-lg transition-all ${
                  !personImage || loading
                    ? "bg-gray-300 text-gray-500 cursor-not-allowed"
                    : "bg-gradient-to-r from-pink-500 to-pink-600 text-white hover:shadow-xl transform hover:scale-105"
                }`}
              >
                {loading ? "Processing..." : "👗 Try On Now"}
              </button>
            </div>
          )}

          {/* Tips */}
          <div className="mt-6 bg-gradient-to-r from-purple-50 to-pink-50 border-2 border-purple-200 rounded-xl p-4">
            <h4 className="font-bold text-purple-700 mb-2">💡 Tips for best results:</h4>
            <ul className="list-disc list-inside space-y-1 text-sm text-gray-700">
              <li>Use a clear, well-lit photo with good contrast</li>
              <li>Stand straight and face the camera directly</li>
              <li>Wear fitted clothing for more accurate results</li>
              <li>Avoid busy backgrounds or patterns</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
