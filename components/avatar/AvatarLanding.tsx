"use client";

import { AgeGroup, Gender } from "../../types/avatar";

type AvatarLandingProps = {
  onSelect: (ageGroup: AgeGroup, gender: Gender) => void;
};

export default function AvatarLanding({ onSelect }: AvatarLandingProps) {
  return (
    <div className="text-center max-w-5xl mx-auto">
      <div className="mb-8">
        <span className="text-8xl">👤</span>
      </div>
      
      <div className="bg-gradient-to-r from-pink-500 to-pink-600 py-6 px-8 rounded-2xl mb-8 shadow-lg inline-block">
        <h2 className="text-4xl font-bold text-white mb-2">
          Build Your Avatar
        </h2>
        <p className="text-white/90 text-lg">
          Create your personalized avatar and try on outfits!
        </p>
      </div>

      <p className="text-xl text-gray-600 mb-12">
        Choose your avatar type to get started
      </p>

      {/* Age Group Selection */}
      <div className="space-y-8">
        {/* Adults */}
        <div>
          <h3 className="text-2xl font-bold text-gray-800 mb-6 flex items-center justify-center gap-2">
            <span>👨‍👩‍👧‍👦</span>
            <span>Adults</span>
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-3xl mx-auto">
            <button
              onClick={() => onSelect("adult", "male")}
              className="group bg-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all transform hover:scale-105 border-2 border-blue-200 hover:border-blue-400"
            >
              <div className="text-7xl mb-4">👨</div>
              <h4 className="text-2xl font-bold text-blue-600 mb-2">Male</h4>
              <p className="text-gray-600">Create a male avatar</p>
              <div className="mt-4 text-blue-600 font-semibold opacity-0 group-hover:opacity-100 transition-opacity">
                Get Started →
              </div>
            </button>

            <button
              onClick={() => onSelect("adult", "female")}
              className="group bg-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all transform hover:scale-105 border-2 border-pink-200 hover:border-pink-400"
            >
              <div className="text-7xl mb-4">👩</div>
              <h4 className="text-2xl font-bold text-pink-600 mb-2">Female</h4>
              <p className="text-gray-600">Create a female avatar</p>
              <div className="mt-4 text-pink-600 font-semibold opacity-0 group-hover:opacity-100 transition-opacity">
                Get Started →
              </div>
            </button>
          </div>
        </div>

        {/* Kids */}
        <div>
          <h3 className="text-2xl font-bold text-gray-800 mb-6 flex items-center justify-center gap-2">
            <span>👧👦</span>
            <span>Kids</span>
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-3xl mx-auto">
            <button
              onClick={() => onSelect("kid", "male")}
              className="group bg-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all transform hover:scale-105 border-2 border-blue-200 hover:border-blue-400"
            >
              <div className="text-7xl mb-4">👦</div>
              <h4 className="text-2xl font-bold text-blue-600 mb-2">Boy</h4>
              <p className="text-gray-600">Create a boy avatar</p>
              <div className="mt-4 text-blue-600 font-semibold opacity-0 group-hover:opacity-100 transition-opacity">
                Get Started →
              </div>
            </button>

            <button
              onClick={() => onSelect("kid", "female")}
              className="group bg-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all transform hover:scale-105 border-2 border-pink-200 hover:border-pink-400"
            >
              <div className="text-7xl mb-4">👧</div>
              <h4 className="text-2xl font-bold text-pink-600 mb-2">Girl</h4>
              <p className="text-gray-600">Create a girl avatar</p>
              <div className="mt-4 text-pink-600 font-semibold opacity-0 group-hover:opacity-100 transition-opacity">
                Get Started →
              </div>
            </button>
          </div>
        </div>
      </div>

      {/* Features */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-16">
        <div className="bg-white p-6 rounded-xl shadow-md border-2 border-pink-200">
          <div className="text-4xl mb-4">✨</div>
          <h3 className="font-bold text-pink-600 mb-2">Customize</h3>
          <p className="text-sm text-gray-600">
            Choose face, hair, skin tone & body type
          </p>
        </div>
        <div className="bg-white p-6 rounded-xl shadow-md border-2 border-pink-200">
          <div className="text-4xl mb-4">👗</div>
          <h3 className="font-bold text-pink-600 mb-2">Try Outfits</h3>
          <p className="text-sm text-gray-600">
            Apply clothing stickers to your avatar
          </p>
        </div>
        <div className="bg-white p-6 rounded-xl shadow-md border-2 border-pink-200">
          <div className="text-4xl mb-4">🛍️</div>
          <h3 className="font-bold text-pink-600 mb-2">Shop</h3>
          <p className="text-sm text-gray-600">
            Buy the exact outfits you created
          </p>
        </div>
      </div>
    </div>
  );
}
