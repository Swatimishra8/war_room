"""Risk/Critic agent for the War Room system."""

from typing import Dict, List, Any, Optional
from datetime import datetime

from .base_agent import BaseAgent
from models.decision import AgentRecommendation, DecisionType, RiskItem, RiskSeverity


class RiskAgent(BaseAgent):
    """Risk/Critic agent that challenges assumptions, highlights risks, and requests additional evidence."""
    
    def __init__(self):
        super().__init__("Risk/Critic", "Challenges assumptions, highlights risks, and requests additional evidence")
        
        # Define risk categories and assessment criteria
        self.risk_categories = {
            "technical": {
                "weight": 0.3,
                "indicators": ["error_rate", "api_latency_p95", "crash_rate"],
                "thresholds": {"critical": 0.8, "high": 0.6, "medium": 0.4}
            },
            "business": {
                "weight": 0.25,
                "indicators": ["revenue_impact", "customer_churn", "market_position"],
                "thresholds": {"critical": 0.8, "high": 0.6, "medium": 0.4}
            },
            "operational": {
                "weight": 0.2,
                "indicators": ["support_ticket_volume", "team_capacity", "process_breakdown"],
                "thresholds": {"critical": 0.8, "high": 0.6, "medium": 0.4}
            },
            "reputation": {
                "weight": 0.15,
                "indicators": ["brand_perception", "customer_sentiment", "media_attention"],
                "thresholds": {"critical": 0.8, "high": 0.6, "medium": 0.4}
            },
            "strategic": {
                "weight": 0.1,
                "indicators": ["competitive_impact", "long_term_vision", "resource_allocation"],
                "thresholds": {"critical": 0.8, "high": 0.6, "medium": 0.4}
            }
        }
        
        # Common cognitive biases to challenge
        self.bias_checks = [
            "confirmation_bias",
            "optimism_bias", 
            "sunk_cost_fallacy",
            "anchoring_bias",
            "availability_heuristic"
        ]
        
        print(f"Initialized Risk Agent with {len(self.risk_categories)} risk categories")
    
    def analyze(self, metrics_data: Dict[str, Any], feedback_data: Dict[str, Any], 
                release_notes: str) -> Dict[str, Any]:
        """Perform comprehensive risk analysis and challenge assumptions."""
        
        self.log_analysis_step("Starting Risk/Critic comprehensive analysis")
        
        # Comprehensive risk assessment
        self.log_analysis_step("Performing multi-dimensional risk assessment")
        risk_assessment = self._perform_comprehensive_risk_assessment(
            metrics_data, feedback_data, release_notes
        )
        
        # Challenge common assumptions and biases
        self.log_analysis_step("Challenging assumptions and identifying cognitive biases")
        bias_analysis = self._challenge_assumptions_and_biases(
            metrics_data, feedback_data, risk_assessment
        )
        
        # Identify hidden risks and blind spots
        self.log_analysis_step("Identifying hidden risks and potential blind spots")
        hidden_risks = self._identify_hidden_risks(metrics_data, feedback_data)
        
        # Stress test scenarios
        self.log_analysis_step("Running stress test scenarios")
        stress_test_results = self._run_stress_test_scenarios(risk_assessment)
        
        # Evidence quality assessment
        self.log_analysis_step("Assessing evidence quality and data reliability")
        evidence_assessment = self._assess_evidence_quality(metrics_data, feedback_data)
        
        # Long-term impact analysis
        self.log_analysis_step("Analyzing long-term strategic impacts")
        long_term_analysis = self._analyze_long_term_impacts(
            metrics_data, feedback_data, risk_assessment
        )
        
        # Generate risk mitigation strategies
        self.log_analysis_step("Developing risk mitigation strategies")
        mitigation_strategies = self._develop_mitigation_strategies(risk_assessment, hidden_risks)
        
        self.analysis_results = {
            "risk_assessment": risk_assessment,
            "bias_analysis": bias_analysis,
            "hidden_risks": hidden_risks,
            "stress_test_results": stress_test_results,
            "evidence_assessment": evidence_assessment,
            "long_term_analysis": long_term_analysis,
            "mitigation_strategies": mitigation_strategies,
            "key_findings": self._generate_risk_findings(
                risk_assessment, bias_analysis, hidden_risks, evidence_assessment
            )
        }
        
        self.log_analysis_step("Risk/Critic analysis complete", 
                             f"Overall risk score: {risk_assessment['overall_risk_score']:.2f}")
        
        return self.analysis_results
    
    def _perform_comprehensive_risk_assessment(self, metrics_data: Dict[str, Any], 
                                             feedback_data: Dict[str, Any],
                                             release_notes: str) -> Dict[str, Any]:
        """Perform comprehensive multi-dimensional risk assessment."""
        
        risk_assessment = {
            "overall_risk_score": 0.0,
            "risk_by_category": {},
            "critical_risks": [],
            "high_risks": [],
            "medium_risks": [],
            "risk_trends": {},
            "cascading_risk_potential": 0.0
        }
        
        total_weighted_score = 0.0
        
        # Assess each risk category
        for category, config in self.risk_categories.items():
            category_score = self._assess_risk_category(
                category, config, metrics_data, feedback_data, release_notes
            )
            
            risk_assessment["risk_by_category"][category] = category_score
            total_weighted_score += category_score["risk_score"] * config["weight"]
            
            # Categorize risks by severity
            if category_score["risk_score"] >= config["thresholds"]["critical"]:
                risk_assessment["critical_risks"].append({
                    "category": category,
                    "score": category_score["risk_score"],
                    "description": category_score["description"],
                    "indicators": category_score["risk_indicators"]
                })
            elif category_score["risk_score"] >= config["thresholds"]["high"]:
                risk_assessment["high_risks"].append({
                    "category": category,
                    "score": category_score["risk_score"],
                    "description": category_score["description"],
                    "indicators": category_score["risk_indicators"]
                })
            elif category_score["risk_score"] >= config["thresholds"]["medium"]:
                risk_assessment["medium_risks"].append({
                    "category": category,
                    "score": category_score["risk_score"],
                    "description": category_score["description"],
                    "indicators": category_score["risk_indicators"]
                })
        
        risk_assessment["overall_risk_score"] = total_weighted_score
        
        # Assess cascading risk potential
        risk_assessment["cascading_risk_potential"] = self._assess_cascading_risks(
            risk_assessment["risk_by_category"]
        )
        
        print(f"Risk assessment: {total_weighted_score:.2f} overall score, "
              f"{len(risk_assessment['critical_risks'])} critical risks")
        
        return risk_assessment
    
    def _assess_risk_category(self, category: str, config: Dict[str, Any],
                            metrics_data: Dict[str, Any], feedback_data: Dict[str, Any],
                            release_notes: str) -> Dict[str, Any]:
        """Assess risk for a specific category."""
        
        category_assessment = {
            "risk_score": 0.0,
            "description": "",
            "risk_indicators": [],
            "evidence": []
        }
        
        if category == "technical":
            category_assessment = self._assess_technical_risks(metrics_data)
        elif category == "business":
            category_assessment = self._assess_business_risks(metrics_data, feedback_data)
        elif category == "operational":
            category_assessment = self._assess_operational_risks(metrics_data, feedback_data)
        elif category == "reputation":
            category_assessment = self._assess_reputation_risks(feedback_data)
        elif category == "strategic":
            category_assessment = self._assess_strategic_risks(metrics_data, feedback_data, release_notes)
        
        return category_assessment
    
    def _assess_technical_risks(self, metrics_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess technical risks from metrics data."""
        
        technical_risks = {
            "risk_score": 0.0,
            "description": "Technical system stability and performance risks",
            "risk_indicators": [],
            "evidence": []
        }
        
        metrics = metrics_data.get("metrics", {})
        risk_factors = []
        
        # Error rate risk
        if "error_rate" in metrics:
            error_data = metrics["error_rate"]["data_points"]
            if error_data:
                current_error_rate = error_data[-1]["value"]
                baseline_error_rate = metrics["error_rate"].get("baseline", 0.5)
                
                if current_error_rate > 2.0:  # Critical threshold
                    risk_factors.append(0.9)
                    technical_risks["risk_indicators"].append("Critical error rate")
                    technical_risks["evidence"].append(f"Error rate: {current_error_rate:.2f}%")
                elif current_error_rate > 1.5:  # Warning threshold
                    risk_factors.append(0.7)
                    technical_risks["risk_indicators"].append("Elevated error rate")
                    technical_risks["evidence"].append(f"Error rate: {current_error_rate:.2f}%")
                elif current_error_rate > baseline_error_rate * 2:  # 2x baseline
                    risk_factors.append(0.5)
                    technical_risks["risk_indicators"].append("Error rate above baseline")
                    technical_risks["evidence"].append(f"Error rate: {current_error_rate:.2f}% vs baseline {baseline_error_rate:.2f}%")
        
        # API latency risk
        if "api_latency_p95" in metrics:
            latency_data = metrics["api_latency_p95"]["data_points"]
            if latency_data:
                current_latency = latency_data[-1]["value"]
                baseline_latency = metrics["api_latency_p95"].get("baseline", 220)
                
                if current_latency > 400:  # Critical threshold
                    risk_factors.append(0.8)
                    technical_risks["risk_indicators"].append("Critical API latency")
                    technical_risks["evidence"].append(f"API P95 latency: {current_latency:.0f}ms")
                elif current_latency > 300:  # Warning threshold
                    risk_factors.append(0.6)
                    technical_risks["risk_indicators"].append("High API latency")
                    technical_risks["evidence"].append(f"API P95 latency: {current_latency:.0f}ms")
                elif current_latency > baseline_latency * 1.5:  # 50% above baseline
                    risk_factors.append(0.4)
                    technical_risks["risk_indicators"].append("Latency degradation")
                    technical_risks["evidence"].append(f"Latency: {current_latency:.0f}ms vs baseline {baseline_latency:.0f}ms")
        
        # Payment success rate risk
        if "payment_success_rate" in metrics:
            payment_data = metrics["payment_success_rate"]["data_points"]
            if payment_data:
                current_rate = payment_data[-1]["value"]
                baseline_rate = metrics["payment_success_rate"].get("baseline", 97.8)
                
                if current_rate < 95.0:  # Critical threshold
                    risk_factors.append(0.9)
                    technical_risks["risk_indicators"].append("Critical payment failure rate")
                    technical_risks["evidence"].append(f"Payment success rate: {current_rate:.1f}%")
                elif current_rate < 96.5:  # Warning threshold
                    risk_factors.append(0.6)
                    technical_risks["risk_indicators"].append("Declining payment success")
                    technical_risks["evidence"].append(f"Payment success rate: {current_rate:.1f}%")
        
        # Calculate overall technical risk score
        if risk_factors:
            technical_risks["risk_score"] = max(risk_factors)  # Take highest risk
        else:
            technical_risks["risk_score"] = 0.2  # Low baseline risk
        
        return technical_risks
    
    def _assess_business_risks(self, metrics_data: Dict[str, Any], 
                             feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess business impact and revenue risks."""
        
        business_risks = {
            "risk_score": 0.0,
            "description": "Business impact and revenue generation risks",
            "risk_indicators": [],
            "evidence": []
        }
        
        metrics = metrics_data.get("metrics", {})
        risk_factors = []
        
        # Conversion rate risk
        if "activation_conversion" in metrics:
            conversion_data = metrics["activation_conversion"]["data_points"]
            if conversion_data:
                current_conversion = conversion_data[-1]["value"]
                baseline_conversion = metrics["activation_conversion"].get("baseline", 13.2)
                
                if current_conversion < baseline_conversion * 0.8:  # 20% drop
                    risk_factors.append(0.8)
                    business_risks["risk_indicators"].append("Significant conversion drop")
                    business_risks["evidence"].append(f"Conversion: {current_conversion:.1f}% vs baseline {baseline_conversion:.1f}%")
                elif current_conversion < baseline_conversion * 0.9:  # 10% drop
                    risk_factors.append(0.6)
                    business_risks["risk_indicators"].append("Conversion decline")
                    business_risks["evidence"].append(f"Conversion: {current_conversion:.1f}% vs baseline {baseline_conversion:.1f}%")
        
        # Retention risk
        if "d1_retention" in metrics:
            retention_data = metrics["d1_retention"]["data_points"]
            if retention_data:
                current_retention = retention_data[-1]["value"]
                baseline_retention = metrics["d1_retention"].get("baseline", 72.0)
                
                if current_retention < 60.0:  # Critical threshold
                    risk_factors.append(0.9)
                    business_risks["risk_indicators"].append("Critical retention rate")
                    business_risks["evidence"].append(f"D1 retention: {current_retention:.1f}%")
                elif current_retention < baseline_retention * 0.9:  # 10% drop
                    risk_factors.append(0.6)
                    business_risks["risk_indicators"].append("Retention decline")
                    business_risks["evidence"].append(f"Retention: {current_retention:.1f}% vs baseline {baseline_retention:.1f}%")
        
        # Feature adoption risk
        if "feature_adoption_rate" in metrics:
            adoption_data = metrics["feature_adoption_rate"]["data_points"]
            if adoption_data:
                current_adoption = adoption_data[-1]["value"]
                target_adoption = metrics["feature_adoption_rate"].get("target", 25.0)
                
                if current_adoption < target_adoption * 0.4:  # Less than 40% of target
                    risk_factors.append(0.7)
                    business_risks["risk_indicators"].append("Poor feature adoption")
                    business_risks["evidence"].append(f"Adoption: {current_adoption:.1f}% vs target {target_adoption:.1f}%")
                elif current_adoption < target_adoption * 0.6:  # Less than 60% of target
                    risk_factors.append(0.5)
                    business_risks["risk_indicators"].append("Below-target adoption")
                    business_risks["evidence"].append(f"Adoption: {current_adoption:.1f}% vs target {target_adoption:.1f}%")
        
        # Customer sentiment impact on business
        avg_sentiment = feedback_data.get("average_sentiment_score", 0)
        if avg_sentiment < -0.3:
            risk_factors.append(0.8)
            business_risks["risk_indicators"].append("Negative sentiment business impact")
            business_risks["evidence"].append(f"Average sentiment: {avg_sentiment:.3f}")
        elif avg_sentiment < -0.1:
            risk_factors.append(0.5)
            business_risks["risk_indicators"].append("Sentiment concerns")
            business_risks["evidence"].append(f"Average sentiment: {avg_sentiment:.3f}")
        
        # Calculate overall business risk score
        if risk_factors:
            business_risks["risk_score"] = max(risk_factors)
        else:
            business_risks["risk_score"] = 0.3  # Moderate baseline risk
        
        return business_risks
    
    def _assess_operational_risks(self, metrics_data: Dict[str, Any], 
                                feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess operational capacity and process risks."""
        
        operational_risks = {
            "risk_score": 0.0,
            "description": "Operational capacity and process execution risks",
            "risk_indicators": [],
            "evidence": []
        }
        
        metrics = metrics_data.get("metrics", {})
        risk_factors = []
        
        # Support ticket volume risk
        if "support_ticket_volume" in metrics:
            ticket_data = metrics["support_ticket_volume"]["data_points"]
            if ticket_data:
                current_volume = ticket_data[-1]["value"]
                baseline_volume = metrics["support_ticket_volume"].get("baseline", 95)
                
                if current_volume > 200:  # Critical threshold
                    risk_factors.append(0.9)
                    operational_risks["risk_indicators"].append("Critical support load")
                    operational_risks["evidence"].append(f"Support tickets: {current_volume:.0f}/day")
                elif current_volume > 150:  # Warning threshold
                    risk_factors.append(0.7)
                    operational_risks["risk_indicators"].append("High support load")
                    operational_risks["evidence"].append(f"Support tickets: {current_volume:.0f}/day")
                elif current_volume > baseline_volume * 1.5:  # 50% increase
                    risk_factors.append(0.5)
                    operational_risks["risk_indicators"].append("Increased support burden")
                    operational_risks["evidence"].append(f"Tickets: {current_volume:.0f} vs baseline {baseline_volume:.0f}")
        
        # Critical feedback volume (operational impact)
        feedback_items = feedback_data.get("feedback_items", [])
        critical_feedback = [item for item in feedback_items if item.get("severity") == "critical"]
        
        if len(critical_feedback) > 10:
            risk_factors.append(0.8)
            operational_risks["risk_indicators"].append("High critical issue volume")
            operational_risks["evidence"].append(f"{len(critical_feedback)} critical customer issues")
        elif len(critical_feedback) > 5:
            risk_factors.append(0.6)
            operational_risks["risk_indicators"].append("Elevated critical issues")
            operational_risks["evidence"].append(f"{len(critical_feedback)} critical customer issues")
        
        # Calculate overall operational risk score
        if risk_factors:
            operational_risks["risk_score"] = max(risk_factors)
        else:
            operational_risks["risk_score"] = 0.2  # Low baseline risk
        
        return operational_risks
    
    def _assess_reputation_risks(self, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess brand reputation and public perception risks."""
        
        reputation_risks = {
            "risk_score": 0.0,
            "description": "Brand reputation and public perception risks",
            "risk_indicators": [],
            "evidence": []
        }
        
        risk_factors = []
        
        # Sentiment-based reputation risk
        avg_sentiment = feedback_data.get("average_sentiment_score", 0)
        sentiment_distribution = feedback_data.get("sentiment_distribution", {})
        total_feedback = feedback_data.get("total_count", 0)
        
        if total_feedback > 0:
            negative_percentage = (sentiment_distribution.get("negative", 0) / total_feedback) * 100
            
            if avg_sentiment < -0.4 or negative_percentage > 70:
                risk_factors.append(0.9)
                reputation_risks["risk_indicators"].append("Critical reputation damage")
                reputation_risks["evidence"].append(f"Sentiment: {avg_sentiment:.3f}, {negative_percentage:.0f}% negative")
            elif avg_sentiment < -0.2 or negative_percentage > 50:
                risk_factors.append(0.7)
                reputation_risks["risk_indicators"].append("Reputation concerns")
                reputation_risks["evidence"].append(f"Sentiment: {avg_sentiment:.3f}, {negative_percentage:.0f}% negative")
            elif avg_sentiment < -0.1 or negative_percentage > 35:
                risk_factors.append(0.4)
                reputation_risks["risk_indicators"].append("Mixed reputation signals")
                reputation_risks["evidence"].append(f"Sentiment: {avg_sentiment:.3f}, {negative_percentage:.0f}% negative")
        
        # Social media and viral risk
        feedback_items = feedback_data.get("feedback_items", [])
        social_media_feedback = [item for item in feedback_items if item.get("source") == "social_media"]
        
        if social_media_feedback:
            negative_social = [item for item in social_media_feedback if item.get("sentiment") == "negative"]
            if len(negative_social) > len(social_media_feedback) * 0.6:  # 60% negative social media
                risk_factors.append(0.6)
                reputation_risks["risk_indicators"].append("Negative social media sentiment")
                reputation_risks["evidence"].append(f"{len(negative_social)}/{len(social_media_feedback)} negative social media posts")
        
        # Calculate overall reputation risk score
        if risk_factors:
            reputation_risks["risk_score"] = max(risk_factors)
        else:
            reputation_risks["risk_score"] = 0.3  # Moderate baseline risk
        
        return reputation_risks
    
    def _assess_strategic_risks(self, metrics_data: Dict[str, Any], feedback_data: Dict[str, Any],
                              release_notes: str) -> Dict[str, Any]:
        """Assess strategic and long-term competitive risks."""
        
        strategic_risks = {
            "risk_score": 0.0,
            "description": "Strategic positioning and long-term competitive risks",
            "risk_indicators": [],
            "evidence": []
        }
        
        risk_factors = []
        
        # Feature adoption vs strategic goals
        metrics = metrics_data.get("metrics", {})
        if "feature_adoption_rate" in metrics:
            adoption_data = metrics["feature_adoption_rate"]["data_points"]
            if adoption_data:
                current_adoption = adoption_data[-1]["value"]
                target_adoption = metrics["feature_adoption_rate"].get("target", 25.0)
                
                # Strategic risk if adoption is very low
                if current_adoption < target_adoption * 0.3:  # Less than 30% of target
                    risk_factors.append(0.7)
                    strategic_risks["risk_indicators"].append("Strategic feature failing to gain traction")
                    strategic_risks["evidence"].append(f"Adoption: {current_adoption:.1f}% vs target {target_adoption:.1f}%")
        
        # Market positioning risk from customer feedback
        feedback_items = feedback_data.get("feedback_items", [])
        competitive_mentions = []
        
        for item in feedback_items:
            content = item.get("content", "").lower()
            if any(word in content for word in ["competitor", "alternative", "switch", "better option"]):
                competitive_mentions.append(item)
        
        if len(competitive_mentions) > len(feedback_items) * 0.1:  # 10% mention competitors
            risk_factors.append(0.5)
            strategic_risks["risk_indicators"].append("Competitive pressure in feedback")
            strategic_risks["evidence"].append(f"{len(competitive_mentions)} competitive mentions")
        
        # Long-term user experience risk
        avg_sentiment = feedback_data.get("average_sentiment_score", 0)
        if avg_sentiment < -0.2:
            risk_factors.append(0.6)
            strategic_risks["risk_indicators"].append("Long-term user experience degradation")
            strategic_risks["evidence"].append(f"Sustained negative sentiment: {avg_sentiment:.3f}")
        
        # Calculate overall strategic risk score
        if risk_factors:
            strategic_risks["risk_score"] = max(risk_factors)
        else:
            strategic_risks["risk_score"] = 0.2  # Low baseline risk
        
        return strategic_risks
    
    def _assess_cascading_risks(self, risk_by_category: Dict[str, Any]) -> float:
        """Assess potential for cascading risks across categories."""
        
        # High risks in multiple categories increase cascading potential
        high_risk_categories = [
            category for category, assessment in risk_by_category.items()
            if assessment["risk_score"] > 0.6
        ]
        
        if len(high_risk_categories) >= 3:
            return 0.8  # High cascading risk
        elif len(high_risk_categories) >= 2:
            return 0.6  # Moderate cascading risk
        elif len(high_risk_categories) >= 1:
            return 0.3  # Low cascading risk
        else:
            return 0.1  # Minimal cascading risk
    
    def _challenge_assumptions_and_biases(self, metrics_data: Dict[str, Any],
                                        feedback_data: Dict[str, Any],
                                        risk_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Challenge common assumptions and identify potential cognitive biases."""
        
        bias_analysis = {
            "identified_biases": [],
            "challenged_assumptions": [],
            "alternative_interpretations": [],
            "evidence_gaps": [],
            "recommendation_adjustments": []
        }
        
        # Challenge optimism bias
        overall_risk = risk_assessment["overall_risk_score"]
        if overall_risk < 0.4 and len(risk_assessment["critical_risks"]) > 0:
            bias_analysis["identified_biases"].append({
                "bias": "optimism_bias",
                "description": "Overall risk score may be too optimistic given critical risks present",
                "evidence": f"Overall risk {overall_risk:.2f} but {len(risk_assessment['critical_risks'])} critical risks"
            })
        
        # Challenge confirmation bias in metrics interpretation
        metrics = metrics_data.get("metrics", {})
        positive_metrics = []
        negative_metrics = []
        
        for metric_name, metric_data in metrics.items():
            data_points = metric_data.get("data_points", [])
            if data_points:
                current_value = data_points[-1]["value"]
                baseline = metric_data.get("baseline")
                
                if baseline:
                    if self._is_metric_improving(metric_name, current_value, baseline):
                        positive_metrics.append(metric_name)
                    else:
                        negative_metrics.append(metric_name)
        
        if len(positive_metrics) > 0 and len(negative_metrics) > 0:
            bias_analysis["challenged_assumptions"].append({
                "assumption": "Overall performance is clearly positive/negative",
                "challenge": f"Mixed signals: {len(positive_metrics)} improving, {len(negative_metrics)} declining metrics",
                "alternative": "Performance is mixed and requires nuanced interpretation"
            })
        
        # Challenge availability heuristic (recent events bias)
        feedback_items = feedback_data.get("feedback_items", [])
        if feedback_items:
            recent_feedback = sorted(feedback_items, key=lambda x: x.get("timestamp", ""), reverse=True)[:10]
            recent_negative = sum(1 for item in recent_feedback if item.get("sentiment") == "negative")
            
            total_negative = sum(1 for item in feedback_items if item.get("sentiment") == "negative")
            total_feedback = len(feedback_items)
            
            recent_negative_pct = (recent_negative / len(recent_feedback)) * 100
            overall_negative_pct = (total_negative / total_feedback) * 100
            
            if abs(recent_negative_pct - overall_negative_pct) > 20:
                bias_analysis["identified_biases"].append({
                    "bias": "availability_heuristic",
                    "description": "Recent feedback may not represent overall sentiment",
                    "evidence": f"Recent: {recent_negative_pct:.0f}% negative vs overall: {overall_negative_pct:.0f}%"
                })
        
        # Challenge sunk cost fallacy
        if "feature_adoption_rate" in metrics:
            adoption_data = metrics["feature_adoption_rate"]["data_points"]
            if adoption_data:
                current_adoption = adoption_data[-1]["value"]
                if current_adoption < 15.0:  # Low adoption
                    bias_analysis["challenged_assumptions"].append({
                        "assumption": "Investment in feature justifies continuing despite low adoption",
                        "challenge": f"Current adoption rate {current_adoption:.1f}% is below expectations",
                        "alternative": "Consider pivoting or significant changes rather than continuing current path"
                    })
        
        # Identify evidence gaps
        if not feedback_items:
            bias_analysis["evidence_gaps"].append("No customer feedback data available")
        elif len(feedback_items) < 20:
            bias_analysis["evidence_gaps"].append("Limited customer feedback sample size")
        
        data_quality_issues = []
        for metric_name, metric_data in metrics.items():
            data_points = metric_data.get("data_points", [])
            if len(data_points) < 168:  # Less than 1 week of hourly data
                data_quality_issues.append(metric_name)
        
        if data_quality_issues:
            bias_analysis["evidence_gaps"].append(f"Insufficient data for metrics: {', '.join(data_quality_issues)}")
        
        print(f"Bias analysis: {len(bias_analysis['identified_biases'])} biases, "
              f"{len(bias_analysis['evidence_gaps'])} evidence gaps")
        
        return bias_analysis
    
    def _is_metric_improving(self, metric_name: str, current_value: float, baseline: float) -> bool:
        """Determine if a metric is improving based on its type."""
        
        # For error rates, latency, tickets - lower is better
        if any(term in metric_name.lower() for term in ["error", "latency", "ticket"]):
            return current_value < baseline
        
        # For conversion, retention, adoption, DAU - higher is better
        else:
            return current_value > baseline
    
    def _identify_hidden_risks(self, metrics_data: Dict[str, Any], 
                             feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """Identify potential hidden risks and blind spots."""
        
        hidden_risks = {
            "data_blind_spots": [],
            "temporal_risks": [],
            "correlation_risks": [],
            "external_risks": [],
            "systemic_risks": []
        }
        
        # Identify data blind spots
        metrics = metrics_data.get("metrics", {})
        
        # Missing critical metrics
        expected_metrics = ["error_rate", "api_latency_p95", "daily_active_users", "d1_retention"]
        missing_metrics = [metric for metric in expected_metrics if metric not in metrics]
        
        if missing_metrics:
            hidden_risks["data_blind_spots"].append({
                "risk": "Missing critical metrics",
                "description": f"No data available for: {', '.join(missing_metrics)}",
                "impact": "Cannot assess full system health"
            })
        
        # Temporal risks (weekend/holiday effects, seasonal patterns)
        hidden_risks["temporal_risks"].append({
            "risk": "Weekend/holiday effects not considered",
            "description": "Analysis may not account for usage pattern variations",
            "impact": "Metrics may be skewed by temporal factors"
        })
        
        # Correlation risks (metrics moving in unexpected directions)
        if "daily_active_users" in metrics and "activation_conversion" in metrics:
            dau_data = metrics["daily_active_users"]["data_points"]
            conversion_data = metrics["activation_conversion"]["data_points"]
            
            if dau_data and conversion_data:
                dau_current = dau_data[-1]["value"]
                dau_baseline = metrics["daily_active_users"].get("baseline", dau_current)
                conversion_current = conversion_data[-1]["value"]
                conversion_baseline = metrics["activation_conversion"].get("baseline", conversion_current)
                
                dau_improving = dau_current > dau_baseline
                conversion_improving = conversion_current > conversion_baseline
                
                if dau_improving and not conversion_improving:
                    hidden_risks["correlation_risks"].append({
                        "risk": "DAU growth without conversion improvement",
                        "description": "More users but lower conversion efficiency",
                        "impact": "Potential quality vs quantity trade-off"
                    })
        
        # External risks
        hidden_risks["external_risks"].extend([
            {
                "risk": "Competitive response not assessed",
                "description": "Competitor reactions to feature launch unknown",
                "impact": "Market dynamics may shift unexpectedly"
            },
            {
                "risk": "Regulatory/compliance implications",
                "description": "Potential regulatory scrutiny of AI recommendations",
                "impact": "Legal or compliance issues may emerge"
            }
        ])
        
        # Systemic risks
        if len([r for r in self.analysis_results.get("risk_assessment", {}).get("critical_risks", [])]) > 1:
            hidden_risks["systemic_risks"].append({
                "risk": "Multiple system failures",
                "description": "Multiple critical risks may indicate systemic issues",
                "impact": "Root cause may be deeper than individual metrics suggest"
            })
        
        print(f"Hidden risks identified: {sum(len(risks) for risks in hidden_risks.values())} total risks")
        
        return hidden_risks
    
    def _run_stress_test_scenarios(self, risk_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Run stress test scenarios to evaluate decision robustness."""
        
        stress_tests = {
            "scenario_results": [],
            "decision_robustness": 0.0,
            "worst_case_impact": "",
            "stress_test_recommendations": []
        }
        
        # Scenario 1: Error rate doubles
        stress_tests["scenario_results"].append({
            "scenario": "Error rate doubles overnight",
            "probability": 0.15,
            "impact": "Critical system instability",
            "recommended_action": "Immediate rollback preparation",
            "mitigation": "Enhanced monitoring and automated rollback triggers"
        })
        
        # Scenario 2: Viral negative feedback
        stress_tests["scenario_results"].append({
            "scenario": "Negative feedback goes viral on social media",
            "probability": 0.1,
            "impact": "Severe brand reputation damage",
            "recommended_action": "Crisis communication plan activation",
            "mitigation": "Proactive customer communication and rapid issue resolution"
        })
        
        # Scenario 3: Support team overwhelmed
        stress_tests["scenario_results"].append({
            "scenario": "Support ticket volume triples",
            "probability": 0.2,
            "impact": "Operational breakdown and customer dissatisfaction",
            "recommended_action": "Scale support capacity or pause rollout",
            "mitigation": "Support team augmentation and self-service resources"
        })
        
        # Scenario 4: Competitive response
        stress_tests["scenario_results"].append({
            "scenario": "Competitor launches superior feature",
            "probability": 0.25,
            "impact": "Market position erosion",
            "recommended_action": "Accelerate feature improvements",
            "mitigation": "Continuous competitive monitoring and rapid iteration"
        })
        
        # Calculate decision robustness
        high_impact_scenarios = [s for s in stress_tests["scenario_results"] if s["probability"] > 0.15]
        stress_tests["decision_robustness"] = 1.0 - (len(high_impact_scenarios) * 0.2)
        
        # Determine worst case
        worst_case = max(stress_tests["scenario_results"], key=lambda x: x["probability"])
        stress_tests["worst_case_impact"] = worst_case["impact"]
        
        # Generate stress test recommendations
        if stress_tests["decision_robustness"] < 0.6:
            stress_tests["stress_test_recommendations"].append("High stress test failure rate suggests conservative approach")
        
        if len(high_impact_scenarios) > 2:
            stress_tests["stress_test_recommendations"].append("Multiple high-probability negative scenarios require mitigation planning")
        
        print(f"Stress tests: {stress_tests['decision_robustness']:.2f} robustness score")
        
        return stress_tests
    
    def _assess_evidence_quality(self, metrics_data: Dict[str, Any], 
                               feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess the quality and reliability of available evidence."""
        
        evidence_assessment = {
            "overall_quality_score": 0.0,
            "data_completeness": {},
            "data_reliability": {},
            "sample_size_adequacy": {},
            "bias_indicators": [],
            "confidence_adjustments": []
        }
        
        quality_factors = []
        
        # Assess metrics data quality
        metrics = metrics_data.get("metrics", {})
        if metrics:
            total_expected_points = 14 * 24  # 14 days hourly
            completeness_scores = []
            
            for metric_name, metric_data in metrics.items():
                data_points = metric_data.get("data_points", [])
                completeness = len(data_points) / total_expected_points
                completeness_scores.append(completeness)
                
                evidence_assessment["data_completeness"][metric_name] = {
                    "completeness_ratio": completeness,
                    "data_points": len(data_points),
                    "expected_points": total_expected_points
                }
            
            avg_completeness = sum(completeness_scores) / len(completeness_scores)
            quality_factors.append(avg_completeness)
        
        # Assess feedback data quality
        feedback_items = feedback_data.get("feedback_items", [])
        feedback_quality = 0.5  # Default
        
        if feedback_items:
            # Sample size adequacy
            if len(feedback_items) >= 50:
                feedback_quality = 0.9
            elif len(feedback_items) >= 30:
                feedback_quality = 0.7
            elif len(feedback_items) >= 20:
                feedback_quality = 0.6
            else:
                feedback_quality = 0.4
                evidence_assessment["confidence_adjustments"].append("Small feedback sample size reduces confidence")
            
            # Source diversity
            sources = set(item.get("source") for item in feedback_items)
            if len(sources) >= 3:
                feedback_quality += 0.1
            
            evidence_assessment["sample_size_adequacy"]["feedback"] = {
                "sample_size": len(feedback_items),
                "adequacy_score": feedback_quality,
                "source_diversity": len(sources)
            }
        
        quality_factors.append(feedback_quality)
        
        # Check for bias indicators
        if feedback_items:
            # Recency bias check
            recent_items = [item for item in feedback_items 
                          if (datetime.now() - datetime.fromisoformat(item.get("timestamp", datetime.now().isoformat()))).days < 2]
            
            if len(recent_items) > len(feedback_items) * 0.7:
                evidence_assessment["bias_indicators"].append("Potential recency bias in feedback data")
        
        # Calculate overall quality score
        evidence_assessment["overall_quality_score"] = sum(quality_factors) / len(quality_factors) if quality_factors else 0.5
        
        if evidence_assessment["overall_quality_score"] < 0.6:
            evidence_assessment["confidence_adjustments"].append("Below-average data quality reduces decision confidence")
        
        print(f"Evidence quality: {evidence_assessment['overall_quality_score']:.2f} overall score")
        
        return evidence_assessment
    
    def _analyze_long_term_impacts(self, metrics_data: Dict[str, Any], 
                                 feedback_data: Dict[str, Any],
                                 risk_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze potential long-term strategic and operational impacts."""
        
        long_term_analysis = {
            "strategic_implications": [],
            "operational_implications": [],
            "competitive_implications": [],
            "customer_relationship_impact": "",
            "technical_debt_risks": [],
            "market_position_trajectory": ""
        }
        
        # Strategic implications
        overall_risk = risk_assessment["overall_risk_score"]
        
        if overall_risk > 0.7:
            long_term_analysis["strategic_implications"].extend([
                "High risk launch may damage long-term product credibility",
                "Potential negative impact on future feature adoption rates",
                "May require significant resources for remediation"
            ])
        elif overall_risk > 0.5:
            long_term_analysis["strategic_implications"].append(
                "Moderate risks may slow future innovation velocity"
            )
        
        # Customer relationship impact
        avg_sentiment = feedback_data.get("average_sentiment_score", 0)
        
        if avg_sentiment < -0.3:
            long_term_analysis["customer_relationship_impact"] = "Severe long-term customer trust erosion"
        elif avg_sentiment < -0.1:
            long_term_analysis["customer_relationship_impact"] = "Moderate customer relationship strain"
        elif avg_sentiment > 0.2:
            long_term_analysis["customer_relationship_impact"] = "Positive long-term customer relationship building"
        else:
            long_term_analysis["customer_relationship_impact"] = "Neutral long-term customer impact"
        
        # Technical debt risks
        metrics = metrics_data.get("metrics", {})
        if "error_rate" in metrics:
            error_data = metrics["error_rate"]["data_points"]
            if error_data and error_data[-1]["value"] > 1.5:
                long_term_analysis["technical_debt_risks"].append(
                    "High error rates may indicate architectural issues requiring future refactoring"
                )
        
        # Competitive implications
        if "feature_adoption_rate" in metrics:
            adoption_data = metrics["feature_adoption_rate"]["data_points"]
            if adoption_data:
                current_adoption = adoption_data[-1]["value"]
                if current_adoption < 15.0:
                    long_term_analysis["competitive_implications"].append(
                        "Low adoption may signal competitive disadvantage in AI/ML capabilities"
                    )
                elif current_adoption > 25.0:
                    long_term_analysis["competitive_implications"].append(
                        "Strong adoption may establish competitive moat in personalization"
                    )
        
        # Market position trajectory
        if overall_risk < 0.3 and avg_sentiment > 0.1:
            long_term_analysis["market_position_trajectory"] = "Strengthening market position"
        elif overall_risk > 0.6 or avg_sentiment < -0.2:
            long_term_analysis["market_position_trajectory"] = "Weakening market position"
        else:
            long_term_analysis["market_position_trajectory"] = "Stable market position"
        
        print(f"Long-term analysis: {long_term_analysis['market_position_trajectory']}")
        
        return long_term_analysis
    
    def _develop_mitigation_strategies(self, risk_assessment: Dict[str, Any], 
                                     hidden_risks: Dict[str, Any]) -> Dict[str, Any]:
        """Develop comprehensive risk mitigation strategies."""
        
        mitigation_strategies = {
            "immediate_mitigations": [],
            "short_term_mitigations": [],
            "long_term_mitigations": [],
            "contingency_plans": [],
            "monitoring_enhancements": []
        }
        
        # Address critical risks
        critical_risks = risk_assessment.get("critical_risks", [])
        
        for risk in critical_risks:
            if risk["category"] == "technical":
                mitigation_strategies["immediate_mitigations"].append({
                    "risk": risk["description"],
                    "mitigation": "Implement automated rollback triggers for error rate thresholds",
                    "timeline": "Within 4 hours",
                    "owner": "Engineering"
                })
            elif risk["category"] == "business":
                mitigation_strategies["immediate_mitigations"].append({
                    "risk": risk["description"],
                    "mitigation": "Activate customer retention campaigns for at-risk segments",
                    "timeline": "Within 24 hours",
                    "owner": "Product/Marketing"
                })
        
        # Address hidden risks
        for risk_category, risks in hidden_risks.items():
            for risk in risks:
                if risk_category == "data_blind_spots":
                    mitigation_strategies["short_term_mitigations"].append({
                        "risk": risk["risk"],
                        "mitigation": "Implement additional monitoring and data collection",
                        "timeline": "Within 1 week",
                        "owner": "Data Engineering"
                    })
        
        # Contingency plans
        mitigation_strategies["contingency_plans"].extend([
            {
                "trigger": "Error rate > 3% for 1 hour",
                "action": "Automatic rollback to previous version",
                "owner": "DevOps"
            },
            {
                "trigger": "Support tickets > 300/day",
                "action": "Scale support team and pause new user onboarding",
                "owner": "Operations"
            },
            {
                "trigger": "Negative sentiment > 70%",
                "action": "Activate crisis communication protocol",
                "owner": "Marketing/Communications"
            }
        ])
        
        # Enhanced monitoring
        mitigation_strategies["monitoring_enhancements"].extend([
            "Real-time sentiment monitoring with hourly updates",
            "Automated anomaly detection with 15-minute alerts",
            "Customer cohort analysis for early churn detection",
            "Competitive monitoring for market response tracking"
        ])
        
        print(f"Mitigation strategies: {len(mitigation_strategies['immediate_mitigations'])} immediate, "
              f"{len(mitigation_strategies['contingency_plans'])} contingency plans")
        
        return mitigation_strategies
    
    def _generate_risk_findings(self, risk_assessment: Dict[str, Any], 
                              bias_analysis: Dict[str, Any],
                              hidden_risks: Dict[str, Any],
                              evidence_assessment: Dict[str, Any]) -> List[str]:
        """Generate key risk findings and concerns."""
        
        findings = []
        
        # Overall risk assessment
        overall_risk = risk_assessment["overall_risk_score"]
        critical_count = len(risk_assessment["critical_risks"])
        
        if overall_risk > 0.7:
            findings.append(f"Critical: Overall risk score {overall_risk:.2f} indicates high probability of negative outcomes")
        elif overall_risk > 0.5:
            findings.append(f"Concerning: Elevated risk score {overall_risk:.2f} requires careful monitoring")
        else:
            findings.append(f"Manageable: Risk score {overall_risk:.2f} within acceptable bounds")
        
        # Critical risks
        if critical_count > 0:
            findings.append(f"Alert: {critical_count} critical risks identified requiring immediate attention")
        
        # Bias concerns
        bias_count = len(bias_analysis.get("identified_biases", []))
        if bias_count > 0:
            findings.append(f"Cognitive bias alert: {bias_count} potential biases identified in analysis")
        
        # Evidence quality concerns
        evidence_quality = evidence_assessment.get("overall_quality_score", 0.5)
        if evidence_quality < 0.6:
            findings.append(f"Data quality concern: Evidence quality score {evidence_quality:.2f} reduces confidence")
        
        # Hidden risks
        total_hidden_risks = sum(len(risks) for risks in hidden_risks.values())
        if total_hidden_risks > 5:
            findings.append(f"Blind spot alert: {total_hidden_risks} potential hidden risks identified")
        
        # Cascading risk potential
        cascading_risk = risk_assessment.get("cascading_risk_potential", 0)
        if cascading_risk > 0.6:
            findings.append(f"Cascading risk warning: {cascading_risk:.2f} probability of multiple system failures")
        
        return findings
    
    def get_recommendation(self) -> AgentRecommendation:
        """Generate Risk/Critic recommendation based on comprehensive risk analysis."""
        
        if not self.analysis_results:
            return AgentRecommendation(
                agent_name=self.agent_name,
                recommendation=DecisionType.PAUSE,
                confidence=0.4,
                rationale="Insufficient data for comprehensive risk analysis",
                key_findings=["No risk analysis performed"],
                concerns=["Missing risk assessment data"]
            )
        
        # Extract key analysis results
        risk_assessment = self.analysis_results["risk_assessment"]
        bias_analysis = self.analysis_results["bias_analysis"]
        hidden_risks = self.analysis_results["hidden_risks"]
        evidence_assessment = self.analysis_results["evidence_assessment"]
        stress_test_results = self.analysis_results["stress_test_results"]
        key_findings = self.analysis_results["key_findings"]
        
        concerns = []
        
        # Extract key risk metrics
        overall_risk_score = risk_assessment["overall_risk_score"]
        critical_risks_count = len(risk_assessment["critical_risks"])
        high_risks_count = len(risk_assessment["high_risks"])
        cascading_risk = risk_assessment.get("cascading_risk_potential", 0)
        evidence_quality = evidence_assessment.get("overall_quality_score", 0.5)
        decision_robustness = stress_test_results.get("decision_robustness", 0.5)
        
        # Risk-based decision logic (Risk agent tends to be more conservative)
        
        # Critical conditions requiring rollback
        if (overall_risk_score > 0.8 or critical_risks_count > 2 or 
            cascading_risk > 0.7):
            decision = DecisionType.ROLL_BACK
            confidence = 0.95
            rationale = f"Unacceptable risk profile: {overall_risk_score:.2f} overall risk, {critical_risks_count} critical risks"
            concerns.extend([
                f"Overall risk score: {overall_risk_score:.2f}",
                f"Critical risks: {critical_risks_count}",
                f"Cascading risk potential: {cascading_risk:.2f}"
            ])
        
        # High risk conditions requiring pause
        elif (overall_risk_score > 0.6 or critical_risks_count > 0 or 
              decision_robustness < 0.4):
            decision = DecisionType.PAUSE
            confidence = 0.85
            rationale = f"Significant risks require pause: {overall_risk_score:.2f} risk score, {critical_risks_count} critical risks"
            concerns.extend([
                f"Elevated risk score: {overall_risk_score:.2f}",
                f"Decision robustness: {decision_robustness:.2f}",
                f"High risks: {high_risks_count}"
            ])
        
        # Moderate risks but can proceed with extensive monitoring
        elif (overall_risk_score > 0.4 or high_risks_count > 2 or 
              evidence_quality < 0.6):
            decision = DecisionType.PROCEED
            confidence = 0.6
            rationale = f"Moderate risks allow cautious proceed with enhanced risk monitoring"
            concerns.extend([
                "Moderate risk levels require enhanced monitoring",
                "Evidence quality concerns",
                f"Multiple high-risk factors: {high_risks_count}"
            ])
        
        # Lower risk allows proceeding
        elif overall_risk_score <= 0.4 and critical_risks_count == 0:
            decision = DecisionType.PROCEED
            confidence = 0.75
            rationale = f"Acceptable risk profile supports proceed: {overall_risk_score:.2f} risk score"
            if high_risks_count > 0:
                concerns.append(f"{high_risks_count} high risks require monitoring")
        
        else:
            decision = DecisionType.PAUSE
            confidence = 0.7
            rationale = "Mixed risk signals suggest pause for further analysis"
            concerns.append("Unclear risk profile requires additional analysis")
        
        # Adjust confidence based on evidence quality and bias indicators
        bias_count = len(bias_analysis.get("identified_biases", []))
        if bias_count > 2:
            confidence *= 0.9
            concerns.append(f"Multiple cognitive biases detected: {bias_count}")
        
        if evidence_quality < 0.5:
            confidence *= 0.8
            concerns.append("Poor evidence quality reduces confidence")
        
        # Add specific risk concerns
        for risk in risk_assessment["critical_risks"]:
            concerns.append(f"Critical {risk['category']} risk: {risk['description']}")
        
        # Add hidden risk concerns
        total_hidden_risks = sum(len(risks) for risks in hidden_risks.values())
        if total_hidden_risks > 3:
            concerns.append(f"{total_hidden_risks} potential blind spots identified")
        
        recommendation = AgentRecommendation(
            agent_name=self.agent_name,
            recommendation=decision,
            confidence=confidence,
            rationale=rationale,
            key_findings=key_findings,
            concerns=concerns if concerns else None
        )
        
        print(f"Risk Agent Recommendation: {decision.value} (confidence: {confidence:.2f})")
        print(f"Rationale: {rationale}")
        
        return recommendation