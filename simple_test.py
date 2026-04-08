"""Simple test of the War Room system without external dependencies."""

import json
import sys
from datetime import datetime
from typing import Dict, Any, List


class SimpleDecision:
    """Simple decision class without Pydantic."""
    
    def __init__(self):
        self.decision = "Pause"
        self.confidence_score = 0.0
        self.rationale = {}
        self.risk_register = []
        self.action_plan = {}
        self.communication_plan = {}
        self.confidence_factors = []
        self.agent_recommendations = []
        self.feature_name = ""
        self.launch_date = datetime.now()
        self.timestamp = datetime.now()
        self.analysis_duration_seconds = 0.0


def simple_metric_analysis(metrics_data: Dict[str, Any]) -> Dict[str, Any]:
    """Simple metric analysis without tools."""
    
    print("Running simple metric analysis...")
    
    analysis = {
        "overall_health_score": 0.5,
        "critical_metrics": [],
        "warning_metrics": [],
        "key_findings": []
    }
    
    metrics = metrics_data.get("metrics", {})
    
    for metric_name, metric_data in metrics.items():
        data_points = metric_data.get("data_points", [])
        if not data_points:
            continue
        
        current_value = data_points[-1]["value"]
        baseline = metric_data.get("baseline", current_value)
        critical_threshold = metric_data.get("threshold_critical")
        warning_threshold = metric_data.get("threshold_warning")
        
        print(f"Analyzing {metric_name}: current={current_value}, baseline={baseline}")
        
        # Check thresholds
        if critical_threshold is not None:
            if "error" in metric_name.lower() or "latency" in metric_name.lower():
                # Higher is worse
                if current_value >= critical_threshold:
                    analysis["critical_metrics"].append(metric_name)
                    analysis["key_findings"].append(f"CRITICAL: {metric_name} = {current_value}")
                elif warning_threshold and current_value >= warning_threshold:
                    analysis["warning_metrics"].append(metric_name)
                    analysis["key_findings"].append(f"WARNING: {metric_name} = {current_value}")
            else:
                # Lower is worse
                if current_value <= critical_threshold:
                    analysis["critical_metrics"].append(metric_name)
                    analysis["key_findings"].append(f"CRITICAL: {metric_name} = {current_value}")
                elif warning_threshold and current_value <= warning_threshold:
                    analysis["warning_metrics"].append(metric_name)
                    analysis["key_findings"].append(f"WARNING: {metric_name} = {current_value}")
    
    # Calculate health score
    total_metrics = len(metrics)
    if total_metrics > 0:
        critical_ratio = len(analysis["critical_metrics"]) / total_metrics
        warning_ratio = len(analysis["warning_metrics"]) / total_metrics
        analysis["overall_health_score"] = max(0.0, 1.0 - critical_ratio * 0.8 - warning_ratio * 0.4)
    
    print(f"Health score: {analysis['overall_health_score']:.2f}")
    print(f"Critical metrics: {len(analysis['critical_metrics'])}")
    print(f"Warning metrics: {len(analysis['warning_metrics'])}")
    
    return analysis


def simple_sentiment_analysis(feedback_data: Dict[str, Any]) -> Dict[str, Any]:
    """Simple sentiment analysis without tools."""
    
    print("Running simple sentiment analysis...")
    
    feedback_items = feedback_data.get("feedback_items", [])
    
    if not feedback_items:
        return {
            "average_sentiment_score": 0.0,
            "negative_percentage": 0.0,
            "critical_issues": 0,
            "key_findings": ["No feedback data available"]
        }
    
    sentiment_scores = []
    negative_count = 0
    critical_count = 0
    
    for item in feedback_items:
        sentiment = item.get("sentiment", "neutral")
        sentiment_score = item.get("sentiment_score", 0.0)
        severity = item.get("severity", "low")
        
        if sentiment_score is not None:
            sentiment_scores.append(sentiment_score)
        
        if sentiment == "negative":
            negative_count += 1
        
        if severity == "critical":
            critical_count += 1
    
    avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0.0
    negative_percentage = (negative_count / len(feedback_items)) * 100
    
    analysis = {
        "average_sentiment_score": avg_sentiment,
        "negative_percentage": negative_percentage,
        "critical_issues": critical_count,
        "key_findings": [
            f"Average sentiment: {avg_sentiment:.3f}",
            f"Negative feedback: {negative_percentage:.1f}%",
            f"Critical issues: {critical_count}"
        ]
    }
    
    print(f"Sentiment analysis: {avg_sentiment:.3f} score, {negative_percentage:.1f}% negative")
    
    return analysis


def make_simple_decision(metric_analysis: Dict[str, Any], 
                        sentiment_analysis: Dict[str, Any]) -> str:
    """Make a simple decision based on analysis."""
    
    print("Making decision...")
    
    # Decision logic
    critical_metrics = len(metric_analysis.get("critical_metrics", []))
    health_score = metric_analysis.get("overall_health_score", 0.5)
    avg_sentiment = sentiment_analysis.get("average_sentiment_score", 0.0)
    negative_percentage = sentiment_analysis.get("negative_percentage", 0.0)
    critical_issues = sentiment_analysis.get("critical_issues", 0)
    
    print(f"Decision factors:")
    print(f"  Critical metrics: {critical_metrics}")
    print(f"  Health score: {health_score:.2f}")
    print(f"  Sentiment score: {avg_sentiment:.3f}")
    print(f"  Negative feedback: {negative_percentage:.1f}%")
    print(f"  Critical issues: {critical_issues}")
    
    # Decision rules
    if critical_metrics > 2 or health_score < 0.3 or avg_sentiment < -0.4 or negative_percentage > 70:
        decision = "Roll Back"
        confidence = 0.9
        rationale = "Critical issues require immediate rollback"
    elif critical_metrics > 0 or health_score < 0.5 or avg_sentiment < -0.2 or negative_percentage > 50:
        decision = "Pause"
        confidence = 0.8
        rationale = "Significant concerns require pause for investigation"
    elif health_score > 0.7 and avg_sentiment > 0.1 and negative_percentage < 30:
        decision = "Proceed"
        confidence = 0.8
        rationale = "Positive indicators support continued rollout"
    else:
        decision = "Proceed"
        confidence = 0.6
        rationale = "Mixed signals allow cautious proceed"
    
    print(f"Decision: {decision} (confidence: {confidence:.2f})")
    print(f"Rationale: {rationale}")
    
    return decision, confidence, rationale


