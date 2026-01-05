"""
Trend Analysis Engine
Calculates moving averages, momentum indicators, and trend classification
"""

from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import statistics


@dataclass
class TrendMetrics:
    """Computed trend metrics for an item"""
    keyword: str
    current_str: float
    ma_7d: Optional[float] = None
    ma_14d: Optional[float] = None
    ma_30d: Optional[float] = None
    ema_7d: Optional[float] = None
    momentum_7d: Optional[float] = None  # % change over 7 days
    momentum_30d: Optional[float] = None  # % change over 30 days
    acceleration: Optional[float] = None  # Is momentum increasing/decreasing
    trend_direction: str = "FLAT"  # STRONG_UP, UP, FLAT, DOWN, STRONG_DOWN
    trend_strength: float = 0.0  # 0-100 scale
    volatility: Optional[float] = None  # Standard deviation of recent values

    def to_dict(self) -> Dict:
        return {
            "keyword": self.keyword,
            "current_str": round(self.current_str, 2),
            "ma_7d": round(self.ma_7d, 2) if self.ma_7d else None,
            "ma_14d": round(self.ma_14d, 2) if self.ma_14d else None,
            "ma_30d": round(self.ma_30d, 2) if self.ma_30d else None,
            "ema_7d": round(self.ema_7d, 2) if self.ema_7d else None,
            "momentum_7d": round(self.momentum_7d, 2) if self.momentum_7d else None,
            "momentum_30d": round(self.momentum_30d, 2) if self.momentum_30d else None,
            "acceleration": round(self.acceleration, 2) if self.acceleration else None,
            "trend_direction": self.trend_direction,
            "trend_strength": round(self.trend_strength, 1),
            "volatility": round(self.volatility, 2) if self.volatility else None
        }


