"use client";

import { useEffect, useState } from "react";
import { useRouter, useParams } from "next/navigation";
import Link from "next/link";
import Header from "../../../components/Header";
import ProductSlider from "../../../components/ProductSlider";
import AIChatBox from "../../../components/AIChatBox";
import AITryOnInterface from "../../../components/AITryOnInterface";
import { useCart } from "../../../context/CartContext";
import {
  getProductDetail,
  getSimilarProducts,
  getReviews,
  addReview,
  BackendProduct,
  Review,
} from "../../../services/backendApi";

// Helper function to adjust prices
const adjustPrice = (price: number): number => {
  if (price < 500) return Math.floor(Math.random() * 1500) + 500;
  if (price > 5000) return Math.floor(Math.random() * 3000) + 2000;
  return Math.floor(price);
};

export default function ProductDetailPage() {
  const router = useRouter();
  const params = useParams();
  const productId = params.id as string;

  const [product, setProduct] = useState<BackendProduct | null>(null);
  const [similarProducts, setSimilarProducts] = useState<BackendProduct[]>([]);
  const [reviews, setReviews] = useState<Review[]>([]);
  const [loading, setLoading] = useState(true);
  const [userName, setUserName] = useState<string | null>(null);
  const [userId, setUserId] = useState<number | null>(null);

  // Review form state
  const [newRating, setNewRating] = useState(5);
  const [newComment, setNewComment] = useState("");
  const [submittingReview, setSubmittingReview] = useState(false);

  // Product options
  const [selectedSize, setSelectedSize] = useState("");
  const [selectedColor, setSelectedColor] = useState("");
  const [quantity, setQuantity] = useState(1);
  
  // AI Virtual Try-On state
  const [showAITryOn, setShowAITryOn] = useState(false);

  // Available sizes (can be expanded based on product data)
  const sizes = ["XS", "S", "M", "L", "XL", "XXL"];
  
  // Color mapping for display
  const getColorHex = (colorName: string): string => {
    const colorMap: { [key: string]: string } = {
      "Black": "#000000",
      "White": "#FFFFFF", 
      "Navy": "#001f3f",
      "Gray": "#808080",
      "Grey": "#808080",
      "Beige": "#D4A574",
      "Pink": "#FFB6C1",
      "Red": "#FF0000",
      "Blue": "#0000FF",
      "Green": "#008000",
      "Yellow": "#FFFF00",
      "Purple": "#800080",
      "Brown": "#A52A2A",
      "Orange": "#FFA500",
    };
    return colorMap[colorName] || "#808080"; // Default to gray if color not found
  };

  const { cart, wishlist, addToCart, removeFromCart, incrementQuantity, decrementQuantity, toggleWishlist, cartCount, cartTotal } = useCart();

  useEffect(() => {
    const user = localStorage.getItem("user");
    if (user) {
      try {
        const userData = JSON.parse(user);
        setUserName(userData.name || "Guest");
        setUserId(userData.id || null);
      } catch {}
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("user");
    setUserName(null);
    setUserId(null);
  };

  useEffect(() => {
    const loadProductData = async () => {
      setLoading(true);
      try {
        // Load product details
        const productData = await getProductDetail(productId);
        if (productData) {
          setProduct({ ...productData, price: adjustPrice(productData.price) });
          // Set initial values from database
          setSelectedSize(productData.size || "M");
          setSelectedColor(productData.color || "");
        }

        // Load similar products
        const similar = await getSimilarProducts(productId, 8);
        setSimilarProducts(similar.map(p => ({ ...p, price: adjustPrice(p.price) })));

        // Load reviews
        const reviewsData = await getReviews(productId);
        setReviews(reviewsData);
      } catch (error) {
        console.error("Error loading product data:", error);
      } finally {
        setLoading(false);
      }
    };

    if (productId) {
      loadProductData();
    }
  }, [productId]);

  const handleAddToCart = () => {
    if (!product) return;
    const displaySize = selectedSize || product.size || "One Size";
    const displayColor = selectedColor || product.color || "Default";
    
    addToCart({
      id: product.product_id,
      title: `${product.title} (${displaySize}, ${displayColor})`,
      price: product.price,
      qty: quantity,
      image: product.image_url,
    });
  };

  const handleBuyNow = () => {
    if (!product) return;
    const displaySize = selectedSize || product.size || "One Size";
    const displayColor = selectedColor || product.color || "Default";
    
    addToCart({
      id: product.product_id,
      title: `${product.title} (${displaySize}, ${displayColor})`,
      price: product.price,
      qty: quantity,
      image: product.image_url,
    });
    router.push("/checkout");
  };

  const handleSubmitReview = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!userId) {
      alert("Please login to submit a review");
      return;
    }

    setSubmittingReview(true);
    const success = await addReview(productId, userId, newRating, newComment);
    
    if (success) {
      // Reload reviews
      const reviewsData = await getReviews(productId);
      setReviews(reviewsData);
      setNewComment("");
      setNewRating(5);
      alert("Review submitted successfully!");
    } else {
      alert("Failed to submit review. Please try again.");
    }
    setSubmittingReview(false);
  };

  const averageRating = reviews.length > 0
    ? (reviews.reduce((sum, r) => sum + r.rating, 0) / reviews.length).toFixed(1)
    : "0.0";

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-pink-50 via-pink-100 to-pink-200 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-16 w-16 border-4 border-pink-300 border-t-pink-600"></div>
          <p className="mt-4 text-pink-700 font-semibold text-lg">Loading product...</p>
        </div>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-pink-50 via-pink-100 to-pink-200 flex items-center justify-center">
        <div className="text-center">
          <span className="text-6xl mb-4 block">😕</span>
          <h2 className="text-2xl font-bold bg-gradient-to-r from-pink-600 to-pink-800 bg-clip-text text-transparent mb-4">Product Not Found</h2>
          <Link href="/home" className="text-pink-600 font-semibold hover:underline">
            Go back to home
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-pink-100 to-pink-200">
      <div className="bg-gradient-to-r from-pink-100 to-pink-200 shadow-lg sticky top-0 z-40 border-b-2 border-pink-300">
        <Header
          searchTerm=""
          onSearch={() => {}}
          cartCount={cartCount}
          cartTotal={cartTotal}
          cartItems={cart}
          onRemoveFromCart={removeFromCart}
          onIncreaseQty={incrementQuantity}
          onDecreaseQty={decrementQuantity}
          onAddToCart={addToCart}
          wishlistItems={wishlist}
          onRemoveFromWishlist={(id) => {
            const item = wishlist.find((it) => it.id === id);
            if (item) toggleWishlist(item);
          }}
          userName={userName}
          onLogout={handleLogout}
        />
      </div>

      <div className="mx-auto max-w-[1400px] px-5 py-8">
        {/* Back Button */}
        <div className="mb-6">
          <button
            onClick={() => router.back()}
            className="inline-flex items-center gap-2 bg-white border-2 border-pink-500 text-pink-600 px-6 py-3 rounded-lg font-semibold hover:bg-pink-50 transition-all shadow-sm"
          >
            <span>←</span>
            <span>Back</span>
          </button>
        </div>

        {/* Product Detail Section */}
        <div className="bg-gradient-to-r from-pink-50 to-pink-100 rounded-xl shadow-lg p-6 mb-8 border border-pink-200">
          <div className="grid md:grid-cols-2 gap-8">
            {/* Product Image */}
            <div>
              <div className="bg-gray-100 rounded-xl overflow-hidden aspect-square">
                <img
                  src={product.image_url}
                  alt={product.title}
                  className="w-full h-full object-contain p-4"
                />
              </div>
            </div>

            {/* Product Info */}
            <div className="space-y-5">
              {/* Title and Wishlist */}
              <div className="flex items-start justify-between gap-3">
                <h1 className="text-2xl font-bold text-gray-900 leading-tight flex-1">
                  {product.title}
                </h1>
                <button
                  onClick={() => toggleWishlist({
                    id: product.product_id,
                    title: product.title,
                    image: product.image_url,
                    price: product.price,
                  })}
                  className="flex-shrink-0 bg-white border-2 border-gray-300 hover:border-red-400 rounded-full p-2 shadow-sm hover:shadow-md transition-all"
                  aria-label="Toggle wishlist"
                >
                  <span className="text-2xl">
                    {wishlist.find((it) => it.id === product.product_id) ? "❤️" : "🤍"}
                  </span>
                </button>
              </div>

              {/* Rating */}
              <div className="flex items-center gap-2">
                <div className="flex text-yellow-400 text-lg">
                  {"★".repeat(Math.floor(Number(averageRating)))}
                  {"☆".repeat(5 - Math.floor(Number(averageRating)))}
                </div>
                <span className="text-gray-600 text-sm">
                  {averageRating} ({reviews.length} reviews)
                </span>
              </div>

              {/* Price */}
              <div className="text-4xl font-bold bg-gradient-to-r from-pink-600 to-pink-800 bg-clip-text text-transparent">
                ₹{product.price.toLocaleString()}
              </div>

              {/* Stock Status */}
              <div className="inline-flex items-center gap-2 bg-green-50 px-4 py-2 rounded-lg border border-green-200">
                <span className="text-green-600 text-lg">✓</span>
                <span className="text-green-700 font-semibold">In Stock - Ready to Ship</span>
              </div>

              {/* Product Description */}
              {product.description && (
                <div className="pt-4 border-t border-pink-200">
                  <h3 className="text-lg font-semibold text-gray-700 mb-3">Product Description</h3>
                  <div className="bg-white rounded-lg p-4 border border-pink-200">
                    <p className="text-gray-700 leading-relaxed whitespace-pre-line">
                      {product.description}
                    </p>
                  </div>
                </div>
              )}

              {/* Product Details */}
              <div className="pt-4 border-t border-pink-200">
                <h3 className="text-lg font-semibold text-gray-700 mb-3">Product Details</h3>
                <div className="bg-white rounded-lg p-4 border border-pink-200 space-y-2">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Category:</span>
                    <span className="font-semibold text-gray-900">{product.category}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Gender:</span>
                    <span className="font-semibold text-gray-900 capitalize">{product.gender}</span>
                  </div>
                  {product.color && (
                    <div className="flex justify-between">
                      <span className="text-gray-600">Available Color:</span>
                      <div className="flex items-center gap-2">
                        <div
                          className="w-4 h-4 rounded-full border border-gray-300"
                          style={{ backgroundColor: getColorHex(product.color) }}
                        />
                        <span className="font-semibold text-gray-900">{product.color}</span>
                      </div>
                    </div>
                  )}
                </div>
              </div>

              {/* Size Selection */}
              <div className="pt-4 border-t border-pink-200">
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Size: <span className="text-pink-600">{selectedSize}</span>
                </label>
                <div className="flex flex-wrap gap-2">
                  {sizes.map((size) => (
                    <button
                      key={size}
                      onClick={() => setSelectedSize(size)}
                      className={`px-5 py-2.5 rounded-md border-2 font-semibold text-sm transition-all ${
                        selectedSize === size
                          ? "border-pink-500 bg-pink-500 text-white shadow-md"
                          : "border-pink-300 text-gray-700 hover:border-pink-500 hover:bg-pink-50"
                      }`}
                    >
                      {size}
                    </button>
                  ))}
                </div>
              </div>

              {/* Color Selection */}
              {product.color && (
                <div className="pt-4 border-t border-pink-200">
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Color: <span className="text-pink-600">{selectedColor}</span>
                  </label>
                  <div className="flex flex-wrap gap-2">
                    <button
                      onClick={() => setSelectedColor(product.color)}
                      className={`flex items-center gap-2 px-4 py-3 rounded-md border-2 transition-all ${
                        selectedColor === product.color
                          ? "border-pink-500 bg-pink-50 shadow-md"
                          : "border-pink-300 hover:border-pink-500 hover:bg-pink-50"
                      }`}
                    >
                      <div
                        className={`w-6 h-6 rounded-full border-2 ${
                          product.color === "White" ? "border-gray-400" : "border-gray-300"
                        }`}
                        style={{ backgroundColor: getColorHex(product.color) }}
                      />
                      <span className="font-semibold text-sm text-gray-900">{product.color}</span>
                    </button>
                  </div>
                </div>
              )}

              {/* Quantity */}
              <div className="pt-4 border-t border-pink-200">
                <label className="block text-sm font-semibold text-gray-700 mb-2">Quantity</label>
                <div className="flex items-center gap-3">
                  <button
                    onClick={() => setQuantity(Math.max(1, quantity - 1))}
                    className="w-10 h-10 flex items-center justify-center rounded-full bg-pink-500 text-white font-bold text-xl hover:bg-pink-600 transition-all shadow-md"
                  >
                    −
                  </button>
                  <div className="w-16 h-10 flex items-center justify-center bg-white border-2 border-pink-300 rounded-md">
                    <span className="text-xl font-bold text-pink-700">{quantity}</span>
                  </div>
                  <button
                    onClick={() => setQuantity(quantity + 1)}
                    className="w-10 h-10 flex items-center justify-center rounded-full bg-pink-500 text-white font-bold text-xl hover:bg-pink-600 transition-all shadow-md"
                  >
                    +
                  </button>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="pt-4 border-t border-pink-200 space-y-3">
                <button
                  onClick={() => setShowAITryOn(true)}
                  className="w-full bg-gradient-to-r from-purple-500 to-purple-600 hover:from-purple-600 hover:to-purple-700 text-white font-bold py-3 px-6 rounded-lg transition-all shadow-md hover:shadow-lg flex items-center justify-center gap-2"
                >
                  <span className="text-xl">🤖</span>
                  <span>AI Virtual Try-On</span>
                </button>
                <button
                  onClick={handleAddToCart}
                  className="w-full bg-gradient-to-r from-pink-500 to-pink-600 hover:from-pink-600 hover:to-pink-700 text-white font-bold py-3 px-6 rounded-lg transition-all shadow-md hover:shadow-lg"
                >
                  🛒 Add to Cart
                </button>
                <button
                  onClick={handleBuyNow}
                  className="w-full bg-gradient-to-r from-pink-600 to-pink-700 hover:from-pink-700 hover:to-pink-800 text-white font-bold py-3 px-6 rounded-lg transition-all shadow-md hover:shadow-lg"
                >
                  ⚡ Buy Now
                </button>
              </div>

              {/* Additional Info */}
              <div className="pt-4 border-t border-pink-200 bg-pink-50 rounded-lg p-4 space-y-2 border border-pink-200">
                <p className="flex items-center gap-2 text-green-600 text-sm font-medium">
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
                <p className="flex items-center gap-2 text-gray-700 text-sm">
                  <span className="text-green-600">✓</span> Free delivery on orders over ₹500
                </p>
                <p className="flex items-center gap-2 text-gray-700 text-sm">
                  <span className="text-green-600">✓</span> Easy 7-day returns
                </p>
                <p className="flex items-center gap-2 text-gray-700 text-sm">
                  <span className="text-green-600">✓</span> Secure payment options
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Reviews Section */}
        <div className="bg-gradient-to-r from-pink-50 to-pink-100 rounded-xl shadow-lg p-8 mb-8 border border-pink-200">
          <h2 className="text-3xl font-bold bg-gradient-to-r from-pink-600 to-pink-800 bg-clip-text text-transparent mb-6">Customer Reviews</h2>

          {/* Average Rating */}
          <div className="flex items-center gap-6 mb-8 pb-8 border-b border-pink-200">
            <div className="text-center">
              <div className="text-6xl font-bold bg-gradient-to-r from-pink-600 to-pink-800 bg-clip-text text-transparent">{averageRating}</div>
              <div className="flex text-yellow-400 text-2xl mt-2 justify-center">
                {"★".repeat(Math.floor(Number(averageRating)))}
                {"☆".repeat(5 - Math.floor(Number(averageRating)))}
              </div>
              <p className="text-pink-700 font-semibold mt-2">{reviews.length} reviews</p>
            </div>
          </div>

          {/* Add Review Form */}
          {userId ? (
            <form onSubmit={handleSubmitReview} className="mb-8 pb-8 border-b border-pink-200">
              <h3 className="text-xl font-bold text-pink-700 mb-4">Write a Review</h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-gray-700 font-semibold mb-2">Rating</label>
                  <div className="flex gap-2">
                    {[1, 2, 3, 4, 5].map((star) => (
                      <button
                        key={star}
                        type="button"
                        onClick={() => setNewRating(star)}
                        className="text-4xl transition-all hover:scale-110"
                      >
                        {star <= newRating ? "⭐" : "☆"}
                      </button>
                    ))}
                  </div>
                </div>
                <div>
                  <label className="block text-gray-700 font-semibold mb-2">Comment</label>
                  <textarea
                    value={newComment}
                    onChange={(e) => setNewComment(e.target.value)}
                    className="w-full border-2 border-pink-300 rounded-lg p-4 focus:border-pink-500 focus:outline-none bg-white"
                    rows={4}
                    placeholder="Share your experience with this product..."
                    required
                  />
                </div>
                <button
                  type="submit"
                  disabled={submittingReview}
                  className="bg-gradient-to-r from-pink-500 to-pink-600 hover:from-pink-600 hover:to-pink-700 text-white font-bold py-3 px-8 rounded-lg transition-all disabled:opacity-50 shadow-md hover:shadow-lg"
                >
                  {submittingReview ? "Submitting..." : "Submit Review"}
                </button>
              </div>
            </form>
          ) : (
            <div className="mb-8 pb-8 border-b border-pink-200 text-center bg-white rounded-lg p-6">
              <p className="text-gray-700 text-lg">
                <Link href="/login" className="text-pink-600 font-bold hover:underline hover:text-pink-700 transition-colors">
                  Login
                </Link>{" "}
                to write a review
              </p>
            </div>
          )}

          {/* Reviews List */}
          <div className="space-y-6">
            {reviews.length === 0 ? (
              <div className="text-center py-12 bg-white rounded-lg">
                <span className="text-6xl mb-4 block">📝</span>
                <p className="text-pink-600 font-semibold text-lg">No reviews yet. Be the first to review!</p>
              </div>
            ) : (
              reviews.map((review) => (
                <div key={review.id} className="border-b border-pink-200 pb-6 last:border-0 bg-white rounded-lg p-4">
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <p className="font-bold text-gray-900">{review.user_name}</p>
                      <div className="flex text-yellow-400 text-lg">
                        {"★".repeat(review.rating)}
                        {"☆".repeat(5 - review.rating)}
                      </div>
                    </div>
                    <p className="text-sm text-pink-600 font-semibold">
                      {new Date(review.created_at).toLocaleDateString()}
                    </p>
                  </div>
                  <p className="text-gray-700">{review.comment}</p>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Similar Products */}
        {similarProducts.length > 0 && (
          <div className="bg-gradient-to-r from-pink-50 to-pink-100 rounded-xl shadow-lg p-8 border border-pink-200">
            <h2 className="text-3xl font-bold bg-gradient-to-r from-pink-600 to-pink-800 bg-clip-text text-transparent mb-6">Similar Products</h2>
            <ProductSlider
              products={similarProducts.map((p) => ({
                id: p.product_id,
                title: p.title,
                price: p.price,
                img: p.image_url,
                imageUrl: p.image_url,
              }))}
              onAdd={(product) =>
                addToCart({
                  id: product.id,
                  title: product.title,
                  price: product.price,
                  qty: 1,
                  image: product.imageUrl,
                })
              }
              onBuy={(product) => {
                addToCart({
                  id: product.id,
                  title: product.title,
                  price: product.price,
                  qty: 1,
                  image: product.imageUrl,
                });
                router.push("/checkout");
              }}
              isWishlisted={(id) => !!wishlist.find((it) => it.id === id)}
              onToggleWishlist={(product) =>
                toggleWishlist({
                  id: product.id,
                  title: product.title,
                  image: product.imageUrl,
                  price: product.price,
                })
              }
              getQty={(id) => cart.find((it) => it.id === id)?.qty ?? 0}
              onIncrease={incrementQuantity}
              onDecrease={decrementQuantity}
              onProductClick={(product) => router.push(`/products/${product.id}`)}
            />
          </div>
        )}
      </div>

      <AIChatBox />

      {/* AI Virtual Try-On Modal */}
      {showAITryOn && product && (
        <AITryOnInterface
          productImage={product.image_url}
          productTitle={product.title}
          productType={product.category === 'dresses' ? 'dress' : 
                      product.category === 'tops' ? 'top' : 
                      product.category === 'bottoms' ? 'bottom' : 
                      product.category === 'outerwear' ? 'outerwear' : 
                      product.category === 'shoes' ? 'shoes' : 'top'}
          onClose={() => setShowAITryOn(false)}
        />
      )}
    </div>
  );
}
