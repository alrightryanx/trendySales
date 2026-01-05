"""
Anomaly Detection Engine
Detects unusual market behavior using statistical methods
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import statistics
import math


@dataclass
class Anomaly:
    """Detected anomaly with context"""
    keyword: str
    anomaly_type: str  # SPIKE, DROP, PATTERN_BREAK, VOLUME_SURGE
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL
    z_score: float
    current_value: float
    expected_value: float
    deviation_percent: float
    message: str
    detected_at: datetime

    def to_dict(self) -> Dict:
        return {
            "keyword": self.keyword,
            "anomaly_type": self.anomaly_type,
            "severity": self.severity,
            "z_score": round(self.z_score, 2),
            "current_value": round(self.current_value, 2),
            "expected_value": round(self.expected_value, 2),
            "deviation_percent": round(self.deviation_percent, 1),
            "message": self.message,
            "detected_at": self.detected_at.isoformat()
        }


class AnomalyDetector:
    """
    Statistical anomaly detection for market data
    Uses Z-score analysis, spike detection, and pattern matching
    """

    # Z-score thresholds
    LOW_THRESHOLD = 1.5
    MEDIUM_THRESHOLD = 2.0
    HIGH_THRESHOLD = 2.5
    CRITICAL_THRESHOLD = 3.0

    # Minimum samples for reliable statistics
    MIN_SAMPLES = 7

    def __init__(self):
        pass

    def calculate_z_score(self, value: float, mean: float, std: float) -> float:
        """Calculate Z-score for a value"""
        if std == 0:
            return 0.0
        return (value - mean) / std

    def get_severity(self, z_score: float) -> str:
        """Determine severity based on Z-score"""
        abs_z = abs(z_score)
        if abs_z >= self.CRITICAL_THRESHOLD:
            return "CRITICAL"
        elif abs_z >= self.HIGH_THRESHOLD:
            return "HIGH"
        elif abs_z >= self.MEDIUM_THRESHOLD:
            return "MEDIUM"
        elif abs_z >= self.LOW_THRESHOLD:
            return "LOW"
        return "NONE"

    def detect_value_anomaly(
        self,
        keyword: str,
        current_value: float,
        historical_values: List[float]
    ) -> Optional[Anomaly]:
        """
        Detect if current value is anomalous compared to history

        Args:
            keyword: Item identifier
            current_value: Latest value to test
            historical_values: Historical values (excluding current)

        Returns:
            Anomaly object if detected, None otherwise
        """
        if len(historical_values) < self.MIN_SAMPLES:
            return None

        mean = statistics.mean(historical_values)
        std = statistics.stdev(historical_values)

        if std == 0:
            return None

        z_score = self.calculate_z_score(current_value, mean, std)
        severity = self.get_severity(z_score)

        if severity == "NONE":
            return None

        # Determine anomaly type
        if z_score > 0:
            anomaly_type = "SPIKE"
            direction = "above"
        else:
            anomaly_type = "DROP"
            direction = "below"

        deviation_percent = ((current_value - mean) / mean) * 100 if mean != 0 else 0

        message = (
            f"{keyword} STR is {abs(deviation_percent):.1f}% {direction} normal "
            f"(current: {current_value:.1f}%, expected: {mean:.1f}%)"
        )

        return Anomaly(
            keyword=keyword,
            anomaly_type=anomaly_type,
            severity=severity,
            z_score=z_score,
            current_value=current_value,
            expected_value=mean,
            deviation_percent=deviation_percent,
            message=message,
            detected_at=datetime.utcnow()
        )

    def detect_spike(
        self,
        keyword: str,
        values: List[float],
        lookback: int = 7,
        threshold_multiplier: float = 2.0
    ) -> Optional[Anomaly]:
        """
        Detect sudden spikes in recent data

        Args:
            keyword: Item identifier
            values: Time series values (newest last)
            lookback: Number of recent values to compare
            threshold_multiplier: How many times larger than average to trigger

        Returns:
            Anomaly if spike detected
        """
        if len(values) < lookback + 1:
            return None

        recent_value = values[-1]
        baseline_values = values[-(lookback + 1):-1]
        baseline_mean = statistics.mean(baseline_values)
        baseline_std = statistics.stdev(baseline_values) if len(baseline_values) > 1 else 0

        if baseline_mean == 0:
            return None

        ratio = recent_value / baseline_mean

        if ratio >= threshold_multiplier:
            z_score = self.calculate_z_score(recent_value, baseline_mean, baseline_std) if baseline_std > 0 else 0
            deviation_percent = (ratio - 1) * 100

            return Anomaly(
                keyword=keyword,
                anomaly_type="SPIKE",
                severity="HIGH" if ratio >= 3 else "MEDIUM",
                z_score=z_score,
                current_value=recent_value,
                expected_value=baseline_mean,
                deviation_percent=deviation_percent,
                message=f"{keyword} spiked {deviation_percent:.0f}% vs {lookback}-day average",
                detected_at=datetime.utcnow()
            )

        return None

    def detect_volume_surge(
        self,
        keyword: str,
        current_volume: int,
        historical_volumes: List[int]
    ) -> Optional[Anomaly]:
        """Detect unusual volume surges"""
        if len(historical_volumes) < self.MIN_SAMPLES:
            return None

        mean_volume = statistics.mean(historical_volumes)
        std_volume = statistics.stdev(historical_volumes)

        if std_volume == 0:
            return None

        z_score = self.calculate_z_score(current_volume, mean_volume, std_volume)
        severity = self.get_severity(z_score)

        if severity == "NONE" or z_score < 0:  # Only care about positive surges
            return None

        deviation_percent = ((current_volume - mean_volume) / mean_volume) * 100

        return Anomaly(
            keyword=keyword,
            anomaly_type="VOLUME_SURGE",
            severity=severity,
            z_score=z_score,
            current_value=float(current_volume),
            expected_value=mean_volume,
            deviation_percent=deviation_percent,
            message=f"{keyword} volume surged {deviation_percent:.0f}% above normal ({current_volume} vs avg {mean_volume:.0f})",
            detected_at=datetime.utcnow()
        )

    def detect_pattern_break(
        self,
        keyword: str,
        values: List[float],
        window: int = 14
    ) -> Optional[Anomaly]:
        """
        Detect when an item breaks its established pattern
        (e.g., stable item suddenly becomes volatile)
        """
        if len(values) < window * 2:
            return None

        # Split into two halves
        older_half = values[-window * 2:-window]
        recent_half = values[-window:]

        # Compare volatility
        older_std = statistics.stdev(older_half)
        recent_std = statistics.stdev(recent_half)

        if older_std == 0:
            return None

        volatility_ratio = recent_std / older_std

        # Also check mean shift
        older_mean = statistics.mean(older_half)
        recent_mean = statistics.mean(recent_half)
        mean_shift = ((recent_mean - older_mean) / older_mean) * 100 if older_mean != 0 else 0

        # Significant pattern break if volatility increased 2x+ OR mean shifted 30%+
        if volatility_ratio >= 2.0 or abs(mean_shift) >= 30:
            severity = "HIGH" if volatility_ratio >= 3.0 or abs(mean_shift) >= 50 else "MEDIUM"

            if volatility_ratio >= 2.0 and abs(mean_shift) >= 30:
                message = f"{keyword} pattern break: volatility {volatility_ratio:.1f}x and mean shift {mean_shift:+.0f}%"
            elif volatility_ratio >= 2.0:
                message = f"{keyword} volatility increased {volatility_ratio:.1f}x"
            else:
                message = f"{keyword} mean shifted {mean_shift:+.0f}% from baseline"

            return Anomaly(
                keyword=keyword,
                anomaly_type="PATTERN_BREAK",
                severity=severity,
                z_score=volatility_ratio,  # Using ratio as proxy
                current_value=recent_mean,
                expected_value=older_mean,
                deviation_percent=mean_shift,
                message=message,
                detected_at=datetime.utcnow()
            )

        return None

    def analyze_batch(
        self,
        items: List[Dict]
    ) -> List[Anomaly]:
        """
        Analyze multiple items and return all anomalies

        Args:
            items: List of dicts with 'keyword', 'current_value', 'history' keys

        Returns:
            List of detected anomalies, sorted by severity
        """
        anomalies = []

        for item in items:
            keyword = item.get('keyword', 'unknown')
            current = item.get('current_value', 0)
            history = item.get('history', [])

            # Check for value anomaly
            anomaly = self.detect_value_anomaly(keyword, current, history)
            if anomaly:
                anomalies.append(anomaly)

            # Check for spike
            if history:
                all_values = history + [current]
                spike = self.detect_spike(keyword, all_values)
                if spike:
                    anomalies.append(spike)

            # Check for pattern break
            if history:
                all_values = history + [current]
                pattern_break = self.detect_pattern_break(keyword, all_values)
                if pattern_break:
                    anomalies.append(pattern_break)

        # Sort by severity
        severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        anomalies.sort(key=lambda a: severity_order.get(a.severity, 4))

        return anomalies

    def get_anomaly_summary(self, anomalies: List[Anomaly]) -> Dict:
        """Generate summary statistics for detected anomalies"""
        if not anomalies:
            return {
                "total": 0,
                "by_severity": {},
                "by_type": {},
                "most_severe": None
            }

        by_severity = {}
        by_type = {}

        for a in anomalies:
            by_severity[a.severity] = by_severity.get(a.severity, 0) + 1
            by_type[a.anomaly_type] = by_type.get(a.anomaly_type, 0) + 1

        return {
            "total": len(anomalies),
            "by_severity": by_severity,
            "by_type": by_type,
            "most_severe": anomalies[0].to_dict() if anomalies else None
        }
