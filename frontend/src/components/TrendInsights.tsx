"use client";

import React, { useState, useEffect } from 'react';
import {
  TrendingUp, Search, Home, Car, Cpu, Bot,
  BarChart3, Globe, ArrowUpRight, Activity,
  Flame, Zap, Target
} from 'lucide-react';

type TrendCategory = 'google' | 'home_sales' | 'car_sales' | 'ai' | 'robotics';

type TrendData = {
  term: string;
  growth: number;
  volume: number;
  category: string;
  trend: 'UP' | 'DOWN' | 'FLAT';
  spike: number;
  related: string[];
};

type CategoryInsights = {
  category: TrendCategory;
  icon: React.ReactNode;
  color: string;
  name: string;
  description: string;
  topTrends: TrendData[];
  overallGrowth: number;
};

export default function TrendInsights() {
  const [activeCategory, setActiveCategory] = useState<TrendCategory>('google');
  const [loading, setLoading] = useState(true);
  const [insights, setInsights] = useState<Record<TrendCategory, CategoryInsights>>({} as any);

  useEffect(() => {
    const fetchTrends = async () => {
      setLoading(true);

      // Simulate API data fetching
      await new Promise(resolve => setTimeout(resolve, 600));

      const mockInsights: Record<TrendCategory, CategoryInsights> = {
        google: {
          category: 'google',
          icon: <Globe className="w-4 h-4" />,
          color: 'text-blue-400',
          name: 'Google Trends',
          description: 'Global search interest and trending topics',
          overallGrowth: 12.5,
          topTrends: [
            { term: 'AI Video Generation', growth: 245, volume: 95000, category: 'Technology', trend: 'UP', spike: 180, related: ['Sora', 'Runway', 'Midjourney'] },
            { term: 'Electric SUV Reviews', growth: 185, volume: 78000, category: 'Automotive', trend: 'UP', spike: 145, related: ['Tesla', 'Rivian', 'Lucid'] },
            { term: 'Smart Home Setup', growth: 120, volume: 65000, category: 'Home', trend: 'UP', spike: 95, related: ['Matter Protocol', 'Home Assistant', 'Zigbee'] },
            { term: 'Sustainable Fashion', growth: 95, volume: 48000, category: 'Fashion', trend: 'UP', spike: 72, related: ['Patagonia', 'Everlane', 'Reformation'] },
            { term: 'Virtual Fitness', growth: 88, volume: 42000, category: 'Health', trend: 'UP', spike: 65, related: ['Oura Ring', 'Peloton', 'Tonal'] },
            { term: 'Plant-Based Meal Kits', growth: 76, volume: 35000, category: 'Food', trend: 'UP', spike: 54, related: ['HelloFresh', 'Daily Harvest', 'Green Chef'] },
            { term: 'Minimalist Home Design', growth: 68, volume: 32000, category: 'Home', trend: 'UP', spike: 48, related: ['Japandi', 'Hygge', 'Wabi-Sabi'] },
            { term: 'Remote Work Tools 2024', growth: 62, volume: 29000, category: 'Technology', trend: 'UP', spike: 42, related: ['Notion', 'Slack', 'Asana'] }
          ]
        },
        home_sales: {
          category: 'home_sales',
          icon: <Home className="w-4 h-4" />,
          color: 'text-emerald-400',
          name: 'Home Sales Market',
          description: 'Real estate and home buying trends',
          overallGrowth: 8.3,
          topTrends: [
            { term: 'Smart Home Integration', growth: 145, volume: 85000, category: 'Tech', trend: 'UP', spike: 110, related: ['Lutron', 'Control4', 'Savant'] },
            { term: 'Energy Efficient HVAC', growth: 135, volume: 72000, category: 'Systems', trend: 'UP', spike: 102, related: ['Heat Pumps', 'Geothermal', 'Solar Integration'] },
            { term: 'ADUs & Accessory Dwelling', growth: 125, volume: 64000, category: 'Property', trend: 'UP', spike: 95, related: ['Prefab ADUs', 'Tiny Homes', 'Granny Flats'] },
            { term: 'Sustainable Building Materials', growth: 118, volume: 58000, category: 'Construction', trend: 'UP', spike: 88, related: ['Bamboo', 'Recycled Steel', 'Hempcrete'] },
            { term: 'Home Office Setup', growth: 98, volume: 52000, category: 'Remote Work', trend: 'UP', spike: 74, related: ['Standing Desks', 'Ergonomic Chairs', 'Acoustic Panels'] },
            { term: 'Outdoor Living Spaces', growth: 92, volume: 48000, category: 'Lifestyle', trend: 'UP', spike: 68, related: ['Decks', 'Patios', 'Outdoor Kitchens'] },
            { term: 'Smart Security Systems', growth: 85, volume: 45000, category: 'Security', trend: 'UP', spike: 62, related: ['Ring', 'Nest', 'Arlo'] },
            { term: 'Water Conservation Systems', growth: 78, volume: 42000, category: 'Sustainability', trend: 'UP', spike: 56, related: ['Rain Harvesting', 'Greywater', 'Smart Irrigation'] }
          ]
        },
        car_sales: {
          category: 'car_sales',
          icon: <Car className="w-4 h-4" />,
          color: 'text-cyan-400',
          name: 'Automotive Market',
          description: 'Vehicle sales and automotive trends',
          overallGrowth: 15.7,
          topTrends: [
            { term: 'Electric Pickup Trucks', growth: 245, volume: 125000, category: 'EV', trend: 'UP', spike: 195, related: ['Ford F-150 Lightning', 'Rivian R1T', 'Tesla Cybertruck'] },
            { term: 'Hybrid SUVs', growth: 210, volume: 108000, category: 'Hybrid', trend: 'UP', spike: 175, related: ['Toyota RAV4 Hybrid', 'Honda CR-V Hybrid', 'Ford Escape Hybrid'] },
            { term: 'Compact EVs', growth: 185, volume: 95000, category: 'EV', trend: 'UP', spike: 152, related: ['Tesla Model 3', 'Chevy Bolt', 'Hyundai Ioniq 5'] },
            { term: 'Luxury EV Market', growth: 165, volume: 78000, category: 'Luxury', trend: 'UP', spike: 135, related: ['Lucid Air', 'Porsche Taycan', 'Mercedes EQS'] },
            { term: 'Autonomous Features', growth: 145, volume: 68000, category: 'Technology', trend: 'UP', spike: 118, related: ['FSD', 'Super Cruise', 'Highway Assist'] },
            { term: 'Subscription Car Services', growth: 125, volume: 56000, category: 'Service', trend: 'UP', spike: 98, related: ['Care by Volvo', 'Polestar Subscription', 'Genesis Access'] },
            { term: 'Vintage Car Market', growth: 112, volume: 49000, category: 'Classic', trend: 'UP', spike: 88, related: ['Japanese Classics', 'European Sports Cars', 'Muscle Cars'] },
            { term: 'Commercial EVs', growth: 98, volume: 45000, category: 'Commercial', trend: 'UP', spike: 76, related: ['Delivery Vans', 'Semi Trucks', 'Electric Buses'] }
          ]
        },
        ai: {
          category: 'ai',
          icon: <Cpu className="w-4 h-4" />,
          color: 'text-purple-400',
          name: 'AI & Machine Learning',
          description: 'Artificial intelligence and automation trends',
          overallGrowth: 285,
          topTrends: [
            { term: 'Multimodal AI', growth: 485, volume: 185000, category: 'Foundation Models', trend: 'UP', spike: 385, related: ['GPT-4V', 'Gemini Ultra', 'Claude 3'] },
            { term: 'AI Code Assistants', growth: 395, volume: 165000, category: 'Development', trend: 'UP', spike: 325, related: ['Copilot', 'Cursor', 'Codeium'] },
            { term: 'Generative Video AI', growth: 365, volume: 148000, category: 'Content Creation', trend: 'UP', spike: 295, related: ['Sora', 'Runway Gen-2', 'Pika Labs'] },
            { term: 'Edge AI Deployment', growth: 285, volume: 125000, category: 'Infrastructure', trend: 'UP', spike: 235, related: ['ONNX Runtime', 'TensorFlow Lite', 'OpenVINO'] },
            { term: 'AI Safety & Governance', growth: 245, volume: 105000, category: 'Policy', trend: 'UP', spike: 198, related: ['AI Ethics', 'Bias Detection', 'Explainable AI'] },
            { term: 'AI-Powered Search', growth: 225, volume: 95000, category: 'Search', trend: 'UP', spike: 182, related: ['Perplexity', 'Bing Chat', 'Google SGE'] },
            { term: 'Custom AI Agents', growth: 198, volume: 85000, category: 'Automation', trend: 'UP', spike: 162, related: ['AutoGPT', 'BabyAGI', 'CrewAI'] },
            { term: 'AI Hardware Acceleration', growth: 185, volume: 78000, category: 'Hardware', trend: 'UP', spike: 148, related: ['TPUs', 'GPUs', 'NPUs'] }
          ]
        },
        robotics: {
          category: 'robotics',
          icon: <Bot className="w-4 h-4" />,
          color: 'text-yellow-400',
          name: 'Robotics & Automation',
          description: 'Robotics systems and automation trends',
          overallGrowth: 142,
          topTrends: [
            { term: 'Humanoid Robots', growth: 425, volume: 145000, category: 'Humanoids', trend: 'UP', spike: 345, related: ['Tesla Optimus', 'Figure AI', 'Agility Robotics'] },
            { term: 'Warehouse Automation', growth: 365, volume: 125000, category: 'Logistics', trend: 'UP', spike: 298, related: ['Amazon Robotics', 'Locus Robotics', 'Zebra Automation'] },
            { term: 'Collaborative Robots', growth: 325, volume: 108000, category: 'Cobots', trend: 'UP', spike: 265, related: ['Universal Robots', 'FANUC CRX', 'Doosan Cobots'] },
            { term: 'Medical Robotics', growth: 295, volume: 95000, category: 'Healthcare', trend: 'UP', spike: 238, related: ['Surgical Robots', 'Rehabilitation', 'Diagnostic Bots'] },
            { term: 'Agricultural Robots', growth: 265, volume: 82000, category: 'AgTech', trend: 'UP', spike: 212, related: ['Autonomous Tractors', 'Harvesting Robots', 'Drone Sprayers'] },
            { term: 'Service Robots', growth: 235, volume: 72000, category: 'Service', trend: 'UP', spike: 188, related: ['Delivery Drones', 'Cleaning Robots', 'Hospitality Bots'] },
            { term: 'Robotics Software Platforms', growth: 205, volume: 65000, category: 'Software', trend: 'UP', spike: 165, related: ['ROS 2', 'MoveIt', 'Gazebo'] },
            { term: 'End-Effector Innovations', growth: 185, volume: 58000, category: 'Components', trend: 'UP', spike: 148, related: ['Soft Robotics', 'Adaptive Grippers', 'Tactile Sensors'] }
          ]
        }
      };

      setInsights(mockInsights);
      setLoading(false);
    };

    fetchTrends();

    // Refresh every 60 seconds
    const interval = setInterval(fetchTrends, 60000);

    return () => clearInterval(interval);
  }, []);

  const categories: Array<{ key: TrendCategory; label: string; icon: React.ReactNode }> = [
    { key: 'google', label: 'Google Trends', icon: <Globe className="w-4 h-4" /> },
    { key: 'home_sales', label: 'Home Sales', icon: <Home className="w-4 h-4" /> },
    { key: 'car_sales', label: 'Car Sales', icon: <Car className="w-4 h-4" /> },
    { key: 'ai', label: 'AI & ML', icon: <Cpu className="w-4 h-4" /> },
    { key: 'robotics', label: 'Robotics', icon: <Bot className="w-4 h-4" /> },
  ];

  const activeInsight = insights[activeCategory];

  if (loading || !activeInsight) {
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
      {/* Category Selector */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-white font-bold uppercase tracking-wider flex items-center gap-2">
          <BarChart3 className="w-4 h-4 text-yellow-500" />
          Trend Insights
        </h2>
      </div>

      {/* Category Tabs */}
      <div className="grid grid-cols-5 gap-2 mb-6">
        {categories.map((cat) => (
          <button
            key={cat.key}
            onClick={() => setActiveCategory(cat.key)}
            className={`flex flex-col items-center gap-2 p-3 rounded-sm border transition-all ${
              activeCategory === cat.key
                ? `bg-white/10 border-${cat.key === 'ai' ? 'purple' : cat.key === 'robotics' ? 'yellow' : cat.key === 'car_sales' ? 'cyan' : cat.key === 'home_sales' ? 'emerald' : 'blue'}-500/50`
                : 'border-white/5 bg-white/0 hover:bg-white/5'
            }`}
          >
            <div className={`${
              activeCategory === cat.key
                ? insights[cat.key]?.color || 'text-slate-400'
                : 'text-slate-500'
            }`}>
              {cat.icon}
            </div>
            <span className={`text-xs uppercase tracking-wider ${
              activeCategory === cat.key ? 'text-white' : 'text-slate-500'
            }`}>
              {cat.label}
            </span>
          </button>
        ))}
      </div>

      {/* Active Category Header */}
      <div className="flex items-center justify-between mb-4 pb-4 border-b border-white/10">
        <div className="flex items-center gap-3">
          <div className={`p-2 bg-white/5 rounded-sm ${activeInsight.color}`}>
            {activeInsight.icon}
          </div>
          <div>
            <h3 className="text-white font-bold text-lg">{activeInsight.name}</h3>
            <p className="text-xs text-slate-500">{activeInsight.description}</p>
          </div>
        </div>
        <div className="text-right">
          <div className={`text-2xl font-bold ${activeInsight.overallGrowth > 100 ? 'text-emerald-400' : 'text-cyan-400'}`}>
            +{activeInsight.overallGrowth}%
          </div>
          <div className="text-xs text-slate-500 uppercase tracking-wider">Growth</div>
        </div>
      </div>

      {/* Trending Items */}
      <div className="flex-1 overflow-y-auto space-y-3 custom-scrollbar">
        {activeInsight.topTrends.map((trend, i) => (
          <div
            key={i}
            className="border border-white/5 hover:border-yellow-500/30 bg-white/0 hover:bg-white/5 transition-all p-4 rounded-sm"
          >
            <div className="flex items-start justify-between mb-3">
              <div className="flex-1">
                <h4 className="text-white font-bold text-sm mb-1">{trend.term}</h4>
                <div className="flex items-center gap-3 text-xs text-slate-500">
                  <span>{trend.category}</span>
                  <span>•</span>
                  <span className="text-slate-400">Volume: {trend.volume.toLocaleString()}</span>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <div className="text-right">
                  <div className={`text-xl font-bold ${trend.growth > 200 ? 'text-emerald-400' : trend.growth > 100 ? 'text-cyan-400' : 'text-yellow-400'}`}>
                    +{trend.growth}%
                  </div>
                  <div className="text-xs text-slate-600 uppercase tracking-wider">Growth</div>
                </div>
                {trend.spike > 100 && (
                  <div className="flex flex-col items-center">
                    <Flame className="w-5 h-5 text-orange-500" />
                    <span className="text-[10px] text-orange-500 font-bold">SPIKE</span>
                  </div>
                )}
              </div>
            </div>

            {/* Growth Bar */}
            <div className="w-full bg-white/5 h-1.5 rounded-full overflow-hidden mb-3">
              <div
                className={`h-full transition-all ${
                  trend.growth > 200 ? 'bg-gradient-to-r from-emerald-500 to-green-400' :
                  trend.growth > 100 ? 'bg-gradient-to-r from-cyan-500 to-blue-400' :
                  'bg-gradient-to-r from-yellow-500 to-orange-400'
                }`}
                style={{ width: `${Math.min(trend.growth / 5, 100)}%` }}
              />
            </div>

            {/* Related Terms */}
            <div className="flex items-center gap-2 mb-3">
              <Target className="w-3 h-3 text-slate-500" />
              <span className="text-xs text-slate-500 uppercase tracking-wider">Related:</span>
              <div className="flex flex-wrap gap-2">
                {trend.related.map((term, j) => (
                  <span
                    key={j}
                    className="text-xs px-2 py-0.5 bg-white/5 border border-white/10 rounded-sm text-slate-400 hover:text-slate-300 hover:border-white/20 transition-colors cursor-default"
                  >
                    {term}
                  </span>
                ))}
              </div>
            </div>

            {/* Trend Direction */}
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2 text-xs">
                {trend.trend === 'UP' ? (
                  <>
                    <TrendingUp className="w-3 h-3 text-emerald-500" />
                    <span className="text-emerald-500 font-bold">RISING TREND</span>
                  </>
                ) : trend.trend === 'DOWN' ? (
                  <>
                    <TrendingUp className="w-3 h-3 text-red-500 rotate-180" />
                    <span className="text-red-500 font-bold">DECLINING</span>
                  </>
                ) : (
                  <>
                    <Activity className="w-3 h-3 text-slate-500" />
                    <span className="text-slate-500">STABLE</span>
                  </>
                )}
              </div>
              {trend.growth > 150 && (
                <div className="flex items-center gap-1 text-xs text-emerald-500 bg-emerald-500/10 px-2 py-1 rounded-sm">
                  <Zap className="w-3 h-3" />
                  <span className="font-bold">HIGH INTEREST</span>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
