"use client";

import React, { useState, useEffect } from 'react';
import {
  Sparkles, TrendingUp, AlertTriangle, Clock, Target,
  DollarSign, ArrowRight, Zap
} from 'lucide-react';

type OpportunityCard = {
  id: string;
  title: string;
  insight: string;
  confidence: number;
  impact: 'HIGH' | 'MEDIUM' | 'LOW';
  category: 'VELOCITY' | 'SATURATION' | 'ANOMALY' | 'FORECAST';
  metrics: {
    keyword: string;
    current_str: number;
    change: number;
    timeframe: string;
  };
  action?: string;
  timestamp: string;
};

export default function OpportunityCards() {
  const [opportunities, setOpportunities] = useState<OpportunityCard[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate AI-powered opportunity cards
    const generateCards = () => {
      const cards: OpportunityCard[] = [
        {
          id: '1',
          title: 'Vintage Digital Camera Surge',
          insight: 'Vintage digital cameras are selling 40% faster this week in NYC metro area. Average prices increased 15%.',
          confidence: 0.92,
          impact: 'HIGH',
          category: 'VELOCITY',
          metrics: {
            keyword: 'Vintage Digital Camera',
            current_str: 78.5,
            change: 40,
            timeframe: '7 days'
          },
          action: 'Consider sourcing from local markets and listing on eBay',
          timestamp: new Date().toISOString()
        },
        {
          id: '2',
          title: 'Carhartt Jacket Opportunity',
          insight: 'Carhartt Detroit Jackets showing unusually high sell-through rate in Portland area with low competition.',
          confidence: 0.88,
          impact: 'HIGH',
          category: 'SATURATION',
          metrics: {
            keyword: 'Carhartt Detroit Jacket',
            current_str: 85.2,
            change: 25,
            timeframe: '5 days'
          },
          action: 'Target local thrift stores and FB Marketplace',
          timestamp: new Date().toISOString()
        },
        {
          id: '3',
          title: 'Anomaly Detected: Analogue Pocket',
          insight: 'Analogue Pocket pricing anomaly detected. Current listings selling 35% above 30-day average.',
          confidence: 0.85,
          impact: 'MEDIUM',
          category: 'ANOMALY',
          metrics: {
            keyword: 'Analogue Pocket',
            current_str: 62.1,
            change: 35,
            timeframe: '24h'
          },
          action: 'Act quickly before prices normalize',
          timestamp: new Date().toISOString()
        },
        {
          id: '4',
          title: 'Forecast: Gaming Consoles',
          insight: 'Gaming consoles predicted to see 22% STR increase over next 14 days based on historical patterns.',
          confidence: 0.76,
          impact: 'MEDIUM',
          category: 'FORECAST',
          metrics: {
            keyword: 'Gaming Consoles',
            current_str: 54.3,
            change: 22,
            timeframe: '14 days'
          },
          action: 'Start building inventory now',
          timestamp: new Date().toISOString()
        },
        {
          id: '5',
          title: 'Birkenstock Boston Demand',
          insight: 'Birkenstock Boston clogs experiencing early spring demand spike. STR up 18% week-over-week.',
          confidence: 0.82,
          impact: 'MEDIUM',
          category: 'VELOCITY',
          metrics: {
            keyword: 'Birkenstock Boston',
            current_str: 71.8,
            change: 18,
            timeframe: '7 days'
          },
          action: 'Source from European markets for better margins',
          timestamp: new Date().toISOString()
        }
      ];

      setOpportunities(cards);
      setLoading(false);
    };

    generateCards();

    // Refresh opportunities periodically
    const interval = setInterval(generateCards, 60000); // Every minute

    return () => clearInterval(interval);
  }, []);

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'VELOCITY':
        return <Zap className="w-4 h-4 text-cyan-500" />;
      case 'SATURATION':
        return <TrendingUp className="w-4 h-4 text-emerald-500" />;
      case 'ANOMALY':
        return <AlertTriangle className="w-4 h-4 text-yellow-500" />;
      case 'FORECAST':
        return <Clock className="w-4 h-4 text-purple-500" />;
      default:
        return <Sparkles className="w-4 h-4 text-slate-500" />;
    }
  };

  const getImpactColor = (impact: string) => {
    switch (impact) {
      case 'HIGH':
        return 'border-red-500/50 bg-red-500/10';
      case 'MEDIUM':
        return 'border-yellow-500/50 bg-yellow-500/10';
      case 'LOW':
        return 'border-slate-500/50 bg-slate-500/10';
      default:
        return 'border-slate-500/50';
    }
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return 'text-emerald-400';
    if (confidence >= 0.6) return 'text-yellow-400';
    return 'text-red-400';
  };

  if (loading) {
    return (
      <div className="bg-zinc-950/50 border border-white/10 rounded-sm p-5 h-full">
        <div className="animate-pulse space-y-4">
          <div className="h-6 bg-white/10 rounded w-48" />
          <div className="h-48 bg-white/5 rounded" />
        </div>
      </div>
    );
  }

  return (
    <div className="bg-zinc-950/50 border border-white/10 rounded-sm p-5 h-full flex flex-col">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-white font-bold uppercase tracking-wider flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-yellow-500" />
          AI Opportunities
        </h2>
        <div className="flex items-center gap-2 text-xs text-slate-500">
          <span className="animate-pulse">●</span>
          <span>Real-time insights</span>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto space-y-4 custom-scrollbar">
        {opportunities.map((card) => (
          <div
            key={card.id}
            className={`border rounded-sm p-4 ${getImpactColor(card.impact)} hover:brightness-110 transition-all`}
          >
            {/* Header */}
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-start gap-3">
                {getCategoryIcon(card.category)}
                <div className="flex-1">
                  <h3 className="text-white font-bold text-sm mb-1">{card.title}</h3>
                  <div className="flex items-center gap-2 text-xs text-slate-500">
                    <span className="uppercase tracking-wider">{card.category}</span>
                    <span>•</span>
                    <span>{card.metrics.keyword}</span>
                  </div>
                </div>
              </div>
              <div className="text-right">
                <div className={`text-xs font-bold uppercase ${getConfidenceColor(card.confidence)}`}>
                  {Math.round(card.confidence * 100)}%
                </div>
                <div className="text-[10px] text-slate-500 uppercase tracking-wider">
                  confidence
                </div>
              </div>
            </div>

            {/* Insight */}
            <p className="text-sm text-slate-300 mb-4 leading-relaxed">{card.insight}</p>

            {/* Metrics */}
            <div className="grid grid-cols-3 gap-3 mb-4">
              <div className="bg-black/30 rounded-sm p-2">
                <div className="flex items-center gap-1 text-xs text-slate-500 mb-1">
                  <Target className="w-3 h-3" />
                  <span className="uppercase tracking-wider">STR</span>
                </div>
                <div className="text-lg font-bold text-white">
                  {card.metrics.current_str.toFixed(1)}%
                </div>
              </div>

              <div className="bg-black/30 rounded-sm p-2">
                <div className="flex items-center gap-1 text-xs text-slate-500 mb-1">
                  <TrendingUp className="w-3 h-3 text-cyan-500" />
                  <span className="uppercase tracking-wider">Change</span>
                </div>
                <div className={`text-lg font-bold ${card.metrics.change > 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                  {card.metrics.change > 0 ? '+' : ''}{card.metrics.change}%
                </div>
              </div>

              <div className="bg-black/30 rounded-sm p-2">
                <div className="flex items-center gap-1 text-xs text-slate-500 mb-1">
                  <Clock className="w-3 h-3 text-purple-500" />
                  <span className="uppercase tracking-wider">Timeframe</span>
                </div>
                <div className="text-lg font-bold text-white">
                  {card.metrics.timeframe}
                </div>
              </div>
            </div>

            {/* Action */}
            {card.action && (
              <div className="flex items-start gap-2 text-xs bg-black/30 rounded-sm p-2">
                <ArrowRight className="w-4 h-4 text-yellow-500 mt-0.5 flex-shrink-0" />
                <span className="text-slate-300">{card.action}</span>
              </div>
            )}

            {/* Footer */}
            <div className="mt-3 pt-3 border-t border-white/10 flex items-center justify-between text-xs text-slate-600">
              <span>Impact: {card.impact}</span>
              <span>{new Date(card.timestamp).toLocaleString()}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
