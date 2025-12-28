"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function WelcomePage() {
  const router = useRouter();

  useEffect(() => {
    // Mark that user has seen welcome page
    sessionStorage.setItem("hasSeenWelcome", "true");

    // Auto redirect to login after 7 seconds
    const timer = setTimeout(() => {
      router.push("/login");
    }, 7000);

    return () => clearTimeout(timer);
  }, [router]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 via-rose-50 to-orange-50 flex items-center justify-center overflow-hidden">
      <div className="text-center animate-fadeIn">
        {/* Animated Clothing Rack */}
        <div className="relative mb-8 animate-slideDown flex justify-center items-center gap-8">
          <div className="text-8xl animate-swing delay-200">
            👕
          </div>
          <div className="text-8xl animate-swing delay-150">
            👖
          </div>
          <div className="text-9xl animate-swing">
            👔
          </div>
          <div className="text-8xl animate-swing delay-100">
            👗
          </div>
          <div className="text-8xl animate-swing delay-250">
            👚
          </div>
        </div>

        {/* Brand Name with Animation */}
        <div className="mb-4 animate-fadeInUp">
          <h1 className="text-6xl md:text-7xl font-bold mb-2 animate-gradient bg-gradient-to-r from-pink-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent">
            FashioPulse
          </h1>
          <div className="flex items-center justify-center gap-2 text-2xl md:text-3xl text-gray-700 font-medium">
            <span>Feel The Beat</span>
            <span className="animate-pulse text-red-500">❤️</span>
            <span>Of Fashion</span>
          </div>
        </div>

        {/* Loading Animation */}
        <div className="mt-12 flex justify-center gap-2">
          <div className="w-3 h-3 bg-pink-500 rounded-full animate-bounce"></div>
          <div className="w-3 h-3 bg-purple-500 rounded-full animate-bounce delay-100"></div>
          <div className="w-3 h-3 bg-indigo-500 rounded-full animate-bounce delay-200"></div>
        </div>

        {/* Skip Button */}
        <button
          onClick={() => router.push("/login")}
          className="mt-8 text-gray-500 hover:text-gray-700 text-sm underline animate-fadeIn"
        >
          Skip
        </button>
      </div>

      <style jsx>{`
        @keyframes fadeIn {
          from {
            opacity: 0;
          }
          to {
            opacity: 1;
          }
        }

        @keyframes fadeInUp {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes slideDown {
          from {
            opacity: 0;
            transform: translateY(-50px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes swing {
          0%, 100% {
            transform: rotate(-5deg);
          }
          50% {
            transform: rotate(5deg);
          }
        }

        @keyframes gradient {
          0% {
            background-position: 0% 50%;
          }
          50% {
            background-position: 100% 50%;
          }
          100% {
            background-position: 0% 50%;
          }
        }

        .animate-fadeIn {
          animation: fadeIn 1s ease-in;
        }

        .animate-fadeInUp {
          animation: fadeInUp 1s ease-out 0.3s both;
        }

        .animate-slideDown {
          animation: slideDown 1s ease-out;
        }

        .animate-swing {
          animation: swing 2s ease-in-out infinite;
        }

        .animate-gradient {
          background-size: 200% 200%;
          animation: gradient 3s ease infinite;
        }

        .delay-100 {
          animation-delay: 0.1s;
        }

        .delay-150 {
          animation-delay: 0.15s;
        }

        .delay-200 {
          animation-delay: 0.2s;
        }

        .delay-250 {
          animation-delay: 0.25s;
        }
      `}</style>
    </div>
  );
}
