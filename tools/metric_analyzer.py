"""Metric analysis tools for the War Room system."""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass


@dataclass
class MetricSummary:
    """Summary statistics for a metric."""
    metric_name: str
    current_value: float
    baseline_value: Optional[float]
    target_value: Optional[float]
    percent_change_from_baseline: Optional[float]
    trend_direction: str  # "increasing", "decreasing", "stable"
    trend_strength: float  # 0-1, how strong the trend is
    threshold_status: str  # "normal", "warning", "critical"
    data_points_count: int
    time_range_hours: int


@dataclass
class TrendAnalysis:
    """Trend analysis results."""
    metric_name: str
    slope: float  # Rate of change per hour
    direction: str  # "increasing", "decreasing", "stable"
    strength: float  # 0-1, confidence in trend
    recent_acceleration: bool  # Is trend accelerating recently?


class MetricAnalyzer:
    """Analyzes time series metrics and provides insights."""
    
    def __init__(self):
        """Initialize the metric analyzer."""
        print("Initializing MetricAnalyzer...")
    
    def load_metrics_from_file(self, filepath: str) -> Dict[str, Any]:
        """Load metrics data from JSON file."""
        print(f"Loading metrics from {filepath}")
        with open(filepath, 'r') as f:
            data = json.load(f)
        print(f"Loaded {len(data.get('metrics', {}))} metrics")
        return data
    
    def analyze_metric(self, metric_data: Dict[str, Any]) -> MetricSummary:
        """Analyze a single metric and return summary statistics."""
        metric_name = metric_data["metric_name"]
        data_points = metric_data["data_points"]
        
        print(f"Analyzing metric: {metric_name}")
        
        if not data_points:
            print(f"Warning: No data points for {metric_name}")
            return MetricSummary(
                metric_name=metric_name,
                current_value=0,
                baseline_value=metric_data.get("baseline"),
                target_value=metric_data.get("target"),
                percent_change_from_baseline=None,
                trend_direction="unknown",
                trend_strength=0,
                threshold_status="unknown",
                data_points_count=0,
                time_range_hours=0
            )
        
        # Get current and baseline values
        current_value = data_points[-1]["value"]
        baseline_value = metric_data.get("baseline")
        target_value = metric_data.get("target")
        
        # Calculate percent change from baseline
        percent_change = None
        if baseline_value and baseline_value != 0:
            percent_change = ((current_value - baseline_value) / baseline_value) * 100
            print(f"{metric_name}: Current={current_value}, Baseline={baseline_value}, Change={percent_change:+.1f}%")
        
        # Analyze trend
        trend = self._analyze_trend(data_points)
        
        # Check threshold status
        threshold_status = self._check_thresholds(
            current_value, 
            metric_data.get("threshold_warning"),
            metric_data.get("threshold_critical"),
            metric_name
        )
        
        # Calculate time range
        if len(data_points) >= 2:
            start_time = datetime.fromisoformat(data_points[0]["timestamp"])
            end_time = datetime.fromisoformat(data_points[-1]["timestamp"])
            time_range_hours = int((end_time - start_time).total_seconds() / 3600)
        else:
            time_range_hours = 0
        
        return MetricSummary(
            metric_name=metric_name,
            current_value=current_value,
            baseline_value=baseline_value,
            target_value=target_value,
            percent_change_from_baseline=percent_change,
            trend_direction=trend.direction,
            trend_strength=trend.strength,
            threshold_status=threshold_status,
            data_points_count=len(data_points),
            time_range_hours=time_range_hours
        )
    
    def _analyze_trend(self, data_points: List[Dict]) -> TrendAnalysis:
        """Analyze trend in time series data."""
        if len(data_points) < 3:
            return TrendAnalysis("", 0, "stable", 0, False)
        
        # Simple linear regression to find slope
        values = [point["value"] for point in data_points]
        n = len(values)
        x_values = list(range(n))
        
        # Calculate slope (rate of change)
        sum_x = sum(x_values)
        sum_y = sum(values)
        sum_xy = sum(x * y for x, y in zip(x_values, values))
        sum_x2 = sum(x * x for x in x_values)
        
        if n * sum_x2 - sum_x * sum_x == 0:
            slope = 0
        else:
            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
        
        # Determine direction and strength
        abs_slope = abs(slope)
        avg_value = sum_y / n
        
        # Normalize slope by average value to get relative strength
        if avg_value != 0:
            normalized_slope = abs_slope / avg_value
            strength = min(normalized_slope * 100, 1.0)  # Cap at 1.0
        else:
            strength = 0
        
        if abs_slope < avg_value * 0.001:  # Very small change
            direction = "stable"
            strength = 0
        elif slope > 0:
            direction = "increasing"
        else:
            direction = "decreasing"
        
        # Check for recent acceleration (compare last 25% vs first 75%)
        split_point = int(n * 0.75)
        recent_values = values[split_point:]
        earlier_values = values[:split_point]
        
        recent_acceleration = False
        if len(recent_values) >= 2 and len(earlier_values) >= 2:
            recent_avg = sum(recent_values) / len(recent_values)
            earlier_avg = sum(earlier_values) / len(earlier_values)
            
            if direction == "increasing" and recent_avg > earlier_avg * 1.1:
                recent_acceleration = True
            elif direction == "decreasing" and recent_avg < earlier_avg * 0.9:
                recent_acceleration = True
        
        return TrendAnalysis(
            metric_name="",
            slope=slope,
            direction=direction,
            strength=strength,
            recent_acceleration=recent_acceleration
        )
    
    def _check_thresholds(
        self, 
        current_value: float, 
        warning_threshold: Optional[float],
        critical_threshold: Optional[float],
        metric_name: str
    ) -> str:
        """Check if metric value exceeds thresholds."""
        
        # For error rates and latency, higher is worse
        if "error" in metric_name.lower() or "latency" in metric_name.lower():
            if critical_threshold and current_value >= critical_threshold:
                print(f"CRITICAL: {metric_name} = {current_value} >= {critical_threshold}")
                return "critical"
            elif warning_threshold and current_value >= warning_threshold:
                print(f"WARNING: {metric_name} = {current_value} >= {warning_threshold}")
                return "warning"
        
        # For conversion rates, retention, etc., lower is worse
        elif any(term in metric_name.lower() for term in ["conversion", "retention", "success"]):
            if critical_threshold and current_value <= critical_threshold:
                print(f"CRITICAL: {metric_name} = {current_value} <= {critical_threshold}")
                return "critical"
            elif warning_threshold and current_value <= warning_threshold:
                print(f"WARNING: {metric_name} = {current_value} <= {warning_threshold}")
                return "warning"
        
        # For volume metrics like tickets, higher is worse
        elif "ticket" in metric_name.lower() or "volume" in metric_name.lower():
            if critical_threshold and current_value >= critical_threshold:
                print(f"CRITICAL: {metric_name} = {current_value} >= {critical_threshold}")
                return "critical"
            elif warning_threshold and current_value >= warning_threshold:
                print(f"WARNING: {metric_name} = {current_value} >= {warning_threshold}")
                return "warning"
        
        return "normal"
    
    def get_critical_metrics(self, metrics_data: Dict[str, Any]) -> List[MetricSummary]:
        """Get all metrics that are in critical state."""
        critical_metrics = []
        
        for metric_name, metric_data in metrics_data.get("metrics", {}).items():
            summary = self.analyze_metric(metric_data)
            if summary.threshold_status == "critical":
                critical_metrics.append(summary)
        
        print(f"Found {len(critical_metrics)} critical metrics")
        return critical_metrics
    
    def get_warning_metrics(self, metrics_data: Dict[str, Any]) -> List[MetricSummary]:
        """Get all metrics that are in warning state."""
        warning_metrics = []
        
        for metric_name, metric_data in metrics_data.get("metrics", {}).items():
            summary = self.analyze_metric(metric_data)
            if summary.threshold_status == "warning":
                warning_metrics.append(summary)
        
        print(f"Found {len(warning_metrics)} warning metrics")
        return warning_metrics
    
    def calculate_overall_health_score(self, metrics_data: Dict[str, Any]) -> float:
        """Calculate an overall health score (0-1) based on all metrics."""
        if not metrics_data.get("metrics"):
            return 0.5
        
        total_score = 0
        metric_count = 0
        
        for metric_name, metric_data in metrics_data.get("metrics", {}).items():
            summary = self.analyze_metric(metric_data)
            
            # Score based on threshold status
            if summary.threshold_status == "critical":
                score = 0.0
            elif summary.threshold_status == "warning":
                score = 0.3
            else:
                score = 1.0
            
            # Adjust score based on trend
            if summary.trend_direction == "decreasing" and any(
                term in metric_name.lower() for term in ["conversion", "retention", "success", "adoption"]
            ):
                score *= (1 - summary.trend_strength * 0.5)  # Penalize negative trends for good metrics
            elif summary.trend_direction == "increasing" and any(
                term in metric_name.lower() for term in ["error", "latency", "ticket"]
            ):
                score *= (1 - summary.trend_strength * 0.5)  # Penalize negative trends for bad metrics
            
            total_score += score
            metric_count += 1
        
        overall_score = total_score / metric_count if metric_count > 0 else 0.5
        print(f"Overall health score: {overall_score:.3f}")
        return overall_score
    
    def get_metric_insights(self, metrics_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get comprehensive insights about all metrics."""
        insights = {
            "overall_health_score": self.calculate_overall_health_score(metrics_data),
            "critical_metrics": [],
            "warning_metrics": [],
            "positive_trends": [],
            "negative_trends": [],
            "stable_metrics": [],
            "summary_stats": {}
        }
        
        for metric_name, metric_data in metrics_data.get("metrics", {}).items():
            summary = self.analyze_metric(metric_data)
            
            # Categorize by threshold status
            if summary.threshold_status == "critical":
                insights["critical_metrics"].append(summary)
            elif summary.threshold_status == "warning":
                insights["warning_metrics"].append(summary)
            
            # Categorize by trend
            if summary.trend_direction == "increasing":
                # Check if increasing is good or bad for this metric
                if any(term in metric_name.lower() for term in ["conversion", "retention", "success", "adoption", "dau"]):
                    insights["positive_trends"].append(summary)
                else:
                    insights["negative_trends"].append(summary)
            elif summary.trend_direction == "decreasing":
                # Check if decreasing is good or bad for this metric
                if any(term in metric_name.lower() for term in ["error", "latency", "ticket"]):
                    insights["positive_trends"].append(summary)
                else:
                    insights["negative_trends"].append(summary)
            else:
                insights["stable_metrics"].append(summary)
        
        # Calculate summary statistics
        insights["summary_stats"] = {
            "total_metrics": len(metrics_data.get("metrics", {})),
            "critical_count": len(insights["critical_metrics"]),
            "warning_count": len(insights["warning_metrics"]),
            "positive_trend_count": len(insights["positive_trends"]),
            "negative_trend_count": len(insights["negative_trends"]),
            "stable_count": len(insights["stable_metrics"])
        }
        
        print(f"Metric insights: {insights['summary_stats']}")
        return insights