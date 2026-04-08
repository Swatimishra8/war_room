"""Sentiment analysis tools for user feedback."""

import json
import re
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from collections import Counter


@dataclass
class SentimentSummary:
    """Summary of sentiment analysis results."""
    total_feedback: int
    positive_count: int
    negative_count: int
    neutral_count: int
    average_sentiment_score: float
    positive_percentage: float
    negative_percentage: float
    neutral_percentage: float
    critical_issues_count: int
    top_positive_themes: List[str]
    top_negative_themes: List[str]
    sentiment_trend: str  # "improving", "declining", "stable"


class SentimentAnalyzer:
    """Analyzes user feedback sentiment and extracts insights."""
    
    def __init__(self):
        """Initialize the sentiment analyzer."""
        print("Initializing SentimentAnalyzer...")
        
        # Keywords for theme extraction
        self.positive_keywords = {
            "accuracy": ["accurate", "relevant", "spot on", "perfect", "precise", "right"],
            "performance": ["fast", "quick", "smooth", "efficient", "responsive"],
            "usability": ["easy", "simple", "intuitive", "user-friendly", "convenient"],
            "personalization": ["personalized", "customized", "tailored", "individual"],
            "discovery": ["discover", "found", "explore", "new", "variety"],
            "satisfaction": ["love", "great", "excellent", "amazing", "impressed", "happy"]
        }
        
        self.negative_keywords = {
            "bugs": ["crash", "freeze", "broken", "error", "bug", "glitch", "hang"],
            "performance": ["slow", "lag", "delay", "timeout", "loading", "wait"],
            "relevance": ["irrelevant", "wrong", "useless", "pointless", "random"],
            "repetition": ["same", "repeat", "duplicate", "again", "over and over"],
            "confusion": ["confusing", "unclear", "complicated", "difficult", "hard"],
            "frustration": ["annoying", "frustrating", "terrible", "awful", "hate"]
        }
    
    def load_feedback_from_file(self, filepath: str) -> Dict[str, Any]:
        """Load feedback data from JSON file."""
        print(f"Loading feedback from {filepath}")
        with open(filepath, 'r') as f:
            data = json.load(f)
        print(f"Loaded {data.get('total_count', 0)} feedback items")
        return data
    
    def analyze_sentiment(self, feedback_data: Dict[str, Any]) -> SentimentSummary:
        """Analyze sentiment of all feedback items."""
        feedback_items = feedback_data.get("feedback_items", [])
        
        if not feedback_items:
            print("Warning: No feedback items to analyze")
            return SentimentSummary(
                total_feedback=0,
                positive_count=0,
                negative_count=0,
                neutral_count=0,
                average_sentiment_score=0.0,
                positive_percentage=0.0,
                negative_percentage=0.0,
                neutral_percentage=0.0,
                critical_issues_count=0,
                top_positive_themes=[],
                top_negative_themes=[],
                sentiment_trend="unknown"
            )
        
        print(f"Analyzing sentiment for {len(feedback_items)} feedback items")
        
        # Count sentiments
        sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
        sentiment_scores = []
        critical_issues = 0
        
        for item in feedback_items:
            sentiment = item.get("sentiment", "neutral")
            sentiment_counts[sentiment] += 1
            
            if item.get("sentiment_score") is not None:
                sentiment_scores.append(item["sentiment_score"])
            
            if item.get("severity") == "critical":
                critical_issues += 1
        
        total_feedback = len(feedback_items)
        avg_sentiment_score = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0.0
        
        # Calculate percentages
        positive_pct = (sentiment_counts["positive"] / total_feedback) * 100
        negative_pct = (sentiment_counts["negative"] / total_feedback) * 100
        neutral_pct = (sentiment_counts["neutral"] / total_feedback) * 100
        
        print(f"Sentiment distribution: {positive_pct:.1f}% positive, {negative_pct:.1f}% negative, {neutral_pct:.1f}% neutral")
        print(f"Average sentiment score: {avg_sentiment_score:.3f}")
        print(f"Critical issues: {critical_issues}")
        
        # Extract themes
        positive_themes = self._extract_themes(feedback_items, "positive")
        negative_themes = self._extract_themes(feedback_items, "negative")
        
        # Determine sentiment trend (simplified - would need time series analysis for real trend)
        if avg_sentiment_score > 0.2:
            sentiment_trend = "improving"
        elif avg_sentiment_score < -0.2:
            sentiment_trend = "declining"
        else:
            sentiment_trend = "stable"
        
        return SentimentSummary(
            total_feedback=total_feedback,
            positive_count=sentiment_counts["positive"],
            negative_count=sentiment_counts["negative"],
            neutral_count=sentiment_counts["neutral"],
            average_sentiment_score=avg_sentiment_score,
            positive_percentage=positive_pct,
            negative_percentage=negative_pct,
            neutral_percentage=neutral_pct,
            critical_issues_count=critical_issues,
            top_positive_themes=positive_themes,
            top_negative_themes=negative_themes,
            sentiment_trend=sentiment_trend
        )
    
    def _extract_themes(self, feedback_items: List[Dict], sentiment_filter: str) -> List[str]:
        """Extract common themes from feedback of a specific sentiment."""
        filtered_items = [item for item in feedback_items if item.get("sentiment") == sentiment_filter]
        
        if sentiment_filter == "positive":
            keywords = self.positive_keywords
        else:
            keywords = self.negative_keywords
        
        theme_counts = Counter()
        
        for item in filtered_items:
            content = item.get("content", "").lower()
            
            for theme, theme_keywords in keywords.items():
                for keyword in theme_keywords:
                    if keyword in content:
                        theme_counts[theme] += 1
                        break  # Count theme only once per feedback item
        
        # Return top 5 themes
        top_themes = [theme for theme, count in theme_counts.most_common(5)]
        print(f"Top {sentiment_filter} themes: {top_themes}")
        return top_themes
    
    def get_critical_feedback(self, feedback_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get feedback items marked as critical severity."""
        feedback_items = feedback_data.get("feedback_items", [])
        critical_items = [item for item in feedback_items if item.get("severity") == "critical"]
        
        print(f"Found {len(critical_items)} critical feedback items")
        return critical_items
    
    def get_negative_feedback_summary(self, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get detailed summary of negative feedback."""
        feedback_items = feedback_data.get("feedback_items", [])
        negative_items = [item for item in feedback_items if item.get("sentiment") == "negative"]
        
        if not negative_items:
            return {"count": 0, "themes": [], "severity_distribution": {}, "sample_feedback": []}
        
        # Analyze severity distribution
        severity_counts = Counter()
        for item in negative_items:
            severity = item.get("severity", "unknown")
            severity_counts[severity] += 1
        
        # Get sample feedback for each severity
        sample_feedback = {}
        for severity in ["critical", "high", "medium", "low"]:
            severity_items = [item for item in negative_items if item.get("severity") == severity]
            if severity_items:
                sample_feedback[severity] = severity_items[0]["content"]  # Take first example
        
        # Extract themes from negative feedback
        negative_themes = self._extract_themes(feedback_items, "negative")
        
        summary = {
            "count": len(negative_items),
            "percentage": (len(negative_items) / len(feedback_items)) * 100,
            "themes": negative_themes,
            "severity_distribution": dict(severity_counts),
            "sample_feedback": sample_feedback,
            "average_sentiment_score": sum(
                item.get("sentiment_score", 0) for item in negative_items
            ) / len(negative_items)
        }
        
        print(f"Negative feedback summary: {summary['count']} items ({summary['percentage']:.1f}%)")
        return summary
    
    def analyze_feedback_by_category(self, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze feedback broken down by category."""
        feedback_items = feedback_data.get("feedback_items", [])
        
        category_analysis = {}
        categories = set(item.get("category", "unknown") for item in feedback_items)
        
        for category in categories:
            category_items = [item for item in feedback_items if item.get("category") == category]
            
            if not category_items:
                continue
            
            # Calculate sentiment distribution for this category
            sentiment_counts = Counter()
            sentiment_scores = []
            
            for item in category_items:
                sentiment = item.get("sentiment", "neutral")
                sentiment_counts[sentiment] += 1
                
                if item.get("sentiment_score") is not None:
                    sentiment_scores.append(item["sentiment_score"])
            
            avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0.0
            
            category_analysis[category] = {
                "total_count": len(category_items),
                "sentiment_distribution": dict(sentiment_counts),
                "average_sentiment_score": avg_sentiment,
                "negative_percentage": (sentiment_counts["negative"] / len(category_items)) * 100
            }
        
        print(f"Analyzed feedback across {len(category_analysis)} categories")
        return category_analysis
    
    def get_sentiment_insights(self, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get comprehensive sentiment insights."""
        sentiment_summary = self.analyze_sentiment(feedback_data)
        negative_summary = self.get_negative_feedback_summary(feedback_data)
        category_analysis = self.analyze_feedback_by_category(feedback_data)
        critical_feedback = self.get_critical_feedback(feedback_data)
        
        insights = {
            "overall_sentiment": {
                "score": sentiment_summary.average_sentiment_score,
                "trend": sentiment_summary.sentiment_trend,
                "distribution": {
                    "positive": sentiment_summary.positive_percentage,
                    "negative": sentiment_summary.negative_percentage,
                    "neutral": sentiment_summary.neutral_percentage
                }
            },
            "positive_insights": {
                "count": sentiment_summary.positive_count,
                "top_themes": sentiment_summary.top_positive_themes
            },
            "negative_insights": negative_summary,
            "critical_issues": {
                "count": len(critical_feedback),
                "items": critical_feedback[:5]  # Top 5 critical items
            },
            "category_breakdown": category_analysis,
            "key_concerns": sentiment_summary.top_negative_themes,
            "recommendation": self._get_sentiment_recommendation(sentiment_summary)
        }
        
        print(f"Generated comprehensive sentiment insights")
        return insights
    
    def _get_sentiment_recommendation(self, summary: SentimentSummary) -> str:
        """Generate recommendation based on sentiment analysis."""
        if summary.negative_percentage > 60:
            return "CRITICAL: Majority negative feedback - consider immediate rollback"
        elif summary.negative_percentage > 40:
            return "HIGH RISK: High negative sentiment - pause rollout and investigate"
        elif summary.critical_issues_count > 5:
            return "MODERATE RISK: Multiple critical issues reported - monitor closely"
        elif summary.positive_percentage > 60:
            return "POSITIVE: Majority positive feedback - continue rollout"
        else:
            return "MIXED: Balanced feedback - proceed with caution and monitoring"