"""
Market Forecaster
Predictive analytics for market trends using statistical methods
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import statistics
import math


@dataclass
class ForecastPoint:
    """Single forecast data point"""
    date: datetime
    predicted_value: float
    confidence_lower: float
    confidence_upper: float
    confidence_level: float  # e.g., 0.95 for 95%


@dataclass
class Forecast:
    """Complete forecast with predictions and metadata"""
    keyword: str
    current_value: float
    forecast_points: List[ForecastPoint]
    model_type: str
    trend_summary: str
    expected_change: float  # % change over forecast period
    confidence: str  # LOW, MEDIUM, HIGH
    generated_at: datetime

    def to_dict(self) -> Dict:
        return {
            "keyword": self.keyword,
            "current_value": round(self.current_value, 2),
            "predictions": [
                {
                    "date": fp.date.isoformat(),
                    "value": round(fp.predicted_value, 2),
                    "lower": round(fp.confidence_lower, 2),
                    "upper": round(fp.confidence_upper, 2),
                    "confidence": fp.confidence_level
                }
                for fp in self.forecast_points
            ],
            "model": self.model_type,
            "trend_summary": self.trend_summary,
            "expected_change": round(self.expected_change, 1),
            "confidence": self.confidence,
            "generated_at": self.generated_at.isoformat()
        }


class Forecaster:
    """
    Time series forecasting engine
    Uses EMA-based forecasting with trend extrapolation
    """

    # Minimum data points for reliable forecast
    MIN_HISTORY = 7
    PREFERRED_HISTORY = 30

    # Confidence interval z-scores
    Z_90 = 1.645
    Z_95 = 1.96
    Z_99 = 2.576

    def __init__(self):
        pass

    def calculate_ema(self, values: List[float], span: int) -> float:
        """Calculate Exponential Moving Average"""
        if not values:
            return 0.0

        multiplier = 2 / (span + 1)
        ema = values[0]

        for value in values[1:]:
            ema = (value - ema) * multiplier + ema

        return ema

    def calculate_trend_slope(self, values: List[float]) -> float:
        """
        Calculate trend slope using linear regression
        Returns: daily rate of change
        """
        if len(values) < 2:
            return 0.0

        n = len(values)
        x_mean = (n - 1) / 2
        y_mean = sum(values) / n

        numerator = sum((i - x_mean) * (values[i] - y_mean) for i in range(n))
        denominator = sum((i - x_mean) ** 2 for i in range(n))

        if denominator == 0:
            return 0.0

        return numerator / denominator

    def calculate_seasonality(
        self,
        values: List[float],
        period: int = 7
    ) -> Dict[int, float]:
        """
        Detect weekly seasonality patterns
        Returns: dict of {day_index: adjustment_factor}
        """
        if len(values) < period * 2:
            return {}

        # Group by day of week position
        day_values = {i: [] for i in range(period)}

        for idx, val in enumerate(values):
            day_idx = idx % period
            day_values[day_idx].append(val)

        # Calculate adjustment factors
        overall_mean = sum(values) / len(values)
        adjustments = {}

        for day_idx, day_vals in day_values.items():
            if day_vals:
                day_mean = sum(day_vals) / len(day_vals)
                adjustments[day_idx] = day_mean / overall_mean if overall_mean != 0 else 1.0

        return adjustments

    def calculate_volatility(self, values: List[float]) -> float:
        """Calculate standard deviation as volatility measure"""
        if len(values) < 2:
            return 0.0
        return statistics.stdev(values)

    def forecast_ema(
        self,
        keyword: str,
        historical_values: List[float],
        days_ahead: int = 14,
        confidence_level: float = 0.95
    ) -> Forecast:
        """
        Generate forecast using EMA with trend extrapolation

        Args:
            keyword: Item identifier
            historical_values: Historical STR values (oldest first)
            days_ahead: Number of days to forecast
            confidence_level: Confidence level for intervals (0.90, 0.95, 0.99)

        Returns:
            Forecast object with predictions
        """
        if len(historical_values) < self.MIN_HISTORY:
            # Not enough data for reliable forecast
            current = historical_values[-1] if historical_values else 0
            return Forecast(
                keyword=keyword,
                current_value=current,
                forecast_points=[],
                model_type="insufficient_data",
                trend_summary="Insufficient data for forecast",
                expected_change=0,
                confidence="LOW",
                generated_at=datetime.utcnow()
            )

        current_value = historical_values[-1]

        # Calculate base metrics
        ema_7 = self.calculate_ema(historical_values, 7)
        ema_14 = self.calculate_ema(historical_values, 14) if len(historical_values) >= 14 else ema_7
        trend_slope = self.calculate_trend_slope(historical_values[-14:])
        volatility = self.calculate_volatility(historical_values)
        seasonality = self.calculate_seasonality(historical_values)

        # Determine z-score for confidence interval
        if confidence_level >= 0.99:
            z_score = self.Z_99
        elif confidence_level >= 0.95:
            z_score = self.Z_95
        else:
            z_score = self.Z_90

        # Generate forecast points
        forecast_points = []
        base_date = datetime.utcnow()

        for day in range(1, days_ahead + 1):
            forecast_date = base_date + timedelta(days=day)

            # Base prediction: EMA + trend extrapolation
            base_prediction = ema_7 + (trend_slope * day)

            # Apply seasonality adjustment if available
            day_idx = (len(historical_values) + day) % 7
            season_adjust = seasonality.get(day_idx, 1.0)
            adjusted_prediction = base_prediction * season_adjust

            # Ensure non-negative
            adjusted_prediction = max(0, adjusted_prediction)

            # Calculate confidence interval (widens with forecast horizon)
            horizon_factor = math.sqrt(day)  # Uncertainty grows with sqrt of time
            interval_width = z_score * volatility * horizon_factor

            forecast_points.append(ForecastPoint(
                date=forecast_date,
                predicted_value=adjusted_prediction,
                confidence_lower=max(0, adjusted_prediction - interval_width),
                confidence_upper=adjusted_prediction + interval_width,
                confidence_level=confidence_level
            ))

        # Calculate expected change
        if forecast_points and current_value > 0:
            final_prediction = forecast_points[-1].predicted_value
            expected_change = ((final_prediction - current_value) / current_value) * 100
        else:
            expected_change = 0

        # Generate trend summary
        if expected_change > 15:
            trend_summary = "Strong upward trend expected"
        elif expected_change > 5:
            trend_summary = "Moderate upward trend expected"
        elif expected_change > -5:
            trend_summary = "Relatively stable with minor fluctuations"
        elif expected_change > -15:
            trend_summary = "Moderate downward trend expected"
        else:
            trend_summary = "Strong downward trend expected"

        # Determine confidence based on data quality
        if len(historical_values) >= self.PREFERRED_HISTORY and volatility < current_value * 0.3:
            confidence = "HIGH"
        elif len(historical_values) >= self.MIN_HISTORY * 2:
            confidence = "MEDIUM"
        else:
            confidence = "LOW"

        return Forecast(
            keyword=keyword,
            current_value=current_value,
            forecast_points=forecast_points,
            model_type="ema_trend",
            trend_summary=trend_summary,
            expected_change=expected_change,
            confidence=confidence,
            generated_at=datetime.utcnow()
        )

    def forecast_mean_reversion(
        self,
        keyword: str,
        historical_values: List[float],
        days_ahead: int = 14,
        mean_reversion_rate: float = 0.1
    ) -> Forecast:
        """
        Alternative forecast model assuming mean reversion
        Useful for items with established stable patterns
        """
        if len(historical_values) < self.MIN_HISTORY:
            current = historical_values[-1] if historical_values else 0
            return Forecast(
                keyword=keyword,
                current_value=current,
                forecast_points=[],
                model_type="insufficient_data",
                trend_summary="Insufficient data for forecast",
                expected_change=0,
                confidence="LOW",
                generated_at=datetime.utcnow()
            )

        current_value = historical_values[-1]
        long_term_mean = statistics.mean(historical_values)
        volatility = self.calculate_volatility(historical_values)

        forecast_points = []
        base_date = datetime.utcnow()
        current_prediction = current_value

        for day in range(1, days_ahead + 1):
            forecast_date = base_date + timedelta(days=day)

            # Mean reversion formula: value moves toward mean at given rate
            reversion = (long_term_mean - current_prediction) * mean_reversion_rate
            current_prediction += reversion
            current_prediction = max(0, current_prediction)

            # Confidence interval
            interval_width = 1.96 * volatility * math.sqrt(day) * (1 - mean_reversion_rate * day / 10)
            interval_width = max(volatility * 0.5, interval_width)  # Floor

            forecast_points.append(ForecastPoint(
                date=forecast_date,
                predicted_value=current_prediction,
                confidence_lower=max(0, current_prediction - interval_width),
                confidence_upper=current_prediction + interval_width,
                confidence_level=0.95
            ))

        # Calculate expected change
        if forecast_points and current_value > 0:
            expected_change = ((forecast_points[-1].predicted_value - current_value) / current_value) * 100
        else:
            expected_change = 0

        trend_summary = f"Expected to revert toward mean of {long_term_mean:.1f}%"

        return Forecast(
            keyword=keyword,
            current_value=current_value,
            forecast_points=forecast_points,
            model_type="mean_reversion",
            trend_summary=trend_summary,
            expected_change=expected_change,
            confidence="MEDIUM",
            generated_at=datetime.utcnow()
        )

    def get_best_forecast(
        self,
        keyword: str,
        historical_values: List[float],
        days_ahead: int = 14
    ) -> Forecast:
        """
        Automatically select and return the best forecast model

        Args:
            keyword: Item identifier
            historical_values: Historical STR values

        Returns:
            Best forecast based on data characteristics
        """
        if len(historical_values) < self.MIN_HISTORY:
            return self.forecast_ema(keyword, historical_values, days_ahead)

        # Analyze data characteristics
        volatility = self.calculate_volatility(historical_values)
        mean_val = statistics.mean(historical_values)
        cv = volatility / mean_val if mean_val > 0 else 0  # Coefficient of variation

        # Calculate recent trend strength
        trend_slope = self.calculate_trend_slope(historical_values[-14:])
        trend_strength = abs(trend_slope) / mean_val if mean_val > 0 else 0

        # Decision logic:
        # - High volatility + weak trend -> mean reversion
        # - Strong trend -> EMA with trend extrapolation
        if cv > 0.3 and trend_strength < 0.05:
            return self.forecast_mean_reversion(keyword, historical_values, days_ahead)
        else:
            return self.forecast_ema(keyword, historical_values, days_ahead)

    def batch_forecast(
        self,
        items: List[Dict],
        days_ahead: int = 14
    ) -> List[Forecast]:
        """
        Generate forecasts for multiple items

        Args:
            items: List of dicts with 'keyword' and 'history' keys
            days_ahead: Number of days to forecast

        Returns:
            List of Forecast objects
        """
        forecasts = []

        for item in items:
            keyword = item.get('keyword', 'unknown')
            history = item.get('history', [])

            forecast = self.get_best_forecast(keyword, history, days_ahead)
            forecasts.append(forecast)

        return forecasts
