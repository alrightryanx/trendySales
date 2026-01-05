"use client";

import React from 'react';
import { useRouter } from 'next/navigation';
import { ArrowLeft } from 'lucide-react';
import ArbitrageFinder from '@/components/ArbitrageFinder';

export default function ArbitragePage() {
  const router = useRouter();

  return (
    <div className="min-h-screen bg-black text-slate-300 font-mono text-sm">

      {/* Header */}
      <header className="border-b border-white/10 bg-black/50 backdrop-blur-sm sticky top-12 z-50">
        <div className="max-w-[1600px] mx-auto px-6 h-14 flex justify-between items-center">
          <div className="flex items-center gap-4">
            <button
              onClick={() => router.back()}
              className="flex items-center gap-2 text-yellow-500 hover:text-yellow-400 transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
              <span className="text-xs uppercase">Back</span>
            </button>
            <div className="h-4 w-px bg-white/20" />
            <h1 className="text-base font-bold tracking-widest text-white uppercase">
              Arbitrage Finder
            </h1>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-[1600px] mx-auto px-6 py-6">
        <ArbitrageFinder />
      </main>
    </div>
  );
}
