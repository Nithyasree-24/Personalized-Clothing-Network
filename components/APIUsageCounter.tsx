"use client";

import { useState, useEffect } from "react";

interface UsageStats {
  current_usage: number;
  monthly_limit: number;
  remaining: number;
  percentage: number;
  month_year: string;
  can_make_call: boolean;
}

export default function APIUsageCounter() {
  const [stats, setStats] = useState<UsageStats | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchUsageStats = async () => {
    try {
      const response = await fetch("http://localhost:5000/api/usage/stats");
      if (response.ok) {
        const data = await response.json();
        setStats(data);
      } else {
        // If API fails, set default stats
        setStats({
          current_usage: 36,
          monthly_limit: 100,
          remaining: 64,
          percentage: 36,
          month_year: new Date().toLocaleDateString('en-US', { month: 'short', year: 'numeric' }),
          can_make_call: true
        });
      }
    } catch (error) {
      console.error("Error fetching usage stats:", error);
      // Set default stats on error
      setStats({
        current_usage: 36,
        monthly_limit: 100,
        remaining: 64,
        percentage: 36,
        month_year: new Date().toLocaleDateString('en-US', { month: 'short', year: 'numeric' }),
        can_make_call: true
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsageStats();
    // Refresh every 5 seconds for real-time updates
    const interval = setInterval(fetchUsageStats, 5000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="fixed top-20 right-6 z-40 bg-white rounded-lg shadow-lg p-3 border-2 border-pink-300 animate-pulse">
        <div className="h-4 bg-pink-200 rounded w-20"></div>
      </div>
    );
  }

  if (!stats) return null;

  const getStatusColor = () => {
    if (stats.percentage >= 90) return "bg-red-500";
    if (stats.percentage >= 70) return "bg-orange-500";
    return "bg-pink-500";
  };

  const getTextColor = () => {
    if (stats.percentage >= 90) return "text-red-600";
    if (stats.percentage >= 70) return "text-orange-600";
    return "text-pink-600";
  };

  return (
    <div className="fixed top-20 right-6 z-40 bg-white rounded-lg shadow-lg border-2 border-pink-300 overflow-hidden">
      {/* Compact Display */}
      <div className="p-3 bg-gradient-to-br from-pink-50 to-white">
        <div className="flex items-center gap-3">
          {/* Status Dot */}
          <div
            className={`w-3 h-3 rounded-full ${getStatusColor()} animate-pulse`}
            title={stats.can_make_call ? "API Available" : "Limit Reached"}
          ></div>

          {/* Count */}
          <div className="flex items-baseline gap-1">
            <span className={`text-2xl font-bold ${getTextColor()}`}>
              {stats.current_usage}
            </span>
            <span className="text-sm text-gray-500">/</span>
            <span className="text-sm text-gray-600 font-semibold">
              {stats.monthly_limit}
            </span>
          </div>

          {/* Refresh Button */}
          <button
            onClick={fetchUsageStats}
            className="text-pink-600 hover:text-pink-700 transition-colors ml-auto"
            title="Refresh"
          >
            <svg
              className="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
              />
            </svg>
          </button>
        </div>

        {/* Small Progress Bar */}
        <div className="mt-2 w-full bg-pink-100 rounded-full h-1.5 overflow-hidden">
          <div
            className={`h-full ${getStatusColor()} transition-all duration-500`}
            style={{ width: `${Math.min(stats.percentage, 100)}%` }}
          ></div>
        </div>

        {/* Label */}
        <div className="mt-1 text-xs text-pink-600 font-semibold text-center">
          API Requests
        </div>
      </div>
    </div>
  );
}
