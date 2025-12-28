"use client";

import { useState } from "react";
import Link from "next/link";
import BodyShapeAnalyzer from "../../components/BodyShapeAnalyzer";

type BodyShape = "hourglass" | "pear" | "apple" | "rectangle" | "inverted-triangle" | null;

export default function StyleFinderPage() {
  const [showAnalyzer, setShowAnalyzer] = useState(false);
  const [detectedShape, setDetectedShape] = useState<BodyShape>(null);

  const bodyShapeInfo = {
    hourglass: {
      title: "Hourglass Shape ⏳",
      description: "You have balanced proportions with a defined waist. Your shoulders and hips are roughly the same width.",
      recommendations: [
        "Wrap dresses that emphasize your waist",
        "Fitted tops and blouses",
        "High-waisted jeans and skirts",
        "Belted outfits to highlight your curves",
        "V-neck and scoop neck tops"
      ],
      avoid: ["Boxy, shapeless clothing", "Oversized tops", "Low-rise pants"],
      categories: ["Dresses", "Tops", "Bottoms"]
    },
    pear: {
      title: "Pear Shape 🍐",
      description: "You have narrower shoulders and a wider hip area. Your lower body is fuller than your upper body.",
      recommendations: [
        "A-line dresses and skirts",
        "Boat neck and off-shoulder tops",
        "Dark colored bottoms",
        "Statement tops with details",
        "Structured jackets"
      ],
      avoid: ["Skinny jeans", "Tapered pants", "Horizontal stripes on bottom"],
      categories: ["Dresses", "Tops", "Jackets"]
    },
    apple: {
      title: "Apple Shape 🍎",
      description: "You have broader shoulders and a fuller midsection. Your legs are typically slimmer.",
      recommendations: [
        "Empire waist dresses",
        "V-neck and deep V tops",
        "Straight leg pants",
        "Flowy tops that skim the body",
        "Structured blazers"
      ],
      avoid: ["Tight fitted tops", "Crop tops", "Clingy fabrics"],
      categories: ["Dresses", "Tops", "Pants"]
    },
    rectangle: {
      title: "Rectangle Shape 📏",
      description: "You have balanced proportions with a less defined waist. Your shoulders, waist, and hips are similar widths.",
      recommendations: [
        "Peplum tops to create curves",
        "Belted dresses and tops",
        "Layered outfits",
        "Ruffled and detailed clothing",
        "Fit-and-flare dresses"
      ],
      avoid: ["Straight, boxy cuts", "Shapeless clothing"],
      categories: ["Dresses", "Tops", "Activewear"]
    },
    "inverted-triangle": {
      title: "Inverted Triangle 🔺",
      description: "You have broader shoulders and a narrower hip area. Your upper body is fuller than your lower body.",
      recommendations: [
        "A-line skirts and dresses",
        "Wide leg pants",
        "V-neck tops to elongate",
        "Dark colored tops",
        "Detailed bottoms"
      ],
      avoid: ["Shoulder pads", "Boat neck tops", "Embellished shoulders"],
      categories: ["Bottoms", "Dresses", "Pants"]
    }
  };

  const handleShapeDetected = (shape: BodyShape) => {
    setDetectedShape(shape);
    setShowAnalyzer(false);
  };

  return (
    <div className="min-h-screen bg-[#fbfbec]">
      {/* Header */}
      <div className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <Link href="/home" className="text-pink-600 hover:text-pink-700 font-semibold">
              ← Back to Home
            </Link>
            <h1 className="text-2xl font-bold text-pink-600">Style Finder</h1>
            <div className="w-20"></div>
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {!detectedShape ? (
          <div className="text-center">
            <div className="mb-8">
              <span className="text-8xl">👗</span>
            </div>
            <div className="bg-gradient-to-r from-pink-500 to-pink-600 py-6 px-8 rounded-2xl mb-8 shadow-lg">
              <h2 className="text-4xl font-bold text-white mb-2">
                Find Your Perfect Style
              </h2>
            </div>
            <p className="text-xl text-gray-600 mb-8">
              Discover clothing recommendations tailored to your body shape
            </p>
            <button
              onClick={() => setShowAnalyzer(true)}
              className="bg-gradient-to-r from-pink-500 to-pink-600 text-white px-12 py-4 rounded-lg text-lg font-semibold hover:shadow-xl transition-all transform hover:scale-105"
            >
              Start Style Analysis
            </button>

            {/* Features */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-16">
              <div className="bg-white p-6 rounded-xl shadow-md border-2 border-pink-200">
                <div className="text-4xl mb-4">📸</div>
                <h3 className="font-bold text-pink-600 mb-2">Upload Photo</h3>
                <p className="text-sm text-gray-600">
                  Upload your photo for instant analysis
                </p>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-md border-2 border-pink-200">
                <div className="text-4xl mb-4">📝</div>
                <h3 className="font-bold text-pink-600 mb-2">Quick Quiz</h3>
                <p className="text-sm text-gray-600">
                  Answer simple questions about your body
                </p>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-md border-2 border-pink-200">
                <div className="text-4xl mb-4">✨</div>
                <h3 className="font-bold text-pink-600 mb-2">Get Recommendations</h3>
                <p className="text-sm text-gray-600">
                  Receive personalized style suggestions
                </p>
              </div>
            </div>
          </div>
        ) : (
          <div className="space-y-8">
            {/* Result Header */}
            <div className="bg-white rounded-2xl p-8 shadow-lg text-center border-2 border-pink-200">
              <h2 className="text-3xl font-bold text-pink-600 mb-4">
                {bodyShapeInfo[detectedShape].title}
              </h2>
              <p className="text-gray-600 text-lg">
                {bodyShapeInfo[detectedShape].description}
              </p>
              <button
                onClick={() => setDetectedShape(null)}
                className="mt-6 text-pink-600 hover:text-pink-700 font-semibold underline"
              >
                Try Again
              </button>
            </div>

            {/* Recommendations */}
            <div className="bg-white rounded-2xl p-8 shadow-lg border-2 border-pink-200">
              <h3 className="text-2xl font-bold text-pink-600 mb-6">
                ✨ Recommended Styles for You
              </h3>
              <ul className="space-y-3">
                {bodyShapeInfo[detectedShape].recommendations.map((rec, idx) => (
                  <li key={idx} className="flex items-start gap-3">
                    <span className="text-pink-500 text-xl">✓</span>
                    <span className="text-gray-700">{rec}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* What to Avoid */}
            <div className="bg-white rounded-2xl p-8 shadow-lg border-2 border-pink-200">
              <h3 className="text-2xl font-bold text-pink-600 mb-6">
                ⚠️ Styles to Avoid
              </h3>
              <ul className="space-y-3">
                {bodyShapeInfo[detectedShape].avoid.map((item, idx) => (
                  <li key={idx} className="flex items-start gap-3">
                    <span className="text-red-400 text-xl">✗</span>
                    <span className="text-gray-700">{item}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Shop Categories */}
            <div className="bg-gradient-to-r from-pink-500 to-pink-600 rounded-2xl p-8 shadow-lg text-white text-center">
              <h3 className="text-2xl font-bold mb-4">
                Shop Recommended Categories
              </h3>
              <div className="flex flex-wrap justify-center gap-4 mt-6">
                {bodyShapeInfo[detectedShape].categories.map((cat) => (
                  <Link
                    key={cat}
                    href="/home"
                    className="bg-white text-pink-600 px-6 py-3 rounded-lg font-semibold hover:shadow-xl transition-all"
                  >
                    {cat}
                  </Link>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>

      {showAnalyzer && (
        <BodyShapeAnalyzer
          onShapeDetected={handleShapeDetected}
          onClose={() => setShowAnalyzer(false)}
        />
      )}
    </div>
  );
}
