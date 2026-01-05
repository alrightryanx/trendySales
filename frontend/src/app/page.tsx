"use client";

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from 'recharts';
import {
  Activity, Zap, Globe, Layers, Terminal,
  TrendingUp, Cloud
} from 'lucide-react';
import Ticker from '@/components/Ticker';

// --- Types ---
type TrendMetric = {
  keyword: string;
  category: string;
  velocity: number;
  volume: number;
  sentiment: string;
};

type PlatformData = {
  platform: string;
  activity_score: number;
  role: string;
};

type Signal = {
  timestamp: string;
  message: string;
  level: "INFO" | "WARNING" | "CRITICAL";
};

type Pulse = {
  global_velocity_index: number;
  active_narratives: number;
  scanned_nodes: string;
  system_status: string;
};

type CloudItem = {
  text: string;
  value: number;
};

export default function Dashboard() {
  const router = useRouter();
  const [trends, setTrends] = useState<TrendMetric[]>([]);
  const [platforms, setPlatforms] = useState<PlatformData[]>([]);
  const [signals, setSignals] = useState<Signal[]>([]);
  const [pulse, setPulse] = useState<Pulse | null>(null);
  const [keywords, setKeywords] = useState<CloudItem[]>([]);

  // Independent fetch functions for non-blocking UI
  const fetchTrends = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/trends');
      const data = await res.json();
      setTrends(data);
    } catch (e) { console.error("Trend Fetch Error", e); }
  };

  const fetchPlatforms = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/platforms');
      const data = await res.json();
      setPlatforms(data);
    } catch (e) { console.error("Platform Fetch Error", e); }
  };

  const fetchSignals = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/signals');
      const data = await res.json();
      setSignals(data);
    } catch (e) { console.error("Signal Fetch Error", e); }
  };

  const fetchPulse = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/pulse');
      const data = await res.json();
      setPulse(data);
    } catch (e) { console.error("Pulse Fetch Error", e); }
  };

  const fetchKeywords = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/keywords');
      const data = await res.json();
      setKeywords(data);
    } catch (e) { console.error("Keyword Fetch Error", e); }
  };

  const handleItemClick = (keyword: string) => {
    router.push(`/items/${encodeURIComponent(keyword)}`);
  };

  useEffect(() => {
    // Initial Load - Fire all requests in parallel
    fetchSignals();
    fetchPulse();
    fetchTrends();
    fetchPlatforms();
    fetchKeywords();

    // Specific intervals for different data freshness needs
    const fastInterval = setInterval(() => {
        fetchSignals();
        fetchPulse();
    }, 5000); // 5s for fast data

    const slowInterval = setInterval(() => {
        fetchTrends();
        fetchPlatforms();
        fetchKeywords();
    }, 30000); // 30s for heavy scraping

    return () => {
        clearInterval(fastInterval);
        clearInterval(slowInterval);
    };
  }, []);

  return (
    <div className="min-h-screen bg-black text-slate-300 font-mono text-sm selection:bg-yellow-500/30 selection:text-yellow-200">

      {/* --- TICKER --- */}
      <Ticker />

      {/* --- HEADER --- */}
      <header className="border-b border-white/10 bg-black/50 backdrop-blur-sm sticky top-12 z-50">
        <div className="max-w-[1600px] mx-auto px-6 h-14 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="w-3 h-3 bg-yellow-500 rounded-sm animate-pulse" />
            <h1 className="text-base font-bold tracking-widest text-white uppercase">
              Omniscient <span className="text-yellow-500">PRIME</span>
            </h1>
          </div>

          <div className="flex items-center gap-6">
            <nav className="flex items-center gap-4">
              <a
                href="/"
                className="text-xs text-yellow-500 uppercase tracking-wider hover:text-yellow-400 transition-colors"
              >
                Dashboard
              </a>
              <a
                href="/arbitrage"
                className="text-xs text-slate-500 uppercase tracking-wider hover:text-slate-300 transition-colors"
              >
                Arbitrage
              </a>
              <a
                href="/niche"
                className="text-xs text-slate-500 uppercase tracking-wider hover:text-slate-300 transition-colors"
              >
                Niche Hunter
              </a>
            </nav>

            <div className="flex items-center gap-4 text-xs text-slate-500 uppercase tracking-wider">
               <div className="flex items-center gap-2">
                 <Activity className="w-4 h-4 text-cyan-500" />
                 <span>Nodes: {pulse?.scanned_nodes || "---"}</span>
               </div>
               <div className="flex items-center gap-2">
                 <Layers className="w-4 h-4 text-purple-500" />
                 <span>Narratives: {pulse?.active_narratives || "---"}</span>
               </div>
               <div className="px-2 py-1 bg-white/5 border border-white/10 text-white rounded-sm">
                 STATUS: {pulse?.system_status || "INIT"}
               </div>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-[1600px] mx-auto px-6 py-6 grid grid-cols-12 gap-6">
        
        {/* --- LEFT COLUMN: TOP TRENDS (4 cols) --- */}
        <section className="col-span-12 lg:col-span-4 flex flex-col gap-6">
          <div className="bg-zinc-950/50 border border-white/10 rounded-sm p-5 h-full">
            <h2 className="text-white font-bold uppercase tracking-wider mb-6 flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-yellow-500" />
              Velocity Leaders (eBay)
            </h2>
            <div className="space-y-4">
              {trends.length === 0 ? <div className="text-xs text-slate-600 animate-pulse">Scanning eBay Nodes (Approx 5s)...</div> : null}
              {trends.map((t, i) => (
                <div
                  key={i}
                  onClick={() => handleItemClick(t.keyword)}
                  className="group relative p-3 border border-white/5 hover:border-yellow-500/50 bg-white/0 hover:bg-white/5 transition-all cursor-pointer"
                >
                  <div className="flex justify-between items-start mb-2">
                    <span className="text-white font-bold">{t.keyword}</span>
                    <span className={`text-xs px-1.5 py-0.5 border ${t.velocity > 50 ? 'border-cyan-500/30 text-cyan-400' : 'border-slate-500/30 text-slate-400'}`}>
                      STR: {t.velocity.toFixed(1)}%
                    </span>
                  </div>
                  <div className="flex justify-between items-center text-xs text-slate-500">
                    <span>{t.category}</span>
                    <span>Sold: {t.volume}</span>
                  </div>
                  {/* Progress Bar for STR */}
                  <div className="w-full h-0.5 bg-white/10 mt-3">
                    <div
                      className="h-full bg-cyan-500 group-hover:bg-cyan-400 transition-all"
                      style={{ width: `${Math.min(t.velocity, 100)}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* --- CENTER COLUMN: VISUALIZATIONS (5 cols) --- */}
        <section className="col-span-12 lg:col-span-5 flex flex-col gap-6">
          
          {/* Keyword Cloud */}
          <div className="bg-zinc-950/50 border border-white/10 rounded-sm p-5 min-h-[300px]">
            <h2 className="text-white font-bold uppercase tracking-wider mb-2 flex items-center gap-2">
              <Cloud className="w-4 h-4 text-purple-500" />
              Narrative Cloud (Reddit)
            </h2>
            <p className="text-xs text-slate-600 mb-6">Extraction from r/forhire [Hiring] posts</p>
            <div className="flex flex-wrap gap-2 content-start">
               {keywords.length === 0 ? <div className="text-xs text-slate-600 animate-pulse">Parsing Narrative Streams...</div> : null}
               {keywords.map((k, i) => {
                 // Dynamic styling based on weight
                 const size = Math.min(Math.max(k.value * 2, 10), 24); // Min 10px, Max 24px
                 const opacity = Math.min(Math.max(k.value / 5, 0.4), 1);
                 const isHot = k.value > 5;
                 
                 return (
                   <span 
                     key={i}
                     className={`cursor-default transition-colors hover:text-white ${isHot ? 'text-purple-400' : 'text-slate-500'}`}
                     style={{ fontSize: `${size}px`, opacity: opacity }}
                     title={`Mentioned ${k.value} times`}
                   >
                     {k.text}
                   </span>
                 )
               })}
            </div>
          </div>

          {/* Trend Radar */}
          <div className="bg-zinc-950/50 border border-white/10 rounded-sm p-5 flex-1">
             <h2 className="text-white font-bold uppercase tracking-wider mb-4 flex items-center gap-2">
               <Zap className="w-4 h-4 text-cyan-500" />
               Saturation Radar
             </h2>
             <div className="h-[200px] w-full">
               <ResponsiveContainer width="100%" height="100%">
                 <BarChart data={trends} layout="vertical" margin={{ left: 0 }}>
                   <CartesianGrid strokeDasharray="1 1" stroke="#333" horizontal={false} />
                   <XAxis type="number" hide />
                   <YAxis dataKey="keyword" type="category" width={100} tick={{fill: '#666', fontSize: 10}} hide />
                   <Tooltip 
                     cursor={{fill: 'transparent'}}
                     contentStyle={{ backgroundColor: '#000', borderColor: '#333', color: '#fff' }}
                   />
                   <Bar dataKey="velocity" fill="#0ea5e9" barSize={20} radius={[0, 4, 4, 0]} />
                 </BarChart>
               </ResponsiveContainer>
             </div>
          </div>
        </section>

        {/* --- RIGHT COLUMN: LIVE SIGNALS (3 cols) --- */}
        <section className="col-span-12 lg:col-span-3 flex flex-col gap-6">
           {/* Platform Heatmap */}
           <div className="bg-zinc-950/50 border border-white/10 rounded-sm p-5">
             <h2 className="text-white font-bold uppercase tracking-wider mb-4 flex items-center gap-2">
               <Globe className="w-4 h-4 text-emerald-500" />
               Platform Health
             </h2>
             <div className="space-y-5">
                {platforms.length === 0 ? <div className="text-xs text-slate-600 animate-pulse">Ping: r/forhire...</div> : null}
                {platforms.map((p, i) => (
                  <div key={i}>
                    <div className="flex justify-between text-xs mb-1">
                      <span className="text-slate-400">{p.platform}</span>
                      <span className="text-white text-[10px]">{p.role}</span>
                    </div>
                    <div className="w-full bg-white/5 h-1.5 rounded-full overflow-hidden">
                       <div 
                         className={`h-full ${p.activity_score > 50 ? 'bg-emerald-500' : 'bg-red-500'}`} 
                         style={{ width: `${p.activity_score}%` }}
                       />
                    </div>
                  </div>
                ))}
             </div>
           </div>

           <div className="bg-zinc-950/50 border border-white/10 rounded-sm p-5 h-full flex flex-col">
              <h2 className="text-white font-bold uppercase tracking-wider mb-6 flex items-center gap-2">
                <Terminal className="w-4 h-4 text-yellow-500" />
                Live Signal Feed
              </h2>
              <div className="flex-1 overflow-y-auto space-y-4 font-mono text-xs pr-2 custom-scrollbar">
                 {signals.map((sig, i) => (
                   <div key={i} className="border-l-2 border-white/10 pl-3 py-1">
                     <div className="text-slate-600 mb-1">{sig.timestamp}</div>
                     <div className={`mb-1 ${
                       sig.level === 'CRITICAL' ? 'text-red-400' : 
                       sig.level === 'WARNING' ? 'text-yellow-400' : 'text-slate-300'
                     }`}>
                       [{sig.level}]
                     </div>
                     <div className="text-slate-400 leading-relaxed">
                       {sig.message}
                     </div>
                   </div>
                 ))}
              </div>
           </div>
        </section>

      </main>
    </div>
  );
}
