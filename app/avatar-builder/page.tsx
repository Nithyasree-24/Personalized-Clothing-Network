"use client";

import { useState } from "react";
import Link from "next/link";
import AvatarLanding from "../../components/avatar/AvatarLanding";
import AvatarCreator from "../../components/avatar/AvatarCreator";
import ClothingLibrary from "../../components/avatar/ClothingLibrary";
import { BaseAvatar, AgeGroup, Gender } from "../../types/avatar";

export default function AvatarBuilderPage() {
  const [step, setStep] = useState<"landing" | "create" | "dress">("landing");
  const [ageGroup, setAgeGroup] = useState<AgeGroup | null>(null);
  const [gender, setGender] = useState<Gender | null>(null);
  const [baseAvatar, setBaseAvatar] = useState<BaseAvatar | null>(null);

  const handleAgeGenderSelect = (age: AgeGroup, gen: Gender) => {
    setAgeGroup(age);
    setGender(gen);
    setStep("create");
  };

  const handleAvatarCreated = (avatar: BaseAvatar) => {
    setBaseAvatar(avatar);
    setStep("dress");
  };

  const handleBack = () => {
    if (step === "dress") {
      setStep("create");
    } else if (step === "create") {
      setStep("landing");
      setAgeGroup(null);
      setGender(null);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-purple-50 to-blue-50">
      {/* Header */}
      <div className="bg-white shadow-sm sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <Link href="/home" className="text-pink-600 hover:text-pink-700 font-semibold flex items-center gap-2">
              <span>←</span>
              <span>Back to Home</span>
            </Link>
            <div className="flex items-center gap-3">
              <span className="text-3xl">👤</span>
              <h1 className="text-2xl font-bold text-pink-600">Avatar Builder</h1>
            </div>
            <div className="w-32"></div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {step === "landing" && (
          <AvatarLanding onSelect={handleAgeGenderSelect} />
        )}

        {step === "create" && ageGroup && gender && (
          <AvatarCreator
            ageGroup={ageGroup}
            gender={gender}
            onComplete={handleAvatarCreated}
            onBack={handleBack}
          />
        )}

        {step === "dress" && baseAvatar && (
          <ClothingLibrary
            baseAvatar={baseAvatar}
            onBack={handleBack}
          />
        )}
      </div>
    </div>
  );
}
