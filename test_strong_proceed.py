"""Create a very strong positive scenario to get 'Proceed' decision."""

import json
from datetime import datetime

def create_very_positive_scenario():
    """Create a very positive scenario that should definitely result in 'Proceed'."""
    
    # Load existing data
    with open("data/metrics.json", 'r') as f:
        metrics_data = json.load(f)
    
    with open("data/feedback.json", 'r') as f:
        feedback_data = json.load(f)
    
    print("Creating very positive scenario for 'Proceed' decision...")
    
    # Modify metrics to be excellent
    metrics = metrics_data["metrics"]
    
    # 1. Make DAU strongly growing
    dau_points = metrics["daily_active_users"]["data_points"]
    for i, point in enumerate(dau_points):
        point["value"] = 42000 + (i * 100)  # Strong growth
    
    # 2. Make error rate very low
    error_points = metrics["error_rate"]["data_points"]
    for point in error_points:
        point["value"] = 0.1  # Very low error rate
    
    # 3. Make support tickets very low
    ticket_points = metrics["support_ticket_volume"]["data_points"]
    for point in ticket_points:
        point["value"] = 30  # Very low ticket volume
    
    # 4. Make feature adoption exceed target
    adoption_points = metrics["feature_adoption_rate"]["data_points"]
    for i, point in enumerate(adoption_points):
        point["value"] = 28.0 + (i * 0.05)  # Growing to exceed target
    
    # 5. Improve retention significantly
    retention_points = metrics["d1_retention"]["data_points"]
    for point in retention_points:
        point["value"] = max(point["value"], 80.0)  # High retention
    
    print("Modified metrics to excellent levels:")
    print(f"  DAU: Growing from 42K to {dau_points[-1]['value']:.0f}")
    print(f"  Error rate: {error_points[-1]['value']:.2f}%")
    print(f"  Support tickets: {ticket_points[-1]['value']:.0f}/day")
    print(f"  Feature adoption: {adoption_points[-1]['value']:.1f}%")
    print(f"  D1 retention: {retention_points[-1]['value']:.1f}%")
    
    # Make feedback very positive
    feedback_items = feedback_data["feedback_items"]
    
    # Convert most negative feedback to positive
    negative_items = [item for item in feedback_items if item["sentiment"] == "negative"]
    
    very_positive_messages = [
        "Absolutely love the new recommendations! Perfect suggestions every time.",
        "This is the best feature update ever! Recommendations are spot on.",
        "Amazing personalization! Found exactly what I was looking for.",
        "Outstanding improvement! The AI recommendations are incredible.",
        "Perfect performance, no issues at all. Great job!",
        "Excellent feature! Saves me so much time with accurate suggestions.",
        "Fantastic recommendations! Much better than any competitor.",
        "Brilliant update! The personalization is amazing.",
        "Love how smooth and fast the recommendations load now.",
        "Perfect suggestions every single time! Very impressed.",
        "This feature is a game changer! Absolutely fantastic.",
        "Best recommendation system I've ever used!",
        "Incredible accuracy! Always finds what I need.",
        "Outstanding performance and great user experience.",
        "Perfect feature! No complaints whatsoever.",
        "Amazing AI! Recommendations are always relevant.",
        "Excellent job! This feature works flawlessly.",
        "Love the new recommendations! Perfect every time.",
        "Great improvement! Very happy with the results.",
        "Fantastic feature! Highly recommend to everyone.",
        "Perfect implementation! No issues at all.",
        "Excellent recommendations! Very satisfied.",
        "Amazing feature! Works perfectly every time."
    ]
    
    # Convert ALL negative to positive
    for i, item in enumerate(negative_items):
        item["sentiment"] = "positive"
        item["sentiment_score"] = 0.7 + (i * 0.01)  # High positive scores
        item["content"] = very_positive_messages[i % len(very_positive_messages)]
        item["severity"] = "low"
    
    # Also convert some neutral to positive
    neutral_items = [item for item in feedback_items if item["sentiment"] == "neutral"]
    for i, item in enumerate(neutral_items[:5]):  # Convert 5 neutral to positive
        item["sentiment"] = "positive"
        item["sentiment_score"] = 0.6 + (i * 0.02)
        item["content"] = very_positive_messages[(i + len(negative_items)) % len(very_positive_messages)]
    
    # Recalculate sentiment distribution
    sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
    sentiment_scores = []
    critical_count = 0
    
    for item in feedback_items:
        sentiment_counts[item["sentiment"]] += 1
        if item.get("sentiment_score") is not None:
            sentiment_scores.append(item["sentiment_score"])
        if item.get("severity") == "critical":
            critical_count += 1
    
    feedback_data["sentiment_distribution"] = sentiment_counts
    feedback_data["average_sentiment_score"] = sum(sentiment_scores) / len(sentiment_scores)
    
    print("Modified feedback to be very positive:")
    print(f"  Positive: {sentiment_counts['positive']} ({sentiment_counts['positive']/len(feedback_items)*100:.1f}%)")
    print(f"  Negative: {sentiment_counts['negative']} ({sentiment_counts['negative']/len(feedback_items)*100:.1f}%)")
    print(f"  Neutral: {sentiment_counts['neutral']} ({sentiment_counts['neutral']/len(feedback_items)*100:.1f}%)")
    print(f"  Average sentiment: {feedback_data['average_sentiment_score']:.3f}")
    print(f"  Critical issues: {critical_count}")
    
    # Save modified data
    with open("data/metrics_excellent.json", 'w') as f:
        json.dump(metrics_data, f, indent=2)
    
    with open("data/feedback_excellent.json", 'w') as f:
        json.dump(feedback_data, f, indent=2)
    
    print("\nSaved excellent scenario data:")
    print("  data/metrics_excellent.json")
    print("  data/feedback_excellent.json")
    
    return metrics_data, feedback_data

if __name__ == "__main__":
    create_very_positive_scenario()
    print("\nNow run: python main.py --metrics data/metrics_excellent.json --feedback data/feedback_excellent.json --verbose")