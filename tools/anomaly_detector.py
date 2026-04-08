"""Anomaly detection tools for time series metrics."""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import statistics


@dataclass
class Anomaly:
    """Represents a detected anomaly in time series data."""
    timestamp: str
    value: float
    expected_value: float
    deviation: float
    severity: str  # "low", "medium", "high", "critical"
    metric_name: str
    anomaly_type: str  # "spike", "drop", "sustained_high", "sustained_low"


@dataclass
class AnomalyReport:
    """Report of anomalies detected in a metric."""
    metric_name: str
    total_anomalies: int
    critical_anomalies: int
    high_anomalies: int
    recent_anomalies_24h: int
    anomaly_rate: float  # Percentage of data points that are anomalous
    anomalies: List[Anomaly]
    trend_anomalies: bool  # Whether there's an anomalous trend
    recommendation: str


class AnomalyDetector:
    """Detects anomalies in time series metrics using statistical methods."""
    
    def __init__(self, sensitivity: float = 2.0):
        """
        Initialize the anomaly detector.
        
        Args:
            sensitivity: Standard deviation multiplier for anomaly detection.
                        Lower values = more sensitive (more anomalies detected)
                        Higher values = less sensitive (fewer anomalies detected)
        """
        self.sensitivity = sensitivity
        print(f"Initializing AnomalyDetector with sensitivity={sensitivity}")
    
    def detect_anomalies_in_metric(self, metric_data: Dict[str, Any]) -> AnomalyReport:
        """Detect anomalies in a single metric time series."""
        metric_name = metric_data["metric_name"]
        data_points = metric_data["data_points"]
        
        print(f"Detecting anomalies in {metric_name} ({len(data_points)} data points)")
        
        if len(data_points) < 10:
            print(f"Warning: Insufficient data points for {metric_name}")
            return AnomalyReport(
                metric_name=metric_name,
                total_anomalies=0,
                critical_anomalies=0,
                high_anomalies=0,
                recent_anomalies_24h=0,
                anomaly_rate=0.0,
                anomalies=[],
                trend_anomalies=False,
                recommendation="Insufficient data for analysis"
            )
        
        anomalies = []
        values = [point["value"] for point in data_points]
        
        # Calculate statistical baselines
        mean_value = statistics.mean(values)
        std_dev = statistics.stdev(values) if len(values) > 1 else 0
        
        # Use rolling window for more accurate anomaly detection
        window_size = min(24, len(data_points) // 4)  # 24 hours or 1/4 of data
        
        for i, point in enumerate(data_points):
            # Calculate expected value using rolling window
            start_idx = max(0, i - window_size)
            end_idx = min(len(data_points), i + window_size + 1)
            window_values = values[start_idx:end_idx]
            
            if len(window_values) < 3:
                continue
            
            window_mean = statistics.mean(window_values)
            window_std = statistics.stdev(window_values) if len(window_values) > 1 else 0
            
            if window_std == 0:
                continue
            
            # Calculate deviation
            deviation = abs(point["value"] - window_mean) / window_std
            
            # Check if it's an anomaly
            if deviation > self.sensitivity:
                severity = self._classify_anomaly_severity(deviation, self.sensitivity)
                anomaly_type = self._classify_anomaly_type(
                    point["value"], window_mean, values[max(0, i-5):i+1]
                )
                
                anomaly = Anomaly(
                    timestamp=point["timestamp"],
                    value=point["value"],
                    expected_value=window_mean,
                    deviation=deviation,
                    severity=severity,
                    metric_name=metric_name,
                    anomaly_type=anomaly_type
                )
                anomalies.append(anomaly)
                print(f"Anomaly detected: {anomaly_type} at {point['timestamp']}, "
                      f"value={point['value']:.2f}, expected={window_mean:.2f}, "
                      f"deviation={deviation:.2f}, severity={severity}")
        
        # Count anomalies by severity
        critical_count = sum(1 for a in anomalies if a.severity == "critical")
        high_count = sum(1 for a in anomalies if a.severity == "high")
        
        # Count recent anomalies (last 24 hours)
        now = datetime.now()
        recent_anomalies = sum(
            1 for a in anomalies 
            if (now - datetime.fromisoformat(a.timestamp)).total_seconds() < 86400
        )
        
        # Calculate anomaly rate
        anomaly_rate = (len(anomalies) / len(data_points)) * 100
        
        # Check for trend anomalies
        trend_anomalies = self._detect_trend_anomalies(values, metric_name)
        
        # Generate recommendation
        recommendation = self._generate_anomaly_recommendation(
            len(anomalies), critical_count, high_count, recent_anomalies, 
            anomaly_rate, trend_anomalies, metric_name
        )
        
        report = AnomalyReport(
            metric_name=metric_name,
            total_anomalies=len(anomalies),
            critical_anomalies=critical_count,
            high_anomalies=high_count,
            recent_anomalies_24h=recent_anomalies,
            anomaly_rate=anomaly_rate,
            anomalies=anomalies,
            trend_anomalies=trend_anomalies,
            recommendation=recommendation
        )
        
        print(f"Anomaly detection complete: {len(anomalies)} anomalies found "
              f"({critical_count} critical, {high_count} high)")
        
        return report
    
    def _classify_anomaly_severity(self, deviation: float, sensitivity: float) -> str:
        """Classify anomaly severity based on deviation magnitude."""
        if deviation > sensitivity * 3:
            return "critical"
        elif deviation > sensitivity * 2:
            return "high"
        elif deviation > sensitivity * 1.5:
            return "medium"
        else:
            return "low"
    
    def _classify_anomaly_type(
        self, 
        current_value: float, 
        expected_value: float, 
        recent_values: List[float]
    ) -> str:
        """Classify the type of anomaly."""
        if current_value > expected_value * 1.5:
            # Check if it's a sustained high
            if len(recent_values) >= 3 and all(v > expected_value for v in recent_values[-3:]):
                return "sustained_high"
            else:
                return "spike"
        elif current_value < expected_value * 0.5:
            # Check if it's a sustained low
            if len(recent_values) >= 3 and all(v < expected_value for v in recent_values[-3:]):
                return "sustained_low"
            else:
                return "drop"
        else:
            return "deviation"
    
    def _detect_trend_anomalies(self, values: List[float], metric_name: str) -> bool:
        """Detect if there's an anomalous trend in the data."""
        if len(values) < 20:
            return False
        
        # Split data into two halves and compare
        mid_point = len(values) // 2
        first_half = values[:mid_point]
        second_half = values[mid_point:]
        
        first_mean = statistics.mean(first_half)
        second_mean = statistics.mean(second_half)
        
        # Calculate relative change
        if first_mean != 0:
            relative_change = abs((second_mean - first_mean) / first_mean)
        else:
            relative_change = 0
        
        # Different thresholds for different metric types
        if any(term in metric_name.lower() for term in ["error", "latency", "ticket"]):
            # For "bad" metrics, increasing trend is anomalous
            threshold = 0.3  # 30% increase is concerning
            return relative_change > threshold and second_mean > first_mean
        else:
            # For "good" metrics, decreasing trend is anomalous
            threshold = 0.2  # 20% decrease is concerning
            return relative_change > threshold and second_mean < first_mean
    
    def _generate_anomaly_recommendation(
        self,
        total_anomalies: int,
        critical_count: int,
        high_count: int,
        recent_count: int,
        anomaly_rate: float,
        trend_anomalies: bool,
        metric_name: str
    ) -> str:
        """Generate recommendation based on anomaly analysis."""
        
        if critical_count > 0 or recent_count > 3:
            return f"CRITICAL: {critical_count} critical anomalies detected, immediate investigation required"
        
        if trend_anomalies:
            return f"HIGH RISK: Anomalous trend detected in {metric_name}, monitor closely"
        
        if high_count > 2:
            return f"MODERATE RISK: {high_count} high-severity anomalies detected"
        
        if anomaly_rate > 10:
            return f"ELEVATED: High anomaly rate ({anomaly_rate:.1f}%), investigate data quality"
        
        if total_anomalies > 0:
            return f"LOW RISK: {total_anomalies} minor anomalies detected, continue monitoring"
        
        return "NORMAL: No significant anomalies detected"
    
    def analyze_all_metrics(self, metrics_data: Dict[str, Any]) -> Dict[str, AnomalyReport]:
        """Analyze anomalies across all metrics."""
        reports = {}
        
        for metric_name, metric_data in metrics_data.get("metrics", {}).items():
            reports[metric_name] = self.detect_anomalies_in_metric(metric_data)
        
        print(f"Analyzed anomalies across {len(reports)} metrics")
        return reports
    
    def get_critical_anomalies(self, metrics_data: Dict[str, Any]) -> List[Anomaly]:
        """Get all critical anomalies across all metrics."""
        critical_anomalies = []
        
        reports = self.analyze_all_metrics(metrics_data)
        for report in reports.values():
            critical_anomalies.extend([a for a in report.anomalies if a.severity == "critical"])
        
        # Sort by timestamp (most recent first)
        critical_anomalies.sort(key=lambda x: x.timestamp, reverse=True)
        
        print(f"Found {len(critical_anomalies)} critical anomalies across all metrics")
        return critical_anomalies
    
    def get_anomaly_summary(self, metrics_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get comprehensive anomaly summary across all metrics."""
        reports = self.analyze_all_metrics(metrics_data)
        
        total_anomalies = sum(report.total_anomalies for report in reports.values())
        total_critical = sum(report.critical_anomalies for report in reports.values())
        total_high = sum(report.high_anomalies for report in reports.values())
        total_recent = sum(report.recent_anomalies_24h for report in reports.values())
        
        # Find metrics with trend anomalies
        trend_anomaly_metrics = [
            name for name, report in reports.items() if report.trend_anomalies
        ]
        
        # Get top concerning metrics
        concerning_metrics = []
        for name, report in reports.items():
            if report.critical_anomalies > 0 or report.recent_anomalies_24h > 2:
                concerning_metrics.append({
                    "metric": name,
                    "critical_anomalies": report.critical_anomalies,
                    "recent_anomalies": report.recent_anomalies_24h,
                    "recommendation": report.recommendation
                })
        
        # Sort by severity
        concerning_metrics.sort(
            key=lambda x: (x["critical_anomalies"], x["recent_anomalies"]), 
            reverse=True
        )
        
        summary = {
            "total_anomalies": total_anomalies,
            "critical_anomalies": total_critical,
            "high_anomalies": total_high,
            "recent_anomalies_24h": total_recent,
            "metrics_with_trend_anomalies": trend_anomaly_metrics,
            "concerning_metrics": concerning_metrics[:5],  # Top 5
            "overall_risk_level": self._assess_overall_risk(
                total_critical, total_high, total_recent, len(trend_anomaly_metrics)
            ),
            "detailed_reports": reports
        }
        
        print(f"Anomaly summary: {total_anomalies} total, {total_critical} critical, "
              f"{len(concerning_metrics)} concerning metrics")
        
        return summary
    
    def _assess_overall_risk(
        self, 
        critical_count: int, 
        high_count: int, 
        recent_count: int, 
        trend_count: int
    ) -> str:
        """Assess overall risk level based on anomaly counts."""
        
        if critical_count > 2 or recent_count > 5:
            return "CRITICAL"
        elif critical_count > 0 or trend_count > 2 or recent_count > 3:
            return "HIGH"
        elif high_count > 3 or trend_count > 0 or recent_count > 1:
            return "MEDIUM"
        elif high_count > 0:
            return "LOW"
        else:
            return "NORMAL"