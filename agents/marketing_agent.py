"""Marketing/Communications agent for the War Room system."""

from typing import Dict, List, Any
from datetime import datetime

from .base_agent import BaseAgent
from models.decision import AgentRecommendation, DecisionType
from tools.sentiment_analyzer import SentimentAnalyzer


class MarketingAgent(BaseAgent):
    """Marketing/Communications agent that assesses messaging, customer perception, and communication actions."""
    
    def __init__(self):
        super().__init__("Marketing/Communications", "Assesses messaging, customer perception, and communication actions")
        self.sentiment_analyzer = SentimentAnalyzer()
        self.add_tool(self.sentiment_analyzer)
        
        # Define communication thresholds and guidelines
        self.communication_thresholds = {
            "negative_sentiment_critical": 0.6,  # 60% negative feedback
            "negative_sentiment_high": 0.4,     # 40% negative feedback
            "critical_issues_threshold": 5,      # Number of critical feedback items
            "sentiment_score_critical": -0.4,   # Average sentiment score
            "sentiment_score_warning": -0.2     # Average sentiment score
        }
        
        # Communication templates and strategies
        self.communication_strategies = {
            "crisis": {
                "internal": "Immediate escalation to leadership, cross-functional war room",
                "external": "Proactive customer communication, transparent issue acknowledgment"
            },
            "concern": {
                "internal": "Stakeholder notification, increased monitoring",
                "external": "Targeted customer outreach, support team briefing"
            },
            "positive": {
                "internal": "Success metrics sharing, team recognition",
                "external": "Success story amplification, customer testimonials"
            }
        }
        
        print(f"Initialized Marketing Agent with communication thresholds: {self.communication_thresholds}")
    
    def analyze(self, metrics_data: Dict[str, Any], feedback_data: Dict[str, Any], 
                release_notes: str) -> Dict[str, Any]:
        """Analyze customer sentiment, perception, and communication needs."""
        
        self.log_analysis_step("Starting Marketing/Communications analysis")
        
        # Comprehensive sentiment analysis
        self.log_analysis_step("Performing sentiment analysis with SentimentAnalyzer tool")
        sentiment_insights = self.sentiment_analyzer.get_sentiment_insights(feedback_data)
        
        # Brand perception analysis
        self.log_analysis_step("Analyzing brand perception and customer impact")
        brand_perception = self._analyze_brand_perception(feedback_data, sentiment_insights)
        
        # Communication risk assessment
        self.log_analysis_step("Assessing communication risks and opportunities")
        communication_risks = self._assess_communication_risks(sentiment_insights, metrics_data)
        
        # Customer segment analysis
        self.log_analysis_step("Analyzing customer segment feedback patterns")
        segment_analysis = self._analyze_customer_segments(feedback_data)
        
        # Competitive impact assessment
        competitive_impact = self._assess_competitive_impact(sentiment_insights, metrics_data)
        
        # Communication strategy recommendations
        self.log_analysis_step("Developing communication strategy recommendations")
        communication_strategy = self._develop_communication_strategy(
            sentiment_insights, brand_perception, communication_risks
        )
        
        # Media and social monitoring insights
        media_insights = self._analyze_media_sentiment(feedback_data)
        
        self.analysis_results = {
            "sentiment_insights": sentiment_insights,
            "brand_perception": brand_perception,
            "communication_risks": communication_risks,
            "segment_analysis": segment_analysis,
            "competitive_impact": competitive_impact,
            "communication_strategy": communication_strategy,
            "media_insights": media_insights,
            "key_findings": self._generate_marketing_findings(
                sentiment_insights, brand_perception, communication_risks
            )
        }
        
        self.log_analysis_step("Marketing/Communications analysis complete", 
                             f"Overall sentiment: {sentiment_insights['overall_sentiment']['score']:.3f}")
        
        return self.analysis_results
    
    def _analyze_brand_perception(self, feedback_data: Dict[str, Any], 
                                sentiment_insights: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze impact on brand perception and customer trust."""
        
        brand_perception = {
            "overall_impact": "neutral",
            "trust_indicators": {},
            "reputation_risks": [],
            "positive_brand_signals": [],
            "customer_advocacy_potential": 0.5,
            "brand_health_score": 0.5
        }
        
        # Analyze overall sentiment impact on brand
        overall_sentiment = sentiment_insights["overall_sentiment"]
        negative_insights = sentiment_insights["negative_insights"]
        positive_insights = sentiment_insights["positive_insights"]
        
        sentiment_score = overall_sentiment["score"]
        negative_percentage = overall_sentiment["distribution"]["negative"]
        positive_percentage = overall_sentiment["distribution"]["positive"]
        
        # Determine overall brand impact
        if sentiment_score < -0.3 or negative_percentage > 60:
            brand_perception["overall_impact"] = "very_negative"
            brand_perception["brand_health_score"] = 0.2
        elif sentiment_score < -0.1 or negative_percentage > 40:
            brand_perception["overall_impact"] = "negative"
            brand_perception["brand_health_score"] = 0.4
        elif sentiment_score > 0.2 and positive_percentage > 50:
            brand_perception["overall_impact"] = "positive"
            brand_perception["brand_health_score"] = 0.8
        else:
            brand_perception["overall_impact"] = "neutral"
            brand_perception["brand_health_score"] = 0.6
        
        # Analyze trust indicators
        feedback_items = feedback_data.get("feedback_items", [])
        trust_keywords = {
            "positive": ["trust", "reliable", "dependable", "consistent", "quality"],
            "negative": ["broken", "unreliable", "disappointing", "frustrated", "angry"]
        }
        
        trust_positive = 0
        trust_negative = 0
        
        for item in feedback_items:
            content = item.get("content", "").lower()
            for keyword in trust_keywords["positive"]:
                if keyword in content:
                    trust_positive += 1
                    break
            for keyword in trust_keywords["negative"]:
                if keyword in content:
                    trust_negative += 1
                    break
        
        total_trust_mentions = trust_positive + trust_negative
        if total_trust_mentions > 0:
            trust_ratio = trust_positive / total_trust_mentions
            brand_perception["trust_indicators"] = {
                "positive_mentions": trust_positive,
                "negative_mentions": trust_negative,
                "trust_ratio": trust_ratio
            }
        
        # Identify reputation risks
        critical_feedback = sentiment_insights.get("critical_issues", {}).get("items", [])
        negative_themes = negative_insights.get("themes", [])
        
        for theme in negative_themes:
            if theme in ["bugs", "performance", "frustration"]:
                brand_perception["reputation_risks"].append({
                    "risk": f"Widespread {theme} complaints",
                    "severity": "high" if negative_percentage > 50 else "medium",
                    "theme": theme
                })
        
        if len(critical_feedback) > 3:
            brand_perception["reputation_risks"].append({
                "risk": f"{len(critical_feedback)} critical customer issues",
                "severity": "high",
                "theme": "critical_issues"
            })
        
        # Identify positive brand signals
        positive_themes = positive_insights.get("top_themes", [])
        for theme in positive_themes:
            if theme in ["accuracy", "personalization", "satisfaction"]:
                brand_perception["positive_brand_signals"].append({
                    "signal": f"Strong {theme} feedback",
                    "theme": theme,
                    "impact": "positive"
                })
        
        # Calculate customer advocacy potential
        if positive_percentage > 60 and sentiment_score > 0.3:
            brand_perception["customer_advocacy_potential"] = 0.8
        elif positive_percentage > 40 and sentiment_score > 0.1:
            brand_perception["customer_advocacy_potential"] = 0.6
        elif negative_percentage > 50:
            brand_perception["customer_advocacy_potential"] = 0.2
        else:
            brand_perception["customer_advocacy_potential"] = 0.4
        
        print(f"Brand perception: {brand_perception['overall_impact']}, "
              f"health score: {brand_perception['brand_health_score']:.2f}")
        
        return brand_perception
    
    def _assess_communication_risks(self, sentiment_insights: Dict[str, Any], 
                                  metrics_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess communication risks and crisis potential."""
        
        communication_risks = {
            "overall_risk_level": "medium",
            "crisis_indicators": [],
            "escalation_triggers": [],
            "communication_urgency": "normal",
            "stakeholder_impact": {},
            "media_attention_risk": "low"
        }
        
        # Analyze crisis indicators
        overall_sentiment = sentiment_insights["overall_sentiment"]
        negative_insights = sentiment_insights["negative_insights"]
        critical_issues = sentiment_insights.get("critical_issues", {})
        
        sentiment_score = overall_sentiment["score"]
        negative_percentage = overall_sentiment["distribution"]["negative"]
        critical_count = critical_issues.get("count", 0)
        
        # Check for crisis indicators
        if sentiment_score < self.communication_thresholds["sentiment_score_critical"]:
            communication_risks["crisis_indicators"].append("Critical sentiment score")
            communication_risks["overall_risk_level"] = "critical"
            communication_risks["communication_urgency"] = "immediate"
        
        if negative_percentage > self.communication_thresholds["negative_sentiment_critical"] * 100:
            communication_risks["crisis_indicators"].append("Majority negative feedback")
            communication_risks["overall_risk_level"] = "critical"
            communication_risks["communication_urgency"] = "immediate"
        
        if critical_count > self.communication_thresholds["critical_issues_threshold"]:
            communication_risks["crisis_indicators"].append(f"{critical_count} critical customer issues")
            if communication_risks["overall_risk_level"] != "critical":
                communication_risks["overall_risk_level"] = "high"
                communication_risks["communication_urgency"] = "urgent"
        
        # Check escalation triggers
        if negative_percentage > self.communication_thresholds["negative_sentiment_high"] * 100:
            communication_risks["escalation_triggers"].append("High negative sentiment")
        
        if sentiment_score < self.communication_thresholds["sentiment_score_warning"]:
            communication_risks["escalation_triggers"].append("Low sentiment score")
        
        # Assess stakeholder impact
        metrics = metrics_data.get("metrics", {})
        
        # Check support ticket volume impact
        if "support_ticket_volume" in metrics:
            ticket_data = metrics["support_ticket_volume"]["data_points"]
            if ticket_data:
                current_tickets = ticket_data[-1]["value"]
                baseline_tickets = metrics["support_ticket_volume"].get("baseline", current_tickets)
                
                if current_tickets > baseline_tickets * 1.5:
                    communication_risks["stakeholder_impact"]["support_team"] = "high_burden"
                    communication_risks["escalation_triggers"].append("Support ticket surge")
        
        # Check error rate impact on engineering
        if "error_rate" in metrics:
            error_data = metrics["error_rate"]["data_points"]
            if error_data:
                current_error_rate = error_data[-1]["value"]
                if current_error_rate > 2.0:  # 2% error rate
                    communication_risks["stakeholder_impact"]["engineering"] = "critical_issues"
        
        # Assess media attention risk
        negative_themes = negative_insights.get("themes", [])
        if "bugs" in negative_themes and negative_percentage > 50:
            communication_risks["media_attention_risk"] = "high"
        elif critical_count > 3:
            communication_risks["media_attention_risk"] = "medium"
        
        print(f"Communication risks: {communication_risks['overall_risk_level']} level, "
              f"{communication_risks['communication_urgency']} urgency")
        
        return communication_risks
    
    def _analyze_customer_segments(self, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze feedback patterns across customer segments."""
        
        segment_analysis = {
            "by_source": {},
            "by_category": {},
            "segment_specific_issues": [],
            "cross_segment_patterns": []
        }
        
        feedback_items = feedback_data.get("feedback_items", [])
        
        # Analyze by feedback source
        source_sentiment = {}
        for item in feedback_items:
            source = item.get("source", "unknown")
            sentiment = item.get("sentiment", "neutral")
            
            if source not in source_sentiment:
                source_sentiment[source] = {"positive": 0, "negative": 0, "neutral": 0, "total": 0}
            
            source_sentiment[source][sentiment] += 1
            source_sentiment[source]["total"] += 1
        
        for source, counts in source_sentiment.items():
            if counts["total"] > 0:
                segment_analysis["by_source"][source] = {
                    "total_feedback": counts["total"],
                    "negative_percentage": (counts["negative"] / counts["total"]) * 100,
                    "positive_percentage": (counts["positive"] / counts["total"]) * 100,
                    "sentiment_balance": "negative" if counts["negative"] > counts["positive"] else "positive"
                }
        
        # Analyze by feedback category
        category_sentiment = {}
        for item in feedback_items:
            category = item.get("category", "unknown")
            sentiment = item.get("sentiment", "neutral")
            
            if category not in category_sentiment:
                category_sentiment[category] = {"positive": 0, "negative": 0, "neutral": 0, "total": 0}
            
            category_sentiment[category][sentiment] += 1
            category_sentiment[category]["total"] += 1
        
        for category, counts in category_sentiment.items():
            if counts["total"] > 0:
                segment_analysis["by_category"][category] = {
                    "total_feedback": counts["total"],
                    "negative_percentage": (counts["negative"] / counts["total"]) * 100,
                    "positive_percentage": (counts["positive"] / counts["total"]) * 100,
                    "dominant_sentiment": max(counts, key=lambda k: counts[k] if k != "total" else 0)
                }
        
        # Identify segment-specific issues
        for source, data in segment_analysis["by_source"].items():
            if data["negative_percentage"] > 60:
                segment_analysis["segment_specific_issues"].append({
                    "segment": source,
                    "issue": f"High negative sentiment in {source}",
                    "severity": "high"
                })
        
        # Identify cross-segment patterns
        if len([s for s in segment_analysis["by_source"].values() if s["negative_percentage"] > 40]) > 2:
            segment_analysis["cross_segment_patterns"].append("Widespread negative sentiment across multiple channels")
        
        print(f"Segment analysis: {len(segment_analysis['by_source'])} sources, "
              f"{len(segment_analysis['segment_specific_issues'])} specific issues")
        
        return segment_analysis
    
    def _assess_competitive_impact(self, sentiment_insights: Dict[str, Any], 
                                 metrics_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess potential competitive impact and market positioning."""
        
        competitive_impact = {
            "market_position_risk": "medium",
            "competitive_advantage_impact": "neutral",
            "customer_churn_risk": "medium",
            "acquisition_impact": "neutral",
            "differentiation_factors": []
        }
        
        # Analyze sentiment impact on competitive position
        overall_sentiment = sentiment_insights["overall_sentiment"]
        sentiment_score = overall_sentiment["score"]
        negative_percentage = overall_sentiment["distribution"]["negative"]
        
        # Assess market position risk
        if sentiment_score < -0.3 or negative_percentage > 60:
            competitive_impact["market_position_risk"] = "high"
            competitive_impact["customer_churn_risk"] = "high"
        elif sentiment_score < -0.1 or negative_percentage > 40:
            competitive_impact["market_position_risk"] = "medium"
            competitive_impact["customer_churn_risk"] = "medium"
        else:
            competitive_impact["market_position_risk"] = "low"
            competitive_impact["customer_churn_risk"] = "low"
        
        # Analyze retention metrics impact
        metrics = metrics_data.get("metrics", {})
        if "d1_retention" in metrics:
            retention_data = metrics["d1_retention"]["data_points"]
            if retention_data:
                current_retention = retention_data[-1]["value"]
                baseline_retention = metrics["d1_retention"].get("baseline", current_retention)
                
                if current_retention < baseline_retention * 0.9:  # 10% drop
                    competitive_impact["customer_churn_risk"] = "high"
                    competitive_impact["competitive_advantage_impact"] = "negative"
        
        # Assess acquisition impact
        if "activation_conversion" in metrics:
            conversion_data = metrics["activation_conversion"]["data_points"]
            if conversion_data:
                current_conversion = conversion_data[-1]["value"]
                baseline_conversion = metrics["activation_conversion"].get("baseline", current_conversion)
                
                if current_conversion < baseline_conversion * 0.9:  # 10% drop
                    competitive_impact["acquisition_impact"] = "negative"
                elif current_conversion > baseline_conversion * 1.1:  # 10% improvement
                    competitive_impact["acquisition_impact"] = "positive"
        
        # Identify differentiation factors from positive feedback
        positive_themes = sentiment_insights.get("positive_insights", {}).get("top_themes", [])
        for theme in positive_themes:
            if theme in ["personalization", "accuracy", "discovery"]:
                competitive_impact["differentiation_factors"].append({
                    "factor": theme,
                    "strength": "high" if theme == "personalization" else "medium"
                })
        
        print(f"Competitive impact: {competitive_impact['market_position_risk']} position risk, "
              f"{competitive_impact['customer_churn_risk']} churn risk")
        
        return competitive_impact
    
    def _develop_communication_strategy(self, sentiment_insights: Dict[str, Any],
                                      brand_perception: Dict[str, Any],
                                      communication_risks: Dict[str, Any]) -> Dict[str, Any]:
        """Develop comprehensive communication strategy recommendations."""
        
        strategy = {
            "immediate_actions": [],
            "short_term_strategy": [],
            "long_term_strategy": [],
            "internal_communications": {},
            "external_communications": {},
            "crisis_response_plan": {},
            "success_amplification": []
        }
        
        risk_level = communication_risks["overall_risk_level"]
        brand_impact = brand_perception["overall_impact"]
        urgency = communication_risks["communication_urgency"]
        
        # Determine strategy based on risk level and brand impact
        if risk_level == "critical" or brand_impact == "very_negative":
            strategy_type = "crisis"
        elif risk_level == "high" or brand_impact == "negative":
            strategy_type = "concern"
        else:
            strategy_type = "positive"
        
        base_strategy = self.communication_strategies[strategy_type]
        
        # Immediate actions
        if urgency == "immediate":
            strategy["immediate_actions"].extend([
                "Activate crisis communication protocol",
                "Brief executive leadership within 2 hours",
                "Prepare holding statements for customer inquiries",
                "Alert customer support team of potential volume increase"
            ])
        elif urgency == "urgent":
            strategy["immediate_actions"].extend([
                "Schedule stakeholder briefing within 24 hours",
                "Prepare customer communication draft",
                "Increase social media monitoring"
            ])
        
        # Internal communications
        strategy["internal_communications"] = {
            "leadership": base_strategy["internal"],
            "engineering": "Provide technical context and resolution timeline",
            "support": "Brief on common issues and response guidelines",
            "sales": "Provide talking points for customer conversations"
        }
        
        # External communications
        strategy["external_communications"] = {
            "customers": base_strategy["external"],
            "channels": self._determine_communication_channels(sentiment_insights),
            "messaging": self._craft_key_messages(sentiment_insights, brand_perception),
            "timeline": self._create_communication_timeline(urgency)
        }
        
        # Crisis response plan
        if strategy_type == "crisis":
            strategy["crisis_response_plan"] = {
                "escalation_path": ["Customer Success Manager", "VP Customer Experience", "CMO", "CEO"],
                "response_timeline": "2-4 hours for initial response",
                "communication_frequency": "Every 4-6 hours until resolved",
                "channels": ["Email", "In-app notification", "Social media", "Website banner"]
            }
        
        # Success amplification (if applicable)
        positive_themes = sentiment_insights.get("positive_insights", {}).get("top_themes", [])
        if positive_themes and brand_impact in ["positive", "neutral"]:
            strategy["success_amplification"] = [
                f"Highlight {theme} success in customer communications" for theme in positive_themes[:3]
            ]
        
        print(f"Communication strategy: {strategy_type} approach, {urgency} urgency")
        
        return strategy
    
    def _determine_communication_channels(self, sentiment_insights: Dict[str, Any]) -> List[str]:
        """Determine appropriate communication channels based on feedback sources."""
        
        channels = ["email"]  # Default channel
        
        # Analyze feedback sources to determine where customers are most active
        category_breakdown = sentiment_insights.get("category_breakdown", {})
        
        if "social_media" in category_breakdown:
            channels.append("social_media")
        
        if "in_app_feedback" in category_breakdown:
            channels.append("in_app_notification")
        
        if "support_ticket" in category_breakdown:
            channels.append("support_portal")
        
        return channels
    
    def _craft_key_messages(self, sentiment_insights: Dict[str, Any],
                           brand_perception: Dict[str, Any]) -> Dict[str, str]:
        """Craft key messages based on sentiment analysis."""
        
        messages = {}
        
        negative_themes = sentiment_insights.get("negative_insights", {}).get("themes", [])
        positive_themes = sentiment_insights.get("positive_insights", {}).get("top_themes", [])
        
        # Address top negative themes
        if "bugs" in negative_themes:
            messages["bug_acknowledgment"] = "We acknowledge the technical issues some users have experienced and are working urgently to resolve them."
        
        if "performance" in negative_themes:
            messages["performance_improvement"] = "We are actively optimizing system performance to ensure a smooth user experience."
        
        # Amplify positive themes
        if "personalization" in positive_themes:
            messages["personalization_success"] = "We're pleased that many users are finding value in our personalized recommendations."
        
        # General reassurance message
        brand_impact = brand_perception["overall_impact"]
        if brand_impact in ["negative", "very_negative"]:
            messages["commitment"] = "Your feedback is invaluable to us, and we remain committed to delivering the quality experience you expect."
        
        return messages
    
    def _create_communication_timeline(self, urgency: str) -> Dict[str, str]:
        """Create communication timeline based on urgency."""
        
        if urgency == "immediate":
            return {
                "initial_response": "Within 2 hours",
                "detailed_update": "Within 6 hours",
                "resolution_update": "Within 24 hours",
                "follow_up": "48-72 hours post-resolution"
            }
        elif urgency == "urgent":
            return {
                "initial_response": "Within 24 hours",
                "detailed_update": "Within 48 hours",
                "resolution_update": "Within 1 week",
                "follow_up": "1-2 weeks post-resolution"
            }
        else:
            return {
                "initial_response": "Within 1 week",
                "detailed_update": "As needed",
                "resolution_update": "As needed",
                "follow_up": "Monthly review"
            }
    
    def _analyze_media_sentiment(self, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze media and social sentiment indicators."""
        
        media_insights = {
            "social_media_sentiment": "neutral",
            "viral_risk": "low",
            "influencer_mentions": 0,
            "trending_topics": [],
            "media_attention_indicators": []
        }
        
        feedback_items = feedback_data.get("feedback_items", [])
        social_media_items = [item for item in feedback_items if item.get("source") == "social_media"]
        
        if social_media_items:
            negative_social = sum(1 for item in social_media_items if item.get("sentiment") == "negative")
            total_social = len(social_media_items)
            
            negative_percentage = (negative_social / total_social) * 100
            
            if negative_percentage > 70:
                media_insights["social_media_sentiment"] = "very_negative"
                media_insights["viral_risk"] = "high"
            elif negative_percentage > 50:
                media_insights["social_media_sentiment"] = "negative"
                media_insights["viral_risk"] = "medium"
            elif negative_percentage < 30:
                media_insights["social_media_sentiment"] = "positive"
        
        # Check for viral risk indicators
        if len(social_media_items) > 10 and media_insights["social_media_sentiment"] in ["negative", "very_negative"]:
            media_insights["media_attention_indicators"].append("High volume negative social media feedback")
        
        print(f"Media insights: {media_insights['social_media_sentiment']} sentiment, "
              f"{media_insights['viral_risk']} viral risk")
        
        return media_insights
    
    def _generate_marketing_findings(self, sentiment_insights: Dict[str, Any],
                                   brand_perception: Dict[str, Any],
                                   communication_risks: Dict[str, Any]) -> List[str]:
        """Generate key marketing and communications findings."""
        
        findings = []
        
        # Sentiment findings
        overall_sentiment = sentiment_insights["overall_sentiment"]
        sentiment_score = overall_sentiment["score"]
        negative_percentage = overall_sentiment["distribution"]["negative"]
        
        if sentiment_score < -0.3:
            findings.append(f"Critical: Very negative customer sentiment ({sentiment_score:.3f})")
        elif sentiment_score < -0.1:
            findings.append(f"Concerning: Negative customer sentiment ({sentiment_score:.3f})")
        elif sentiment_score > 0.2:
            findings.append(f"Positive: Strong customer sentiment ({sentiment_score:.3f})")
        
        # Brand perception findings
        brand_impact = brand_perception["overall_impact"]
        if brand_impact in ["negative", "very_negative"]:
            findings.append(f"Brand risk: {brand_impact} impact on brand perception")
        elif brand_impact == "positive":
            findings.append("Opportunity: Positive brand impact detected")
        
        # Communication risk findings
        risk_level = communication_risks["overall_risk_level"]
        urgency = communication_risks["communication_urgency"]
        
        if risk_level == "critical":
            findings.append(f"Crisis alert: {risk_level} communication risk requires immediate action")
        elif risk_level == "high":
            findings.append(f"Escalation needed: {risk_level} communication risk")
        
        # Customer segment findings
        negative_themes = sentiment_insights.get("negative_insights", {}).get("themes", [])
        if "bugs" in negative_themes and negative_percentage > 40:
            findings.append("Customer experience: Widespread technical issues reported")
        
        # Positive opportunities
        positive_themes = sentiment_insights.get("positive_insights", {}).get("top_themes", [])
        if "personalization" in positive_themes:
            findings.append("Success story: Personalization resonating well with customers")
        
        return findings
    
    def get_recommendation(self) -> AgentRecommendation:
        """Generate Marketing/Communications recommendation based on sentiment and brand analysis."""
        
        if not self.analysis_results:
            return AgentRecommendation(
                agent_name=self.agent_name,
                recommendation=DecisionType.PAUSE,
                confidence=0.3,
                rationale="Insufficient sentiment data for marketing analysis",
                key_findings=["No analysis performed"],
                concerns=["Missing sentiment analysis"]
            )
        
        # Extract key analysis results
        sentiment_insights = self.analysis_results["sentiment_insights"]
        brand_perception = self.analysis_results["brand_perception"]
        communication_risks = self.analysis_results["communication_risks"]
        competitive_impact = self.analysis_results["competitive_impact"]
        key_findings = self.analysis_results["key_findings"]
        
        concerns = []
        
        # Extract key metrics
        sentiment_score = sentiment_insights["overall_sentiment"]["score"]
        negative_percentage = sentiment_insights["overall_sentiment"]["distribution"]["negative"]
        brand_impact = brand_perception["overall_impact"]
        risk_level = communication_risks["overall_risk_level"]
        critical_issues_count = sentiment_insights.get("critical_issues", {}).get("count", 0)
        
        # Decision logic based on marketing and communications analysis
        
        # Critical conditions requiring rollback
        if (sentiment_score < -0.4 or negative_percentage > 70 or 
            brand_impact == "very_negative" or risk_level == "critical"):
            decision = DecisionType.ROLL_BACK
            confidence = 0.9
            rationale = f"Critical brand/communication risk: {sentiment_score:.3f} sentiment, {negative_percentage:.0f}% negative feedback"
            concerns.extend([
                f"Sentiment score: {sentiment_score:.3f}",
                f"Negative feedback: {negative_percentage:.0f}%",
                f"Brand impact: {brand_impact}",
                f"Communication risk: {risk_level}"
            ])
        
        # High risk conditions requiring pause
        elif (sentiment_score < -0.2 or negative_percentage > 50 or 
              brand_impact == "negative" or critical_issues_count > 5):
            decision = DecisionType.PAUSE
            confidence = 0.8
            rationale = f"Significant customer sentiment concerns require pause: {negative_percentage:.0f}% negative feedback"
            concerns.extend([
                f"High negative sentiment: {negative_percentage:.0f}%",
                f"Brand perception impact: {brand_impact}",
                f"Critical customer issues: {critical_issues_count}"
            ])
        
        # Moderate concerns but can proceed with caution
        elif (sentiment_score < -0.1 or negative_percentage > 35 or 
              competitive_impact["customer_churn_risk"] == "high"):
            decision = DecisionType.PROCEED
            confidence = 0.6
            rationale = f"Mixed customer sentiment allows cautious proceed with enhanced monitoring"
            concerns.extend([
                "Mixed customer sentiment",
                "Requires enhanced communication strategy"
            ])
        
        # Positive indicators support proceeding
        elif (sentiment_score > 0.2 and negative_percentage < 30 and 
              brand_impact in ["positive", "neutral"]):
            decision = DecisionType.PROCEED
            confidence = 0.85
            rationale = f"Positive customer sentiment supports continued rollout: {sentiment_score:.3f} score"
        
        else:
            decision = DecisionType.PROCEED
            confidence = 0.7
            rationale = f"Balanced customer sentiment allows proceed: {sentiment_score:.3f} score, {negative_percentage:.0f}% negative"
            concerns.append("Monitor customer sentiment closely")
        
        # Adjust confidence based on data completeness
        feedback_count = sentiment_insights.get("overall_sentiment", {}).get("distribution", {})
        total_feedback = sum(feedback_count.values()) if feedback_count else 0
        
        if total_feedback < 20:
            confidence *= 0.8  # Reduce confidence for limited feedback
            concerns.append("Limited feedback sample size")
        
        recommendation = AgentRecommendation(
            agent_name=self.agent_name,
            recommendation=decision,
            confidence=confidence,
            rationale=rationale,
            key_findings=key_findings,
            concerns=concerns if concerns else None
        )
        
        print(f"Marketing Recommendation: {decision.value} (confidence: {confidence:.2f})")
        print(f"Rationale: {rationale}")
        
        return recommendation