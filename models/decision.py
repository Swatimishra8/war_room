"""Decision output models for the War Room system."""

from datetime import datetime
from typing import List, Dict, Optional, Any
from enum import Enum
from pydantic import BaseModel, Field


class DecisionType(str, Enum):
    """Possible launch decisions."""
    PROCEED = "Proceed"
    PAUSE = "Pause" 
    ROLL_BACK = "Roll Back"


class RiskSeverity(str, Enum):
    """Risk severity levels."""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class RiskItem(BaseModel):
    """Individual risk item in the risk register."""
    risk: str
    severity: RiskSeverity
    probability: Optional[float] = Field(None, ge=0.0, le=1.0)
    impact: Optional[str] = None
    mitigation: str
    owner: Optional[str] = None


class ActionItem(BaseModel):
    """Individual action item in the action plan."""
    action: str
    owner: str
    timeline: str  # e.g., "24 hours", "48 hours"
    priority: Optional[str] = None  # high, medium, low
    dependencies: Optional[List[str]] = None


class AgentRecommendation(BaseModel):
    """Recommendation from an individual agent."""
    agent_name: str
    recommendation: DecisionType
    confidence: float = Field(ge=0.0, le=1.0)
    rationale: str
    key_findings: List[str]
    concerns: Optional[List[str]] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class DecisionOutput(BaseModel):
    """Final structured decision output from the war room."""
    
    # Core decision
    decision: DecisionType
    timestamp: datetime = Field(default_factory=datetime.now)
    
    # Rationale
    rationale: Dict[str, Any] = Field(default_factory=dict)
    
    # Risk management
    risk_register: List[RiskItem] = Field(default_factory=list)
    
    # Action planning
    action_plan: Dict[str, List[ActionItem]] = Field(default_factory=dict)
    
    # Communication
    communication_plan: Dict[str, str] = Field(default_factory=dict)
    
    # Confidence and validation
    confidence_score: float = Field(ge=0.0, le=1.0)
    confidence_factors: List[str] = Field(default_factory=list)
    
    # Agent inputs
    agent_recommendations: List[AgentRecommendation] = Field(default_factory=list)
    
    # Metadata
    feature_name: str
    launch_date: datetime
    analysis_duration_seconds: Optional[float] = None
    
    def add_agent_recommendation(self, recommendation: AgentRecommendation) -> None:
        """Add an agent recommendation to the decision."""
        self.agent_recommendations.append(recommendation)
        print(f"Added recommendation from {recommendation.agent_name}: {recommendation.recommendation}")
    
    def add_risk(self, risk: RiskItem) -> None:
        """Add a risk item to the risk register."""
        self.risk_register.append(risk)
        print(f"Added {risk.severity.value} risk: {risk.risk}")
    
    def add_action(self, timeline: str, action: ActionItem) -> None:
        """Add an action item to the action plan."""
        if timeline not in self.action_plan:
            self.action_plan[timeline] = []
        self.action_plan[timeline].append(action)
        print(f"Added action for {timeline}: {action.action} (owner: {action.owner})")
    
    def get_consensus_decision(self) -> DecisionType:
        """Calculate consensus decision from agent recommendations."""
        if not self.agent_recommendations:
            return self.decision
        
        decision_counts = {}
        weighted_scores = {}
        
        for rec in self.agent_recommendations:
            decision = rec.recommendation
            confidence = rec.confidence
            
            decision_counts[decision] = decision_counts.get(decision, 0) + 1
            weighted_scores[decision] = weighted_scores.get(decision, 0) + confidence
        
        # Find decision with highest weighted score
        consensus = max(weighted_scores.items(), key=lambda x: x[1])[0]
        print(f"Consensus decision: {consensus} (weighted score: {weighted_scores[consensus]:.2f})")
        
        return consensus