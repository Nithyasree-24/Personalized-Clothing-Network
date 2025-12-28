"use client";

import { useState } from "react";

type AvatarConfig = {
  gender: "women" | "men" | "kids";
  skinTone: string;
  hairStyle: string;
  hairColor: string;
  eyeStyle: string;
  eyeColor: string;
  noseStyle: string;
  mouthStyle: string;
  faceShape: string;
  bodyType: string;
  outfit: string;
};

type AvatarBuilderProps = {
  gender: "women" | "men" | "kids";
  onComplete: (config: AvatarConfig) => void;
  onBack: () => void;
};

export default function AvatarBuilder({ gender, onComplete, onBack }: AvatarBuilderProps) {
  const [config, setConfig] = useState<AvatarConfig>({
    gender,
    skinTone: "#FFE0BD",
    hairStyle: "short",
    hairColor: "#4A2511",
    eyeStyle: "normal",
    eyeColor: "#4A2511",
    noseStyle: "normal",
    mouthStyle: "smile",
    faceShape: "oval",
    bodyType: "average",
    outfit: "casual",
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
    { id: "blue", color: "#0066CC", name: "Blue" },
    { id: "pink", color: "#FF69B4", name: "Pink" },
  ];

  const eyeColors = [
    { id: "brown", color: "#4A2511", name: "Brown" },
    { id: "blue", color: "#4A90E2", name: "Blue" },
    { id: "green", color: "#50C878", name: "Green" },
    { id: "hazel", color: "#8E7618", name: "Hazel" },
    { id: "gray", color: "#708090", name: "Gray" },
  ];

  const hairStyles = gender === "women"
    ? [
        { id: "long", name: "Long", icon: "💁‍♀️" },
        { id: "short", name: "Short", icon: "👩" },
        { id: "curly", name: "Curly", icon: "👩‍🦱" },
        { id: "wavy", name: "Wavy", icon: "🌊" },
        { id: "ponytail", name: "Ponytail", icon: "🎀" },
        { id: "bun", name: "Bun", icon: "🍩" },
      ]
    : gender === "men"
    ? [
        { id: "short", name: "Short", icon: "👨" },
        { id: "medium", name: "Medium", icon: "👨‍🦰" },
        { id: "curly", name: "Curly", icon: "👨‍🦱" },
        { id: "bald", name: "Bald", icon: "👨‍🦲" },
        { id: "fade", name: "Fade", icon: "✂️" },
        { id: "spiky", name: "Spiky", icon: "⚡" },
      ]
    : [
        { id: "short", name: "Short", icon: "👧" },
        { id: "pigtails", name: "Pigtails", icon: "🎀" },
        { id: "curly", name: "Curly", icon: "🧒" },
        { id: "bob", name: "Bob", icon: "💇" },
        { id: "bangs", name: "Bangs", icon: "✨" },
        { id: "messy", name: "Messy", icon: "🌪️" },
      ];

  const eyeStyles = [
    { id: "normal", name: "Normal", icon: "👁️" },
    { id: "wide", name: "Wide", icon: "😳" },
    { id: "narrow", name: "Narrow", icon: "😑" },
    { id: "round", name: "Round", icon: "😊" },
    { id: "almond", name: "Almond", icon: "😌" },
  ];
  
  const noseStyles = [
    { id: "normal", name: "Normal", icon: "👃" },
    { id: "small", name: "Small", icon: "🔹" },
    { id: "large", name: "Large", icon: "🔸" },
    { id: "button", name: "Button", icon: "⚪" },
    { id: "pointed", name: "Pointed", icon: "🔺" },
  ];
  
  const mouthStyles = [
    { id: "smile", name: "Smile", icon: "😊" },
    { id: "neutral", name: "Neutral", icon: "😐" },
    { id: "grin", name: "Grin", icon: "😁" },
    { id: "smirk", name: "Smirk", icon: "😏" },
    { id: "laugh", name: "Laugh", icon: "😄" },
  ];
  
  const faceShapes = [
    { id: "oval", name: "Oval", icon: "⭕" },
    { id: "round", name: "Round", icon: "🔴" },
    { id: "square", name: "Square", icon: "🟦" },
    { id: "heart", name: "Heart", icon: "💗" },
    { id: "long", name: "Long", icon: "📏" },
  ];
  
  const bodyTypes = [
    { id: "slim", name: "Slim", icon: "🌿" },
    { id: "average", name: "Average", icon: "👤" },
    { id: "athletic", name: "Athletic", icon: "💪" },
    { id: "curvy", name: "Curvy", icon: "🌊" },
  ];

  return (
    <div className="max-w-6xl mx-auto">
      <button onClick={onBack} className="mb-6 text-pink-600 hover:text-pink-700 font-semibold">
        ← Back to Gender Selection
      </button>

      <div className="bg-white rounded-2xl shadow-xl p-8">
        <h2 className="text-3xl font-bold text-pink-600 mb-6 text-center">
          Build Your Avatar
        </h2>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Avatar Preview */}
          <div className="bg-gradient-to-br from-pink-100 to-purple-100 rounded-xl p-8">
            <div className="flex items-center justify-center">
              <svg width="300" height="400" viewBox="0 0 300 400" className="drop-shadow-lg">
                {/* Body */}
                <ellipse cx="150" cy="350" rx="60" ry="40" fill={config.skinTone} opacity="0.9" />
                <rect x="90" y="250" width="120" height="120" rx="20" fill="#E8E8E8" />
                
                {/* Neck */}
                <rect x="130" y="200" width="40" height="50" fill={config.skinTone} />
                
                {/* Head - Face Shape */}
                <ellipse 
                  cx="150" 
                  cy="150" 
                  rx={config.faceShape === "round" ? "70" : config.faceShape === "square" ? "65" : config.faceShape === "long" ? "60" : "65"} 
                  ry={config.faceShape === "round" ? "70" : config.faceShape === "long" ? "80" : "75"} 
                  fill={config.skinTone} 
                />
                
                {/* Hair */}
                {config.hairStyle === "long" && (
                  <>
                    <ellipse cx="150" cy="100" rx="75" ry="50" fill={config.hairColor} />
                    <rect x="75" y="100" width="150" height="120" fill={config.hairColor} rx="40" />
                  </>
                )}
                {config.hairStyle === "short" && (
                  <ellipse cx="150" cy="100" rx="70" ry="45" fill={config.hairColor} />
                )}
                {config.hairStyle === "curly" && (
                  <>
                    <circle cx="120" cy="100" r="25" fill={config.hairColor} />
                    <circle cx="150" cy="90" r="30" fill={config.hairColor} />
                    <circle cx="180" cy="100" r="25" fill={config.hairColor} />
                    <circle cx="110" cy="130" r="20" fill={config.hairColor} />
                    <circle cx="190" cy="130" r="20" fill={config.hairColor} />
                  </>
                )}
                {config.hairStyle === "ponytail" && (
                  <>
                    <ellipse cx="150" cy="100" rx="70" ry="40" fill={config.hairColor} />
                    <ellipse cx="200" cy="140" rx="20" ry="50" fill={config.hairColor} />
                  </>
                )}
                {config.hairStyle === "bun" && (
                  <>
                    <ellipse cx="150" cy="100" rx="70" ry="35" fill={config.hairColor} />
                    <circle cx="150" cy="80" r="25" fill={config.hairColor} />
                  </>
                )}
                {config.hairStyle === "bald" && (
                  <ellipse cx="150" cy="110" rx="70" ry="30" fill={config.skinTone} />
                )}
                
                {/* Eyes */}
                <ellipse cx="125" cy="145" rx="12" ry={config.eyeStyle === "wide" ? "15" : "10"} fill="white" />
                <ellipse cx="175" cy="145" rx="12" ry={config.eyeStyle === "wide" ? "15" : "10"} fill="white" />
                <circle cx="125" cy="145" r="6" fill={config.eyeColor} />
                <circle cx="175" cy="145" r="6" fill={config.eyeColor} />
                <circle cx="127" cy="143" r="2" fill="white" />
                <circle cx="177" cy="143" r="2" fill="white" />
                
                {/* Eyebrows */}
                <path d="M 110 135 Q 125 130 140 135" stroke={config.hairColor} strokeWidth="3" fill="none" strokeLinecap="round" />
                <path d="M 160 135 Q 175 130 190 135" stroke={config.hairColor} strokeWidth="3" fill="none" strokeLinecap="round" />
                
                {/* Nose */}
                <ellipse cx="150" cy="160" rx={config.noseStyle === "small" ? "6" : "8"} ry={config.noseStyle === "large" ? "12" : "10"} fill={config.skinTone} opacity="0.6" />
                <path d="M 145 165 L 145 170" stroke={config.skinTone} strokeWidth="2" opacity="0.4" />
                <path d="M 155 165 L 155 170" stroke={config.skinTone} strokeWidth="2" opacity="0.4" />
                
                {/* Mouth */}
                {config.mouthStyle === "smile" && (
                  <path d="M 130 180 Q 150 190 170 180" stroke="#C93305" strokeWidth="3" fill="none" strokeLinecap="round" />
                )}
                {config.mouthStyle === "grin" && (
                  <>
                    <path d="M 130 180 Q 150 195 170 180" stroke="#C93305" strokeWidth="3" fill="none" strokeLinecap="round" />
                    <rect x="140" y="185" width="20" height="8" fill="white" rx="2" />
                  </>
                )}
                {config.mouthStyle === "neutral" && (
                  <line x1="135" y1="180" x2="165" y2="180" stroke="#C93305" strokeWidth="2" strokeLinecap="round" />
                )}
                
                {/* Blush */}
                <ellipse cx="110" cy="160" rx="15" ry="10" fill="#FFB6C1" opacity="0.4" />
                <ellipse cx="190" cy="160" rx="15" ry="10" fill="#FFB6C1" opacity="0.4" />
              </svg>
            </div>
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
                    onClick={() => setConfig({...config, skinTone: tone.color})}
                    className={`p-3 rounded-lg border-2 transition-all ${
                      config.skinTone === tone.color ? "border-pink-500 scale-110" : "border-gray-200"
                    }`}
                  >
                    <div className="w-full h-8 rounded" style={{ backgroundColor: tone.color }}></div>
                    <p className="text-xs mt-1">{tone.name}</p>
                  </button>
                ))}
              </div>
            </div>

            {/* Hair Style */}
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-3">Hair Style</label>
              <div className="grid grid-cols-3 gap-2">
                {hairStyles.map((style) => (
                  <button
                    key={style.id}
                    onClick={() => setConfig({...config, hairStyle: style.id})}
                    className={`p-3 rounded-lg border-2 transition-all ${
                      config.hairStyle === style.id ? "border-pink-500 bg-pink-50 scale-105" : "border-gray-200 hover:border-pink-300"
                    }`}
                  >
                    <div className="text-2xl mb-1">{style.icon}</div>
                    <div className="text-xs font-semibold">{style.name}</div>
                  </button>
                ))}
              </div>
            </div>

            {/* Hair Color */}
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-3">Hair Color</label>
              <div className="grid grid-cols-7 gap-2">
                {hairColors.map((color) => (
                  <button
                    key={color.id}
                    onClick={() => setConfig({...config, hairColor: color.color})}
                    className={`p-2 rounded-lg border-2 transition-all ${
                      config.hairColor === color.color ? "border-pink-500 scale-110" : "border-gray-200"
                    }`}
                  >
                    <div className="w-full h-8 rounded" style={{ backgroundColor: color.color }}></div>
                  </button>
                ))}
              </div>
            </div>

            {/* Eye Style */}
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-3">Eye Style</label>
              <div className="grid grid-cols-5 gap-2">
                {eyeStyles.map((style) => (
                  <button
                    key={style.id}
                    onClick={() => setConfig({...config, eyeStyle: style.id})}
                    className={`p-2 rounded-lg border-2 transition-all ${
                      config.eyeStyle === style.id ? "border-pink-500 bg-pink-50 scale-105" : "border-gray-200 hover:border-pink-300"
                    }`}
                  >
                    <div className="text-xl mb-1">{style.icon}</div>
                    <div className="text-xs font-semibold">{style.name}</div>
                  </button>
                ))}
              </div>
            </div>

            {/* Eye Color */}
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-3">Eye Color</label>
              <div className="grid grid-cols-5 gap-2">
                {eyeColors.map((color) => (
                  <button
                    key={color.id}
                    onClick={() => setConfig({...config, eyeColor: color.color})}
                    className={`p-2 rounded-lg border-2 transition-all ${
                      config.eyeColor === color.color ? "border-pink-500 scale-110" : "border-gray-200"
                    }`}
                  >
                    <div className="w-full h-8 rounded-full" style={{ backgroundColor: color.color }}></div>
                    <p className="text-xs mt-1">{color.name}</p>
                  </button>
                ))}
              </div>
            </div>

            {/* Nose Style */}
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-3">Nose Style</label>
              <div className="grid grid-cols-5 gap-2">
                {noseStyles.map((style) => (
                  <button
                    key={style.id}
                    onClick={() => setConfig({...config, noseStyle: style.id})}
                    className={`p-2 rounded-lg border-2 transition-all ${
                      config.noseStyle === style.id ? "border-pink-500 bg-pink-50 scale-105" : "border-gray-200 hover:border-pink-300"
                    }`}
                  >
                    <div className="text-xl mb-1">{style.icon}</div>
                    <div className="text-xs font-semibold">{style.name}</div>
                  </button>
                ))}
              </div>
            </div>

            {/* Mouth Style */}
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-3">Mouth Style</label>
              <div className="grid grid-cols-5 gap-2">
                {mouthStyles.map((style) => (
                  <button
                    key={style.id}
                    onClick={() => setConfig({...config, mouthStyle: style.id})}
                    className={`p-2 rounded-lg border-2 transition-all ${
                      config.mouthStyle === style.id ? "border-pink-500 bg-pink-50 scale-105" : "border-gray-200 hover:border-pink-300"
                    }`}
                  >
                    <div className="text-2xl mb-1">{style.icon}</div>
                    <div className="text-xs font-semibold">{style.name}</div>
                  </button>
                ))}
              </div>
            </div>

            {/* Face Shape */}
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-3">Face Shape</label>
              <div className="grid grid-cols-5 gap-2">
                {faceShapes.map((shape) => (
                  <button
                    key={shape.id}
                    onClick={() => setConfig({...config, faceShape: shape.id})}
                    className={`p-2 rounded-lg border-2 transition-all ${
                      config.faceShape === shape.id ? "border-pink-500 bg-pink-50 scale-105" : "border-gray-200 hover:border-pink-300"
                    }`}
                  >
                    <div className="text-xl mb-1">{shape.icon}</div>
                    <div className="text-xs font-semibold">{shape.name}</div>
                  </button>
                ))}
              </div>
            </div>

            {/* Body Type */}
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-3">Body Type</label>
              <div className="grid grid-cols-4 gap-2">
                {bodyTypes.map((type) => (
                  <button
                    key={type.id}
                    onClick={() => setConfig({...config, bodyType: type.id})}
                    className={`p-3 rounded-lg border-2 transition-all ${
                      config.bodyType === type.id ? "border-pink-500 bg-pink-50 scale-105" : "border-gray-200 hover:border-pink-300"
                    }`}
                  >
                    <div className="text-2xl mb-1">{type.icon}</div>
                    <div className="text-xs font-semibold">{type.name}</div>
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Complete Button */}
        <div className="mt-8 text-center">
          <button
            onClick={() => onComplete(config)}
            className="bg-gradient-to-r from-pink-500 to-pink-600 text-white px-12 py-4 rounded-lg text-lg font-semibold hover:shadow-xl transition-all transform hover:scale-105"
          >
            Continue to Dress Up →
          </button>
        </div>
      </div>
    </div>
  );
}
