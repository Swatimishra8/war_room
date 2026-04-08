"""Generate realistic mock data for the War Room simulation."""

import json
import random
from datetime import datetime, timedelta
from typing import List, Dict
import numpy as np

from models.metrics import MetricPoint, MetricSeries, DashboardMetrics
from models.feedback import UserFeedback, FeedbackCollection, SentimentType, FeedbackSource


def generate_time_series(
    start_date: datetime,
    days: int,
    base_value: float,
    trend: float = 0.0,
    volatility: float = 0.1,
    anomaly_probability: float = 0.05,
    anomaly_magnitude: float = 0.3
) -> List[MetricPoint]:
    """Generate realistic time series data with trends and anomalies."""
    points = []
    current_value = base_value
    
    print(f"Generating time series: base={base_value}, trend={trend}, volatility={volatility}")
    
    for i in range(days * 24):  # Hourly data points
        timestamp = start_date + timedelta(hours=i)
        
        # Apply trend
        current_value += trend / 24  # Daily trend divided by hours
        
        # Add normal volatility
        noise = np.random.normal(0, volatility * base_value)
        
        # Occasional anomalies
        if random.random() < anomaly_probability:
            anomaly = random.choice([-1, 1]) * anomaly_magnitude * base_value
            noise += anomaly
            print(f"Added anomaly at {timestamp}: {anomaly:+.2f}")
        
        value = max(0, current_value + noise)  # Ensure non-negative
        points.append(MetricPoint(timestamp=timestamp, value=value))
    
    return points