class TrendEngine:
    """
    Professional trend analysis engine
    Computes moving averages, momentum, and trend classifications
    """

    # Trend direction thresholds
    STRONG_UP_THRESHOLD = 15.0   # >15% momentum = strong uptrend
    UP_THRESHOLD = 5.0           # >5% momentum = uptrend
    DOWN_THRESHOLD = -5.0        # <-5% momentum = downtrend
    STRONG_DOWN_THRESHOLD = -15.0  # <-15% momentum = strong downtrend

    def __init__(self):
        pass

    def calculate_sma(self, values: List[float], period: int) -> Optional[float]:
        """Calculate Simple Moving Average"""
        if len(values) < period:
            return None
        return sum(values[-period:]) / period

    def calculate_ema(self, values: List[float], period: int) -> Optional[float]:
        """Calculate Exponential Moving Average"""
        if len(values) < period:
            return None

        multiplier = 2 / (period + 1)
        ema = values[0]  # Start with first value

        for value in values[1:]:
            ema = (value - ema) * multiplier + ema

        return ema

    def calculate_momentum(self, values: List[float], period: int) -> Optional[float]:
        """
        Calculate momentum as percentage change over period
        Returns: % change (positive = up, negative = down)
        """
        if len(values) < period + 1:
            return None

        old_value = values[-(period + 1)]
        current_value = values[-1]

        if old_value == 0:
            return None

        return ((current_value - old_value) / old_value) * 100

    def calculate_acceleration(self, momentum_recent: float, momentum_old: float) -> float:
        """
        Calculate if momentum is accelerating or decelerating
        Positive = accelerating, Negative = decelerating
        """
        return momentum_recent - momentum_old

    def calculate_volatility(self, values: List[float], period: int = 14) -> Optional[float]:
        """Calculate standard deviation as volatility measure"""
        if len(values) < period:
            return None
        return statistics.stdev(values[-period:])

    def classify_trend(self, momentum: Optional[float]) -> Tuple[str, float]:
        """
        Classify trend direction and strength based on momentum
        Returns: (direction, strength 0-100)
        """
        if momentum is None:
            return "FLAT", 0.0

        if momentum > self.STRONG_UP_THRESHOLD:
            strength = min(100, 50 + (momentum - self.STRONG_UP_THRESHOLD) * 2)
            return "STRONG_UP", strength
        elif momentum > self.UP_THRESHOLD:
            strength = 30 + (momentum - self.UP_THRESHOLD) * 2
            return "UP", strength
        elif momentum < self.STRONG_DOWN_THRESHOLD:
            strength = min(100, 50 + abs(momentum - self.STRONG_DOWN_THRESHOLD) * 2)
            return "STRONG_DOWN", strength
        elif momentum < self.DOWN_THRESHOLD:
            strength = 30 + abs(momentum - self.DOWN_THRESHOLD) * 2
            return "DOWN", strength
        else:
            # Flat trend
            strength = 10 - abs(momentum) * 2
            return "FLAT", max(0, strength)

    def analyze(self, keyword: str, historical_data: List[Dict]) -> TrendMetrics:
        """
        Perform comprehensive trend analysis on historical data

        Args:
            keyword: Item identifier
            historical_data: List of dicts with 'str' (sell-through-rate) and 'date' keys
                           Should be sorted oldest to newest

        Returns:
            TrendMetrics with all computed indicators
        """
        if not historical_data:
            return TrendMetrics(keyword=keyword, current_str=0.0)

        # Extract STR values (assuming sorted by date, oldest first)
        str_values = [d.get('str', d.get('sell_through_rate', 0)) for d in historical_data]
        current_str = str_values[-1] if str_values else 0.0

        # Calculate moving averages
        ma_7d = self.calculate_sma(str_values, 7)
        ma_14d = self.calculate_sma(str_values, 14)
        ma_30d = self.calculate_sma(str_values, 30)
        ema_7d = self.calculate_ema(str_values, 7)

        # Calculate momentum
        momentum_7d = self.calculate_momentum(str_values, 7)
        momentum_30d = self.calculate_momentum(str_values, 30)

        # Calculate acceleration (momentum of momentum)
        acceleration = None
        if len(str_values) >= 14:
            # Compare recent 7-day momentum to 7 days ago
            recent_momentum = self.calculate_momentum(str_values, 7)
            older_values = str_values[:-7]
            older_momentum = self.calculate_momentum(older_values, 7) if len(older_values) >= 8 else None
            if recent_momentum is not None and older_momentum is not None:
                acceleration = self.calculate_acceleration(recent_momentum, older_momentum)

        # Calculate volatility
        volatility = self.calculate_volatility(str_values)

        # Classify trend
        trend_direction, trend_strength = self.classify_trend(momentum_7d)

        return TrendMetrics(
            keyword=keyword,
            current_str=current_str,
            ma_7d=ma_7d,
            ma_14d=ma_14d,
            ma_30d=ma_30d,
            ema_7d=ema_7d,
            momentum_7d=momentum_7d,
            momentum_30d=momentum_30d,
            acceleration=acceleration,
            trend_direction=trend_direction,
            trend_strength=trend_strength,
            volatility=volatility
        )

    def detect_crossovers(self, str_values: List[float]) -> List[Dict]:
        """
        Detect MA crossovers (bullish/bearish signals)
        Returns list of crossover events
        """
        if len(str_values) < 15:
            return []

        crossovers = []

        for i in range(14, len(str_values)):
            # Get current and previous day MAs
            current_slice = str_values[:i+1]
            prev_slice = str_values[:i]

            ma_7_curr = self.calculate_sma(current_slice, 7)
            ma_14_curr = self.calculate_sma(current_slice, 14)
            ma_7_prev = self.calculate_sma(prev_slice, 7)
            ma_14_prev = self.calculate_sma(prev_slice, 14)

            if all(v is not None for v in [ma_7_curr, ma_14_curr, ma_7_prev, ma_14_prev]):
                # Bullish crossover: 7MA crosses above 14MA
                if ma_7_prev <= ma_14_prev and ma_7_curr > ma_14_curr:
                    crossovers.append({
                        "type": "BULLISH_CROSSOVER",
                        "index": i,
                        "ma_7": ma_7_curr,
                        "ma_14": ma_14_curr
                    })
                # Bearish crossover: 7MA crosses below 14MA
                elif ma_7_prev >= ma_14_prev and ma_7_curr < ma_14_curr:
                    crossovers.append({
                        "type": "BEARISH_CROSSOVER",
                        "index": i,
                        "ma_7": ma_7_curr,
                        "ma_14": ma_14_curr
                    })

        return crossovers

    def get_trend_summary(self, metrics: TrendMetrics) -> str:
        """Generate human-readable trend summary"""
        direction_text = {
            "STRONG_UP": "strongly trending upward",
            "UP": "trending upward",
            "FLAT": "relatively stable",
            "DOWN": "trending downward",
            "STRONG_DOWN": "strongly trending downward"
        }

        summary = f"{metrics.keyword} is {direction_text.get(metrics.trend_direction, 'unknown')}"

        if metrics.momentum_7d:
            summary += f" with {abs(metrics.momentum_7d):.1f}% "
            summary += "gain" if metrics.momentum_7d > 0 else "decline"
            summary += " over 7 days"

        if metrics.acceleration and abs(metrics.acceleration) > 2:
            if metrics.acceleration > 0:
                summary += " (accelerating)"
            else:
                summary += " (decelerating)"

        return summary
