"use client";

import { useState } from "react";

type AvatarCreatorProps = {
  gender: "women" | "men" | "kids";
  onComplete: (avatarData: any) => void;
  onBack: () => void;
};

export default function AvatarCreator({ gender, onComplete, onBack }: AvatarCreatorProps) {
  const [skinTone, setSkinTone] = useState("light");
  const [hairStyle, setHairStyle] = useState("short");
  const [hairColor, setHairColor] = useState("brown");
  const [faceShape, setFaceShape] = useState("oval");
  const [eyeStyle, setEyeStyle] = useState("normal");
  const [bodyType, setBodyType] = useState("average");

  const skinTones = [
    { id: "light", name: "Light", color: "#FFE0BD" },
    { id: "medium", name: "Medium", color: "#D4A574" },
    { id: "tan", name: "Tan", color: "#C68642" },
    { id: "dark", name: "Dark", color: "#8D5524" },
  ];

  const hairStyles = gender === "women" 
    ? [
        { id: "long", name: "Long", emoji: "👱‍♀️" },
        { id: "short", name: "Short", emoji: "👩" },
        { id: "curly", name: "Curly", emoji: "👩‍🦱" },
        { id: "wavy", name: "Wavy", emoji: "👱‍♀️" },
      ]
    : gender === "men"
    ? [
        { id: "short", name: "Short", emoji: "👨" },
        { id: "medium", name: "Medium", emoji: "👨‍🦰" },
        { id: "curly", name: "Curly", emoji: "👨‍🦱" },
        { id: "bald", name: "Bald", emoji: "👨‍🦲" },
      ]
    : [
        { id: "short", name: "Short", emoji: "👧" },
        { id: "pigtails", name: "Pigtails", emoji: "👧" },
        { id: "curly", name: "Curly", emoji: "🧒" },
        { id: "bob", name: "Bob", emoji: "👧" },
      ];

  const hairColors = [
    { id: "black", name: "Black", color: "#000000" },
    { id: "brown", name: "Brown", color: "#4A2511" },
    { id: "blonde", name: "Blonde", color: "#F5D76E" },
    { id: "red", name: "Red", color: "#C93305" },
    { id: "gray", name: "Gray", color: "#808080" },
  ];

  const handleComplete = () => {
    const avatarData = {
      gender,
      skinTone,
      hairStyle,
      hairColor,
      faceShape,
      eyeStyle,
      bodyType,
    };
    onComplete(avatarData);
  };

  return (
    <div className="max-w-5xl mx-auto">
      <button
        onClick={onBack}
        className="mb-6 text-pink-600 hover:text-pink-700 font-semibold"
      >
        ← Back to Gender Selection
      </button>

      <div className="bg-white rounded-2xl shadow-xl p-8">
        <h2 className="text-3xl font-bold text-pink-600 mb-6 text-center">
          Customize Your {gender === "women" ? "Female" : gender === "men" ? "Male" : "Kids"} Avatar
        </h2>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Avatar Preview */}
          <div className="bg-gradient-to-br from-pink-100 to-purple-100 rounded-xl p-8 flex items-center justify-center">
            <div className="text-center">
              <div className="text-9xl mb-4">
                {gender === "women" ? "👩" : gender === "men" ? "👨" : "👧"}
              </div>
              <p className="text-gray-600 font-semibold">Avatar Preview</p>
              <div className="mt-4 space-y-2 text-sm text-gray-600">
                <p>Skin: {skinTone}</p>
                <p>Hair: {hairStyle} ({hairColor})</p>
                <p>Body: {bodyType}</p>
              </div>
            </div>
          </div>

          {/* Customization Options */}
          <div className="space-y-6">
            {/* Skin Tone */}
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-3">
                Skin Tone
              </label>
              <div className="grid grid-cols-4 gap-3">
                {skinTones.map((tone) => (
                  <button
                    key={tone.id}
                    onClick={() => setSkinTone(tone.id)}
                    className={`p-4 rounded-lg border-2 transition-all ${
                      skinTone === tone.id
                        ? "border-pink-500 shadow-lg scale-105"
                        : "border-gray-200 hover:border-pink-300"
                    }`}
                  >
                    <div
                      className="w-full h-12 rounded-lg mb-2"
                      style={{ backgroundColor: tone.color }}
                    ></div>
                    <p className="text-xs font-semibold text-gray-700">{tone.name}</p>
                  </button>
                ))}
              </div>
            </div>

            {/* Hair Style */}
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-3">
                Hair Style
              </label>
              <div className="grid grid-cols-4 gap-3">
                {hairStyles.map((style) => (
                  <button
                    key={style.id}
                    onClick={() => setHairStyle(style.id)}
                    className={`p-4 rounded-lg border-2 transition-all ${
                      hairStyle === style.id
                        ? "border-pink-500 shadow-lg scale-105"
                        : "border-gray-200 hover:border-pink-300"
                    }`}
                  >
                    <div className="text-3xl mb-2">{style.emoji}</div>
                    <p className="text-xs font-semibold text-gray-700">{style.name}</p>
                  </button>
                ))}
              </div>
            </div>

            {/* Hair Color */}
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-3">
                Hair Color
              </label>
              <div className="grid grid-cols-5 gap-3">
                {hairColors.map((color) => (
                  <button
                    key={color.id}
                    onClick={() => setHairColor(color.id)}
                    className={`p-3 rounded-lg border-2 transition-all ${
                      hairColor === color.id
                        ? "border-pink-500 shadow-lg scale-105"
                        : "border-gray-200 hover:border-pink-300"
                    }`}
                  >
                    <div
                      className="w-full h-10 rounded-lg mb-2"
                      style={{ backgroundColor: color.color }}
                    ></div>
                    <p className="text-xs font-semibold text-gray-700">{color.name}</p>
                  </button>
                ))}
              </div>
            </div>

            {/* Body Type */}
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-3">
                Body Type
              </label>
              <div className="grid grid-cols-3 gap-3">
                {["slim", "average", "athletic"].map((type) => (
                  <button
                    key={type}
                    onClick={() => setBodyType(type)}
                    className={`p-4 rounded-lg border-2 transition-all ${
                      bodyType === type
                        ? "border-pink-500 bg-pink-50 shadow-lg"
                        : "border-gray-200 hover:border-pink-300"
                    }`}
                  >
                    <p className="text-sm font-semibold text-gray-700 capitalize">{type}</p>
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Complete Button */}
        <div className="mt-8 text-center">
          <button
            onClick={handleComplete}
            className="bg-gradient-to-r from-pink-500 to-pink-600 text-white px-12 py-4 rounded-lg text-lg font-semibold hover:shadow-xl transition-all transform hover:scale-105"
          >
            Continue to Dress Up →
          </button>
        </div>
      </div>
    </div>
  );
}
