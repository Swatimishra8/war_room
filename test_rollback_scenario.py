"""Test script to generate a 'Roll Back' decision scenario."""

import json
from datetime import datetime

def create_rollback_scenario():
    """Create a critical scenario that should result in 'Roll Back'."""
    
    # Load existing data
    with open("data/metrics.json", 'r') as f:
        metrics_data = json.load(f)
    
    with open("data/feedback.json", 'r') as f:
        feedback_data = json.load(f)
    
    print("Creating ROLL BACK scenario...")
    print("=" * 50)
    
    # Modify metrics to be critical/failing
    metrics = metrics_data["metrics"]
    
    # 1. Make DAU crash dramatically
    dau_points = metrics["daily_active_users"]["data_points"]
    for i, point in enumerate(dau_points):
        point["value"] = 42000 - (i * 150)  # Dramatic decline
    
    # 2. Make error rate critical
    error_points = metrics["error_rate"]["data_points"]
    for i, point in enumerate(error_points):
        point["value"] = 2.5 + (i * 0.01)  # Above critical threshold and growing
    
    # 3. Make support tickets explode
    ticket_points = metrics["support_ticket_volume"]["data_points"]
    for i, point in enumerate(ticket_points):
        point["value"] = 150 + (i * 5)  # Rapidly increasing tickets
    
    # 4. Feature adoption very poor
    adoption_points = metrics["feature_adoption_rate"]["data_points"]
    for i, point in enumerate(adoption_points):
        point["value"] = max(8.0 - (i * 0.02), 5.0)  # Declining, well below minimum
    
    # 5. Retention crashing
    retention_points = metrics["d1_retention"]["data_points"]
    for i, point in enumerate(retention_points):
        point["value"] = max(72.0 - (i * 0.5), 45.0)  # Dramatic retention drop
    
    # 6. API performance degrading
    latency_points = metrics["api_latency_p95"]["data_points"]
    for i, point in enumerate(latency_points):
        point["value"] = 220 + (i * 3)  # Increasing latency
    
    # 7. Payment failures increasing
    payment_points = metrics["payment_success_rate"]["data_points"]
    for i, point in enumerate(payment_points):
        point["value"] = max(97.8 - (i * 0.1), 92.0)  # Declining payment success
    
    # 8. Conversion rate dropping
    conversion_points = metrics["activation_conversion"]["data_points"]
    for i, point in enumerate(conversion_points):
        point["value"] = max(13.2 - (i * 0.05), 8.0)  # Declining conversion
    
    print("Modified metrics to critical levels:")
    print(f"  🚨 DAU: Crashing from 42K to {dau_points[-1]['value']:.0f}")
    print(f"  🚨 Error rate: {error_points[-1]['value']:.2f}% (CRITICAL)")
    print(f"  🚨 Support tickets: {ticket_points[-1]['value']:.0f}/day (EXPLODING)")
    print(f"  🚨 Feature adoption: {adoption_points[-1]['value']:.1f}% (FAILING)")
    print(f"  🚨 D1 retention: {retention_points[-1]['value']:.1f}% (CRASHING)")
    print(f"  🚨 API latency: {latency_points[-1]['value']:.0f}ms (DEGRADING)")
    print(f"  🚨 Payment success: {payment_points[-1]['value']:.1f}% (DECLINING)")
    print(f"  🚨 Conversion: {conversion_points[-1]['value']:.1f}% (DROPPING)")
    
    # Create very negative feedback (70%+ negative)
    feedback_items = feedback_data["feedback_items"]
    
    critical_negative_messages = [
        "This feature completely broke the app! Can't use it at all anymore.",
        "Worst update ever! The app crashes constantly since the new feature.",
        "Terrible performance! Everything is slow and buggy now.",
        "The recommendations are completely useless and wrong every time.",
        "App is unusable since this update. Please roll it back immediately!",
        "This feature ruined the entire user experience. Very disappointed.",
        "Constant crashes and errors. This is completely unacceptable.",
        "The app was perfect before, now it's a disaster. Fix this now!",
        "Horrible update! Lost all my data and can't complete any tasks.",
        "This feature is broken beyond repair. Please remove it completely.",
        "Worst experience ever! The app is completely unusable now.",
        "Everything is broken since this update. Can't recommend this app anymore.",
        "The new feature destroyed the app's functionality. Roll it back!",
        "Critical bugs everywhere! This should never have been released.",
        "App crashes every time I try to use the new recommendations.",
        "This update made the app 10x worse. Completely broken.",
        "Terrible performance and constant errors. Very frustrated.",
        "The feature doesn't work at all and breaks other parts of the app.",
        "Worst update in the app's history. Please fix this disaster.",
        "Everything is slow, buggy, and unreliable now. Very disappointed.",
        "The app is completely broken. Can't use any features properly.",
        "This update ruined everything. The app was much better before.",
        "Critical failure! The app is unusable and crashes constantly.",
        "Horrible experience! Nothing works properly since this update.",
        "The new feature broke the entire app. Please roll back immediately.",
        "Completely unusable! This update destroyed the user experience.",
        "Everything is broken and slow. This is completely unacceptable.",
        "The app crashes every few minutes. This is a disaster.",
        "Worst feature ever! It broke everything else in the app.",
        "Critical bugs and crashes everywhere. Please fix this mess.",
        "The app is completely broken since this terrible update.",
        "Everything stopped working properly. Very frustrated and angry.",
        "This feature ruined the app completely. Roll it back now!",
        "Constant errors and crashes. This is completely unacceptable.",
        "The app was great before, now it's completely unusable."
    ]
    
    # Convert most feedback to very negative
    for i, item in enumerate(feedback_items):
        if i < 35:  # Make 35 items very negative
            item["sentiment"] = "negative"
            item["sentiment_score"] = -0.8 - (i * 0.005)  # Very negative scores
            item["content"] = critical_negative_messages[i % len(critical_negative_messages)]
            item["severity"] = "critical" if i < 15 else "high"
        elif i < 40:  # Make 5 items neutral (mixed signals)
            item["sentiment"] = "neutral"
            item["sentiment_score"] = -0.1
            item["content"] = "The feature has some issues but might work with fixes."
            item["severity"] = "medium"
        else:  # Keep some positive (but overwhelmed by negative)
            item["sentiment"] = "positive"
            item["sentiment_score"] = 0.3
            item["severity"] = "low"
    
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
    
    print("\nModified feedback to be very negative:")
    print(f"  🚨 Positive: {sentiment_counts['positive']} ({sentiment_counts['positive']/len(feedback_items)*100:.1f}%)")
    print(f"  🚨 Negative: {sentiment_counts['negative']} ({sentiment_counts['negative']/len(feedback_items)*100:.1f}%)")
    print(f"  🚨 Neutral: {sentiment_counts['neutral']} ({sentiment_counts['neutral']/len(feedback_items)*100:.1f}%)")
    print(f"  🚨 Average sentiment: {feedback_data['average_sentiment_score']:.3f}")
    print(f"  🚨 Critical issues: {critical_count}")
    
    # Save data
    with open("data/metrics_rollback.json", 'w') as f:
        json.dump(metrics_data, f, indent=2)
    
    with open("data/feedback_rollback.json", 'w') as f:
        json.dump(feedback_data, f, indent=2)
    
    print(f"\n{'='*50}")
    print("🚨 ROLL BACK scenario data saved:")
    print("  📁 data/metrics_rollback.json")
    print("  📁 data/feedback_rollback.json")
    print(f"{'='*50}")
    
    return "rollback"

def run_rollback_test():
    """Run the rollback scenario test."""
    scenario = create_rollback_scenario()
    
    print("\n🔴 To test ROLL BACK scenario, run:")
    print("python main.py --metrics data/metrics_rollback.json --feedback data/feedback_rollback.json --output output/rollback_decision.json")
    print("\n📊 Expected result: Decision = 'Roll Back' (Exit Code 2)")
    
    return scenario

if __name__ == "__main__":
    run_rollback_test()