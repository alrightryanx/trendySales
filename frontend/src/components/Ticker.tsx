"use client";

import React, { useState, useEffect } from 'react';
import { ShoppingCart, Clock } from 'lucide-react';

type TickerItem = {
  keyword: string;
  price: number;
  time: string;
  platform: string;
  change?: number;
};

export default function Ticker() {
  const [items, setItems] = useState<TickerItem[]>([]);
  const [scrollPosition, setScrollPosition] = useState(0);

  useEffect(() => {
    // Simulate ticker data (in real app, this would come from API)
    const generateTickerData = () => {
      const keywords = [
        "Fujifilm X100V", "Sony Walkman", "Steam Deck OLED",
        "Carhartt Detroit Jacket", "Arc'teryx Beta LT",
        "Analogue Pocket", "Jellycat Plush", "Leatherman Arc",
        "Nvidia RTX 4090", "Nintendo 3DS XL", "Birkenstock Boston",
        "One Piece TCG Booster", "Lego Rivendell", "Flipper Zero"
      ];

      const newItem: TickerItem = {
        keyword: keywords[Math.floor(Math.random() * keywords.length)],
        price: Math.floor(Math.random() * 500) + 50,
        time: new Date().toLocaleTimeString(),
        platform: 'eBay',
        change: Math.random() > 0.5 ? Math.random() * 10 : -Math.random() * 5
      };

      setItems(prev => {
        const updated = [newItem, ...prev].slice(0, 15);
        return updated;
      });
    };

    // Initial load
    for (let i = 0; i < 10; i++) {
      setTimeout(() => generateTickerData(), i * 200);
    }

    // Add new items periodically
    const interval = setInterval(generateTickerData, 3000);

    // Auto-scroll
    const scrollInterval = setInterval(() => {
      setScrollPosition(prev => (prev + 1) % 100);
    }, 50);

    return () => {
      clearInterval(interval);
      clearInterval(scrollInterval);
    };
  }, []);

  return (
    <div className="bg-zinc-950/80 border-b border-white/10 backdrop-blur-sm overflow-hidden">
      <div className="max-w-[1600px] mx-auto px-6 py-2">
        <div className="flex items-center gap-2 text-xs text-slate-500 mb-2">
          <ShoppingCart className="w-3 h-3 text-emerald-500" />
          <span className="uppercase tracking-wider">Live Sales Feed</span>
          <span className="text-slate-600">•</span>
          <Clock className="w-3 h-3" />
          <span>Real-time</span>
        </div>

        <div
          className="flex gap-6 overflow-hidden"
          style={{
            animation: 'scroll 60s linear infinite'
          }}
        >
          {[...items, ...items].map((item, i) => (
            <div
              key={`${item.keyword}-${item.time}-${i}`}
              className="flex-shrink-0 px-3 py-1 bg-white/5 border border-white/5 rounded-sm hover:border-white/20 transition-colors"
            >
              <div className="flex items-center gap-3 text-xs">
                <span className="text-slate-400">{item.keyword}</span>
                <span className="font-bold text-white">${item.price}</span>
                {item.change !== undefined && (
                  <span className={`font-bold ${item.change >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                    {item.change >= 0 ? '+' : ''}{item.change.toFixed(1)}%
                  </span>
                )}
                <span className="text-slate-600">{item.time}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      <style jsx>{`
        @keyframes scroll {
          0% { transform: translateX(0); }
          100% { transform: translateX(-50%); }
        }
      `}</style>
    </div>
  );
}
