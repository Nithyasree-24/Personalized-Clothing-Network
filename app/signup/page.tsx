"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

export default function SignupPage() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    // Validation
    if (!formData.name || !formData.email || !formData.password || !formData.confirmPassword) {
      setError("Please fill in all fields");
      setLoading(false);
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      setError("Passwords do not match");
      setLoading(false);
      return;
    }

    if (formData.password.length < 6) {
      setError("Password must be at least 6 characters");
      setLoading(false);
      return;
    }

    try {
      // Call authentication API
      const response = await fetch('http://localhost:5002/api/auth/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: formData.name,
          email: formData.email,
          password: formData.password
        })
      });

      const result = await response.json();

      if (result.success) {
        // Show success message and redirect to login
        alert(result.message);
        router.push("/login");
      } else {
        setError(result.message);
      }
    } catch (err) {
      setError("Connection error. Please check if the authentication server is running on port 5002.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-pink-100 to-pink-200 flex items-center justify-center p-6">
      <div className="w-full max-w-5xl rounded-2xl bg-white shadow-2xl overflow-hidden flex flex-col md:flex-row">
        {/* Left branding column with image */}
        <div className="hidden md:flex w-1/2 items-center justify-center bg-gradient-to-br from-pink-50 to-pink-100 p-8">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src="/assets/fashiopulse-logo.svg"
            alt="FashioPulse - Feel The Beat Of Fashion"
            className="w-full h-full max-h-[600px] object-contain"
          />
        </div>

        {/* Right form column */}
        <div className="w-full md:w-1/2 p-8 md:p-12 bg-gradient-to-br from-pink-50 to-white">
          {/* Logo and Branding for small screens */}
          <div className="mb-6 flex md:hidden flex-col items-center">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src="/assets/fashiopulse-logo.svg"
              alt="FashioPulse"
              className="w-48 h-auto mb-4"
            />
          </div>
          {/* Heading */}
          <div className="mb-8 text-center md:text-left">
            <h2 className="text-3xl font-bold bg-gradient-to-r from-pink-600 to-pink-800 bg-clip-text text-transparent">Create Account</h2>
            <p className="mt-2 text-gray-700 font-medium">Join us to start shopping</p>
          </div>

          {/* Error Message */}
          {error && (
            <div className="mb-4 rounded-lg bg-red-50 border border-red-200 p-4 text-sm text-red-700 font-medium">
              ⚠️ {error}
            </div>
          )}

          {/* Signup Form */}
          <form onSubmit={handleSignup} className="space-y-4">
          {/* Name Field */}
          <div>
            <label htmlFor="name" className="block text-sm font-bold text-gray-800 mb-2">
              Full Name
            </label>
            <div className="relative">
              <span className="absolute left-3 top-1/2 -translate-y-1/2 text-pink-400">👤</span>
              <input
                id="name"
                type="text"
                name="name"
                placeholder="John Doe"
                value={formData.name}
                onChange={handleChange}
                className="w-full rounded-lg border-2 border-pink-200 bg-white pl-10 pr-4 py-3 text-gray-800 placeholder-gray-400 focus:border-pink-500 focus:outline-none focus:ring-2 focus:ring-pink-200 transition-all"
              />
            </div>
          </div>

          {/* Email Field */}
          <div>
            <label htmlFor="email" className="block text-sm font-bold text-gray-800 mb-2">
              Email
            </label>
            <div className="relative">
              <span className="absolute left-3 top-1/2 -translate-y-1/2 text-pink-400">✉️</span>
              <input
                id="email"
                type="email"
                name="email"
                placeholder="you@example.com"
                value={formData.email}
                onChange={handleChange}
                className="w-full rounded-lg border-2 border-pink-200 bg-white pl-10 pr-4 py-3 text-gray-800 placeholder-gray-400 focus:border-pink-500 focus:outline-none focus:ring-2 focus:ring-pink-200 transition-all"
              />
            </div>
          </div>

          {/* Password Field */}
          <div>
            <label htmlFor="password" className="block text-sm font-bold text-gray-800 mb-2">
              Password
            </label>
            <div className="relative">
              <span className="absolute left-3 top-1/2 -translate-y-1/2 text-pink-400">🔒</span>
              <input
                id="password"
                type="password"
                name="password"
                placeholder="••••••••"
                value={formData.password}
                onChange={handleChange}
                className="w-full rounded-lg border-2 border-pink-200 bg-white pl-10 pr-4 py-3 text-gray-800 placeholder-gray-400 focus:border-pink-500 focus:outline-none focus:ring-2 focus:ring-pink-200 transition-all"
              />
            </div>
          </div>

          {/* Confirm Password Field */}
          <div>
            <label htmlFor="confirmPassword" className="block text-sm font-bold text-gray-800 mb-2">
              Confirm Password
            </label>
            <div className="relative">
              <span className="absolute left-3 top-1/2 -translate-y-1/2 text-pink-400">🔒</span>
              <input
                id="confirmPassword"
                type="password"
                name="confirmPassword"
                placeholder="••••••••"
                value={formData.confirmPassword}
                onChange={handleChange}
                className="w-full rounded-lg border-2 border-pink-200 bg-white pl-10 pr-4 py-3 text-gray-800 placeholder-gray-400 focus:border-pink-500 focus:outline-none focus:ring-2 focus:ring-pink-200 transition-all"
              />
            </div>
          </div>

          {/* Sign Up Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-lg bg-gradient-to-r from-pink-500 to-pink-600 py-3.5 font-bold text-white shadow-lg transition-all hover:shadow-xl hover:from-pink-600 hover:to-pink-700 disabled:opacity-70 disabled:cursor-not-allowed mt-6"
          >
            {loading ? "Creating Account..." : "Sign Up"}
          </button>
          </form>

          {/* Sign In Link */}
          <div className="mt-8 text-center md:text-left">
            <p className="text-gray-700 font-medium">
              Already have an account?{" "}
              <Link
                href="/login"
                className="font-bold text-pink-600 hover:text-pink-700 transition-colors underline decoration-2 underline-offset-2"
              >
                Sign In
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