def create_mock_metrics() -> DashboardMetrics:
    """Create comprehensive mock metrics for the dashboard."""
    launch_date = datetime.now() - timedelta(days=7)
    dashboard = DashboardMetrics(
        launch_date=launch_date,
        feature_name="Smart Recommendations Engine"
    )
    
    print("Creating mock metrics dashboard...")
    
    # 1. Activation/Signup Conversion (%)
    activation_data = generate_time_series(
        start_date=launch_date,
        days=14,
        base_value=12.5,
        trend=-0.2,  # Slight decline
        volatility=0.15,
        anomaly_probability=0.03
    )
    dashboard.add_metric(MetricSeries(
        metric_name="activation_conversion",
        unit="%",
        description="User activation conversion rate",
        data_points=activation_data,
        baseline=13.2,
        target=15.0,
        threshold_critical=10.0,
        threshold_warning=11.5
    ))
    
    # 2. Daily Active Users (DAU)
    dau_data = generate_time_series(
        start_date=launch_date,
        days=14,
        base_value=45000,
        trend=150,  # Growing
        volatility=0.08,
        anomaly_probability=0.02
    )
    dashboard.add_metric(MetricSeries(
        metric_name="daily_active_users",
        unit="users",
        description="Daily active users",
        data_points=dau_data,
        baseline=42000,
        target=50000,
        threshold_critical=35000,
        threshold_warning=38000
    ))
    
    # 3. D1 Retention (%)
    retention_data = generate_time_series(
        start_date=launch_date,
        days=14,
        base_value=68.5,
        trend=-0.5,  # Declining retention
        volatility=0.12,
        anomaly_probability=0.04
    )
    dashboard.add_metric(MetricSeries(
        metric_name="d1_retention",
        unit="%",
        description="Day 1 user retention rate",
        data_points=retention_data,
        baseline=72.0,
        target=75.0,
        threshold_critical=60.0,
        threshold_warning=65.0
    ))
    
    # 4. Error Rate (%)
    error_data = generate_time_series(
        start_date=launch_date,
        days=14,
        base_value=0.8,
        trend=0.05,  # Increasing errors
        volatility=0.3,
        anomaly_probability=0.08,
        anomaly_magnitude=0.5
    )
    dashboard.add_metric(MetricSeries(
        metric_name="error_rate",
        unit="%",
        description="Application error rate",
        data_points=error_data,
        baseline=0.5,
        target=0.3,
        threshold_critical=2.0,
        threshold_warning=1.5
    ))
    
    # 5. API Latency P95 (ms)
    latency_data = generate_time_series(
        start_date=launch_date,
        days=14,
        base_value=245,
        trend=3.2,  # Increasing latency
        volatility=0.2,
        anomaly_probability=0.06,
        anomaly_magnitude=0.4
    )
    dashboard.add_metric(MetricSeries(
        metric_name="api_latency_p95",
        unit="ms",
        description="95th percentile API response time",
        data_points=latency_data,
        baseline=220,
        target=200,
        threshold_critical=400,
        threshold_warning=300
    ))
    
    # 6. Payment Success Rate (%)
    payment_data = generate_time_series(
        start_date=launch_date,
        days=14,
        base_value=97.2,
        trend=-0.1,  # Slight decline
        volatility=0.05,
        anomaly_probability=0.03,
        anomaly_magnitude=0.2
    )
    dashboard.add_metric(MetricSeries(
        metric_name="payment_success_rate",
        unit="%",
        description="Payment transaction success rate",
        data_points=payment_data,
        baseline=97.8,
        target=98.5,
        threshold_critical=95.0,
        threshold_warning=96.5
    ))
    
    # 7. Support Ticket Volume
    support_data = generate_time_series(
        start_date=launch_date,
        days=14,
        base_value=125,
        trend=8.5,  # Increasing tickets
        volatility=0.25,
        anomaly_probability=0.05,
        anomaly_magnitude=0.3
    )
    dashboard.add_metric(MetricSeries(
        metric_name="support_ticket_volume",
        unit="tickets",
        description="Daily support ticket volume",
        data_points=support_data,
        baseline=95,
        target=80,
        threshold_critical=200,
        threshold_warning=150
    ))
    
    # 8. Feature Adoption Rate (%)
    adoption_data = generate_time_series(
        start_date=launch_date,
        days=14,
        base_value=23.5,
        trend=1.2,  # Growing adoption
        volatility=0.18,
        anomaly_probability=0.02
    )
    dashboard.add_metric(MetricSeries(
        metric_name="feature_adoption_rate",
        unit="%",
        description="Smart recommendations feature adoption rate",
        data_points=adoption_data,
        baseline=0,
        target=30.0,
        threshold_critical=10.0,
        threshold_warning=15.0
    ))
    
    print(f"Created dashboard with {len(dashboard.metrics)} metrics")
    return dashboard


