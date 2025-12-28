"use client";

import { useState } from "react";

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
  onLogin: (user: any) => void;
}

export default function AuthModal({ isOpen, onClose, onLogin }: AuthModalProps) {
  const [mode, setMode] = useState<'login' | 'signup' | 'forgot'>('login');
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [showForgot, setShowForgot] = useState(false);
  const [resetToken, setResetToken] = useState('');

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      if (mode === 'signup') {
        // Validate passwords match
        if (formData.password !== formData.confirmPassword) {
          setMessage('Passwords do not match.');
          setLoading(false);
          return;
        }

        // Signup request
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
        setMessage(result.message);

        if (result.success) {
          // Switch to login mode after successful signup
          setMode('login');
          setFormData({ ...formData, name: '', password: '', confirmPassword: '' });
        }
      } else if (mode === 'login') {
        // Login request
        const response = await fetch('http://localhost:5002/api/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            email: formData.email,
            password: formData.password
          })
        });

        const result = await response.json();
        setMessage(result.message);

        if (result.success) {
          // Store user data and close modal
          localStorage.setItem('user_id', result.user.email);
          localStorage.setItem('user_name', result.user.name);
          localStorage.setItem('user_email', result.user.email);
          onLogin(result.user);
          onClose();
        } else if (result.show_forgot) {
          setShowForgot(true);
        } else if (result.show_signup) {
          // Switch to signup mode if account not found
          setMode('signup');
        }
      } else if (mode === 'forgot') {
        // Forgot password request
        const response = await fetch('http://localhost:5002/api/auth/forgot-password', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            email: formData.email
          })
        });

        const result = await response.json();
        setMessage(result.message);

        if (result.success) {
          // In production, user would receive email with token
          // For now, we show the token in the message
          setResetToken(result.token);
        }
      }
    } catch (error) {
      setMessage('Connection error. Please check if the authentication server is running.');
    } finally {
      setLoading(false);
    }
  };

  const handleResetPassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const response = await fetch('http://localhost:5002/api/auth/reset-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          token: resetToken,
          password: formData.password
        })
      });

      const result = await response.json();
      setMessage(result.message);

      if (result.success) {
        // Switch back to login mode
        setMode('login');
        setResetToken('');
        setFormData({ name: '', email: '', password: '', confirmPassword: '' });
      }
    } catch (error) {
      setMessage('Connection error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-pink-500 to-purple-500 p-6 text-white">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold">
              {mode === 'login' ? 'Welcome Back!' : 
               mode === 'signup' ? 'Join FashionPulse' : 
               'Reset Password'}
            </h2>
            <button
              onClick={onClose}
              className="text-white/80 hover:text-white text-2xl font-bold"
            >
              ✕
            </button>
          </div>
          <p className="text-white/90 mt-2">
            {mode === 'login' ? 'Sign in to your account' : 
             mode === 'signup' ? 'Create your account' : 
             'Reset your password'}
          </p>
        </div>

        {/* Content */}
        <div className="p-6">
          {/* Message */}
          {message && (
            <div className={`mb-4 p-3 rounded-lg text-sm ${
              message.includes('successful') || message.includes('created') 
                ? 'bg-green-100 text-green-700 border border-green-200'
                : 'bg-red-100 text-red-700 border border-red-200'
            }`}>
              {message}
            </div>
          )}

          {/* Reset Password Form */}
          {resetToken && (
            <form onSubmit={handleResetPassword} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Reset Token (from email)
                </label>
                <input
                  type="text"
                  value={resetToken}
                  onChange={(e) => setResetToken(e.target.value)}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-pink-500"
                  placeholder="Enter reset token"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  New Password
                </label>
                <input
                  type="password"
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-pink-500"
                  placeholder="Enter new password"
                  required
                />
              </div>
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-gradient-to-r from-pink-500 to-purple-500 text-white py-3 rounded-lg font-semibold hover:from-pink-600 hover:to-purple-600 transition-all disabled:opacity-50"
              >
                {loading ? 'Resetting...' : 'Reset Password'}
              </button>
              <button
                type="button"
                onClick={() => {
                  setResetToken('');
                  setMode('login');
                }}
                className="w-full text-gray-600 hover:text-gray-800 text-sm"
              >
                Back to Login
              </button>
            </form>
          )}

          {/* Main Form */}
          {!resetToken && (
            <form onSubmit={handleSubmit} className="space-y-4">
              {/* Name field for signup */}
              {mode === 'signup' && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Full Name
                  </label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-pink-500"
                    placeholder="Enter your full name"
                    required
                  />
                </div>
              )}

              {/* Email field */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Email Address
                </label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-pink-500"
                  placeholder="Enter your email"
                  required
                />
              </div>

              {/* Password field */}
              {mode !== 'forgot' && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Password
                  </label>
                  <input
                    type="password"
                    value={formData.password}
                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-pink-500"
                    placeholder="Enter your password"
                    required
                  />
                </div>
              )}

              {/* Confirm Password field for signup */}
              {mode === 'signup' && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Confirm Password
                  </label>
                  <input
                    type="password"
                    value={formData.confirmPassword}
                    onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-pink-500"
                    placeholder="Confirm your password"
                    required
                  />
                </div>
              )}

              {/* Submit Button */}
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-gradient-to-r from-pink-500 to-purple-500 text-white py-3 rounded-lg font-semibold hover:from-pink-600 hover:to-purple-600 transition-all disabled:opacity-50"
              >
                {loading ? 'Please wait...' : 
                 mode === 'login' ? 'Sign In' : 
                 mode === 'signup' ? 'Create Account' : 
                 'Send Reset Link'}
              </button>

              {/* Forgot Password Link */}
              {mode === 'login' && showForgot && (
                <button
                  type="button"
                  onClick={() => setMode('forgot')}
                  className="w-full text-pink-600 hover:text-pink-800 text-sm font-medium"
                >
                  Forgot Password?
                </button>
              )}

              {/* Mode Switch */}
              <div className="text-center text-sm text-gray-600">
                {mode === 'login' ? (
                  <>
                    Don't have an account?{' '}
                    <button
                      type="button"
                      onClick={() => {
                        setMode('signup');
                        setMessage('');
                        setShowForgot(false);
                      }}
                      className="text-pink-600 hover:text-pink-800 font-medium"
                    >
                      Sign up
                    </button>
                  </>
                ) : mode === 'signup' ? (
                  <>
                    Already have an account?{' '}
                    <button
                      type="button"
                      onClick={() => {
                        setMode('login');
                        setMessage('');
                      }}
                      className="text-pink-600 hover:text-pink-800 font-medium"
                    >
                      Sign in
                    </button>
                  </>
                ) : (
                  <button
                    type="button"
                    onClick={() => {
                      setMode('login');
                      setMessage('');
                    }}
                    className="text-pink-600 hover:text-pink-800 font-medium"
                  >
                    Back to Sign In
                  </button>
                )}
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}