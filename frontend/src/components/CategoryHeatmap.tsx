"use client";

import React, { useState, useEffect } from 'react';
import { Thermometer, TrendingUp, DollarSign, Layers } from 'lucide-react';

type CategoryData = {
  category: string;
  avg_str: number;
  total_volume: number;
  item_count: number;
  heat_level: 'HOT' | 'WARM' | 'COLD';
  items: {
    keyword: string;
    str: number;
    volume: number;
    score: number;
  }[];
};

export default function CategoryHeatmap() {
  const [categories, setCategories] = useState<CategoryData[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHeatmapData = async () => {
      try {
        // In real app, this would call /api/analytics/heatmap
        // const res = await fetch('http://localhost:8000/api/analytics/heatmap');
        // const data = await res.json();

        // Simulate heatmap data
        await new Promise(resolve => setTimeout(resolve, 600));

        const mockData: CategoryData[] = [
          {
            category: 'Electronics',
            avg_str: 72.5,
            total_volume: 15420,
            item_count: 4,
            heat_level: 'HOT',
            items: [
              { keyword: 'Vintage Digital Camera', str: 85.2, volume: 4200, score: 88 },
              { keyword: 'Sony Walkman', str: 78.5, volume: 3800, score: 82 },
              { keyword: 'Flipper Zero', str: 65.3, volume: 3200, score: 75 },
              { keyword: 'Nvidia RTX 4090', str: 71.1, volume: 4220, score: 79 }
            ]
          },
          {
            category: 'Gaming',
            avg_str: 68.8,
            total_volume: 12350,
            item_count: 4,
            heat_level: 'HOT',
            items: [
              { keyword: 'Steam Deck OLED', str: 75.6, volume: 3500, score: 85 },
              { keyword: 'Analogue Pocket', str: 62.1, volume: 2800, score: 72 },
              { keyword: 'Nintendo 3DS XL', str: 58.4, volume: 2500, score: 68 },
              { keyword: 'Lego Rivendell', str: 79.2, volume: 3550, score: 83 }
            ]
          },
          {
            category: 'Fashion',
            avg_str: 61.3,
            total_volume: 8750,
            item_count: 4,
            heat_level: 'WARM',
            items: [
              { keyword: 'Carhartt Detroit Jacket', str: 85.2, volume: 2800, score: 87 },
              { keyword: 'Arc\'teryx Beta LT', str: 55.8, volume: 2100, score: 64 },
              { keyword: 'Birkenstock Boston', str: 54.3, volume: 1950, score: 62 },
              { keyword: 'Onitsuka Tiger Mexico 66', str: 49.9, volume: 1900, score: 58 }
            ]
          },
          {
            category: 'Collectibles',
            avg_str: 55.7,
            total_volume: 6420,
            item_count: 4,
            heat_level: 'WARM',
            items: [
              { keyword: 'Sonny Angel', str: 62.4, volume: 1800, score: 71 },
              { keyword: 'Jellycat Plush', str: 58.1, volume: 1620, score: 67 },
              { keyword: 'One Piece TCG Booster', str: 49.2, volume: 1450, score: 55 },
              { keyword: 'Lego Rivendell', str: 79.2, volume: 1550, score: 83 }
            ]
          },
          {
            category: 'Tools',
            avg_str: 48.2,
            total_volume: 4280,
            item_count: 3,
            heat_level: 'COLD',
            items: [
              { keyword: 'Leatherman Arc', str: 55.6, volume: 1550, score: 63 },
              { keyword: 'Knipex Cobra XS', str: 45.3, volume: 1320, score: 52 },
              { keyword: 'Yeti Rambler', str: 43.8, volume: 1410, score: 49 }
            ]
          }
        ];

        setCategories(mockData);
      } catch (err) {
        console.error('Heatmap fetch error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchHeatmapData();

    // Refresh heatmap data periodically
    const interval = setInterval(fetchHeatmapData, 120000); // Every 2 minutes

    return () => clearInterval(interval);
  }, []);

  const getHeatColor = (level: string) => {
    switch (level) {
      case 'HOT':
        return 'bg-gradient-to-br from-red-500/20 to-orange-500/20 border-red-500/50';
      case 'WARM':
        return 'bg-gradient-to-br from-yellow-500/20 to-amber-500/20 border-yellow-500/50';
      case 'COLD':
        return 'bg-gradient-to-br from-slate-500/20 to-blue-500/20 border-slate-500/50';
      default:
        return 'bg-white/5 border-slate-500/50';
    }
  };

  const getHeatIconColor = (level: string) => {
    switch (level) {
      case 'HOT': return 'text-red-500';
      case 'WARM': return 'text-yellow-500';
      case 'COLD': return 'text-blue-400';
      default: return 'text-slate-500';
    }
  };

  if (loading) {
    return (
      <div className="bg-zinc-950/50 border border-white/10 rounded-sm p-5 h-full">
        <div className="animate-pulse space-y-4">
          <div className="h-6 bg-white/10 rounded w-48" />
          <div className="h-64 bg-white/5 rounded" />
        </div>
      </div>
    );
  }

  return (
    <div className="bg-zinc-950/50 border border-white/10 rounded-sm p-5 h-full flex flex-col">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-white font-bold uppercase tracking-wider flex items-center gap-2">
          <Thermometer className="w-4 h-4 text-yellow-500" />
          Category Heatmap
        </h2>
        <div className="flex items-center gap-3 text-xs">
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded-sm bg-red-500" />
            <span className="text-slate-500">HOT</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded-sm bg-yellow-500" />
            <span className="text-slate-500">WARM</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded-sm bg-slate-500" />
            <span className="text-slate-500">COLD</span>
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto space-y-4 custom-scrollbar">
        {categories.map((cat, i) => (
          <div
            key={i}
            className={`border rounded-sm p-4 ${getHeatColor(cat.heat_level)} hover:brightness-110 transition-all`}
          >
            {/* Category Header */}
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-center gap-2">
                <Thermometer className={`w-4 h-4 ${getHeatIconColor(cat.heat_level)}`} />
                <div>
                  <h3 className="text-white font-bold text-sm">{cat.category}</h3>
                  <div className="flex items-center gap-2 text-xs text-slate-600">
                    <span>{cat.item_count} items</span>
                    <span>•</span>
                    <span className="uppercase tracking-wider">{cat.heat_level}</span>
                  </div>
                </div>
              </div>
              <div className="text-right">
                <div className="text-xl font-bold text-white">{cat.avg_str.toFixed(1)}%</div>
                <div className="text-xs text-slate-600">Avg STR</div>
              </div>
            </div>

            {/* Progress Bar */}
            <div className="w-full bg-black/30 h-2 rounded-full overflow-hidden mb-3">
              <div
                className={`h-full transition-all duration-500 ${
                  cat.heat_level === 'HOT' ? 'bg-gradient-to-r from-red-500 to-orange-500' :
                  cat.heat_level === 'WARM' ? 'bg-gradient-to-r from-yellow-500 to-amber-500' :
                  'bg-gradient-to-r from-slate-500 to-blue-500'
                }`}
                style={{ width: `${Math.min(cat.avg_str, 100)}%` }}
              />
            </div>

            {/* Category Stats */}
            <div className="grid grid-cols-2 gap-3 mb-3">
              <div className="flex items-center gap-2 bg-black/30 rounded-sm p-2">
                <TrendingUp className="w-3 h-3 text-cyan-500" />
                <div>
                  <div className="text-xs text-slate-500 uppercase tracking-wider">Volume</div>
                  <div className="text-sm font-bold text-white">
                    {cat.total_volume.toLocaleString()}
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-2 bg-black/30 rounded-sm p-2">
                <DollarSign className="w-3 h-3 text-emerald-500" />
                <div>
                  <div className="text-xs text-slate-500 uppercase tracking-wider">Avg Score</div>
                  <div className="text-sm font-bold text-white">
                    {(cat.items.reduce((sum, item) => sum + item.score, 0) / cat.items.length).toFixed(0)}
                  </div>
                </div>
              </div>
            </div>

            {/* Top Items */}
            <div className="space-y-2">
              <div className="text-xs text-slate-600 uppercase tracking-wider mb-2">Top Performing Items</div>
              {cat.items.slice(0, 3).map((item, j) => (
                <div
                  key={j}
                  className="flex items-center justify-between py-1.5 px-2 bg-black/20 rounded-sm"
                >
                  <div className="flex items-center gap-2 flex-1">
                    <Layers className="w-3 h-3 text-slate-600" />
                    <span className="text-sm text-slate-300">{item.keyword}</span>
                  </div>
                  <div className="flex items-center gap-4">
                    <div className="text-right">
                      <div className="text-xs text-slate-600">STR</div>
                      <div className="text-sm font-bold text-white">{item.str.toFixed(1)}%</div>
                    </div>
                    <div className="text-right">
                      <div className="text-xs text-slate-600">Score</div>
                      <div className="text-sm font-bold text-cyan-400">{item.score}</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
