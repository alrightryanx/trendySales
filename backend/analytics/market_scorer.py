"""
Market Opportunity Scorer
Computes composite opportunity scores for prioritization
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class OpportunityLevel(Enum):
    EXCEPTIONAL = "EXCEPTIONAL"  # 90-100
    HIGH = "HIGH"                # 70-89
    MEDIUM = "MEDIUM"            # 50-69
    LOW = "LOW"                  # 30-49
    POOR = "POOR"                # 0-29


@dataclass
class MarketScore:
    """Complete market opportunity score with breakdown"""
    keyword: str

    # Overall
    total_score: float  # 0-100
    opportunity_level: str
    confidence: str  # LOW, MEDIUM, HIGH (based on data quality)

    # Component Scores (all 0-100)
    velocity_score: float
    supply_score: float
    momentum_score: float
    stability_score: float
    volume_score: float

    # Raw Metrics for Context
    sell_through_rate: float
    active_listings: int
    volume_sold: int
    momentum_7d: Optional[float]
    volatility: Optional[float]

    # Analysis
    strengths: List[str]
    weaknesses: List[str]
    recommendation: str

    def to_dict(self) -> Dict:
        return {
            "keyword": self.keyword,
            "total_score": round(self.total_score, 1),
            "opportunity_level": self.opportunity_level,
            "confidence": self.confidence,
            "components": {
                "velocity": round(self.velocity_score, 1),
                "supply": round(self.supply_score, 1),
                "momentum": round(self.momentum_score, 1),
                "stability": round(self.stability_score, 1),
                "volume": round(self.volume_score, 1)
            },
            "metrics": {
                "str": round(self.sell_through_rate, 1),
                "active_listings": self.active_listings,
                "volume_sold": self.volume_sold,
                "momentum_7d": round(self.momentum_7d, 1) if self.momentum_7d else None,
                "volatility": round(self.volatility, 2) if self.volatility else None
            },
            "strengths": self.strengths,
            "weaknesses": self.weaknesses,
            "recommendation": self.recommendation
        }


class MarketScorer:
    """
    Professional market opportunity scoring engine
    Calculates composite scores for investment/effort prioritization
    """

    # Score weights (must sum to 1.0)
    WEIGHTS = {
        "velocity": 0.30,    # How fast items are selling
        "supply": 0.25,      # Supply scarcity (lower = better)
        "momentum": 0.20,    # Trend direction
        "stability": 0.15,   # Price/STR stability
        "volume": 0.10       # Market size (higher volume = proven demand)
    }

    # Thresholds for scoring
    STR_EXCELLENT = 80.0
    STR_GOOD = 50.0
    STR_FAIR = 30.0

    SUPPLY_LOW = 100       # < 100 listings = scarce
    SUPPLY_MEDIUM = 500    # < 500 listings = moderate
    SUPPLY_HIGH = 2000     # > 2000 = oversaturated

    VOLUME_HIGH = 500      # > 500 sold = proven market
    VOLUME_MEDIUM = 100    # > 100 sold = viable
    VOLUME_LOW = 30        # > 30 sold = emerging

    def __init__(self):
        pass

    def score_velocity(self, str_pct: float) -> float:
        """Score based on sell-through rate"""
        if str_pct >= self.STR_EXCELLENT:
            return 90 + min(10, (str_pct - self.STR_EXCELLENT) / 2)
        elif str_pct >= self.STR_GOOD:
            return 60 + ((str_pct - self.STR_GOOD) / (self.STR_EXCELLENT - self.STR_GOOD)) * 30
        elif str_pct >= self.STR_FAIR:
            return 30 + ((str_pct - self.STR_FAIR) / (self.STR_GOOD - self.STR_FAIR)) * 30
        else:
            return (str_pct / self.STR_FAIR) * 30

    def score_supply(self, active_listings: int) -> float:
        """Score based on supply scarcity (lower supply = higher score)"""
        if active_listings <= self.SUPPLY_LOW:
            return 90 + min(10, (self.SUPPLY_LOW - active_listings) / 10)
        elif active_listings <= self.SUPPLY_MEDIUM:
            return 60 + ((self.SUPPLY_MEDIUM - active_listings) / (self.SUPPLY_MEDIUM - self.SUPPLY_LOW)) * 30
        elif active_listings <= self.SUPPLY_HIGH:
            return 30 + ((self.SUPPLY_HIGH - active_listings) / (self.SUPPLY_HIGH - self.SUPPLY_MEDIUM)) * 30
        else:
            # Oversaturated
            return max(0, 30 - ((active_listings - self.SUPPLY_HIGH) / 100))

    def score_momentum(self, momentum_7d: Optional[float]) -> float:
        """Score based on 7-day momentum"""
        if momentum_7d is None:
            return 50  # Neutral if no data

        if momentum_7d >= 20:
            return 95
        elif momentum_7d >= 10:
            return 80 + (momentum_7d - 10)
        elif momentum_7d >= 5:
            return 65 + (momentum_7d - 5) * 3
        elif momentum_7d >= 0:
            return 50 + momentum_7d * 3
        elif momentum_7d >= -5:
            return 50 + momentum_7d * 4
        elif momentum_7d >= -10:
            return 30 + (momentum_7d + 10) * 4
        else:
            return max(0, 30 + (momentum_7d + 10) * 2)

    def score_stability(self, volatility: Optional[float], avg_str: float) -> float:
        """Score based on price/STR stability"""
        if volatility is None:
            return 50  # Neutral if no data

        # Coefficient of variation (CV) - volatility relative to mean
        if avg_str == 0:
            return 50

        cv = volatility / avg_str

        if cv <= 0.1:
            return 95  # Very stable
        elif cv <= 0.2:
            return 80 + (0.2 - cv) * 150
        elif cv <= 0.3:
            return 60 + (0.3 - cv) * 200
        elif cv <= 0.5:
            return 30 + (0.5 - cv) * 150
        else:
            return max(0, 30 - (cv - 0.5) * 50)

    def score_volume(self, volume_sold: int) -> float:
        """Score based on market volume"""
        if volume_sold >= self.VOLUME_HIGH:
            return 85 + min(15, (volume_sold - self.VOLUME_HIGH) / 100)
        elif volume_sold >= self.VOLUME_MEDIUM:
            return 60 + ((volume_sold - self.VOLUME_MEDIUM) / (self.VOLUME_HIGH - self.VOLUME_MEDIUM)) * 25
        elif volume_sold >= self.VOLUME_LOW:
            return 35 + ((volume_sold - self.VOLUME_LOW) / (self.VOLUME_MEDIUM - self.VOLUME_LOW)) * 25
        else:
            return (volume_sold / self.VOLUME_LOW) * 35

    def get_opportunity_level(self, score: float) -> str:
        """Convert numeric score to opportunity level"""
        if score >= 90:
            return OpportunityLevel.EXCEPTIONAL.value
        elif score >= 70:
            return OpportunityLevel.HIGH.value
        elif score >= 50:
            return OpportunityLevel.MEDIUM.value
        elif score >= 30:
            return OpportunityLevel.LOW.value
        else:
            return OpportunityLevel.POOR.value

    def get_confidence(self, data_points: int, has_history: bool) -> str:
        """Determine confidence level based on data quality"""
        if data_points >= 30 and has_history:
            return "HIGH"
        elif data_points >= 7:
            return "MEDIUM"
        else:
            return "LOW"

    def identify_strengths_weaknesses(
        self,
        velocity_score: float,
        supply_score: float,
        momentum_score: float,
        stability_score: float,
        volume_score: float
    ) -> tuple:
        """Identify key strengths and weaknesses"""
        strengths = []
        weaknesses = []

        scores = {
            "velocity": (velocity_score, "High demand velocity", "Low demand velocity"),
            "supply": (supply_score, "Limited supply", "Oversaturated market"),
            "momentum": (momentum_score, "Positive trend momentum", "Declining trend"),
            "stability": (stability_score, "Stable performance", "High volatility"),
            "volume": (volume_score, "Proven market volume", "Limited market size")
        }

        for _, (score, strength_msg, weakness_msg) in scores.items():
            if score >= 70:
                strengths.append(strength_msg)
            elif score < 40:
                weaknesses.append(weakness_msg)

        return strengths[:3], weaknesses[:3]  # Limit to top 3 each

    def generate_recommendation(
        self,
        total_score: float,
        strengths: List[str],
        weaknesses: List[str],
        momentum_score: float
    ) -> str:
        """Generate actionable recommendation"""
        if total_score >= 90:
            return "STRONG BUY - Exceptional opportunity with high demand and limited supply"
        elif total_score >= 75:
            if momentum_score >= 70:
                return "BUY - Strong fundamentals with positive momentum"
            else:
                return "BUY - Strong fundamentals, monitor for momentum shift"
        elif total_score >= 60:
            if len(weaknesses) == 0:
                return "CONSIDER - Balanced opportunity with no major concerns"
            else:
                return f"CONSIDER - Watch for: {weaknesses[0]}" if weaknesses else "CONSIDER"
        elif total_score >= 45:
            return "HOLD - Mixed signals, wait for clearer trend"
        elif total_score >= 30:
            return "AVOID - Unfavorable conditions"
        else:
            return "STRONG AVOID - Poor market conditions"

    def score(
        self,
        keyword: str,
        sell_through_rate: float,
        active_listings: int,
        volume_sold: int,
        momentum_7d: Optional[float] = None,
        volatility: Optional[float] = None,
        data_points: int = 1,
        has_history: bool = False
    ) -> MarketScore:
        """
        Calculate comprehensive market opportunity score

        Args:
            keyword: Item identifier
            sell_through_rate: Current STR percentage
            active_listings: Number of active listings
            volume_sold: Number of items sold
            momentum_7d: 7-day momentum (% change)
            volatility: Standard deviation of STR
            data_points: Number of historical data points
            has_history: Whether historical data exists

        Returns:
            MarketScore with full breakdown
        """
        # Calculate component scores
        velocity_score = self.score_velocity(sell_through_rate)
        supply_score = self.score_supply(active_listings)
        momentum_score = self.score_momentum(momentum_7d)
        stability_score = self.score_stability(volatility, sell_through_rate)
        volume_score = self.score_volume(volume_sold)

        # Calculate weighted total
        total_score = (
            velocity_score * self.WEIGHTS["velocity"] +
            supply_score * self.WEIGHTS["supply"] +
            momentum_score * self.WEIGHTS["momentum"] +
            stability_score * self.WEIGHTS["stability"] +
            volume_score * self.WEIGHTS["volume"]
        )

        # Get level and confidence
        opportunity_level = self.get_opportunity_level(total_score)
        confidence = self.get_confidence(data_points, has_history)

        # Identify strengths and weaknesses
        strengths, weaknesses = self.identify_strengths_weaknesses(
            velocity_score, supply_score, momentum_score, stability_score, volume_score
        )

        # Generate recommendation
        recommendation = self.generate_recommendation(
            total_score, strengths, weaknesses, momentum_score
        )

        return MarketScore(
            keyword=keyword,
            total_score=total_score,
            opportunity_level=opportunity_level,
            confidence=confidence,
            velocity_score=velocity_score,
            supply_score=supply_score,
            momentum_score=momentum_score,
            stability_score=stability_score,
            volume_score=volume_score,
            sell_through_rate=sell_through_rate,
            active_listings=active_listings,
            volume_sold=volume_sold,
            momentum_7d=momentum_7d,
            volatility=volatility,
            strengths=strengths,
            weaknesses=weaknesses,
            recommendation=recommendation
        )

    def rank_opportunities(self, items: List[Dict]) -> List[MarketScore]:
        """
        Score and rank multiple items

        Args:
            items: List of dicts with required metrics

        Returns:
            List of MarketScore objects, sorted by score descending
        """
        scores = []

        for item in items:
            score = self.score(
                keyword=item.get("keyword", "unknown"),
                sell_through_rate=item.get("sell_through_rate", 0),
                active_listings=item.get("active_listings", 1000),
                volume_sold=item.get("volume_sold", 0),
                momentum_7d=item.get("momentum_7d"),
                volatility=item.get("volatility"),
                data_points=item.get("data_points", 1),
                has_history=item.get("has_history", False)
            )
            scores.append(score)

        # Sort by total score descending
        scores.sort(key=lambda s: s.total_score, reverse=True)

        return scores
