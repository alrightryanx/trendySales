from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, Index
from sqlalchemy.sql import func
from database import Base
import datetime


class MarketStat(Base):
    """Time-series market statistics for trend analysis"""
    __tablename__ = "market_stats"

    id = Column(Integer, primary_key=True, index=True)

    # Identification
    keyword = Column(String(255), index=True, nullable=False)
    category = Column(String(100), index=True, default="General")
    platform = Column(String(50), index=True, default="ebay")

    # Core Metrics
    sell_through_rate = Column(Float, nullable=True)  # STR percentage
    volume_sold = Column(Integer, nullable=True)       # Units sold
    active_listings = Column(Integer, nullable=True)   # Current supply

    # Price Analytics
    avg_price = Column(Float, nullable=True)
    price_min = Column(Float, nullable=True)
    price_max = Column(Float, nullable=True)
    price_stddev = Column(Float, nullable=True)

    # Computed Analytics (populated by analytics engine)
    momentum_7d = Column(Float, nullable=True)         # 7-day rate of change
    momentum_30d = Column(Float, nullable=True)        # 30-day rate of change
    moving_avg_7d = Column(Float, nullable=True)       # 7-day SMA
    moving_avg_30d = Column(Float, nullable=True)      # 30-day SMA
    anomaly_score = Column(Float, nullable=True)       # Z-score from baseline
    opportunity_score = Column(Float, nullable=True)   # Composite rating 0-100
    trend_direction = Column(String(20), nullable=True)  # UP, DOWN, FLAT, STRONG_UP, STRONG_DOWN

    # Status
    market_status = Column(String(50), nullable=True)  # COLD, WARM, HOT, ON_FIRE

    # Timestamps
    recorded_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    __table_args__ = (
        Index('idx_keyword_recorded', 'keyword', 'recorded_at'),
        Index('idx_category_recorded', 'category', 'recorded_at'),
    )


class PricePoint(Base):
    """Individual price observations for detailed price tracking"""
    __tablename__ = "price_points"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String(255), index=True, nullable=False)
    platform = Column(String(50), index=True, default="ebay")
    price = Column(Float, nullable=False)
    currency = Column(String(10), default="USD")
    listing_type = Column(String(20), nullable=True)  # auction, buy_it_now
    is_sold = Column(Boolean, default=False)
    recorded_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    __table_args__ = (
        Index('idx_price_keyword_time', 'keyword', 'recorded_at'),
    )


class Signal(Base):
    """Market signals and alerts"""
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True, index=True)

    # Signal Details
    signal_type = Column(String(50), index=True, nullable=False)  # ANOMALY, OPPORTUNITY, WARNING, INFO
    level = Column(String(20), index=True, default="INFO")  # INFO, WARNING, CRITICAL
    keyword = Column(String(255), nullable=True, index=True)
    category = Column(String(100), nullable=True)

    # Content
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)

    # Metrics at time of signal
    metric_value = Column(Float, nullable=True)
    threshold_value = Column(Float, nullable=True)
    change_percent = Column(Float, nullable=True)

    # Status
    is_read = Column(Boolean, default=False)
    is_dismissed = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    expires_at = Column(DateTime, nullable=True)

    __table_args__ = (
        Index('idx_signal_type_time', 'signal_type', 'created_at'),
    )


class Correlation(Base):
    """Cross-item correlation matrix"""
    __tablename__ = "correlations"

    id = Column(Integer, primary_key=True, index=True)
    item_a = Column(String(255), index=True, nullable=False)
    item_b = Column(String(255), index=True, nullable=False)
    correlation_coefficient = Column(Float, nullable=False)  # -1 to 1
    lag_days = Column(Integer, default=0)  # If A leads B by X days
    sample_size = Column(Integer, nullable=True)
    confidence = Column(Float, nullable=True)  # Statistical confidence
    calculated_at = Column(DateTime, default=datetime.datetime.utcnow)

    __table_args__ = (
        Index('idx_correlation_items', 'item_a', 'item_b'),
    )


class ScanSession(Base):
    """Track scraping sessions for monitoring"""
    __tablename__ = "scan_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_type = Column(String(50), index=True)  # ebay, reddit, google_trends
    items_scanned = Column(Integer, default=0)
    items_success = Column(Integer, default=0)
    items_failed = Column(Integer, default=0)
    duration_seconds = Column(Float, nullable=True)
    error_log = Column(Text, nullable=True)
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)


class RedditMetric(Base):
    """Reddit-specific metrics for service economy tracking"""
    __tablename__ = "reddit_metrics"

    id = Column(Integer, primary_key=True, index=True)
    subreddit = Column(String(100), index=True, nullable=False)

    # Post Counts
    hiring_posts = Column(Integer, default=0)
    for_hire_posts = Column(Integer, default=0)
    total_posts = Column(Integer, default=0)

    # Derived Metrics
    saturation_ratio = Column(Float, nullable=True)  # for_hire / hiring
    activity_score = Column(Float, nullable=True)    # 0-100 health score
    market_status = Column(String(50), nullable=True)  # HEALTHY, SATURATED, GOLDMINE

    # Top Demands (JSON stored as text)
    top_demands_json = Column(Text, nullable=True)

    recorded_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    __table_args__ = (
        Index('idx_reddit_sub_time', 'subreddit', 'recorded_at'),
    )


class Forecast(Base):
    """Stored forecasts for items"""
    __tablename__ = "forecasts"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String(255), index=True, nullable=False)

    # Forecast Details
    forecast_date = Column(DateTime, nullable=False)  # Date being predicted
    predicted_str = Column(Float, nullable=True)      # Predicted STR
    confidence_lower = Column(Float, nullable=True)   # Lower bound
    confidence_upper = Column(Float, nullable=True)   # Upper bound
    confidence_level = Column(Float, default=0.95)    # 95% confidence

    # Model Info
    model_type = Column(String(50), default="ema")    # ema, arima, prophet

    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    __table_args__ = (
        Index('idx_forecast_keyword_date', 'keyword', 'forecast_date'),
    )
