"""Test script to generate a 'Proceed' decision by modifying data."""

import json
from datetime import datetime

def create_positive_scenario():
    """Create a more positive scenario that should result in 'Proceed'."""
    
    # Load existing data
    with open("data/metrics.json", 'r') as f:
        metrics_data = json.load(f)
    
    with open("data/feedback.json", 'r') as f:
        feedback_data = json.load(f)
    
    print("Creating positive scenario for 'Proceed' decision...")
    
    # Modify metrics to be more favorable
    metrics = metrics_data["metrics"]
    
    # 1. Improve DAU (was declining, make it stable/growing)
    dau_points = metrics["daily_active_users"]["data_points"]
    for i, point in enumerate(dau_points):
        # Gradually increase DAU instead of decline
        point["value"] = 42000 + (i * 50)  # Growing trend
    
    # 2. Reduce error rate further
    error_points = metrics["error_rate"]["data_points"]
    for point in error_points:
        point["value"] = max(0.1, point["value"] * 0.5)  # Cut error rate in half
    
    # 3. Improve support ticket volume
    ticket_points = metrics["support_ticket_volume"]["data_points"]
    for point in ticket_points:
        point["value"] = max(50, point["value"] * 0.6)  # Reduce tickets by 40%
    
    # 4. Boost feature adoption
    adoption_points = metrics["feature_adoption_rate"]["data_points"]
    for i, point in enumerate(adoption_points):
        point["value"] = min(35.0, point["value"] * 1.2)  # Increase adoption by 20%
    
    print("Modified metrics:")
    print(f"  DAU: Now growing from 42K to {dau_points[-1]['value']:.0f}")
    print(f"  Error rate: Reduced to {error_points[-1]['value']:.2f}%")
    print(f"  Support tickets: Reduced to {ticket_points[-1]['value']:.0f}/day")
    print(f"  Feature adoption: Increased to {adoption_points[-1]['value']:.1f}%")
    
    # Modify feedback to be more positive
    feedback_items = feedback_data["feedback_items"]
    
    # Convert some negative feedback to positive
    negative_items = [item for item in feedback_items if item["sentiment"] == "negative"]
    items_to_convert = negative_items[:10]  # Convert 10 negative to positive
    
    positive_messages = [
        "The new recommendations are fantastic! Much better than before.",
        "Love the improved accuracy of suggestions.",
        "Great job on the personalization improvements.",
        "The feature is working smoothly now, very impressed.",
        "Excellent recommendations, found exactly what I needed.",
        "Much better performance, no more issues.",
        "The AI suggestions are spot on, keep it up!",
        "Perfect recommendations, saves me so much time.",
        "Outstanding improvement in recommendation quality.",
        "The feature works flawlessly, great update!"
    ]
    
    for i, item in enumerate(items_to_convert):
        item["sentiment"] = "positive"
        item["sentiment_score"] = 0.6 + (i * 0.04)  # 0.6 to 0.96
        item["content"] = positive_messages[i]
        item["severity"] = "low"
    
    # Recalculate sentiment distribution
    sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
    sentiment_scores = []
    
    for item in feedback_items:
        sentiment_counts[item["sentiment"]] += 1
        if item.get("sentiment_score") is not None:
            sentiment_scores.append(item["sentiment_score"])
    
    feedback_data["sentiment_distribution"] = sentiment_counts
    feedback_data["average_sentiment_score"] = sum(sentiment_scores) / len(sentiment_scores)
    
    print("Modified feedback:")
    print(f"  Positive: {sentiment_counts['positive']} ({sentiment_counts['positive']/len(feedback_items)*100:.1f}%)")
    print(f"  Negative: {sentiment_counts['negative']} ({sentiment_counts['negative']/len(feedback_items)*100:.1f}%)")
    print(f"  Average sentiment: {feedback_data['average_sentiment_score']:.3f}")
    
    # Save modified data
    with open("data/metrics_positive.json", 'w') as f:
        json.dump(metrics_data, f, indent=2)
    
    with open("data/feedback_positive.json", 'w') as f:
        json.dump(feedback_data, f, indent=2)
    
    print("\nSaved positive scenario data:")
    print("  data/metrics_positive.json")
    print("  data/feedback_positive.json")
    
    return metrics_data, feedback_data

if __name__ == "__main__":
    create_positive_scenario()
    print("\nNow run: python main.py --metrics data/metrics_positive.json --feedback data/feedback_positive.json --verbose")