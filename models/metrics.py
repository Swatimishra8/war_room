"""Metric data models for the War Room system."""

from datetime import datetime
from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field


class MetricPoint(BaseModel):
    """Single metric data point."""
    timestamp: datetime
    value: float
    metadata: Optional[Dict[str, Union[str, float, int]]] = None


class MetricSeries(BaseModel):
    """Time series for a single metric."""
    metric_name: str
    unit: str
    description: str
    data_points: List[MetricPoint]
    baseline: Optional[float] = None
    target: Optional[float] = None
    threshold_critical: Optional[float] = None
    threshold_warning: Optional[float] = None


class DashboardMetrics(BaseModel):
    """Complete dashboard metrics collection."""
    launch_date: datetime
    feature_name: str
    metrics: Dict[str, MetricSeries] = Field(default_factory=dict)
    
    def add_metric(self, metric: MetricSeries) -> None:
        """Add a metric series to the dashboard."""
        self.metrics[metric.metric_name] = metric
        print(f"Added metric: {metric.metric_name} with {len(metric.data_points)} data points")
    
    def get_metric(self, name: str) -> Optional[MetricSeries]:
        """Get a specific metric by name."""
        return self.metrics.get(name)
    
    def get_latest_values(self) -> Dict[str, float]:
        """Get the latest value for each metric."""
        latest_values = {}
        for name, series in self.metrics.items():
            if series.data_points:
                latest_values[name] = series.data_points[-1].value
                print(f"Latest {name}: {latest_values[name]} {series.unit}")
        return latest_values