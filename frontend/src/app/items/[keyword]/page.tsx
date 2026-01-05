"use client";

import React, { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  AreaChart, Area, Legend
} from 'recharts';
import {
  ArrowLeft, TrendingUp, TrendingDown, Activity, AlertTriangle,
  BarChart3, DollarSign, Clock
} from 'lucide-react';

// --- Types ---
type TrendDetail = {
  keyword: string;
  current: {
    str: number;
    volume: number;
    supply: number;
    avg_price: number | null;
    status: string;
    recorded_at: string;
  };
  trend: {
    direction: 'BULLISH' | 'BEARISH' | 'NEUTRAL' | 'FLAT';
    momentum_7d: number;
    momentum_30d: number;
    ma_7d: number;
    volatility: number;
  } | null;
  history: {
    date: string;
    str: number;
    volume: number;
    price: number | null;
  }[];
  anomaly: {
    severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
    type: string;
    message: string;
    detected_at: string;
  } | null;
  forecast: {
    model: string;
    confidence: number;
    predictions: { date: string; predicted_str: number }[];
  } | null;
};

export default function ItemDetailPage() {
  const params = useParams();
  const router = useRouter();
  const keyword = params.keyword as string;

  const [data, setData] = useState<TrendDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDetail = async () => {
      try {
        setLoading(true);
        const res = await fetch(`http://localhost:8000/api/trends/${encodeURIComponent(keyword)}`);
        if (!res.ok) {
          throw new Error('Item not found');
        }
        const detailData = await res.json();
        setData(detailData);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch data');
      } finally {
        setLoading(false);
      }
    };

    fetchDetail();
  }, [keyword]);

  if (loading) {
    return (
      <div className="min-h-screen bg-black text-slate-300 font-mono p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-white/10 rounded w-64" />
          <div className="h-64 bg-white/5 rounded" />
          <div className="h-64 bg-white/5 rounded" />
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="min-h-screen bg-black text-slate-300 font-mono p-6">
        <button
          onClick={() => router.back()}
          className="flex items-center gap-2 mb-6 text-yellow-500 hover:text-yellow-400"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Dashboard
        </button>
        <div className="bg-red-500/10 border border-red-500/50 rounded-sm p-6">
          <h2 className="text-red-400 font-bold mb-2">Error</h2>
          <p className="text-slate-400">{error || 'Item not found'}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black text-slate-300 font-mono text-sm">
      {/* Header */}
      <header className="border-b border-white/10 bg-black/50 backdrop-blur-sm sticky top-0 z-50">
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
              {data.keyword}
            </h1>
            <span className={`text-xs px-2 py-0.5 border ${
              data.trend?.direction === 'BULLISH' ? 'border-emerald-500/30 text-emerald-400' :
              data.trend?.direction === 'BEARISH' ? 'border-red-500/30 text-red-400' :
              'border-slate-500/30 text-slate-400'
            }`}>
              {data.trend?.direction || 'NEUTRAL'}
            </span>
          </div>
        </div>
      </header>

      <main className="max-w-[1600px] mx-auto px-6 py-6 space-y-6">
        {/* Current Stats */}
        <section className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-zinc-950/50 border border-white/10 rounded-sm p-4">
            <div className="flex items-center gap-2 text-xs text-slate-500 mb-2">
              <Activity className="w-3 h-3" />
              <span className="uppercase tracking-wider">Sell-Through Rate</span>
            </div>
            <div className="text-2xl font-bold text-white">{data.current.str.toFixed(1)}%</div>
          </div>

          <div className="bg-zinc-950/50 border border-white/10 rounded-sm p-4">
            <div className="flex items-center gap-2 text-xs text-slate-500 mb-2">
              <BarChart3 className="w-3 h-3" />
              <span className="uppercase tracking-wider">Volume (24h)</span>
            </div>
            <div className="text-2xl font-bold text-white">{data.current.volume}</div>
          </div>

          <div className="bg-zinc-950/50 border border-white/10 rounded-sm p-4">
            <div className="flex items-center gap-2 text-xs text-slate-500 mb-2">
              <DollarSign className="w-3 h-3" />
              <span className="uppercase tracking-wider">Avg Price</span>
            </div>
            <div className="text-2xl font-bold text-white">
              {data.current.avg_price ? `$${data.current.avg_price.toFixed(2)}` : 'N/A'}
            </div>
          </div>

          <div className="bg-zinc-950/50 border border-white/10 rounded-sm p-4">
            <div className="flex items-center gap-2 text-xs text-slate-500 mb-2">
              <Clock className="w-3 h-3" />
              <span className="uppercase tracking-wider">Supply</span>
            </div>
            <div className="text-2xl font-bold text-white">{data.current.supply}</div>
          </div>
        </section>

        {/* Trend Metrics */}
        {data.trend && (
          <section className="bg-zinc-950/50 border border-white/10 rounded-sm p-5">
            <h2 className="text-white font-bold uppercase tracking-wider mb-4 flex items-center gap-2">
              {data.trend.direction === 'BULLISH' ? (
                <TrendingUp className="w-4 h-4 text-emerald-500" />
              ) : (
                <TrendingDown className="w-4 h-4 text-red-500" />
              )}
              Trend Analysis
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <div className="text-xs text-slate-500 mb-1">7-Day Momentum</div>
                <div className={`text-lg font-bold ${
                  data.trend.momentum_7d > 0 ? 'text-emerald-400' : 'text-red-400'
                }`}>
                  {data.trend.momentum_7d > 0 ? '+' : ''}{data.trend.momentum_7d.toFixed(2)}%
                </div>
              </div>
              <div>
                <div className="text-xs text-slate-500 mb-1">30-Day Momentum</div>
                <div className={`text-lg font-bold ${
                  data.trend.momentum_30d > 0 ? 'text-emerald-400' : 'text-red-400'
                }`}>
                  {data.trend.momentum_30d > 0 ? '+' : ''}{data.trend.momentum_30d.toFixed(2)}%
                </div>
              </div>
              <div>
                <div className="text-xs text-slate-500 mb-1">7-Day Moving Avg</div>
                <div className="text-lg font-bold text-white">
                  {data.trend.ma_7d.toFixed(1)}%
                </div>
              </div>
              <div>
                <div className="text-xs text-slate-500 mb-1">Volatility</div>
                <div className="text-lg font-bold text-yellow-400">
                  {data.trend.volatility.toFixed(2)}%
                </div>
              </div>
            </div>
          </section>
        )}

        {/* Anomaly Alert */}
        {data.anomaly && (
          <section className={`border rounded-sm p-5 ${
            data.anomaly.severity === 'CRITICAL' ? 'bg-red-500/10 border-red-500/50' :
            data.anomaly.severity === 'HIGH' ? 'bg-orange-500/10 border-orange-500/50' :
            'bg-yellow-500/10 border-yellow-500/50'
          }`}>
            <div className="flex items-start gap-3">
              <AlertTriangle className={`w-5 h-5 mt-0.5 ${
                data.anomaly.severity === 'CRITICAL' ? 'text-red-400' :
                data.anomaly.severity === 'HIGH' ? 'text-orange-400' :
                'text-yellow-400'
              }`} />
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-xs font-bold uppercase tracking-wider">
                    [{data.anomaly.severity}] {data.anomaly.type}
                  </span>
                  <span className="text-xs text-slate-500">
                    Detected: {new Date(data.anomaly.detected_at).toLocaleString()}
                  </span>
                </div>
                <p className="text-sm">{data.anomaly.message}</p>
              </div>
            </div>
          </section>
        )}

        {/* History Chart */}
        <section className="bg-zinc-950/50 border border-white/10 rounded-sm p-5">
          <h2 className="text-white font-bold uppercase tracking-wider mb-4">
            Historical Performance
          </h2>
          <div className="h-[300px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={data.history}>
                <defs>
                  <linearGradient id="colorStr" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#0ea5e9" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#0ea5e9" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="1 1" stroke="#333" />
                <XAxis
                  dataKey="date"
                  tick={{ fill: '#666', fontSize: 10 }}
                  tickFormatter={(val) => new Date(val).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                />
                <YAxis tick={{ fill: '#666', fontSize: 10 }} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#000', borderColor: '#333', color: '#fff' }}
                  labelFormatter={(val) => new Date(val).toLocaleDateString()}
                  formatter={(val: number | undefined) => val !== undefined ? [`${val.toFixed(1)}%`, 'STR'] : ['', '']}
                />
                <Legend />
                <Area
                  type="monotone"
                  dataKey="str"
                  stroke="#0ea5e9"
                  fillOpacity={1}
                  fill="url(#colorStr)"
                  name="Sell-Through Rate"
                />
                <Area
                  type="monotone"
                  dataKey="volume"
                  stroke="#a855f7"
                  fillOpacity={0.1}
                  name="Volume"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </section>

        {/* Forecast */}
        {data.forecast && (
          <section className="bg-zinc-950/50 border border-white/10 rounded-sm p-5">
            <h2 className="text-white font-bold uppercase tracking-wider mb-4">
              Forecast
            </h2>
            <div className="flex items-center gap-4 mb-4 text-xs">
              <span className="text-slate-500">Model: {data.forecast.model}</span>
              <span className={`font-bold ${
                data.forecast.confidence > 0.8 ? 'text-emerald-400' :
                data.forecast.confidence > 0.6 ? 'text-yellow-400' :
                'text-red-400'
              }`}>
                Confidence: {(data.forecast.confidence * 100).toFixed(0)}%
              </span>
            </div>
            <div className="h-[250px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={[...data.history, ...data.forecast.predictions.map(p => ({
                  date: p.date,
                  str: p.predicted_str,
                  isForecast: true
                  }
                ))]}>
                  <CartesianGrid strokeDasharray="1 1" stroke="#333" />
                  <XAxis
                    dataKey="date"
                    tick={{ fill: '#666', fontSize: 10 }}
                    tickFormatter={(val) => new Date(val).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                  />
                  <YAxis tick={{ fill: '#666', fontSize: 10 }} />
                  <Tooltip
                    contentStyle={{ backgroundColor: '#000', borderColor: '#333', color: '#fff' }}
                    labelFormatter={(val) => new Date(val).toLocaleDateString()}
                    formatter={(val: number | undefined, name: string | undefined, props: any) => {
                      const isForecast = props.payload?.isForecast;
                      return val !== undefined ? [
                        `${val.toFixed(1)}%`,
                        isForecast ? 'Forecast' : 'Actual'
                      ] : ['', ''];
                    }}
                  />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="str"
                    stroke="#0ea5e9"
                    strokeWidth={2}
                    dot={false}
                    name="Actual STR"
                    connectNulls={false}
                  />
                  <Line
                    type="monotone"
                    dataKey="str"
                    stroke="#a855f7"
                    strokeWidth={2}
                    strokeDasharray="5 5"
                    dot={false}
                    name="Forecast"
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}
