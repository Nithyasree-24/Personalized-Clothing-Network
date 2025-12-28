"use client";

import { useState } from "react";

type BodyShape = "hourglass" | "pear" | "apple" | "rectangle" | "inverted-triangle" | null;

interface BodyShapeAnalyzerProps {
  onShapeDetected: (shape: BodyShape) => void;
  onClose: () => void;
}

export default function BodyShapeAnalyzer({ onShapeDetected, onClose }: BodyShapeAnalyzerProps) {
  const [step, setStep] = useState<"upload" | "quiz">("upload");
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [analyzing, setAnalyzing] = useState(false);
  
  // Quiz answers
  const [shoulders, setShoulders] = useState<string>("");
  const [waist, setWaist] = useState<string>("");
  const [hips, setHips] = useState<string>("");

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setSelectedImage(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const analyzeImage = () => {
    setAnalyzing(true);
    // Simulate analysis
    setTimeout(() => {
      setAnalyzing(false);
      setStep("quiz");
    }, 2000);
  };

  const calculateBodyShape = (): BodyShape => {
    // Simple logic based on quiz answers
    if (shoulders === "narrow" && waist === "defined" && hips === "wide") {
      return "pear";
    } else if (shoulders === "wide" && waist === "defined" && hips === "narrow") {
      return "inverted-triangle";
    } else if (shoulders === "balanced" && waist === "defined" && hips === "balanced") {
      return "hourglass";
    } else if (shoulders === "wide" && waist === "undefined" && hips === "narrow") {
      return "apple";
    } else {
      return "rectangle";
    }
  };

  const handleSubmitQuiz = () => {
    const shape = calculateBodyShape();
    onShapeDetected(shape);
  };

  const bodyShapeRecommendations = {
    hourglass: {
      title: "Hourglass Shape",
      description: "Balanced proportions with defined waist",
      recommendations: ["Wrap dresses", "Fitted tops", "High-waisted bottoms", "Belted outfits"],
      icon: "⏳"
    },
    pear: {
      title: "Pear Shape",
      description: "Narrower shoulders, wider hips",
      recommendations: ["A-line dresses", "Boat neck tops", "Dark colored bottoms", "Statement tops"],
      icon: "🍐"
    },
    apple: {
      title: "Apple Shape",
      description: "Broader shoulders, undefined waist",
      recommendations: ["Empire waist dresses", "V-neck tops", "Straight leg pants", "Flowy tops"],
      icon: "🍎"
    },
    rectangle: {
      title: "Rectangle Shape",
      description: "Balanced proportions, less defined waist",
      recommendations: ["Peplum tops", "Belted dresses", "Layered outfits", "Ruffled details"],
      icon: "📏"
    },
    "inverted-triangle": {
      title: "Inverted Triangle",
      description: "Broader shoulders, narrower hips",
      recommendations: ["A-line skirts", "Wide leg pants", "V-neck tops", "Dark colored tops"],
      icon: "🔺"
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-gradient-to-r from-[#8B6F47] to-[#D4A574] p-6 text-white">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold">Body Shape Analyzer</h2>
              <p className="text-sm text-white/80">Find your perfect fit</p>
            </div>
            <button
              onClick={onClose}
              className="text-white hover:text-white/80 text-2xl"
            >
              ✕
            </button>
          </div>
        </div>

        <div className="p-6">
          {step === "upload" && (
            <div className="space-y-6">
              <div className="text-center">
                <div className="mb-4">
                  <span className="text-6xl">📸</span>
                </div>
                <h3 className="text-xl font-bold text-gray-800 mb-2">Upload Your Photo</h3>
                <p className="text-gray-600 mb-6">
                  Upload a full-body photo to help us recommend the best styles for you
                </p>
              </div>

              {/* Image Upload */}
              <div className="border-2 border-dashed border-[#D4A574] rounded-xl p-8 text-center">
                {selectedImage ? (
                  <div className="space-y-4">
                    <img
                      src={selectedImage}
                      alt="Uploaded"
                      className="max-h-64 mx-auto rounded-lg"
                    />
                    <button
                      onClick={analyzeImage}
                      disabled={analyzing}
                      className="bg-gradient-to-r from-[#8B6F47] to-[#D4A574] text-white px-8 py-3 rounded-lg font-semibold hover:shadow-lg transition-all disabled:opacity-50"
                    >
                      {analyzing ? "Analyzing..." : "Analyze Photo"}
                    </button>
                  </div>
                ) : (
                  <label className="cursor-pointer">
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleImageUpload}
                      className="hidden"
                    />
                    <div className="space-y-2">
                      <div className="text-4xl">📤</div>
                      <div className="text-[#8B6F47] font-semibold">Click to upload</div>
                      <div className="text-sm text-gray-500">PNG, JPG up to 10MB</div>
                    </div>
                  </label>
                )}
              </div>

              <div className="text-center">
                <div className="text-gray-500 mb-4">OR</div>
                <button
                  onClick={() => setStep("quiz")}
                  className="text-[#8B6F47] font-semibold hover:text-[#7A5F3A] underline"
                >
                  Take a quick quiz instead →
                </button>
              </div>
            </div>
          )}

          {step === "quiz" && (
            <div className="space-y-6">
              <div className="text-center mb-6">
                <h3 className="text-xl font-bold text-gray-800 mb-2">Body Shape Quiz</h3>
                <p className="text-gray-600">Answer a few questions to find your body shape</p>
              </div>

              {/* Question 1 */}
              <div>
                <label className="block text-sm font-semibold text-gray-800 mb-3">
                  1. How would you describe your shoulders?
                </label>
                <div className="grid grid-cols-1 gap-3">
                  {["narrow", "balanced", "wide"].map((option) => (
                    <button
                      key={option}
                      onClick={() => setShoulders(option)}
                      className={`p-4 rounded-lg border-2 text-left transition-all ${
                        shoulders === option
                          ? "border-[#8B6F47] bg-[#f5f1e8]"
                          : "border-gray-200 hover:border-[#D4A574]"
                      }`}
                    >
                      <span className="font-medium capitalize">{option}</span>
                    </button>
                  ))}
                </div>
              </div>

              {/* Question 2 */}
              <div>
                <label className="block text-sm font-semibold text-gray-800 mb-3">
                  2. How defined is your waist?
                </label>
                <div className="grid grid-cols-1 gap-3">
                  {["defined", "somewhat-defined", "undefined"].map((option) => (
                    <button
                      key={option}
                      onClick={() => setWaist(option)}
                      className={`p-4 rounded-lg border-2 text-left transition-all ${
                        waist === option
                          ? "border-[#8B6F47] bg-[#f5f1e8]"
                          : "border-gray-200 hover:border-[#D4A574]"
                      }`}
                    >
                      <span className="font-medium capitalize">{option.replace("-", " ")}</span>
                    </button>
                  ))}
                </div>
              </div>

              {/* Question 3 */}
              <div>
                <label className="block text-sm font-semibold text-gray-800 mb-3">
                  3. How would you describe your hips?
                </label>
                <div className="grid grid-cols-1 gap-3">
                  {["narrow", "balanced", "wide"].map((option) => (
                    <button
                      key={option}
                      onClick={() => setHips(option)}
                      className={`p-4 rounded-lg border-2 text-left transition-all ${
                        hips === option
                          ? "border-[#8B6F47] bg-[#f5f1e8]"
                          : "border-gray-200 hover:border-[#D4A574]"
                      }`}
                    >
                      <span className="font-medium capitalize">{option}</span>
                    </button>
                  ))}
                </div>
              </div>

              {/* Submit Button */}
              <button
                onClick={handleSubmitQuiz}
                disabled={!shoulders || !waist || !hips}
                className="w-full bg-gradient-to-r from-[#8B6F47] to-[#D4A574] text-white py-4 rounded-lg font-semibold hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Get My Recommendations
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
