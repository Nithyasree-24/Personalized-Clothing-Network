import type { Metadata } from "next";
import { Geist, Geist_Mono, Great_Vibes } from "next/font/google";
import "./globals.css";
import "./pink-theme.css";
import { CartProvider } from "../context/CartContext";
import CartNotificationWrapper from "../components/CartNotificationWrapper";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

const greatVibes = Great_Vibes({
  weight: "400",
  variable: "--font-great-vibes",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "FashioPulse - Your Fashion Destination",
  description: "Shop the latest fashion trends for men, women, and kids",
};

export const viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} ${greatVibes.variable} antialiased`}
      >
        <CartProvider>
          {children}
          <CartNotificationWrapper />
        </CartProvider>
      </body>
    </html>
  );
}
