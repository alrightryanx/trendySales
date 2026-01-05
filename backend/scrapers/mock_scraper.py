import random
from datetime import datetime, timedelta

def generate_trend_metrics():
    """
    Generates high-level trend intelligence.
    Focus: Volume, Velocity (Growth Rate), and Saturation.
    """
    trends = [
        {"keyword": "Vintage Digital Cameras", "category": "Tech", "velocity": 8.5, "volume": 12500, "sentiment": "Nostalgic"},
        {"keyword": "AI Agent Frameworks", "category": "SaaS", "velocity": 9.8, "volume": 45000, "sentiment": "Hype"},
        {"keyword": "Mushroom Coffee", "category": "Health", "velocity": -2.3, "volume": 89000, "sentiment": "Saturated"},
        {"keyword": "Portable Monitor", "category": "Electronics", "velocity": 1.2, "volume": 3200, "sentiment": "Stable"},
        {"keyword": "Cyberpunk Aesthetics", "category": "Design", "velocity": 4.5, "volume": 1500, "sentiment": "Rising"},
        {"keyword": "Local LLM Hardware", "category": "Tech", "velocity": 12.1, "volume": 800, "sentiment": "Explosive"},
    ]
    
    # Simulate live fluctuations
    for t in trends:
        t["velocity"] += random.uniform(-0.5, 0.5)
        t["volume"] += random.randint(-100, 500)
    
    return sorted(trends, key=lambda x: x["velocity"], reverse=True)

def generate_platform_breakdown():
    """
    Shows where the conversation is happening.
    """
    return [
        {"platform": "Reddit", "activity_score": 85, "role": "Genesis"},
        {"platform": "Twitter/X", "activity_score": 72, "role": "Amplification"},
        {"platform": "TikTok", "activity_score": 45, "role": "Viral Mass"},
        {"platform": "eBay/Amazon", "activity_score": 30, "role": "Monetization"},
    ]

def generate_live_signals():
    """
    Raw data stream of 'significant events'.
    """
    events = [
        "Spike detected: 'CCD Sensor' search volume +400% in NYC.",
        "Saturation Warning: 'UGC Creator' supply exceeds demand by 15x.",
        "New Niche: 'Silence Retreats' mentioned 50x in r/stressed.",
        "Pricing Anomaly: 'CRT TV' avg price moved $40 -> $120.",
        "Cross-Correlated: 'Mechanical Keyboards' hit TikTok Viral threshold.",
    ]
    return [
        {"timestamp": datetime.now().strftime("%H:%M:%S"), "message": random.choice(events), "level": random.choice(["INFO", "WARNING", "CRITICAL"])}
        for _ in range(6)
    ]

def generate_market_pulse():
    return {
        "global_velocity_index": round(random.uniform(40, 90), 1),
        "active_narratives": 142,
        "scanned_nodes": "4.2M",
        "system_status": "HUNTING"
    }