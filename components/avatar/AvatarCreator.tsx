"use client";

import { useState } from "react";
import { BaseAvatar, AgeGroup, Gender } from "../../types/avatar";
import AvatarCanvas from "./AvatarCanvas";

type AvatarCreatorProps = {
  ageGroup: AgeGroup;
  gender: Gender;
  onComplete: (avatar: BaseAvatar) => void;
  onBack: () => void;
};

export default function AvatarCreator({ ageGroup, gender, onComplete, onBack }: AvatarCreatorProps) {
  const [avatar, setAvatar] = useState<BaseAvatar>({
    id: `avatar-${Date.now()}`,
    ageGroup,
    gender,
    faceStyle: "oval",
    skinTone: "#FFE0BD",
    hairStyle: "short",
    hairColor: "#4A2511",
    bodyType: "average",
    eyeStyle: "normal",
    eyeColor: "#4A2511",
  });

  const skinTones = [
    { id: "light", color: "#FFE0BD", name: "Light" },
    { id: "medium", color: "#D4A574", name: "Medium" },
    { id: "tan", color: "#C68642", name: "Tan" },
    { id: "dark", color: "#8D5524", name: "Dark" },
    { id: "deep", color: "#5C3317", name: "Deep" },
  ];

  const hairColors = [
    { id: "black", color: "#000000", name: "Black" },
    { id: "brown", color: "#4A2511", name: "Brown" },
    { id: "blonde", color: "#F5D76E", name: "Blonde" },
    { id: "red", color: "#C93305", name: "Red" },
    { id: "gray", color: "#808080", name: "Gray" },
  ];

  const hairStyles = gender === "female"
    ? [
        { id: "long", name: "Long", icon: "💁‍♀️" },
        { id: "short", name: "Short", icon: "👩" },
        { id: "curly", name: "Curly", icon: "👩‍🦱" },
        { id: "wavy", name: "Wavy", icon: "🌊" },
        { id: "ponytail", name: "Ponytail", icon: "🎀" },
        { id: "bun", name: "Bun", icon: "🍩" },
      ]
    : [
        { id: "short", name: "Short", icon: "👨" },
        { id: "medium", name: "Medium", icon: "👨‍🦰" },
        { id: "curly", name: "Curly", icon: "👨‍🦱" },
        { id: "bald", name: "Bald", icon: "👨‍🦲" },
        { id: "fade", name: "Fade", icon: "✂️" },
        { id: "spiky", name: "Spiky", icon: "⚡" },
      ];

  const faceStyles = [
    { id: "oval", name: "Oval", icon: "⭕" },
    { id: "round", name: "Round", icon: "🔴" },
    { id: "square", name: "Square", icon: "🟦" },
    { id: "long", name: "Long", icon: "📏" },
  ];

  const bodyTypes = [
    { id: "slim", name: "Slim", icon: "🌿" },
    { id: "average", name: "Average", icon: "👤" },
    { id: "athletic", name: "Athletic", icon: "💪" },
  ];

  return (
    <div className="max-w-6xl mx-auto">
      <button onClick={onBack} className="mb-6 text-pink-600 hover:text-pink-700 font-semibold flex items-center gap-2">
        <span>←</span>
        <span>Back to Selection</span>
      </button>

      <div className="bg-white rounded-2xl shadow-xl p-8">
        <h2 className="text-3xl font-bold text-pink-600 mb-2 text-center">
          Step 1: Create Your Base Avatar
        </h2>
        <p className="text-gray-600 text-center mb-8">
          Customize your avatar's appearance
        </p>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Avatar Preview */}
          <div className="bg-gradient-to-br from-pink-100 to-purple-100 rounded-xl p-8 flex items-center justify-center">
            <AvatarCanvas avatar={avatar} appliedStickers={[]} size={350} />
          </div>

          {/* Customization Options */}
          <div className="space-y-6 max-h-[600px] overflow-y-auto pr-4">
            {/* Skin Tone */}
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-3">Skin Tone</label>
              <div className="grid grid-cols-5 gap-2">
                {skinTones.map((tone) => (
                  <button
                    key={tone.id}
                    onClick={() => setAvatar({...avatar, skinTone: tone.color})}
                    className={`p-3 rounded-lg border-2 transition-all ${
                      avatar.skinTone === tone.color ? "border-pink-500 scale-110 shadow-lg" : "border-gray-200 hover:border-pink-300"
                    }`}
                  >
                    <div className="w-full h-10 rounded-lg mb-1" style={{ backgroundColor: tone.color }}></div>
                    <p className="text-xs font-semibold">{tone.name}</p>
                  </button>
                ))}
              </div>
            </div>

            {/* Hair Style */}
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-3">Hair Style</label>
              <div className="grid grid-cols-3 gap-3">
                {hairStyles.map((style) => (
                  <button
                    key={style.id}
                    onClick={() => setAvatar({...avatar, hairStyle: style.id})}
                    className={`p-3 rounded-lg border-2 transition-all ${
                      avatar.hairStyle === style.id ? "border-pink-500 bg-pink-50 scale-105" : "border-gray-200 hover:border-pink-300"
                    }`}
                  >
                    <div className="text-3xl mb-1">{style.icon}</div>
                    <div className="text-xs font-semibold">{style.name}</div>
                  </button>
                ))}
              </div>
            </div>

            {/* Hair Color */}
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-3">Hair Color</label>
              <div className="grid grid-cols-5 gap-2">
                {hairColors.map((color) => (
                  <button
                    key={color.id}
                    onClick={() => setAvatar({...avatar, hairColor: color.color})}
                    className={`p-2 rounded-lg border-2 transition-all ${
                      avatar.hairColor === color.color ? "border-pink-500 scale-110 shadow-lg" : "border-gray-200 hover:border-pink-300"
                    }`}
                  >
                    <div className="w-full h-10 rounded-lg mb-1" style={{ backgroundColor: color.color }}></div>
                    <p className="text-xs font-semibold">{color.name}</p>
                  </button>
                ))}
              </div>
            </div>

            {/* Face Style */}
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-3">Face Shape</label>
              <div className="grid grid-cols-4 gap-2">
                {faceStyles.map((style) => (
                  <button
                    key={style.id}
                    onClick={() => setAvatar({...avatar, faceStyle: style.id})}
                    className={`p-3 rounded-lg border-2 transition-all ${
                      avatar.faceStyle === style.id ? "border-pink-500 bg-pink-50 scale-105" : "border-gray-200 hover:border-pink-300"
                    }`}
                  >
                    <div className="text-2xl mb-1">{style.icon}</div>
                    <div className="text-xs font-semibold">{style.name}</div>
                  </button>
                ))}
              </div>
            </div>

            {/* Body Type */}
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-3">Body Type</label>
              <div className="grid grid-cols-3 gap-3">
                {bodyTypes.map((type) => (
                  <button
                    key={type.id}
                    onClick={() => setAvatar({...avatar, bodyType: type.id})}
                    className={`p-3 rounded-lg border-2 transition-all ${
                      avatar.bodyType === type.id ? "border-pink-500 bg-pink-50 scale-105" : "border-gray-200 hover:border-pink-300"
                    }`}
                  >
                    <div className="text-3xl mb-1">{type.icon}</div>
                    <div className="text-xs font-semibold">{type.name}</div>
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Continue Button */}
        <div className="mt-8 text-center">
          <button
            onClick={() => onComplete(avatar)}
            className="bg-gradient-to-r from-pink-500 to-pink-600 text-white px-12 py-4 rounded-lg text-lg font-semibold hover:shadow-xl transition-all transform hover:scale-105"
          >
            Continue to Clothing Library →
          </button>
        </div>
      </div>
    </div>
  );
}
