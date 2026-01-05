import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Omniscient Market Intelligence - AI-Powered Sales Trend Tracker",
  description: "Real-time market analytics tracking sell-through rates, velocity, and arbitrage opportunities across eBay, Reddit, and local markets",
  keywords: ["market intelligence", "sales trends", "arbitrage", "eBay analytics", "sell-through rate"],
  authors: [{ name: "Omniscient" }],
  openGraph: {
    title: "Omniscient Market Intelligence",
    description: "AI-powered market analytics and trend tracking",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
