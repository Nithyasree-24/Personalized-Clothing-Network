"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [showForgot, setShowForgot] = useState(false);
  const [resetToken, setResetToken] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [resetMode, setResetMode] = useState(false);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    // Simple validation
    if (!email || !password) {
      setError("Please fill in all fields");
      setLoading(false);
      return;
    }

    // Email validation
    if (!email.includes("@")) {
      setError("Please enter a valid email");
      setLoading(false);
      return;
    }

    try {
      // Call authentication API
      const response = await fetch('http://localhost:5002/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });

      const result = await response.json();

      if (result.success) {
        // Store user info in localStorage
        localStorage.setItem("user", JSON.stringify({
          email: result.user.email,
          name: result.user.name,
          loggedIn: true,
        }));
        localStorage.setItem('user_id', result.user.email);
        localStorage.setItem('user_name', result.user.name);
        localStorage.setItem('user_email', result.user.email);

        // Redirect to home page
        router.push("/home");
      } else {
        setError(result.message);
        if (result.show_forgot) {
          setShowForgot(true);
        }
      }
    } catch (err) {
      setError("Connection error. Please check if the authentication server is running on port 5002.");
    } finally {
      setLoading(false);
    }
  };

  const handleForgotPassword = async () => {
    if (!email) {
      setError("Please enter your email first");
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('http://localhost:5002/api/auth/forgot-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
      });

      const result = await response.json();
      
      if (result.success) {
        setResetToken(result.token);
        setResetMode(true);
        setShowForgot(false);
        setError("");
      } else {
        setError(result.message);
      }
    } catch (err) {
      setError("Connection error. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleResetPassword = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!resetToken || !newPassword) {
      setError("Please enter both token and new password");
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('http://localhost:5002/api/auth/reset-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token: resetToken, password: newPassword })
      });

      const result = await response.json();
      
      if (result.success) {
        setResetMode(false);
        setResetToken("");
        setNewPassword("");
        setError("");
        alert("Password reset successful! You can now login with your new password.");
      } else {
        setError(result.message);
      }
    } catch (err) {
      setError("Connection error. Please try again.");
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
            <h2 className="text-3xl font-bold bg-gradient-to-r from-pink-600 to-pink-800 bg-clip-text text-transparent">
              {resetMode ? "Reset Password" : "Welcome Back"}
            </h2>
            <p className="mt-2 text-gray-700 font-medium">
              {resetMode ? "Enter your reset token and new password" : "Sign in to continue shopping"}
            </p>
          </div>

          {/* Error Message */}
          {error && (
            <div className="mb-4 rounded-lg bg-red-50 border border-red-200 p-4 text-sm text-red-700 font-medium">
              ⚠️ {error}
            </div>
          )}

          {/* Reset Password Form */}
          {resetMode ? (
            <form onSubmit={handleResetPassword} className="space-y-5">
              <div>
                <label className="block text-sm font-bold text-gray-800 mb-2">
                  Reset Token (from system)
                </label>
                <input
                  type="text"
                  value={resetToken}
                  onChange={(e) => setResetToken(e.target.value)}
                  className="w-full rounded-lg border-2 border-pink-200 bg-white px-4 py-3 text-gray-800 focus:border-pink-500 focus:outline-none"
                  placeholder="Enter reset token"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-bold text-gray-800 mb-2">
                  New Password
                </label>
                <input
                  type="password"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  className="w-full rounded-lg border-2 border-pink-200 bg-white px-4 py-3 text-gray-800 focus:border-pink-500 focus:outline-none"
                  placeholder="Enter new password"
                  required
                />
              </div>
              <button
                type="submit"
                disabled={loading}
                className="w-full rounded-lg bg-gradient-to-r from-pink-500 to-pink-600 py-3.5 font-bold text-white shadow-lg transition-all hover:shadow-xl hover:from-pink-600 hover:to-pink-700 disabled:opacity-70"
              >
                {loading ? "Resetting..." : "Reset Password"}
              </button>
              <button
                type="button"
                onClick={() => setResetMode(false)}
                className="w-full text-gray-600 hover:text-gray-800 text-sm"
              >
                Back to Login
              </button>
            </form>
          ) : (
            /* Login Form */
            <form onSubmit={handleLogin} className="space-y-5">
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
                    placeholder="you@example.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
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
                    placeholder="••••••••"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full rounded-lg border-2 border-pink-200 bg-white pl-10 pr-4 py-3 text-gray-800 placeholder-gray-400 focus:border-pink-500 focus:outline-none focus:ring-2 focus:ring-pink-200 transition-all"
                  />
                </div>
              </div>

              {/* Forgot Password Link */}
              <div className="flex justify-end">
                <button
                  type="button"
                  onClick={handleForgotPassword}
                  className="text-sm font-semibold text-pink-600 hover:text-pink-700 transition-colors"
                >
                  Forgot Password?
                </button>
              </div>

              {/* Sign In Button */}
              <button
                type="submit"
                disabled={loading}
                className="w-full rounded-lg bg-gradient-to-r from-pink-500 to-pink-600 py-3.5 font-bold text-white shadow-lg transition-all hover:shadow-xl hover:from-pink-600 hover:to-pink-700 disabled:opacity-70 disabled:cursor-not-allowed"
              >
                {loading ? "Signing in..." : "Sign In"}
              </button>
            </form>
          )}

          {/* Sign Up Link */}
          {!resetMode && (
            <div className="mt-8 text-center md:text-left">
              <p className="text-gray-700 font-medium">
                Don't have an account?{" "}
                <Link
                  href="/signup"
                  className="font-bold text-pink-600 hover:text-pink-700 transition-colors underline decoration-2 underline-offset-2"
                >
                  Sign Up
                </Link>
              </p>
            </div>
          )}
        </div>

        {/* Forgot Password Modal */}
        {showForgot && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
            <div className="w-full max-w-md rounded-xl bg-white p-8 shadow-2xl border-2 border-pink-200">
              <div className="text-center mb-4">
                <span className="text-5xl">📧</span>
              </div>
              <h3 className="text-2xl font-bold mb-3 text-center bg-gradient-to-r from-pink-600 to-pink-800 bg-clip-text text-transparent">Reset Password</h3>
              <p className="text-gray-700 mb-6 text-center">
                Click "Send Reset Link" to get a password reset token for <span className="font-bold text-pink-600">{email}</span>.
              </p>
              <div className="flex gap-3 justify-center">
                <button
                  onClick={handleForgotPassword}
                  disabled={loading}
                  className="rounded-lg bg-gradient-to-r from-pink-500 to-pink-600 text-white px-6 py-3 font-bold hover:from-pink-600 hover:to-pink-700 transition-all shadow-md hover:shadow-lg disabled:opacity-50"
                >
                  {loading ? "Sending..." : "Send Reset Link"}
                </button>
                <button
                  onClick={() => setShowForgot(false)}
                  className="rounded-lg bg-gray-200 text-gray-700 px-6 py-3 font-bold hover:bg-gray-300 transition-all"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