def create_mock_feedback() -> FeedbackCollection:
    """Create realistic user feedback data."""
    feedback_items = []
    base_time = datetime.now() - timedelta(days=7)
    
    print("Creating mock user feedback...")
    
    # Positive feedback examples
    positive_feedback = [
        "The new recommendations are spot on! Found exactly what I was looking for.",
        "Love the smart suggestions feature - saves me so much time browsing.",
        "Recommendations have gotten much better, very relevant to my interests.",
        "The AI suggestions are actually useful, unlike other apps I've tried.",
        "Great improvement! The recommendations feel personalized.",
        "Finally, suggestions that make sense. Well done!",
        "The new feature helped me discover products I wouldn't have found otherwise.",
        "Smart recommendations work perfectly. Very impressed.",
        "Loving the personalized suggestions - they're very accurate.",
        "The recommendation engine is a game changer for discovery."
    ]
    
    # Negative feedback examples  
    negative_feedback = [
        "App keeps crashing when I try to use the new recommendations feature.",
        "Recommendations are completely irrelevant to my purchase history.",
        "The new feature is slow and buggy, takes forever to load suggestions.",
        "Getting the same recommendations over and over, no variety.",
        "App freezes whenever I click on recommended items.",
        "Recommendations don't match my preferences at all, very disappointed.",
        "The feature is broken - shows error messages constantly.",
        "Terrible recommendations, completely off-base from what I like.",
        "App became much slower since the update, very frustrating.",
        "Recommendations feature doesn't work half the time.",
        "Getting recommendations for things I already bought, makes no sense.",
        "The new feature is annoying and I can't figure out how to turn it off.",
        "App crashes every time I try to view recommended products.",
        "Recommendations are generic and not personalized at all.",
        "Feature is buggy and recommendations don't load properly."
    ]
    
    # Neutral feedback examples
    neutral_feedback = [
        "The recommendations are okay, nothing special but not bad either.",
        "New feature works fine, though I don't use it much.",
        "Recommendations are hit or miss, some good ones, some not so much.",
        "The feature is there but I haven't really noticed a big difference.",
        "It's an okay addition, might be useful for some people.",
        "Recommendations work as expected, no major issues.",
        "The feature is fine, though I prefer browsing on my own.",
        "Not bad, but not amazing either. Pretty standard recommendations.",
        "Works well enough, though the interface could be better.",
        "Decent feature, though it could use some improvements."
    ]
    
    # Generate feedback items
    feedback_sources = list(FeedbackSource)
    severities = ["low", "medium", "high", "critical"]
    categories = ["feature_request", "bug_report", "performance", "usability", "content_quality"]
    
    # Add positive feedback (40%)
    for i, content in enumerate(positive_feedback):
        timestamp = base_time + timedelta(hours=random.randint(0, 168))
        feedback_items.append(UserFeedback(
            id=f"pos_{i+1:03d}",
            timestamp=timestamp,
            source=random.choice(feedback_sources),
            user_id=f"user_{random.randint(1000, 9999)}",
            content=content,
            sentiment=SentimentType.POSITIVE,
            sentiment_score=random.uniform(0.3, 1.0),
            category=random.choice(categories),
            severity=random.choice(severities[:2])  # low or medium
        ))
    
    # Add negative feedback (45%)
    for i, content in enumerate(negative_feedback):
        timestamp = base_time + timedelta(hours=random.randint(0, 168))
        feedback_items.append(UserFeedback(
            id=f"neg_{i+1:03d}",
            timestamp=timestamp,
            source=random.choice(feedback_sources),
            user_id=f"user_{random.randint(1000, 9999)}",
            content=content,
            sentiment=SentimentType.NEGATIVE,
            sentiment_score=random.uniform(-1.0, -0.2),
            category=random.choice(categories),
            severity=random.choice(severities)  # All severities
        ))
    
    # Add neutral feedback (15%)
    for i, content in enumerate(neutral_feedback):
        timestamp = base_time + timedelta(hours=random.randint(0, 168))
        feedback_items.append(UserFeedback(
            id=f"neu_{i+1:03d}",
            timestamp=timestamp,
            source=random.choice(feedback_sources),
            user_id=f"user_{random.randint(1000, 9999)}",
            content=content,
            sentiment=SentimentType.NEUTRAL,
            sentiment_score=random.uniform(-0.2, 0.2),
            category=random.choice(categories),
            severity=random.choice(severities[:2])  # low or medium
        ))
    
    collection = FeedbackCollection(feedback_items=feedback_items)
    print(f"Created feedback collection with {len(feedback_items)} items")
    return collection


