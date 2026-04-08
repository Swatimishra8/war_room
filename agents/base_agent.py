"""Base agent class for the War Room multi-agent system."""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from datetime import datetime

from models.decision import AgentRecommendation, DecisionType


class BaseAgent(ABC):
    """Base class for all War Room agents."""
    
    def __init__(self, agent_name: str, agent_role: str):
        """
        Initialize the base agent.
        
        Args:
            agent_name: Name of the agent
            agent_role: Role/responsibility of the agent
        """
        self.agent_name = agent_name
        self.agent_role = agent_role
        self.analysis_results: Dict[str, Any] = {}
        self.tools: List[Any] = []
        
        print(f"Initialized {self.agent_name} ({self.agent_role})")
    
    @abstractmethod
    def analyze(self, metrics_data: Dict[str, Any], feedback_data: Dict[str, Any], 
                release_notes: str) -> Dict[str, Any]:
        """
        Analyze the provided data and generate insights.
        
        Args:
            metrics_data: Dashboard metrics data
            feedback_data: User feedback data  
            release_notes: Release notes and context
            
        Returns:
            Dictionary containing analysis results
        """
        pass
    
    @abstractmethod
    def get_recommendation(self) -> AgentRecommendation:
        """
        Generate a recommendation based on the analysis.
        
        Returns:
            AgentRecommendation with decision, confidence, and rationale
        """
        pass
    
    def add_tool(self, tool: Any) -> None:
        """Add an analysis tool to this agent."""
        self.tools.append(tool)
        print(f"Added tool {type(tool).__name__} to {self.agent_name}")
    
    def log_analysis_step(self, step: str, details: Any = None) -> None:
        """Log an analysis step for traceability."""
        timestamp = datetime.now().isoformat()
        print(f"[{timestamp}] {self.agent_name}: {step}")
        if details:
            print(f"  Details: {details}")
    
    def _calculate_confidence(self, factors: Dict[str, float]) -> float:
        """
        Calculate confidence score based on various factors.
        
        Args:
            factors: Dictionary of factor names to weights (0-1)
            
        Returns:
            Overall confidence score (0-1)
        """
        if not factors:
            return 0.5
        
        # Weighted average of factors
        total_weight = sum(factors.values())
        if total_weight == 0:
            return 0.5
        
        confidence = sum(score * weight for score, weight in factors.items()) / total_weight
        return max(0.0, min(1.0, confidence))  # Clamp to [0, 1]
    
    def _assess_data_quality(self, metrics_data: Dict[str, Any], 
                           feedback_data: Dict[str, Any]) -> float:
        """
        Assess the quality and completeness of input data.
        
        Returns:
            Data quality score (0-1)
        """
        quality_score = 0.0
        
        # Check metrics data quality
        metrics = metrics_data.get("metrics", {})
        if metrics:
            quality_score += 0.4
            
            # Check if we have sufficient data points
            avg_data_points = sum(
                len(metric.get("data_points", [])) 
                for metric in metrics.values()
            ) / len(metrics)
            
            if avg_data_points >= 100:  # ~4+ days of hourly data
                quality_score += 0.1
        
        # Check feedback data quality
        feedback_items = feedback_data.get("feedback_items", [])
        if feedback_items:
            quality_score += 0.3
            
            # Check if we have diverse feedback
            if len(feedback_items) >= 20:
                quality_score += 0.1
            
            # Check if sentiment analysis is available
            if any(item.get("sentiment_score") is not None for item in feedback_items):
                quality_score += 0.1
        
        return min(1.0, quality_score)
    
    def get_analysis_summary(self) -> Dict[str, Any]:
        """Get a summary of this agent's analysis."""
        return {
            "agent_name": self.agent_name,
            "agent_role": self.agent_role,
            "analysis_timestamp": datetime.now().isoformat(),
            "analysis_results": self.analysis_results,
            "tools_used": [type(tool).__name__ for tool in self.tools]
        }