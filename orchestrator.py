"""War Room Orchestrator - Coordinates multi-agent decision making."""

import json
from datetime import datetime, timedelta

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False
from typing import Dict, List, Any, Optional
from pathlib import Path

from models.decision import DecisionOutput, DecisionType, RiskItem, ActionItem, RiskSeverity
from agents import ProductManagerAgent, DataAnalystAgent, MarketingAgent, RiskAgent


class WarRoomOrchestrator:
    """Orchestrates the multi-agent war room decision-making process."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the War Room Orchestrator.
        
        Args:
            config: Optional configuration dictionary
        """
        # Start with default config and merge with provided config
        self.config = self._load_default_config()
        if config:
            self.config.update(config)
        self.agents = {}
        self.analysis_start_time = None
        self.analysis_results = {}
        self.agent_recommendations = []
        
        # Initialize agents
        self._initialize_agents()
        
        print("War Room Orchestrator initialized")
        print(f"Configuration: {self.config}")
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration."""
        return {
            "output_format": "json",  # json or yaml
            "enable_detailed_logging": True,
            "confidence_threshold": 0.7,
            "consensus_weight": {
                "product_manager": 0.3,
                "data_analyst": 0.3,
                "marketing": 0.2,
                "risk": 0.2
            },
            "decision_thresholds": {
                "rollback_threshold": 0.8,  # If weighted risk score > 0.8, recommend rollback
                "pause_threshold": 0.6      # If weighted risk score > 0.6, recommend pause
            }
        }
    
    def _initialize_agents(self) -> None:
        """Initialize all agents in the war room."""
        print("Initializing war room agents...")
        
        self.agents = {
            "product_manager": ProductManagerAgent(),
            "data_analyst": DataAnalystAgent(), 
            "marketing": MarketingAgent(),
            "risk": RiskAgent()
        }
        
        print(f"Initialized {len(self.agents)} agents: {list(self.agents.keys())}")
    
    def run_war_room_analysis(self, metrics_file: str, feedback_file: str, 
                            release_notes_file: str) -> DecisionOutput:
        """
        Run the complete war room analysis and decision-making process.
        
        Args:
            metrics_file: Path to metrics JSON file
            feedback_file: Path to feedback JSON file  
            release_notes_file: Path to release notes markdown file
            
        Returns:
            DecisionOutput with final recommendation and analysis
        """
        
        self.analysis_start_time = datetime.now()
        print(f"\n{'='*60}")
        print(f"STARTING WAR ROOM ANALYSIS - {self.analysis_start_time}")
        print(f"{'='*60}")
        
        # Load input data
        print("\n1. Loading input data...")
        metrics_data, feedback_data, release_notes = self._load_input_data(
            metrics_file, feedback_file, release_notes_file
        )
        
        # Run agent analyses in parallel (conceptually - sequential for traceability)
        print("\n2. Running agent analyses...")
        self._run_agent_analyses(metrics_data, feedback_data, release_notes)
        
        # Collect agent recommendations
        print("\n3. Collecting agent recommendations...")
        self._collect_agent_recommendations()
        
        # Synthesize final decision
        print("\n4. Synthesizing final decision...")
        final_decision = self._synthesize_final_decision(
            metrics_data, feedback_data, release_notes
        )
        
        # Calculate analysis duration
        analysis_end_time = datetime.now()
        analysis_duration = (analysis_end_time - self.analysis_start_time).total_seconds()
        final_decision.analysis_duration_seconds = analysis_duration
        
        print(f"\n{'='*60}")
        print(f"WAR ROOM ANALYSIS COMPLETE - {analysis_end_time}")
        print(f"Duration: {analysis_duration:.1f} seconds")
        print(f"Final Decision: {final_decision.decision.value}")
        print(f"Confidence: {final_decision.confidence_score:.2f}")
        print(f"{'='*60}")
        
        return final_decision
    
    def _load_input_data(self, metrics_file: str, feedback_file: str, 
                        release_notes_file: str) -> tuple:
        """Load and validate input data files."""
        
        print(f"Loading metrics from: {metrics_file}")
        with open(metrics_file, 'r') as f:
            metrics_data = json.load(f)
        print(f"Loaded {len(metrics_data.get('metrics', {}))} metrics")
        
        print(f"Loading feedback from: {feedback_file}")
        with open(feedback_file, 'r') as f:
            feedback_data = json.load(f)
        print(f"Loaded {feedback_data.get('total_count', 0)} feedback items")
        
        print(f"Loading release notes from: {release_notes_file}")
        with open(release_notes_file, 'r') as f:
            release_notes = f.read()
        print(f"Loaded release notes ({len(release_notes)} characters)")
        
        return metrics_data, feedback_data, release_notes
    
    def _run_agent_analyses(self, metrics_data: Dict[str, Any], 
                          feedback_data: Dict[str, Any], release_notes: str) -> None:
        """Run analysis for each agent in sequence."""
        
        for agent_name, agent in self.agents.items():
            print(f"\n--- Running {agent_name.replace('_', ' ').title()} Analysis ---")
            
            try:
                analysis_results = agent.analyze(metrics_data, feedback_data, release_notes)
                self.analysis_results[agent_name] = analysis_results
                print(f"✓ {agent_name} analysis completed successfully")
                
            except Exception as e:
                print(f"✗ {agent_name} analysis failed: {str(e)}")
                self.analysis_results[agent_name] = {"error": str(e)}
    
    def _collect_agent_recommendations(self) -> None:
        """Collect recommendations from all agents."""
        
        print("\nCollecting agent recommendations:")
        
        for agent_name, agent in self.agents.items():
            try:
                recommendation = agent.get_recommendation()
                self.agent_recommendations.append(recommendation)
                
                print(f"✓ {agent_name}: {recommendation.recommendation.value} "
                      f"(confidence: {recommendation.confidence:.2f})")
                
            except Exception as e:
                print(f"✗ {agent_name} recommendation failed: {str(e)}")
    
    def _synthesize_final_decision(self, metrics_data: Dict[str, Any],
                                 feedback_data: Dict[str, Any], 
                                 release_notes: str) -> DecisionOutput:
        """Synthesize final decision from all agent inputs."""
        
        # Extract feature info from data
        feature_name = metrics_data.get("feature_name", "Unknown Feature")
        launch_date_str = metrics_data.get("launch_date")
        launch_date = datetime.fromisoformat(launch_date_str) if launch_date_str else datetime.now()
        
        # Initialize decision output
        decision = DecisionOutput(
            decision=DecisionType.PAUSE,  # Default, will be updated
            feature_name=feature_name,
            launch_date=launch_date,
            timestamp=datetime.now(),
            confidence_score=0.5  # Default, will be updated
        )
        
        # Add agent recommendations
        for recommendation in self.agent_recommendations:
            decision.add_agent_recommendation(recommendation)
        
        # Calculate consensus decision using weighted voting
        consensus_decision = self._calculate_consensus_decision()
        decision.decision = consensus_decision
        
        # Calculate overall confidence score
        decision.confidence_score = self._calculate_overall_confidence()
        
        # Generate rationale
        decision.rationale = self._generate_decision_rationale()
        
        # Build risk register
        self._build_risk_register(decision)
        
        # Create action plan
        self._create_action_plan(decision)
        
        # Develop communication plan
        self._develop_communication_plan(decision)
        
        # Identify confidence factors
        self._identify_confidence_factors(decision)
        
        return decision
    
    def _calculate_consensus_decision(self) -> DecisionType:
        """Calculate consensus decision using weighted voting."""
        
        if not self.agent_recommendations:
            return DecisionType.PAUSE
        
        # Weight agent votes based on configuration
        decision_scores = {
            DecisionType.PROCEED: 0.0,
            DecisionType.PAUSE: 0.0,
            DecisionType.ROLL_BACK: 0.0
        }
        
        weights = self.config["consensus_weight"]
        
        for recommendation in self.agent_recommendations:
            agent_name = recommendation.agent_name.lower().replace("/", "_").replace(" ", "_")
            agent_key = None
            
            # Map agent names to weight keys
            if "product" in agent_name:
                agent_key = "product_manager"
            elif "data" in agent_name:
                agent_key = "data_analyst"
            elif "marketing" in agent_name:
                agent_key = "marketing"
            elif "risk" in agent_name:
                agent_key = "risk"
            
            if agent_key and agent_key in weights:
                weight = weights[agent_key]
                confidence_weight = recommendation.confidence
                
                # Weight the vote by both agent importance and confidence
                vote_strength = weight * confidence_weight
                decision_scores[recommendation.recommendation] += vote_strength
        
        # Find the decision with highest weighted score
        consensus = max(decision_scores.items(), key=lambda x: x[1])[0]
        
        print(f"Consensus calculation: {decision_scores}")
        print(f"Consensus decision: {consensus.value}")
        
        return consensus
    
    def _calculate_overall_confidence(self) -> float:
        """Calculate overall confidence score."""
        
        if not self.agent_recommendations:
            return 0.5
        
        # Weighted average of agent confidences
        weights = self.config["consensus_weight"]
        total_weighted_confidence = 0.0
        total_weight = 0.0
        
        for recommendation in self.agent_recommendations:
            agent_name = recommendation.agent_name.lower().replace("/", "_").replace(" ", "_")
            agent_key = None
            
            if "product" in agent_name:
                agent_key = "product_manager"
            elif "data" in agent_name:
                agent_key = "data_analyst"
            elif "marketing" in agent_name:
                agent_key = "marketing"
            elif "risk" in agent_name:
                agent_key = "risk"
            
            if agent_key and agent_key in weights:
                weight = weights[agent_key]
                total_weighted_confidence += recommendation.confidence * weight
                total_weight += weight
        
        overall_confidence = total_weighted_confidence / total_weight if total_weight > 0 else 0.5
        
        # Adjust confidence based on consensus strength
        decision_agreement = self._calculate_decision_agreement()
        if decision_agreement < 0.5:  # Low agreement
            overall_confidence *= 0.8
        
        print(f"Overall confidence: {overall_confidence:.3f} (agreement: {decision_agreement:.3f})")
        
        return overall_confidence
    
    def _calculate_decision_agreement(self) -> float:
        """Calculate how much agents agree on the decision."""
        
        if not self.agent_recommendations:
            return 0.5
        
        # Count votes for each decision
        decision_counts = {}
        for recommendation in self.agent_recommendations:
            decision = recommendation.recommendation
            decision_counts[decision] = decision_counts.get(decision, 0) + 1
        
        # Calculate agreement as percentage of agents agreeing with majority
        max_count = max(decision_counts.values())
        total_agents = len(self.agent_recommendations)
        
        return max_count / total_agents
    
    def _generate_decision_rationale(self) -> Dict[str, Any]:
        """Generate comprehensive decision rationale."""
        
        rationale = {
            "key_drivers": [],
            "metric_references": {},
            "feedback_summary": "",
            "agent_consensus": {},
            "risk_factors": [],
            "opportunity_factors": []
        }
        
        # Collect key drivers from agent findings
        for recommendation in self.agent_recommendations:
            agent_name = recommendation.agent_name
            
            # Add key findings as drivers
            for finding in recommendation.key_findings:
                rationale["key_drivers"].append(f"{agent_name}: {finding}")
            
            # Track agent positions
            rationale["agent_consensus"][agent_name] = {
                "recommendation": recommendation.recommendation.value,
                "confidence": recommendation.confidence,
                "rationale": recommendation.rationale
            }
        
        # Extract metric references from analysis results
        if "data_analyst" in self.analysis_results:
            da_results = self.analysis_results["data_analyst"]
            metric_insights = da_results.get("metric_insights", {})
            
            rationale["metric_references"]["overall_health_score"] = metric_insights.get("overall_health_score", 0.5)
            rationale["metric_references"]["critical_metrics"] = len(metric_insights.get("critical_metrics", []))
            rationale["metric_references"]["warning_metrics"] = len(metric_insights.get("warning_metrics", []))
        
        # Generate feedback summary
        if "marketing" in self.analysis_results:
            marketing_results = self.analysis_results["marketing"]
            sentiment_insights = marketing_results.get("sentiment_insights", {})
            overall_sentiment = sentiment_insights.get("overall_sentiment", {})
            
            sentiment_score = overall_sentiment.get("score", 0)
            negative_pct = overall_sentiment.get("distribution", {}).get("negative", 0)
            
            rationale["feedback_summary"] = (
                f"Customer sentiment score: {sentiment_score:.3f}, "
                f"{negative_pct:.0f}% negative feedback"
            )
        
        # Identify risk and opportunity factors
        for recommendation in self.agent_recommendations:
            if recommendation.concerns:
                rationale["risk_factors"].extend(recommendation.concerns)
            
            # Look for positive indicators in findings
            for finding in recommendation.key_findings:
                if any(word in finding.lower() for word in ["positive", "strong", "success", "exceeds"]):
                    rationale["opportunity_factors"].append(finding)
        
        return rationale
    
    def _build_risk_register(self, decision: DecisionOutput) -> None:
        """Build comprehensive risk register from agent analyses."""
        
        # Collect risks from Risk Agent analysis
        if "risk" in self.analysis_results:
            risk_results = self.analysis_results["risk"]
            risk_assessment = risk_results.get("risk_assessment", {})
            
            # Add critical risks
            for risk in risk_assessment.get("critical_risks", []):
                decision.add_risk(RiskItem(
                    risk=risk.get("description", "Critical risk identified"),
                    severity=RiskSeverity.CRITICAL,
                    mitigation="Immediate investigation and resolution required",
                    owner="Engineering/Product"
                ))
            
            # Add high risks
            for risk in risk_assessment.get("high_risks", []):
                decision.add_risk(RiskItem(
                    risk=risk.get("description", "High risk identified"),
                    severity=RiskSeverity.HIGH,
                    mitigation="Close monitoring and mitigation planning required",
                    owner="Cross-functional team"
                ))
        
        # Add risks from other agents
        for recommendation in self.agent_recommendations:
            if recommendation.concerns:
                for concern in recommendation.concerns:
                    # Determine severity based on agent type and concern content
                    severity = RiskSeverity.MEDIUM
                    if any(word in concern.lower() for word in ["critical", "severe", "major"]):
                        severity = RiskSeverity.HIGH
                    elif any(word in concern.lower() for word in ["minor", "low", "small"]):
                        severity = RiskSeverity.LOW
                    
                    decision.add_risk(RiskItem(
                        risk=f"{recommendation.agent_name}: {concern}",
                        severity=severity,
                        mitigation="Monitor and address as needed",
                        owner=self._determine_risk_owner(concern)
                    ))
    
    def _determine_risk_owner(self, concern: str) -> str:
        """Determine appropriate owner for a risk based on its content."""
        
        concern_lower = concern.lower()
        
        if any(word in concern_lower for word in ["technical", "error", "latency", "performance"]):
            return "Engineering"
        elif any(word in concern_lower for word in ["customer", "sentiment", "feedback", "brand"]):
            return "Marketing/Customer Success"
        elif any(word in concern_lower for word in ["business", "revenue", "conversion", "adoption"]):
            return "Product Management"
        elif any(word in concern_lower for word in ["support", "operational", "capacity"]):
            return "Operations"
        else:
            return "Cross-functional team"
    
    def _create_action_plan(self, decision: DecisionOutput) -> None:
        """Create detailed action plan based on decision and risks."""
        
        # 24-hour actions
        immediate_actions = []
        
        if decision.decision == DecisionType.ROLL_BACK:
            immediate_actions.extend([
                ActionItem(
                    action="Execute emergency rollback to previous version",
                    owner="DevOps/Engineering",
                    timeline="24 hours",
                    priority="critical"
                ),
                ActionItem(
                    action="Notify all stakeholders of rollback decision",
                    owner="Product Manager",
                    timeline="24 hours", 
                    priority="high"
                ),
                ActionItem(
                    action="Prepare customer communication about service restoration",
                    owner="Marketing/Communications",
                    timeline="24 hours",
                    priority="high"
                )
            ])
        
        elif decision.decision == DecisionType.PAUSE:
            immediate_actions.extend([
                ActionItem(
                    action="Halt new user onboarding to feature",
                    owner="Product/Engineering",
                    timeline="24 hours",
                    priority="high"
                ),
                ActionItem(
                    action="Convene emergency stakeholder meeting",
                    owner="Product Manager", 
                    timeline="24 hours",
                    priority="high"
                ),
                ActionItem(
                    action="Implement enhanced monitoring and alerting",
                    owner="DevOps",
                    timeline="24 hours",
                    priority="medium"
                )
            ])
        
        else:  # PROCEED
            immediate_actions.extend([
                ActionItem(
                    action="Increase monitoring frequency for key metrics",
                    owner="DevOps/Data",
                    timeline="24 hours",
                    priority="medium"
                ),
                ActionItem(
                    action="Brief customer support team on potential issues",
                    owner="Customer Success",
                    timeline="24 hours",
                    priority="medium"
                )
            ])
        
        # Add immediate actions to decision
        for action in immediate_actions:
            decision.add_action("24 hours", action)
        
        # 48-hour actions
        followup_actions = []
        
        if decision.decision in [DecisionType.ROLL_BACK, DecisionType.PAUSE]:
            followup_actions.extend([
                ActionItem(
                    action="Conduct root cause analysis of issues",
                    owner="Engineering/Product",
                    timeline="48 hours",
                    priority="high"
                ),
                ActionItem(
                    action="Develop remediation plan with timeline",
                    owner="Cross-functional team",
                    timeline="48 hours",
                    priority="high"
                ),
                ActionItem(
                    action="Assess customer impact and retention measures",
                    owner="Customer Success/Marketing",
                    timeline="48 hours",
                    priority="medium"
                )
            ])
        
        else:  # PROCEED
            followup_actions.extend([
                ActionItem(
                    action="Analyze user cohort performance for early signals",
                    owner="Data/Product",
                    timeline="48 hours",
                    priority="medium"
                ),
                ActionItem(
                    action="Prepare success metrics report for stakeholders",
                    owner="Product Manager",
                    timeline="48 hours",
                    priority="low"
                )
            ])
        
        # Add followup actions to decision
        for action in followup_actions:
            decision.add_action("48 hours", action)
    
    def _develop_communication_plan(self, decision: DecisionOutput) -> None:
        """Develop internal and external communication plan."""
        
        communication_plan = {}
        
        # Internal communications
        if decision.decision == DecisionType.ROLL_BACK:
            communication_plan["internal"] = (
                "URGENT: Immediate notification to all stakeholders about rollback decision. "
                "Engineering leadership briefing within 2 hours. All-hands update within 6 hours. "
                "Daily status updates until resolution."
            )
            communication_plan["external"] = (
                "Proactive customer communication acknowledging issues and service restoration. "
                "Status page updates every 2 hours. Customer support talking points prepared. "
                "Follow-up communication within 48 hours with resolution timeline."
            )
        
        elif decision.decision == DecisionType.PAUSE:
            communication_plan["internal"] = (
                "Stakeholder notification of pause decision within 4 hours. "
                "Cross-functional war room established. Daily leadership briefings. "
                "Team updates every 24 hours during pause period."
            )
            communication_plan["external"] = (
                "Targeted communication to affected users about temporary pause in rollout. "
                "Support team briefing on potential customer questions. "
                "Proactive outreach to key customers if needed."
            )
        
        else:  # PROCEED
            communication_plan["internal"] = (
                "Success metrics shared with stakeholders. Enhanced monitoring alerts to key personnel. "
                "Weekly progress reports during continued rollout. Team recognition for successful launch."
            )
            communication_plan["external"] = (
                "Positive customer communication highlighting feature benefits. "
                "Success story development for marketing. Customer feedback collection intensified. "
                "Community engagement to amplify positive reception."
            )
        
        decision.communication_plan = communication_plan
    
    def _identify_confidence_factors(self, decision: DecisionOutput) -> None:
        """Identify factors that would increase confidence in the decision."""
        
        confidence_factors = []
        
        # Data quality factors
        if "data_analyst" in self.analysis_results:
            da_results = self.analysis_results["data_analyst"]
            data_quality = da_results.get("data_quality", {}).get("overall_score", 0.5)
            
            if data_quality < 0.7:
                confidence_factors.append("Improve data completeness and quality")
        
        # Sample size factors
        if "marketing" in self.analysis_results:
            marketing_results = self.analysis_results["marketing"]
            sentiment_insights = marketing_results.get("sentiment_insights", {})
            feedback_count = sentiment_insights.get("overall_sentiment", {}).get("distribution", {})
            total_feedback = sum(feedback_count.values()) if feedback_count else 0
            
            if total_feedback < 50:
                confidence_factors.append("Collect larger customer feedback sample")
        
        # Time-based factors
        confidence_factors.extend([
            "Additional 48-72 hours of metric observation",
            "A/B test results with statistical significance",
            "Customer cohort analysis over longer time period"
        ])
        
        # Agent-specific factors
        low_confidence_agents = [
            rec.agent_name for rec in self.agent_recommendations 
            if rec.confidence < 0.7
        ]
        
        if low_confidence_agents:
            confidence_factors.append(
                f"Address concerns from {', '.join(low_confidence_agents)}"
            )
        
        # Risk mitigation factors
        if len(decision.risk_register) > 5:
            confidence_factors.append("Implement risk mitigation strategies")
        
        decision.confidence_factors = confidence_factors
    
    def save_decision(self, decision: DecisionOutput, output_path: str) -> None:
        """Save the decision output to file."""
        
        # Convert decision to dictionary for serialization
        decision_dict = self._decision_to_dict(decision)
        
        output_format = self.config.get("output_format", "json")
        
        if output_format == "yaml" and HAS_YAML:
            with open(output_path, 'w') as f:
                yaml.dump(decision_dict, f, default_flow_style=False, indent=2)
        elif output_format == "yaml" and not HAS_YAML:
            print("Warning: YAML not available, saving as JSON instead")
            with open(output_path, 'w') as f:
                json.dump(decision_dict, f, indent=2, default=str)
        else:  # JSON
            with open(output_path, 'w') as f:
                json.dump(decision_dict, f, indent=2, default=str)
        
        print(f"Decision saved to: {output_path}")
    
    def _decision_to_dict(self, decision: DecisionOutput) -> Dict[str, Any]:
        """Convert DecisionOutput to dictionary for serialization."""
        
        return {
            "decision": decision.decision.value,
            "timestamp": decision.timestamp.isoformat(),
            "feature_name": decision.feature_name,
            "launch_date": decision.launch_date.isoformat(),
            "analysis_duration_seconds": decision.analysis_duration_seconds,
            "rationale": decision.rationale,
            "risk_register": [
                {
                    "risk": risk.risk,
                    "severity": risk.severity.value,
                    "probability": risk.probability,
                    "impact": risk.impact,
                    "mitigation": risk.mitigation,
                    "owner": risk.owner
                }
                for risk in decision.risk_register
            ],
            "action_plan": {
                timeline: [
                    {
                        "action": action.action,
                        "owner": action.owner,
                        "timeline": action.timeline,
                        "priority": action.priority,
                        "dependencies": action.dependencies
                    }
                    for action in actions
                ]
                for timeline, actions in decision.action_plan.items()
            },
            "communication_plan": decision.communication_plan,
            "confidence_score": decision.confidence_score,
            "confidence_factors": decision.confidence_factors,
            "agent_recommendations": [
                {
                    "agent_name": rec.agent_name,
                    "recommendation": rec.recommendation.value,
                    "confidence": rec.confidence,
                    "rationale": rec.rationale,
                    "key_findings": rec.key_findings,
                    "concerns": rec.concerns,
                    "timestamp": rec.timestamp.isoformat()
                }
                for rec in decision.agent_recommendations
            ]
        }
    
    def get_analysis_summary(self) -> Dict[str, Any]:
        """Get summary of the complete analysis process."""
        
        return {
            "orchestrator_config": self.config,
            "agents_initialized": list(self.agents.keys()),
            "analysis_start_time": self.analysis_start_time.isoformat() if self.analysis_start_time else None,
            "agent_analysis_results": {
                agent_name: {
                    "completed": agent_name in self.analysis_results,
                    "has_error": "error" in self.analysis_results.get(agent_name, {})
                }
                for agent_name in self.agents.keys()
            },
            "agent_recommendations_count": len(self.agent_recommendations),
            "consensus_weights": self.config["consensus_weight"]
        }