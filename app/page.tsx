"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function RootPage() {
  const router = useRouter();

  useEffect(() => {
    // Check if user is logged in
    const user = localStorage.getItem("user");
    if (user) {
      // If logged in, redirect to personalized home
      router.push("/home");
    } else {
      // If not logged in, redirect to login (first page)
      router.push("/login");
    }
  }, [router]);

  return null; // This page doesn't render anything, just redirects
}