def run_simple_test():
    """Run a simple test of the system."""
    
    print("PurpleMerit War Room - Simple Test")
    print("=" * 50)
    
    # Load data
    print("Loading data...")
    
    try:
        with open("data/metrics.json", 'r') as f:
            metrics_data = json.load(f)
        print(f"Loaded {len(metrics_data.get('metrics', {}))} metrics")
        
        with open("data/feedback.json", 'r') as f:
            feedback_data = json.load(f)
        print(f"Loaded {feedback_data.get('total_count', 0)} feedback items")
        
        with open("data/release_notes.md", 'r') as f:
            release_notes = f.read()
        print(f"Loaded release notes ({len(release_notes)} characters)")
        
    except FileNotFoundError as e:
        print(f"Error: Required data file not found: {e}")
        return
    
    print("\n" + "=" * 50)
    
    # Run analyses
    metric_analysis = simple_metric_analysis(metrics_data)
    print("\n" + "-" * 30)
    sentiment_analysis = simple_sentiment_analysis(feedback_data)
    print("\n" + "-" * 30)
    
    # Make decision
    decision, confidence, rationale = make_simple_decision(metric_analysis, sentiment_analysis)
    
    # Create output
    output = {
        "decision": decision,
        "timestamp": datetime.now().isoformat(),
        "feature_name": metrics_data.get("feature_name", "Smart Recommendations Engine"),
        "launch_date": metrics_data.get("launch_date", datetime.now().isoformat()),
        "confidence_score": confidence,
        "rationale": {
            "key_drivers": [
                f"System health score: {metric_analysis['overall_health_score']:.2f}",
                f"Customer sentiment: {sentiment_analysis['average_sentiment_score']:.3f}",
                f"Critical metrics: {len(metric_analysis['critical_metrics'])}",
                f"Negative feedback: {sentiment_analysis['negative_percentage']:.1f}%"
            ],
            "decision_rationale": rationale
        },
        "risk_register": [
            {
                "risk": f"{len(metric_analysis['critical_metrics'])} critical metrics identified",
                "severity": "High" if len(metric_analysis['critical_metrics']) > 0 else "Low",
                "mitigation": "Monitor closely and investigate root causes"
            },
            {
                "risk": f"{sentiment_analysis['negative_percentage']:.1f}% negative customer feedback",
                "severity": "High" if sentiment_analysis['negative_percentage'] > 50 else "Medium",
                "mitigation": "Improve customer communication and address top issues"
            }
        ],
        "action_plan": {
            "24_hours": [
                {
                    "action": "Increase monitoring frequency for all critical metrics",
                    "owner": "DevOps/Engineering",
                    "priority": "high"
                },
                {
                    "action": "Brief customer support team on current issues",
                    "owner": "Customer Success",
                    "priority": "medium"
                }
            ],
            "48_hours": [
                {
                    "action": "Conduct detailed analysis of negative feedback themes",
                    "owner": "Product/Marketing",
                    "priority": "medium"
                },
                {
                    "action": "Prepare stakeholder report with recommendations",
                    "owner": "Product Manager",
                    "priority": "medium"
                }
            ]
        },
        "communication_plan": {
            "internal": "Brief stakeholders on current status and decision rationale",
            "external": "Monitor customer feedback and prepare communication if needed"
        },
        "confidence_factors": [
            "Additional 48 hours of monitoring data",
            "Larger customer feedback sample",
            "Root cause analysis of critical issues"
        ],
        "analysis_summary": {
            "metric_analysis": metric_analysis,
            "sentiment_analysis": sentiment_analysis
        }
    }
    
    # Save output
    with open("output/simple_decision.json", 'w') as f:
        json.dump(output, f, indent=2, default=str)
    
    print("\n" + "=" * 50)
    print("SIMPLE TEST RESULTS")
    print("=" * 50)
    print(f"Decision: {decision}")
    print(f"Confidence: {confidence:.2f}")
    print(f"Rationale: {rationale}")
    print(f"Critical Metrics: {len(metric_analysis['critical_metrics'])}")
    print(f"Health Score: {metric_analysis['overall_health_score']:.2f}")
    print(f"Sentiment Score: {sentiment_analysis['average_sentiment_score']:.3f}")
    print(f"Negative Feedback: {sentiment_analysis['negative_percentage']:.1f}%")
    print("\nOutput saved to: output/simple_decision.json")
    print("=" * 50)
    
    # Return appropriate exit code
    if decision == "Roll Back":
        return 2
    elif decision == "Pause":
        return 1
    else:
        return 0


if __name__ == "__main__":
    try:
        exit_code = run_simple_test()
        sys.exit(exit_code)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)