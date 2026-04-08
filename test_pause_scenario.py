"""Test script to generate a 'Pause' decision scenario."""

import json
from datetime import datetime

def create_pause_scenario():
    """Create a mixed scenario that should result in 'Pause'."""
    
    # Load existing data
    with open("data/metrics.json", 'r') as f:
        metrics_data = json.load(f)
    
    with open("data/feedback.json", 'r') as f:
        feedback_data = json.load(f)
    
    print("Creating PAUSE scenario...")
    print("=" * 50)
    
    # Modify metrics to have mixed signals (some good, some concerning)
    metrics = metrics_data["metrics"]
    
    # 1. Keep DAU declining (concerning)
    dau_points = metrics["daily_active_users"]["data_points"]
    for i, point in enumerate(dau_points):
        point["value"] = 42000 - (i * 30)  # Gradual decline
    
    # 2. Moderate error rate (not critical but elevated)
    error_points = metrics["error_rate"]["data_points"]
    for point in error_points:
        point["value"] = 1.2  # Elevated but not critical
    
    # 3. Increased support tickets (concerning trend)
    ticket_points = metrics["support_ticket_volume"]["data_points"]
    for i, point in enumerate(ticket_points):
        point["value"] = 95 + (i * 2)  # Growing ticket volume
    
    # 4. Feature adoption progressing but below target
    adoption_points = metrics["feature_adoption_rate"]["data_points"]
    for i, point in enumerate(adoption_points):
        point["value"] = 18.0 + (i * 0.02)  # Slow growth, below target
    
    # 5. Retention stable but not great
    retention_points = metrics["d1_retention"]["data_points"]
    for point in retention_points:
        point["value"] = min(max(point["value"], 65.0), 70.0)  # Mediocre retention
    
    # 6. Some performance improvements (mixed signals)
    latency_points = metrics["api_latency_p95"]["data_points"]
    for point in latency_points:
        point["value"] = max(point["value"] * 0.8, 180)  # Some improvement but not great
    
    print("Modified metrics to show mixed signals:")
    print(f"  ⚠️  DAU: Declining from 42K to {dau_points[-1]['value']:.0f}")
    print(f"  ⚠️  Error rate: {error_points[-1]['value']:.2f}% (elevated)")
    print(f"  ⚠️  Support tickets: {ticket_points[-1]['value']:.0f}/day (increasing)")
    print(f"  ⚠️  Feature adoption: {adoption_points[-1]['value']:.1f}% (below target)")
    print(f"  ⚠️  D1 retention: {retention_points[-1]['value']:.1f}% (mediocre)")
    print(f"  ✅ API latency: {latency_points[-1]['value']:.0f}ms (improved)")
    
    # Create mixed feedback (40-50% negative, some positive)
    feedback_items = feedback_data["feedback_items"]
    
    # Keep some negative feedback as is, but not too extreme
    negative_items = [item for item in feedback_items if item["sentiment"] == "negative"]
    moderate_negative_messages = [
        "The recommendations are okay but could be better.",
        "Some good suggestions but also some irrelevant ones.",
        "The feature works but has room for improvement.",
        "Mixed results - sometimes good, sometimes not so much.",
        "It's an improvement but still has some issues to work out.",
        "Decent feature but needs more fine-tuning.",
        "Some recommendations are great, others miss the mark.",
        "The feature is functional but could use optimization.",
        "Good concept but execution could be better.",
        "Works most of the time, but occasional issues.",
        "Promising feature but still needs work.",
        "Some accuracy issues but generally helpful.",
        "The feature is useful but has performance problems sometimes."
    ]
    
    # Convert some negative to neutral/moderate negative
    for i, item in enumerate(negative_items[:13]):  # Keep 13 negative, convert rest
        item["sentiment"] = "negative"
        item["sentiment_score"] = -0.3 + (i * 0.02)  # Moderate negative scores
        item["content"] = moderate_negative_messages[i % len(moderate_negative_messages)]
        item["severity"] = "medium" if i < 5 else "low"
    
    # Convert remaining negative to neutral
    for item in negative_items[13:]:
        item["sentiment"] = "neutral"
        item["sentiment_score"] = -0.05 + (len(negative_items) * 0.01)
        item["content"] = "The feature is okay, nothing special but works."
        item["severity"] = "low"
    
    # Keep some positive feedback
    positive_items = [item for item in feedback_items if item["sentiment"] == "positive"]
    for item in positive_items[:15]:  # Keep 15 positive
        item["sentiment_score"] = 0.4 + (len(positive_items) * 0.01)
    
    # Convert some positive to neutral for mixed signals
    for item in positive_items[15:]:
        item["sentiment"] = "neutral"
        item["sentiment_score"] = 0.1
        item["content"] = "The recommendations are decent, not bad but not amazing either."
    
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
    
    print("\nModified feedback to show mixed sentiment:")
    print(f"  ⚠️  Positive: {sentiment_counts['positive']} ({sentiment_counts['positive']/len(feedback_items)*100:.1f}%)")
    print(f"  ⚠️  Negative: {sentiment_counts['negative']} ({sentiment_counts['negative']/len(feedback_items)*100:.1f}%)")
    print(f"  ⚠️  Neutral: {sentiment_counts['neutral']} ({sentiment_counts['neutral']/len(feedback_items)*100:.1f}%)")
    print(f"  ⚠️  Average sentiment: {feedback_data['average_sentiment_score']:.3f}")
    print(f"  ⚠️  Critical issues: {critical_count}")
    
    # Save data
    with open("data/metrics_pause.json", 'w') as f:
        json.dump(metrics_data, f, indent=2)
    
    with open("data/feedback_pause.json", 'w') as f:
        json.dump(feedback_data, f, indent=2)
    
    print(f"\n{'='*50}")
    print("⚠️  PAUSE scenario data saved:")
    print("  📁 data/metrics_pause.json")
    print("  📁 data/feedback_pause.json")
    print(f"{'='*50}")
    
    return "pause"

def run_pause_test():
    """Run the pause scenario test."""
    scenario = create_pause_scenario()
    
    print("\n⏸️  To test PAUSE scenario, run:")
    print("python main.py --metrics data/metrics_pause.json --feedback data/feedback_pause.json --output output/pause_decision.json")
    print("\n📊 Expected result: Decision = 'Pause' (Exit Code 1)")
    
    return scenario

if __name__ == "__main__":
    run_pause_test()