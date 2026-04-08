"""User feedback data models for the War Room system."""

from datetime import datetime
from typing import List, Optional, Dict
from enum import Enum
from pydantic import BaseModel, Field


class SentimentType(str, Enum):
    """Sentiment classification types."""
    POSITIVE = "positive"
    NEUTRAL = "neutral" 
    NEGATIVE = "negative"


class FeedbackSource(str, Enum):
    """Sources of user feedback."""
    APP_REVIEW = "app_review"
    SUPPORT_TICKET = "support_ticket"
    USER_SURVEY = "user_survey"
    SOCIAL_MEDIA = "social_media"
    IN_APP_FEEDBACK = "in_app_feedback"


class UserFeedback(BaseModel):
    """Individual user feedback entry."""
    id: str
    timestamp: datetime
    source: FeedbackSource
    user_id: Optional[str] = None
    content: str
    sentiment: Optional[SentimentType] = None
    sentiment_score: Optional[float] = Field(None, ge=-1.0, le=1.0)
    category: Optional[str] = None
    severity: Optional[str] = None  # low, medium, high, critical
    metadata: Optional[Dict[str, str]] = None


class FeedbackCollection(BaseModel):
    """Collection of user feedback with analysis."""
    feedback_items: List[UserFeedback]
    total_count: int = 0
    sentiment_distribution: Dict[SentimentType, int] = Field(default_factory=dict)
    category_distribution: Dict[str, int] = Field(default_factory=dict)
    average_sentiment_score: Optional[float] = None
    
    def __init__(self, **data):
        super().__init__(**data)
        self.total_count = len(self.feedback_items)
        self._calculate_distributions()
        print(f"Initialized feedback collection with {self.total_count} items")
    
    def _calculate_distributions(self) -> None:
        """Calculate sentiment and category distributions."""
        sentiment_counts = {sentiment: 0 for sentiment in SentimentType}
        category_counts = {}
        sentiment_scores = []
        
        for feedback in self.feedback_items:
            if feedback.sentiment:
                sentiment_counts[feedback.sentiment] += 1
            
            if feedback.category:
                category_counts[feedback.category] = category_counts.get(feedback.category, 0) + 1
            
            if feedback.sentiment_score is not None:
                sentiment_scores.append(feedback.sentiment_score)
        
        self.sentiment_distribution = sentiment_counts
        self.category_distribution = category_counts
        
        if sentiment_scores:
            self.average_sentiment_score = sum(sentiment_scores) / len(sentiment_scores)
            print(f"Average sentiment score: {self.average_sentiment_score:.3f}")
    
    def get_negative_feedback(self) -> List[UserFeedback]:
        """Get all negative feedback items."""
        return [f for f in self.feedback_items if f.sentiment == SentimentType.NEGATIVE]
    
    def get_critical_issues(self) -> List[UserFeedback]:
        """Get feedback marked as critical severity."""
        return [f for f in self.feedback_items if f.severity == "critical"]