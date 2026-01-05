"""
Omniscient Market Intelligence API
Professional-grade market analytics backend
"""

from fastapi import FastAPI, Depends, HTTPException, Query, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from collections import Counter
import asyncio
import json
import logging
from concurrent.futures import ThreadPoolExecutor

# Local imports
from database import init_db, get_db, get_db_session
from models import MarketStat, Signal, RedditMetric, Forecast as ForecastModel
from scrapers.reddit_reality import RedditRealityScanner
from scrapers.ebay_velocity import EbayVelocityProbe
from analytics import TrendEngine, AnomalyDetector, MarketScorer, Forecaster

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Omniscient Market Intelligence API",
    description="Professional-grade market analytics for sales and trend analysis",
    version="2.0.0"
)

# CORS Configuration
origins = [
    "http://localhost:3000",
    "http://localhost:4303",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:4303",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
reddit_scanner = RedditRealityScanner()
ebay_probe = EbayVelocityProbe()
trend_engine = TrendEngine()
anomaly_detector = AnomalyDetector()
market_scorer = MarketScorer()
forecaster = Forecaster()

# WebSocket connections
active_connections: List[WebSocket] = []

# Watchlists
WATCHLIST = [
    # Tech / Electronics
    {"keyword": "Vintage Digital Camera", "category": "Electronics"},
    {"keyword": "Fujifilm X100V", "category": "Electronics"},
    {"keyword": "Sony Walkman", "category": "Electronics"},
    {"keyword": "Flipper Zero", "category": "Electronics"},
    {"keyword": "Steam Deck OLED", "category": "Gaming"},
    {"keyword": "Analogue Pocket", "category": "Gaming"},
    {"keyword": "Nintendo 3DS XL", "category": "Gaming"},
    {"keyword": "Nvidia RTX 4090", "category": "Electronics"},

    # Fashion / Streetwear
    {"keyword": "Carhartt Detroit Jacket", "category": "Fashion"},
    {"keyword": "Arc'teryx Beta LT", "category": "Fashion"},
    {"keyword": "Birkenstock Boston", "category": "Fashion"},
    {"keyword": "Onitsuka Tiger Mexico 66", "category": "Fashion"},

    # Collectibles
    {"keyword": "Sonny Angel", "category": "Collectibles"},
    {"keyword": "Jellycat Plush", "category": "Collectibles"},
    {"keyword": "One Piece TCG Booster", "category": "Collectibles"},
    {"keyword": "Lego Rivendell", "category": "Collectibles"},

    # Tools / EDC
    {"keyword": "Leatherman Arc", "category": "Tools"},
    {"keyword": "Knipex Cobra XS", "category": "Tools"},
    {"keyword": "Yeti Rambler", "category": "Tools"},
]

SUBREDDITS = ["forhire", "freelance_forhire", "hardwareswap", "mechmarket", "photomarket"]

# In-memory cache for fast access
cache = {
    "trends": [],
    "keywords": [],
    "signals": [],
    "platforms": [],
    "opportunities": [],
    "last_scan": None
}


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database and start background tasks"""
    logger.info("Starting Omniscient Market Intelligence API...")
    init_db()
    logger.info("Database initialized")


# ============== CORE DATA ENDPOINTS ==============

@app.get("/")
def read_root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Omniscient Market Intelligence Engine",
        "version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/api/trends")
async def get_trends(db: Session = Depends(get_db)):
    """Get current velocity leaders with full analytics"""
    logger.info("Starting trend scan...")

    loop = asyncio.get_running_loop()
    results = []
    signals = []

    # Parallel scraping with ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=10) as executor:
        tasks = [
            loop.run_in_executor(executor, ebay_probe.analyze_market_health, item["keyword"])
            for item in WATCHLIST
        ]
        raw_results = await asyncio.gather(*tasks)

    # Get historical data for analytics
    for idx, data in enumerate(raw_results):
        if data:
            keyword = data.get("keyword", WATCHLIST[idx]["keyword"])
            category = WATCHLIST[idx]["category"]

            # Get historical STR values for this keyword
            history = db.query(MarketStat.sell_through_rate).filter(
                MarketStat.keyword == keyword
            ).order_by(MarketStat.recorded_at).limit(30).all()

            history_values = [h[0] for h in history if h[0] is not None]

            # Calculate trend metrics
            trend_metrics = None
            if history_values:
                historical_data = [{"str": v} for v in history_values]
                trend_metrics = trend_engine.analyze(keyword, historical_data)

            # Calculate opportunity score
            score = market_scorer.score(
                keyword=keyword,
                sell_through_rate=data.get("sell_through_rate", 0),
                active_listings=data.get("active_supply", 1000),
                volume_sold=data.get("sold_demand", 0),
                momentum_7d=trend_metrics.momentum_7d if trend_metrics else None,
                volatility=trend_metrics.volatility if trend_metrics else None,
                data_points=len(history_values),
                has_history=len(history_values) >= 7
            )

            result = {
                "keyword": keyword,
                "category": category,
                "velocity": data.get("sell_through_rate", 0),
                "volume": data.get("sold_demand", 0),
                "supply": data.get("active_supply", 0),
                "sentiment": data.get("market_status", "UNKNOWN"),
                "avg_price": data.get("avg_price"),
                "price_range": {
                    "min": data.get("price_min"),
                    "max": data.get("price_max")
                },
                "trend": {
                    "direction": trend_metrics.trend_direction if trend_metrics else "FLAT",
                    "momentum_7d": trend_metrics.momentum_7d if trend_metrics else None,
                    "momentum_30d": trend_metrics.momentum_30d if trend_metrics else None,
                    "ma_7d": trend_metrics.ma_7d if trend_metrics else None,
                },
                "opportunity": {
                    "score": score.total_score,
                    "level": score.opportunity_level,
                    "recommendation": score.recommendation
                },
                "is_estimated": data.get("is_estimated", False)
            }
            results.append(result)

            # Store in database
            stat = MarketStat(
                keyword=keyword,
                category=category,
                platform="ebay",
                sell_through_rate=data.get("sell_through_rate", 0),
                volume_sold=data.get("sold_demand", 0),
                active_listings=data.get("active_supply", 0),
                avg_price=data.get("avg_price"),
                price_min=data.get("price_min"),
                price_max=data.get("price_max"),
                price_stddev=data.get("price_stddev"),
                momentum_7d=trend_metrics.momentum_7d if trend_metrics else None,
                moving_avg_7d=trend_metrics.ma_7d if trend_metrics else None,
                opportunity_score=score.total_score,
                trend_direction=trend_metrics.trend_direction if trend_metrics else None,
                market_status=data.get("market_status"),
                recorded_at=datetime.utcnow()
            )
            db.add(stat)

            # Generate signals for notable items
            if data.get("sell_through_rate", 0) > 100:
                signals.append({
                    "type": "CRITICAL",
                    "keyword": keyword,
                    "message": f"{keyword} ON FIRE with {data['sell_through_rate']:.0f}% STR"
                })
            elif data.get("sell_through_rate", 0) > 70:
                signals.append({
                    "type": "WARNING",
                    "keyword": keyword,
                    "message": f"High demand detected for {keyword}"
                })

    db.commit()

    # Sort by velocity and cache
    results.sort(key=lambda x: x["velocity"], reverse=True)
    cache["trends"] = results

    # Update signals
    timestamp = datetime.utcnow().strftime("%H:%M:%S")
    new_signals = [
        {"timestamp": timestamp, "message": s["message"], "level": s["type"], "keyword": s["keyword"]}
        for s in signals
    ]
    cache["signals"] = (new_signals + cache["signals"])[:50]
    cache["last_scan"] = datetime.utcnow().isoformat()

    logger.info(f"Trend scan complete. {len(results)} items tracked.")
    return results


@app.get("/api/trends/{keyword}")
async def get_trend_detail(keyword: str, db: Session = Depends(get_db)):
    """Get detailed trend data for a specific keyword"""
    # Get latest stat
    latest = db.query(MarketStat).filter(
        MarketStat.keyword == keyword
    ).order_by(desc(MarketStat.recorded_at)).first()

    if not latest:
        raise HTTPException(status_code=404, detail=f"No data found for '{keyword}'")

    # Get history
    history = db.query(MarketStat).filter(
        MarketStat.keyword == keyword
    ).order_by(desc(MarketStat.recorded_at)).limit(90).all()

    # Prepare history for analytics
    history_data = [{"str": h.sell_through_rate, "date": h.recorded_at} for h in reversed(history)]
    str_values = [h.sell_through_rate for h in history if h.sell_through_rate]

    # Calculate analytics
    trend_metrics = trend_engine.analyze(keyword, history_data) if history_data else None

    # Check for anomalies
    anomaly = None
    if len(str_values) >= 7:
        anomaly = anomaly_detector.detect_value_anomaly(keyword, str_values[-1], str_values[:-1])

    # Generate forecast
    forecast = forecaster.get_best_forecast(keyword, str_values) if str_values else None

    return {
        "keyword": keyword,
        "current": {
            "str": latest.sell_through_rate,
            "volume": latest.volume_sold,
            "supply": latest.active_listings,
            "avg_price": latest.avg_price,
            "status": latest.market_status,
            "recorded_at": latest.recorded_at.isoformat()
        },
        "trend": trend_metrics.to_dict() if trend_metrics else None,
        "history": [
            {
                "date": h.recorded_at.isoformat(),
                "str": h.sell_through_rate,
                "volume": h.volume_sold,
                "price": h.avg_price
            }
            for h in history[:30]
        ],
        "anomaly": anomaly.to_dict() if anomaly else None,
        "forecast": forecast.to_dict() if forecast else None
    }


@app.get("/api/platforms")
async def get_platforms(db: Session = Depends(get_db)):
    """Get platform health metrics from Reddit"""
    logger.info("Starting platform scan...")

    loop = asyncio.get_running_loop()

    with ThreadPoolExecutor(max_workers=5) as executor:
        tasks = [
            loop.run_in_executor(executor, reddit_scanner.get_saturation_metrics, sub)
            for sub in SUBREDDITS
        ]
        raw_results = await asyncio.gather(*tasks)

    platforms_data = []
    all_keywords = []

    for data in raw_results:
        if data:
            health = data.get("activity_score", 50)

            platform_info = {
                "platform": data.get("platform", "unknown"),
                "activity_score": health,
                "saturation_ratio": data.get("saturation_ratio", 0),
                "market_status": data.get("market_status", "UNKNOWN"),
                "hiring_posts": data.get("hiring_posts", 0),
                "for_hire_posts": data.get("for_hire_posts", 0),
                "sentiment": {
                    "score": data.get("sentiment_score", 0),
                    "label": data.get("sentiment_label", "NEUTRAL")
                },
                "categories": data.get("categories", {}),
                "role": f"Ratio: {data.get('saturation_ratio', 0)}:1 ({data.get('market_status', 'N/A')})"
            }
            platforms_data.append(platform_info)

            # Collect keywords
            if "top_demands" in data:
                all_keywords.extend(data["top_demands"])

            # Store in database
            with get_db_session() as session:
                metric = RedditMetric(
                    subreddit=data.get("subreddit", "unknown"),
                    hiring_posts=data.get("hiring_posts", 0),
                    for_hire_posts=data.get("for_hire_posts", 0),
                    total_posts=data.get("total_posts", 0),
                    saturation_ratio=data.get("saturation_ratio", 0),
                    activity_score=health,
                    market_status=data.get("market_status"),
                    top_demands_json=json.dumps(data.get("top_demands", [])[:20]),
                    recorded_at=datetime.utcnow()
                )
                session.add(metric)

    # Aggregate keywords
    flat_words = []
    for word, count in all_keywords:
        flat_words.extend([word] * count)

    final_cloud = Counter(flat_words).most_common(60)
    cache["keywords"] = [{"text": k[0], "value": k[1]} for k in final_cloud]
    cache["platforms"] = platforms_data

    logger.info("Platform scan complete")
    return platforms_data


@app.get("/api/keywords")
def get_keywords():
    """Get keyword cloud data"""
    return cache["keywords"]


@app.get("/api/signals")
def get_signals(limit: int = Query(default=50, le=100)):
    """Get live signal feed"""
    if not cache["signals"]:
        return [{
            "timestamp": datetime.utcnow().strftime("%H:%M:%S"),
            "message": "System initialized. Awaiting first scan...",
            "level": "INFO"
        }]
    return cache["signals"][:limit]


@app.get("/api/pulse")
def get_pulse():
    """Get system-wide pulse metrics"""
    trends = cache.get("trends", [])

    avg_velocity = sum(t["velocity"] for t in trends) / max(len(trends), 1) if trends else 0

    # Count by trend direction
    trend_counts = Counter(t.get("trend", {}).get("direction", "FLAT") for t in trends)

    return {
        "global_velocity_index": round(avg_velocity, 1),
        "active_narratives": len(cache.get("keywords", [])),
        "scanned_nodes": f"{len(WATCHLIST) + len(SUBREDDITS)} Nodes",
        "system_status": "LOCKED" if trends else "SCANNING",
        "last_scan": cache.get("last_scan"),
        "trend_distribution": dict(trend_counts),
        "total_items_tracked": len(trends),
        "platforms_monitored": len(SUBREDDITS)
    }


# ============== HISTORICAL ANALYSIS ==============

@app.get("/api/history/item/{keyword}")
async def get_item_history(
    keyword: str,
    days: int = Query(default=30, le=90),
    db: Session = Depends(get_db)
):
    """Get historical data for a specific item"""
    cutoff = datetime.utcnow() - timedelta(days=days)

    history = db.query(MarketStat).filter(
        MarketStat.keyword == keyword,
        MarketStat.recorded_at >= cutoff
    ).order_by(MarketStat.recorded_at).all()

    if not history:
        raise HTTPException(status_code=404, detail=f"No history found for '{keyword}'")

    return {
        "keyword": keyword,
        "period_days": days,
        "data_points": len(history),
        "history": [
            {
                "date": h.recorded_at.isoformat(),
                "str": h.sell_through_rate,
                "volume": h.volume_sold,
                "supply": h.active_listings,
                "avg_price": h.avg_price,
                "momentum_7d": h.momentum_7d,
                "opportunity_score": h.opportunity_score
            }
            for h in history
        ]
    }


@app.get("/api/history/market")
async def get_market_history(
    days: int = Query(default=7, le=30),
    db: Session = Depends(get_db)
):
    """Get aggregated market history"""
    cutoff = datetime.utcnow() - timedelta(days=days)

    # Get daily aggregates
    daily_stats = db.query(
        func.date(MarketStat.recorded_at).label('date'),
        func.avg(MarketStat.sell_through_rate).label('avg_str'),
        func.sum(MarketStat.volume_sold).label('total_volume'),
        func.count(MarketStat.id).label('items_tracked')
    ).filter(
        MarketStat.recorded_at >= cutoff
    ).group_by(
        func.date(MarketStat.recorded_at)
    ).order_by('date').all()

    return {
        "period_days": days,
        "daily_data": [
            {
                "date": str(d.date),
                "avg_str": round(d.avg_str, 2) if d.avg_str else 0,
                "total_volume": d.total_volume or 0,
                "items_tracked": d.items_tracked
            }
            for d in daily_stats
        ]
    }


# ============== ANALYTICS ENDPOINTS ==============

@app.get("/api/analytics/forecast/{keyword}")
async def get_forecast(
    keyword: str,
    days: int = Query(default=14, le=30),
    db: Session = Depends(get_db)
):
    """Get forecast for a specific item"""
    # Get historical data
    history = db.query(MarketStat.sell_through_rate).filter(
        MarketStat.keyword == keyword
    ).order_by(MarketStat.recorded_at).limit(90).all()

    str_values = [h[0] for h in history if h[0] is not None]

    if len(str_values) < 7:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient data for forecast. Need 7+ data points, have {len(str_values)}"
        )

    forecast = forecaster.get_best_forecast(keyword, str_values, days)

    return forecast.to_dict()


@app.get("/api/analytics/anomalies")
async def get_anomalies(db: Session = Depends(get_db)):
    """Get all detected anomalies"""
    anomalies = []

    # Get recent data for each tracked item
    for item in WATCHLIST:
        keyword = item["keyword"]

        history = db.query(MarketStat.sell_through_rate).filter(
            MarketStat.keyword == keyword
        ).order_by(desc(MarketStat.recorded_at)).limit(30).all()

        str_values = [h[0] for h in history if h[0] is not None]

        if len(str_values) >= 7:
            # Check for value anomaly
            anomaly = anomaly_detector.detect_value_anomaly(
                keyword, str_values[0], str_values[1:]
            )
            if anomaly:
                anomalies.append(anomaly.to_dict())

            # Check for spike
            spike = anomaly_detector.detect_spike(keyword, list(reversed(str_values)))
            if spike:
                anomalies.append(spike.to_dict())

    # Sort by severity
    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    anomalies.sort(key=lambda a: severity_order.get(a["severity"], 4))

    return {
        "total": len(anomalies),
        "anomalies": anomalies
    }


@app.get("/api/analytics/opportunities")
async def get_opportunities(
    limit: int = Query(default=20, le=50),
    db: Session = Depends(get_db)
):
    """Get ranked opportunities"""
    opportunities = []

    for item in WATCHLIST:
        keyword = item["keyword"]
        category = item["category"]

        # Get latest stats
        latest = db.query(MarketStat).filter(
            MarketStat.keyword == keyword
        ).order_by(desc(MarketStat.recorded_at)).first()

        if latest:
            # Get history for momentum calculation
            history = db.query(MarketStat.sell_through_rate).filter(
                MarketStat.keyword == keyword
            ).order_by(MarketStat.recorded_at).limit(30).all()

            str_values = [h[0] for h in history if h[0] is not None]

            # Calculate trend
            trend_metrics = None
            if str_values:
                historical_data = [{"str": v} for v in str_values]
                trend_metrics = trend_engine.analyze(keyword, historical_data)

            # Score opportunity
            score = market_scorer.score(
                keyword=keyword,
                sell_through_rate=latest.sell_through_rate or 0,
                active_listings=latest.active_listings or 1000,
                volume_sold=latest.volume_sold or 0,
                momentum_7d=trend_metrics.momentum_7d if trend_metrics else None,
                volatility=trend_metrics.volatility if trend_metrics else None,
                data_points=len(str_values),
                has_history=len(str_values) >= 7
            )

            opportunities.append({
                "keyword": keyword,
                "category": category,
                "score": score.to_dict()
            })

    # Sort by score
    opportunities.sort(key=lambda x: x["score"]["total_score"], reverse=True)
    cache["opportunities"] = opportunities[:limit]

    return opportunities[:limit]


@app.get("/api/analytics/heatmap")
async def get_category_heatmap(db: Session = Depends(get_db)):
    """Get category performance heatmap"""
    categories = {}

    for item in WATCHLIST:
        category = item["category"]
        keyword = item["keyword"]

        latest = db.query(MarketStat).filter(
            MarketStat.keyword == keyword
        ).order_by(desc(MarketStat.recorded_at)).first()

        if latest:
            if category not in categories:
                categories[category] = {
                    "items": [],
                    "total_str": 0,
                    "total_volume": 0,
                    "count": 0
                }

            categories[category]["items"].append({
                "keyword": keyword,
                "str": latest.sell_through_rate,
                "volume": latest.volume_sold,
                "score": latest.opportunity_score
            })
            categories[category]["total_str"] += latest.sell_through_rate or 0
            categories[category]["total_volume"] += latest.volume_sold or 0
            categories[category]["count"] += 1

    # Calculate averages
    heatmap = []
    for cat, data in categories.items():
        avg_str = data["total_str"] / max(data["count"], 1)
        heatmap.append({
            "category": cat,
            "avg_str": round(avg_str, 1),
            "total_volume": data["total_volume"],
            "item_count": data["count"],
            "heat_level": "HOT" if avg_str > 60 else "WARM" if avg_str > 40 else "COLD",
            "items": sorted(data["items"], key=lambda x: x["str"] or 0, reverse=True)
        })

    heatmap.sort(key=lambda x: x["avg_str"], reverse=True)

    return heatmap


# ============== WEBSOCKET FOR REAL-TIME ==============

@app.websocket("/api/ws/live")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await websocket.accept()
    active_connections.append(websocket)
    logger.info(f"WebSocket connected. Total: {len(active_connections)}")

    try:
        while True:
            # Send pulse data every 5 seconds
            pulse = get_pulse()
            await websocket.send_json({
                "type": "pulse",
                "data": pulse,
                "timestamp": datetime.utcnow().isoformat()
            })

            # Send latest signals
            if cache["signals"]:
                await websocket.send_json({
                    "type": "signals",
                    "data": cache["signals"][:10],
                    "timestamp": datetime.utcnow().isoformat()
                })

            await asyncio.sleep(5)

    except WebSocketDisconnect:
        active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected. Total: {len(active_connections)}")


# ============== UTILITY ENDPOINTS ==============

@app.get("/api/stats")
def get_system_stats():
    """Get system statistics"""
    return {
        "ebay_scraper": ebay_probe.get_stats(),
        "reddit_scanner": reddit_scanner.get_stats(),
        "watchlist_size": len(WATCHLIST),
        "subreddits_monitored": len(SUBREDDITS),
        "active_websockets": len(active_connections),
        "cache_status": {
            "trends": len(cache.get("trends", [])),
            "signals": len(cache.get("signals", [])),
            "keywords": len(cache.get("keywords", [])),
            "platforms": len(cache.get("platforms", []))
        }
    }


@app.get("/api/watchlist")
def get_watchlist():
    """Get current watchlist"""
    return {
        "items": WATCHLIST,
        "categories": list(set(item["category"] for item in WATCHLIST))
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
