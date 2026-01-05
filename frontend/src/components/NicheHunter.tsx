"use client";

import React, { useState } from 'react';
import { Search, TrendingUp, Activity, Users, AlertCircle } from 'lucide-react';

type SearchResult = {
  keyword: string;
  sell_through_rate: number;
  saturation_ratio: number;
  market_status: string;
  avg_price: number | null;
  volume_sold: number;
  active_listings: number;
  last_updated: string;
};

export default function NicheHunter() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    setResults(null);

    try {
      // In real app, this would call the API
      // const res = await fetch(`http://localhost:8000/api/niche/search?q=${encodeURIComponent(query)}`);

      // Simulate search response
      await new Promise(resolve => setTimeout(resolve, 800));

      const mockData: SearchResult = {
        keyword: query,
        sell_through_rate: Math.random() * 80 + 20,
        saturation_ratio: Math.random() * 50 + 5,
        market_status: Math.random() > 0.5 ? 'SELLER_MARKET' : 'BUYER_MARKET',
        avg_price: Math.floor(Math.random() * 300) + 50,
        volume_sold: Math.floor(Math.random() * 200) + 50,
        active_listings: Math.floor(Math.random() * 1000) + 200,
        last_updated: new Date().toISOString()
      };

      setResults(mockData);
    } catch (err) {
      setError('Failed to fetch data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getMarketStatusColor = (status: string) => {
    return status === 'SELLER_MARKET' ? 'text-emerald-400 border-emerald-500/30' : 'text-red-400 border-red-500/30';
  };

  return (
    <div className="bg-zinc-950/50 border border-white/10 rounded-sm p-5 h-full flex flex-col">
      <h2 className="text-white font-bold uppercase tracking-wider mb-4 flex items-center gap-2">
        <Search className="w-4 h-4 text-yellow-500" />
        Niche Hunter
      </h2>

      {/* Search Form */}
      <form onSubmit={handleSearch} className="mb-6">
        <div className="relative">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search any keyword (e.g., 'vintage camera', 'retro gaming')..."
            className="w-full bg-black border border-white/20 text-white text-sm px-4 py-3 pr-12 rounded-sm focus:outline-none focus:border-yellow-500/50 transition-colors"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading || !query.trim()}
            className="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-yellow-500 hover:text-yellow-400 disabled:text-slate-600 transition-colors"
          >
            <Search className="w-4 h-4" />
          </button>
        </div>
      </form>

      {/* Loading State */}
      {loading && (
        <div className="flex items-center justify-center py-12">
          <div className="animate-pulse text-slate-500">Searching...</div>
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="bg-red-500/10 border border-red-500/50 rounded-sm p-4 mb-4">
          <div className="flex items-center gap-2 text-red-400 text-sm">
            <AlertCircle className="w-4 h-4" />
            {error}
          </div>
        </div>
      )}

      {/* Results */}
      {results && !loading && (
        <div className="space-y-4 flex-1 overflow-y-auto">
          {/* Header */}
          <div className="border-b border-white/10 pb-4">
            <h3 className="text-xl font-bold text-white mb-2">{results.keyword}</h3>
            <div className="flex items-center gap-2">
              <span className={`text-xs px-2 py-1 border rounded-sm font-bold ${getMarketStatusColor(results.market_status)}`}>
                {results.market_status.replace('_', ' ')}
              </span>
              <span className="text-xs text-slate-600">
                Last updated: {new Date(results.last_updated).toLocaleString()}
              </span>
            </div>
          </div>

          {/* Key Metrics */}
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-white/5 border border-white/5 rounded-sm p-4">
              <div className="flex items-center gap-2 text-xs text-slate-500 mb-2">
                <TrendingUp className="w-3 h-3" />
                <span className="uppercase tracking-wider">Sell-Through Rate</span>
              </div>
              <div className="text-2xl font-bold text-white">{results.sell_through_rate.toFixed(1)}%</div>
              <div className="text-xs text-slate-600 mt-1">
                {results.sell_through_rate > 50 ? 'High demand' : 'Moderate demand'}
              </div>
            </div>

            <div className="bg-white/5 border border-white/5 rounded-sm p-4">
              <div className="flex items-center gap-2 text-xs text-slate-500 mb-2">
                <Users className="w-3 h-3" />
                <span className="uppercase tracking-wider">Saturation Ratio</span>
              </div>
              <div className="text-2xl font-bold text-white">{results.saturation_ratio.toFixed(1)}:1</div>
              <div className="text-xs text-slate-600 mt-1">
                {results.saturation_ratio < 20 ? 'Low competition' : 'Moderate competition'}
              </div>
            </div>
          </div>

          {/* Additional Metrics */}
          <div className="space-y-3">
            <div className="flex justify-between items-center py-2 border-b border-white/5">
              <span className="text-xs text-slate-500">Avg Price</span>
              <span className="text-sm font-bold text-white">
                {results.avg_price ? `$${results.avg_price.toFixed(2)}` : 'N/A'}
              </span>
            </div>

            <div className="flex justify-between items-center py-2 border-b border-white/5">
              <div className="flex items-center gap-2">
                <Activity className="w-3 h-3 text-cyan-500" />
                <span className="text-xs text-slate-500">Volume Sold (24h)</span>
              </div>
              <span className="text-sm font-bold text-white">{results.volume_sold}</span>
            </div>

            <div className="flex justify-between items-center py-2 border-b border-white/5">
              <div className="flex items-center gap-2">
                <Activity className="w-3 h-3 text-purple-500" />
                <span className="text-xs text-slate-500">Active Listings</span>
              </div>
              <span className="text-sm font-bold text-white">{results.active_listings}</span>
            </div>
          </div>

          {/* Recommendation */}
          <div className="bg-emerald-500/10 border border-emerald-500/30 rounded-sm p-4 mt-4">
            <div className="flex items-start gap-3">
              <TrendingUp className="w-5 h-5 text-emerald-400 mt-0.5" />
              <div>
                <div className="text-xs font-bold text-emerald-400 uppercase tracking-wider mb-1">
                  Recommendation
                </div>
                <p className="text-sm text-slate-300">
                  {results.sell_through_rate > 50 && results.saturation_ratio < 20
                    ? "Strong opportunity! High demand with low competition. Consider entering this market."
                    : results.sell_through_rate > 50
                    ? "Good demand but competition is moderate. Consider targeting specific sub-niches."
                    : "Lower than average demand. Research further before investing."}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Empty State */}
      {!results && !loading && !error && (
        <div className="flex items-center justify-center h-full min-h-[200px]">
          <div className="text-center text-slate-600">
            <Search className="w-12 h-12 mx-auto mb-4 opacity-50" />
            <p className="text-sm">Search any keyword to analyze market demand</p>
          </div>
        </div>
      )}
    </div>
  );
}
