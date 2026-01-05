"use client";

import React, { useState, useEffect } from 'react';
import {
  ArrowRight, DollarSign, TrendingUp, AlertCircle
} from 'lucide-react';

type ArbitrageOpportunity = {
  item: string;
  localPrice: number;
  localSource: string;
  ebaySoldPrice: number;
  potentialProfit: number;
  profitMargin: number;
  difficulty: 'EASY' | 'MEDIUM' | 'HARD';
  risk: 'LOW' | 'MEDIUM' | 'HIGH';
  lastUpdated: string;
};

export default function ArbitrageFinder() {
  const [opportunities, setOpportunities] = useState<ArbitrageOpportunity[]>([]);
  const [loading, setLoading] = useState(true);
  const [sortBy, setSortBy] = useState<'profit' | 'margin' | 'difficulty'>('profit');

  useEffect(() => {
    // Simulate arbitrage data (in real app, this would come from API)
    const simulateData = () => {
      const data: ArbitrageOpportunity[] = [
        {
          item: "Vintage Sony Walkman WM-D6C",
          localPrice: 150,
          localSource: "Craigslist - San Francisco",
          ebaySoldPrice: 450,
          potentialProfit: 300,
          profitMargin: 200,
          difficulty: 'EASY',
          risk: 'LOW',
          lastUpdated: new Date().toISOString()
        },
        {
          item: "Nintendo 3DS XL (New)",
          localPrice: 80,
          localSource: "FB Marketplace - Austin",
          ebaySoldPrice: 220,
          potentialProfit: 140,
          profitMargin: 175,
          difficulty: 'MEDIUM',
          risk: 'MEDIUM',
          lastUpdated: new Date().toISOString()
        },
        {
          item: "Carhartt Detroit Jacket (Vintage)",
          localPrice: 45,
          localSource: "Thrift Store - Portland",
          ebaySoldPrice: 180,
          potentialProfit: 135,
          profitMargin: 300,
          difficulty: 'EASY',
          risk: 'LOW',
          lastUpdated: new Date().toISOString()
        },
        {
          item: "Analogue Pocket",
          localPrice: 180,
          localSource: "FB Marketplace - Seattle",
          ebaySoldPrice: 320,
          potentialProfit: 140,
          profitMargin: 78,
          difficulty: 'HARD',
          risk: 'HIGH',
          lastUpdated: new Date().toISOString()
        },
        {
          item: "Fujifilm X100V",
          localPrice: 950,
          localSource: "Craigslist - New York",
          ebaySoldPrice: 1450,
          potentialProfit: 500,
          profitMargin: 53,
          difficulty: 'MEDIUM',
          risk: 'MEDIUM',
          lastUpdated: new Date().toISOString()
        },
        {
          item: "Arc'teryx Beta LT Jacket",
          localPrice: 200,
          localSource: "FB Marketplace - Denver",
          ebaySoldPrice: 450,
          potentialProfit: 250,
          profitMargin: 125,
          difficulty: 'EASY',
          risk: 'LOW',
          lastUpdated: new Date().toISOString()
        }
      ];

      // Sort by selected criteria
      let sorted = [...data];
      if (sortBy === 'profit') {
        sorted.sort((a, b) => b.potentialProfit - a.potentialProfit);
      } else if (sortBy === 'margin') {
        sorted.sort((a, b) => b.profitMargin - a.profitMargin);
      } else if (sortBy === 'difficulty') {
        const diffOrder = { 'EASY': 0, 'MEDIUM': 1, 'HARD': 2 };
        sorted.sort((a, b) => diffOrder[a.difficulty] - diffOrder[b.difficulty]);
      }

      setOpportunities(sorted);
      setLoading(false);
    };

    simulateData();
  }, [sortBy]);

  const getDifficultyColor = (diff: string) => {
    switch (diff) {
      case 'EASY': return 'text-emerald-400 border-emerald-500/30';
      case 'MEDIUM': return 'text-yellow-400 border-yellow-500/30';
      case 'HARD': return 'text-red-400 border-red-500/30';
      default: return 'text-slate-400 border-slate-500/30';
    }
  };

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'LOW': return 'text-emerald-400';
      case 'MEDIUM': return 'text-yellow-400';
      case 'HIGH': return 'text-red-400';
      default: return 'text-slate-400';
    }
  };

  if (loading) {
    return (
      <div className="bg-zinc-950/50 border border-white/10 rounded-sm p-5 h-full">
        <div className="animate-pulse space-y-4">
          <div className="h-6 bg-white/10 rounded w-48" />
          <div className="h-40 bg-white/5 rounded" />
        </div>
      </div>
    );
  }

  return (
    <div className="bg-zinc-950/50 border border-white/10 rounded-sm p-5 h-full flex flex-col">
      <div className="flex justify-between items-start mb-4">
        <h2 className="text-white font-bold uppercase tracking-wider flex items-center gap-2">
          <TrendingUp className="w-4 h-4 text-yellow-500" />
          Arbitrage Finder
        </h2>
        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-500 uppercase tracking-wider">Sort by:</span>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as any)}
            className="bg-black border border-white/20 text-white text-xs px-2 py-1 rounded-sm focus:outline-none focus:border-yellow-500/50"
          >
            <option value="profit">Potential Profit</option>
            <option value="margin">Profit Margin %</option>
            <option value="difficulty">Difficulty</option>
          </select>
        </div>
      </div>

      <div className="text-xs text-slate-600 mb-4 flex items-center gap-2">
        <AlertCircle className="w-3 h-3" />
        <span>Find low local prices, sell high on eBay</span>
      </div>

      <div className="flex-1 overflow-y-auto space-y-3 custom-scrollbar">
        {opportunities.map((opp, i) => (
          <div
            key={i}
            className="border border-white/5 hover:border-yellow-500/30 bg-white/0 hover:bg-white/5 transition-all p-4 rounded-sm"
          >
            <div className="flex justify-between items-start mb-3">
              <div className="flex-1">
                <h3 className="text-white font-bold text-sm mb-1">{opp.item}</h3>
                <div className="flex items-center gap-2 text-xs text-slate-500">
                  <span>{opp.localSource}</span>
                </div>
              </div>
              <div className={`text-xs px-2 py-1 border rounded-sm font-bold ${getDifficultyColor(opp.difficulty)}`}>
                {opp.difficulty}
              </div>
            </div>

            <div className="grid grid-cols-3 gap-4 mb-3">
              <div>
                <div className="text-xs text-slate-500 mb-1 flex items-center gap-1">
                  <DollarSign className="w-3 h-3" />
                  <span>Local Price</span>
                </div>
                <div className="text-lg font-bold text-white">${opp.localPrice}</div>
              </div>

              <div>
                <div className="text-xs text-slate-500 mb-1">eBay Sold</div>
                <div className="text-lg font-bold text-cyan-400">${opp.ebaySoldPrice}</div>
              </div>

              <div>
                <div className="text-xs text-slate-500 mb-1">Potential Profit</div>
                <div className="text-lg font-bold text-emerald-400">+${opp.potentialProfit}</div>
                <div className="text-xs text-emerald-500/80">{opp.profitMargin}% margin</div>
              </div>
            </div>

            <div className="flex items-center justify-between text-xs">
              <div className="flex items-center gap-2">
                <span className="text-slate-600">Risk:</span>
                <span className={`font-bold ${getRiskColor(opp.risk)}`}>{opp.risk}</span>
              </div>
              <div className="flex items-center gap-2 text-slate-600">
                <span>{new Date(opp.lastUpdated).toLocaleTimeString()}</span>
                <ArrowRight className="w-3 h-3 text-yellow-500" />
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