def save_mock_data():
    """Generate and save all mock data to files."""
    print("Generating and saving mock data...")
    
    # Generate metrics
    metrics = create_mock_metrics()
    metrics_dict = {
        "launch_date": metrics.launch_date.isoformat(),
        "feature_name": metrics.feature_name,
        "metrics": {}
    }
    
    for name, series in metrics.metrics.items():
        metrics_dict["metrics"][name] = {
            "metric_name": series.metric_name,
            "unit": series.unit,
            "description": series.description,
            "baseline": series.baseline,
            "target": series.target,
            "threshold_critical": series.threshold_critical,
            "threshold_warning": series.threshold_warning,
            "data_points": [
                {
                    "timestamp": point.timestamp.isoformat(),
                    "value": point.value,
                    "metadata": point.metadata
                }
                for point in series.data_points
            ]
        }
    
    with open("/Users/apple/Desktop/war_room/data/metrics.json", "w") as f:
        json.dump(metrics_dict, f, indent=2)
    
    # Generate feedback
    feedback = create_mock_feedback()
    feedback_dict = {
        "total_count": feedback.total_count,
        "sentiment_distribution": {k.value: v for k, v in feedback.sentiment_distribution.items()},
        "category_distribution": feedback.category_distribution,
        "average_sentiment_score": feedback.average_sentiment_score,
        "feedback_items": [
            {
                "id": item.id,
                "timestamp": item.timestamp.isoformat(),
                "source": item.source.value,
                "user_id": item.user_id,
                "content": item.content,
                "sentiment": item.sentiment.value if item.sentiment else None,
                "sentiment_score": item.sentiment_score,
                "category": item.category,
                "severity": item.severity,
                "metadata": item.metadata
            }
            for item in feedback.feedback_items
        ]
    }
    
    with open("/Users/apple/Desktop/war_room/data/feedback.json", "w") as f:
        json.dump(feedback_dict, f, indent=2)
    
    # Create release notes
    release_notes = """# Smart Recommendations Engine - Release Notes

## Version 2.1.0 - Launch Date: {launch_date}

### New Features
- **Smart Recommendations Engine**: AI-powered product recommendations based on user behavior, purchase history, and preferences
- **Personalized Discovery**: Dynamic content suggestions that adapt to user interactions
- **Real-time Learning**: Recommendation model updates based on user feedback and engagement

### Technical Implementation
- Machine learning model deployed with A/B testing framework
- Real-time inference pipeline with <200ms response time target
- Fallback to collaborative filtering when ML model unavailable

### Known Risks & Considerations
1. **Performance Impact**: New recommendation service adds ~50ms to page load times
2. **Data Privacy**: Enhanced user tracking for personalization (compliant with privacy policy)
3. **Model Accuracy**: Cold start problem for new users with limited interaction history
4. **Infrastructure Load**: Additional 15% increase in database queries for recommendation generation

### Rollout Strategy
- **Phase 1** (Days 1-3): 25% of users
- **Phase 2** (Days 4-7): 50% of users  
- **Phase 3** (Days 8-14): 100% rollout

### Success Metrics
- **Primary**: Feature adoption rate >25% within 14 days
- **Secondary**: User engagement increase >10%, conversion rate improvement >5%
- **Quality**: Recommendation click-through rate >8%

### Rollback Triggers
- Error rate >2% for >2 hours
- API latency P95 >400ms for >1 hour  
- Support ticket volume >200/day for >24 hours
- Feature adoption <10% after 7 days

### Monitoring & Alerts
- Real-time dashboards for all key metrics
- Automated alerts for threshold breaches
- Daily stakeholder reports during launch window

### Dependencies
- Recommendation service (new microservice)
- User behavior tracking updates
- A/B testing framework integration
- Enhanced analytics pipeline

### Team Contacts
- **Product Manager**: Sarah Chen (sarah.chen@purplemerit.com)
- **Engineering Lead**: Mike Rodriguez (mike.rodriguez@purplemerit.com)  
- **Data Science**: Dr. Lisa Wang (lisa.wang@purplemerit.com)
- **DevOps**: James Kim (james.kim@purplemerit.com)
""".format(launch_date=metrics.launch_date.strftime("%Y-%m-%d"))
    
    with open("/Users/apple/Desktop/war_room/data/release_notes.md", "w") as f:
        f.write(release_notes)
    
    print("Mock data generation complete!")
    print(f"- Metrics: {len(metrics.metrics)} time series saved")
    print(f"- Feedback: {feedback.total_count} items saved")
    print("- Release notes created")


if __name__ == "__main__":
    save_mock_data()