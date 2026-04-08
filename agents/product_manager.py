"""Product Manager agent for the War Room system."""

from typing import Dict, List, Any
from datetime import datetime

from .base_agent import BaseAgent
from models.decision import AgentRecommendation, DecisionType
from tools.metric_analyzer import MetricAnalyzer


class ProductManagerAgent(BaseAgent):
    """Product Manager agent that evaluates success criteria and makes go/no-go decisions."""
    
    def __init__(self):
        super().__init__("Product Manager", "Defines success criteria and go/no-go decisions")
        self.metric_analyzer = MetricAnalyzer()
        self.add_tool(self.metric_analyzer)
        
        # Define success criteria thresholds
        self.success_criteria = {
            "feature_adoption_rate": {"target": 25.0, "minimum": 15.0},
            "user_engagement": {"target": 10.0, "minimum": 5.0},  # % increase
            "conversion_improvement": {"target": 5.0, "minimum": 2.0},  # % increase
            "error_rate": {"maximum": 2.0, "critical": 3.0},
            "user_satisfaction": {"minimum": 0.2, "target": 0.4}  # sentiment score
        }
        
        print(f"Initialized PM with success criteria: {self.success_criteria}")
    
    def analyze(self, metrics_data: Dict[str, Any], feedback_data: Dict[str, Any], 
                release_notes: str) -> Dict[str, Any]:
        """Analyze metrics against success criteria and business objectives."""
        
        self.log_analysis_step("Starting Product Manager analysis")
        
        # Analyze metrics using the metric analyzer tool
        self.log_analysis_step("Analyzing metrics against success criteria")
        metric_insights = self.metric_analyzer.get_metric_insights(metrics_data)
        
        # Evaluate each success criterion
        success_evaluation = self._evaluate_success_criteria(metrics_data, feedback_data)
        
        # Assess feature adoption and user impact
        adoption_analysis = self._analyze_feature_adoption(metrics_data)
        
        # Evaluate business impact
        business_impact = self._assess_business_impact(metrics_data, feedback_data)
        
        # Calculate overall product health score
        product_health_score = self._calculate_product_health_score(
            success_evaluation, adoption_analysis, business_impact
        )
        
        self.analysis_results = {
            "metric_insights": metric_insights,
            "success_evaluation": success_evaluation,
            "adoption_analysis": adoption_analysis,
            "business_impact": business_impact,
            "product_health_score": product_health_score,
            "key_findings": self._generate_key_findings(
                success_evaluation, adoption_analysis, business_impact
            )
        }
        
        self.log_analysis_step("Product Manager analysis complete", 
                             f"Health score: {product_health_score:.2f}")
        
        return self.analysis_results
    
    def _evaluate_success_criteria(self, metrics_data: Dict[str, Any], 
                                 feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate performance against defined success criteria."""
        
        evaluation = {
            "criteria_met": 0,
            "total_criteria": len(self.success_criteria),
            "detailed_evaluation": {},
            "critical_failures": []
        }
        
        metrics = metrics_data.get("metrics", {})
        
        # Feature adoption rate
        if "feature_adoption_rate" in metrics:
            adoption_metric = metrics["feature_adoption_rate"]
            current_adoption = adoption_metric["data_points"][-1]["value"] if adoption_metric["data_points"] else 0
            
            criteria = self.success_criteria["feature_adoption_rate"]
            if current_adoption >= criteria["target"]:
                status = "exceeds_target"
                evaluation["criteria_met"] += 1
            elif current_adoption >= criteria["minimum"]:
                status = "meets_minimum"
                evaluation["criteria_met"] += 0.5
            else:
                status = "below_minimum"
                evaluation["critical_failures"].append("Feature adoption below minimum threshold")
            
            evaluation["detailed_evaluation"]["feature_adoption"] = {
                "current_value": current_adoption,
                "target": criteria["target"],
                "minimum": criteria["minimum"],
                "status": status
            }
            
            print(f"Feature adoption: {current_adoption:.1f}% (target: {criteria['target']}%, status: {status})")
        
        # Error rate evaluation
        if "error_rate" in metrics:
            error_metric = metrics["error_rate"]
            current_error_rate = error_metric["data_points"][-1]["value"] if error_metric["data_points"] else 0
            
            criteria = self.success_criteria["error_rate"]
            if current_error_rate >= criteria["critical"]:
                status = "critical_failure"
                evaluation["critical_failures"].append(f"Error rate {current_error_rate:.2f}% exceeds critical threshold")
            elif current_error_rate <= criteria["maximum"]:
                status = "acceptable"
                evaluation["criteria_met"] += 1
            else:
                status = "elevated"
            
            evaluation["detailed_evaluation"]["error_rate"] = {
                "current_value": current_error_rate,
                "maximum": criteria["maximum"],
                "critical": criteria["critical"],
                "status": status
            }
            
            print(f"Error rate: {current_error_rate:.2f}% (max: {criteria['maximum']}%, status: {status})")
        
        # User satisfaction (from feedback sentiment)
        avg_sentiment = feedback_data.get("average_sentiment_score", 0)
        criteria = self.success_criteria["user_satisfaction"]
        
        if avg_sentiment >= criteria["target"]:
            status = "exceeds_target"
            evaluation["criteria_met"] += 1
        elif avg_sentiment >= criteria["minimum"]:
            status = "meets_minimum"
            evaluation["criteria_met"] += 0.5
        else:
            status = "below_minimum"
            evaluation["critical_failures"].append("User satisfaction below minimum threshold")
        
        evaluation["detailed_evaluation"]["user_satisfaction"] = {
            "current_value": avg_sentiment,
            "target": criteria["target"],
            "minimum": criteria["minimum"],
            "status": status
        }
        
        print(f"User satisfaction: {avg_sentiment:.3f} (target: {criteria['target']}, status: {status})")
        
        return evaluation
    
    def _analyze_feature_adoption(self, metrics_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze feature adoption patterns and trends."""
        
        metrics = metrics_data.get("metrics", {})
        adoption_analysis = {
            "current_adoption_rate": 0,
            "adoption_trend": "unknown",
            "adoption_velocity": 0,  # Rate of adoption increase
            "user_engagement": "unknown",
            "conversion_impact": "unknown"
        }
        
        # Analyze feature adoption rate
        if "feature_adoption_rate" in metrics:
            adoption_metric = metrics["feature_adoption_rate"]
            data_points = adoption_metric["data_points"]
            
            if len(data_points) >= 2:
                current_rate = data_points[-1]["value"]
                initial_rate = data_points[0]["value"]
                
                adoption_analysis["current_adoption_rate"] = current_rate
                adoption_analysis["adoption_velocity"] = (current_rate - initial_rate) / len(data_points)
                
                if current_rate > initial_rate * 1.1:
                    adoption_analysis["adoption_trend"] = "increasing"
                elif current_rate < initial_rate * 0.9:
                    adoption_analysis["adoption_trend"] = "decreasing"
                else:
                    adoption_analysis["adoption_trend"] = "stable"
                
                print(f"Adoption trend: {adoption_analysis['adoption_trend']}, "
                      f"velocity: {adoption_analysis['adoption_velocity']:.2f}%/hour")
        
        # Analyze user engagement (DAU trend)
        if "daily_active_users" in metrics:
            dau_metric = metrics["daily_active_users"]
            data_points = dau_metric["data_points"]
            
            if len(data_points) >= 2:
                current_dau = data_points[-1]["value"]
                baseline_dau = dau_metric.get("baseline", current_dau)
                
                if baseline_dau > 0:
                    engagement_change = ((current_dau - baseline_dau) / baseline_dau) * 100
                    
                    if engagement_change > 5:
                        adoption_analysis["user_engagement"] = "strong_positive"
                    elif engagement_change > 0:
                        adoption_analysis["user_engagement"] = "positive"
                    elif engagement_change > -5:
                        adoption_analysis["user_engagement"] = "stable"
                    else:
                        adoption_analysis["user_engagement"] = "declining"
                    
                    print(f"User engagement change: {engagement_change:+.1f}%")
        
        # Analyze conversion impact
        if "activation_conversion" in metrics:
            conversion_metric = metrics["activation_conversion"]
            data_points = conversion_metric["data_points"]
            
            if len(data_points) >= 2:
                current_conversion = data_points[-1]["value"]
                baseline_conversion = conversion_metric.get("baseline", current_conversion)
                
                if baseline_conversion > 0:
                    conversion_change = ((current_conversion - baseline_conversion) / baseline_conversion) * 100
                    
                    if conversion_change > 2:
                        adoption_analysis["conversion_impact"] = "positive"
                    elif conversion_change > -2:
                        adoption_analysis["conversion_impact"] = "neutral"
                    else:
                        adoption_analysis["conversion_impact"] = "negative"
                    
                    print(f"Conversion impact: {conversion_change:+.1f}%")
        
        return adoption_analysis
    
    def _assess_business_impact(self, metrics_data: Dict[str, Any], 
                              feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess overall business impact of the feature launch."""
        
        impact_assessment = {
            "revenue_impact": "unknown",
            "user_experience_impact": "unknown",
            "operational_impact": "unknown",
            "risk_level": "medium",
            "strategic_alignment": "aligned"
        }
        
        # Assess revenue impact (based on conversion and payment success)
        metrics = metrics_data.get("metrics", {})
        
        if "payment_success_rate" in metrics:
            payment_metric = metrics["payment_success_rate"]
            current_rate = payment_metric["data_points"][-1]["value"] if payment_metric["data_points"] else 0
            baseline_rate = payment_metric.get("baseline", current_rate)
            
            if current_rate < baseline_rate * 0.95:  # 5% drop
                impact_assessment["revenue_impact"] = "negative"
                impact_assessment["risk_level"] = "high"
            elif current_rate > baseline_rate * 1.02:  # 2% improvement
                impact_assessment["revenue_impact"] = "positive"
            else:
                impact_assessment["revenue_impact"] = "neutral"
            
            print(f"Payment success rate impact: {impact_assessment['revenue_impact']}")
        
        # Assess user experience impact (based on sentiment and retention)
        avg_sentiment = feedback_data.get("average_sentiment_score", 0)
        negative_feedback_pct = feedback_data.get("sentiment_distribution", {}).get("negative", 0)
        total_feedback = feedback_data.get("total_count", 1)
        
        negative_pct = (negative_feedback_pct / total_feedback) * 100 if total_feedback > 0 else 0
        
        if avg_sentiment < -0.3 or negative_pct > 60:
            impact_assessment["user_experience_impact"] = "very_negative"
            impact_assessment["risk_level"] = "critical"
        elif avg_sentiment < -0.1 or negative_pct > 40:
            impact_assessment["user_experience_impact"] = "negative"
            impact_assessment["risk_level"] = "high"
        elif avg_sentiment > 0.2 and negative_pct < 30:
            impact_assessment["user_experience_impact"] = "positive"
        else:
            impact_assessment["user_experience_impact"] = "mixed"
        
        print(f"User experience impact: {impact_assessment['user_experience_impact']} "
              f"(sentiment: {avg_sentiment:.3f}, negative: {negative_pct:.1f}%)")
        
        # Assess operational impact (based on support tickets and error rates)
        if "support_ticket_volume" in metrics:
            ticket_metric = metrics["support_ticket_volume"]
            current_volume = ticket_metric["data_points"][-1]["value"] if ticket_metric["data_points"] else 0
            baseline_volume = ticket_metric.get("baseline", current_volume)
            
            if current_volume > baseline_volume * 1.5:  # 50% increase
                impact_assessment["operational_impact"] = "high_burden"
                if impact_assessment["risk_level"] == "medium":
                    impact_assessment["risk_level"] = "high"
            elif current_volume > baseline_volume * 1.2:  # 20% increase
                impact_assessment["operational_impact"] = "increased_burden"
            else:
                impact_assessment["operational_impact"] = "manageable"
            
            print(f"Operational impact: {impact_assessment['operational_impact']}")
        
        return impact_assessment
    
    def _calculate_product_health_score(self, success_evaluation: Dict[str, Any],
                                      adoption_analysis: Dict[str, Any],
                                      business_impact: Dict[str, Any]) -> float:
        """Calculate overall product health score (0-1)."""
        
        score_factors = {}
        
        # Success criteria score (40% weight)
        criteria_score = success_evaluation["criteria_met"] / success_evaluation["total_criteria"]
        score_factors["success_criteria"] = criteria_score * 0.4
        
        # Adoption score (25% weight)
        adoption_rate = adoption_analysis.get("current_adoption_rate", 0)
        target_adoption = self.success_criteria["feature_adoption_rate"]["target"]
        adoption_score = min(1.0, adoption_rate / target_adoption) if target_adoption > 0 else 0.5
        score_factors["adoption"] = adoption_score * 0.25
        
        # Business impact score (35% weight)
        impact_score = 0.5  # Default neutral
        
        if business_impact["user_experience_impact"] == "very_negative":
            impact_score = 0.0
        elif business_impact["user_experience_impact"] == "negative":
            impact_score = 0.2
        elif business_impact["user_experience_impact"] == "positive":
            impact_score = 0.8
        elif business_impact["user_experience_impact"] == "mixed":
            impact_score = 0.4
        
        # Adjust for critical failures
        if success_evaluation["critical_failures"]:
            impact_score *= 0.3  # Severe penalty for critical failures
        
        score_factors["business_impact"] = impact_score * 0.35
        
        total_score = sum(score_factors.values())
        
        print(f"Product health score components: {score_factors}")
        print(f"Total product health score: {total_score:.3f}")
        
        return total_score
    
    def _generate_key_findings(self, success_evaluation: Dict[str, Any],
                             adoption_analysis: Dict[str, Any],
                             business_impact: Dict[str, Any]) -> List[str]:
        """Generate key findings from the analysis."""
        
        findings = []
        
        # Success criteria findings
        criteria_met = success_evaluation["criteria_met"]
        total_criteria = success_evaluation["total_criteria"]
        
        if criteria_met >= total_criteria * 0.8:
            findings.append(f"Strong performance: {criteria_met}/{total_criteria} success criteria met")
        elif criteria_met >= total_criteria * 0.5:
            findings.append(f"Mixed performance: {criteria_met}/{total_criteria} success criteria met")
        else:
            findings.append(f"Poor performance: Only {criteria_met}/{total_criteria} success criteria met")
        
        # Critical failures
        if success_evaluation["critical_failures"]:
            findings.append(f"Critical issues identified: {', '.join(success_evaluation['critical_failures'])}")
        
        # Adoption findings
        adoption_rate = adoption_analysis.get("current_adoption_rate", 0)
        target_rate = self.success_criteria["feature_adoption_rate"]["target"]
        
        if adoption_rate >= target_rate:
            findings.append(f"Feature adoption exceeds target: {adoption_rate:.1f}% vs {target_rate}% target")
        elif adoption_rate >= target_rate * 0.6:
            findings.append(f"Feature adoption progressing: {adoption_rate:.1f}% of {target_rate}% target")
        else:
            findings.append(f"Feature adoption below expectations: {adoption_rate:.1f}% vs {target_rate}% target")
        
        # Business impact findings
        if business_impact["user_experience_impact"] in ["negative", "very_negative"]:
            findings.append("Negative user experience impact detected")
        elif business_impact["user_experience_impact"] == "positive":
            findings.append("Positive user experience impact observed")
        
        if business_impact["risk_level"] in ["high", "critical"]:
            findings.append(f"Elevated risk level: {business_impact['risk_level']}")
        
        return findings
    
    def get_recommendation(self) -> AgentRecommendation:
        """Generate Product Manager recommendation based on analysis."""
        
        if not self.analysis_results:
            return AgentRecommendation(
                agent_name=self.agent_name,
                recommendation=DecisionType.PAUSE,
                confidence=0.3,
                rationale="Insufficient analysis data available",
                key_findings=["No analysis performed"],
                concerns=["Missing analysis data"]
            )
        
        # Extract key metrics for decision making
        success_evaluation = self.analysis_results["success_evaluation"]
        business_impact = self.analysis_results["business_impact"]
        product_health_score = self.analysis_results["product_health_score"]
        key_findings = self.analysis_results["key_findings"]
        
        # Decision logic
        concerns = []
        
        # Check for critical failures
        if success_evaluation["critical_failures"]:
            decision = DecisionType.ROLL_BACK
            confidence = 0.9
            rationale = "Critical success criteria failures require immediate rollback"
            concerns.extend(success_evaluation["critical_failures"])
        
        # Check business impact
        elif business_impact["user_experience_impact"] == "very_negative":
            decision = DecisionType.ROLL_BACK
            confidence = 0.85
            rationale = "Severe negative user experience impact requires rollback"
            concerns.append("Very negative user experience impact")
        
        elif business_impact["risk_level"] == "critical":
            decision = DecisionType.PAUSE
            confidence = 0.8
            rationale = "Critical risk level requires pause for investigation"
            concerns.append("Critical risk level identified")
        
        # Check product health score
        elif product_health_score < 0.3:
            decision = DecisionType.ROLL_BACK
            confidence = 0.75
            rationale = f"Low product health score ({product_health_score:.2f}) indicates rollback needed"
            concerns.append("Poor overall product health")
        
        elif product_health_score < 0.5:
            decision = DecisionType.PAUSE
            confidence = 0.7
            rationale = f"Moderate product health score ({product_health_score:.2f}) suggests pause for improvements"
            concerns.append("Below-average product health")
        
        # Positive indicators
        elif product_health_score > 0.7 and not success_evaluation["critical_failures"]:
            decision = DecisionType.PROCEED
            confidence = 0.8
            rationale = f"Strong product health score ({product_health_score:.2f}) supports continued rollout"
        
        else:
            decision = DecisionType.PROCEED
            confidence = 0.6
            rationale = f"Acceptable product health score ({product_health_score:.2f}) allows cautious proceed"
            concerns.append("Mixed performance indicators")
        
        # Adjust confidence based on data quality
        data_quality = self._assess_data_quality(
            self.analysis_results.get("metric_insights", {}), 
            {}
        )
        confidence *= (0.7 + 0.3 * data_quality)  # Reduce confidence if data quality is poor
        
        recommendation = AgentRecommendation(
            agent_name=self.agent_name,
            recommendation=decision,
            confidence=confidence,
            rationale=rationale,
            key_findings=key_findings,
            concerns=concerns if concerns else None
        )
        
        print(f"PM Recommendation: {decision.value} (confidence: {confidence:.2f})")
        print(f"Rationale: {rationale}")
        
        return recommendation