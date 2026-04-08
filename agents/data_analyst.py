"""Data Analyst agent for the War Room system."""

from typing import Dict, List, Any
from datetime import datetime

from .base_agent import BaseAgent
from models.decision import AgentRecommendation, DecisionType
from tools.metric_analyzer import MetricAnalyzer
from tools.anomaly_detector import AnomalyDetector


class DataAnalystAgent(BaseAgent):
    """Data Analyst agent that analyzes quantitative metrics, trends, and anomalies."""
    
    def __init__(self):
        super().__init__("Data Analyst", "Analyzes quantitative metrics, trends, and anomalies")
        self.metric_analyzer = MetricAnalyzer()
        self.anomaly_detector = AnomalyDetector(sensitivity=2.0)
        self.add_tool(self.metric_analyzer)
        self.add_tool(self.anomaly_detector)
        
        # Define critical thresholds for key metrics
        self.critical_thresholds = {
            "error_rate": 2.0,  # %
            "api_latency_p95": 400,  # ms
            "support_ticket_volume": 200,  # tickets/day
            "activation_conversion": 10.0,  # %
            "d1_retention": 60.0,  # %
            "payment_success_rate": 95.0  # %
        }
        
        print(f"Initialized Data Analyst with critical thresholds: {self.critical_thresholds}")
    
    def analyze(self, metrics_data: Dict[str, Any], feedback_data: Dict[str, Any], 
                release_notes: str) -> Dict[str, Any]:
        """Perform comprehensive data analysis on metrics and trends."""
        
        self.log_analysis_step("Starting Data Analyst comprehensive analysis")
        
        # Comprehensive metric analysis
        self.log_analysis_step("Performing metric analysis with MetricAnalyzer tool")
        metric_insights = self.metric_analyzer.get_metric_insights(metrics_data)
        
        # Anomaly detection analysis
        self.log_analysis_step("Running anomaly detection with AnomalyDetector tool")
        anomaly_summary = self.anomaly_detector.get_anomaly_summary(metrics_data)
        
        # Statistical trend analysis
        self.log_analysis_step("Analyzing statistical trends")
        trend_analysis = self._perform_trend_analysis(metrics_data)
        
        # Performance benchmarking
        self.log_analysis_step("Benchmarking performance against baselines")
        performance_benchmark = self._benchmark_performance(metrics_data)
        
        # Data quality assessment
        self.log_analysis_step("Assessing data quality and confidence")
        data_quality = self._assess_data_quality_detailed(metrics_data)
        
        # Risk assessment based on data
        self.log_analysis_step("Performing data-driven risk assessment")
        data_risk_assessment = self._assess_data_risks(metric_insights, anomaly_summary)
        
        # Generate statistical confidence intervals
        confidence_analysis = self._calculate_confidence_intervals(metrics_data)
        
        self.analysis_results = {
            "metric_insights": metric_insights,
            "anomaly_summary": anomaly_summary,
            "trend_analysis": trend_analysis,
            "performance_benchmark": performance_benchmark,
            "data_quality": data_quality,
            "risk_assessment": data_risk_assessment,
            "confidence_analysis": confidence_analysis,
            "key_findings": self._generate_data_findings(
                metric_insights, anomaly_summary, trend_analysis, performance_benchmark
            )
        }
        
        self.log_analysis_step("Data Analyst analysis complete", 
                             f"Overall health: {metric_insights['overall_health_score']:.2f}")
        
        return self.analysis_results
    
    def _perform_trend_analysis(self, metrics_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform detailed trend analysis on all metrics."""
        
        trend_analysis = {
            "positive_trends": [],
            "negative_trends": [],
            "concerning_accelerations": [],
            "trend_strength_summary": {},
            "correlation_analysis": {}
        }
        
        metrics = metrics_data.get("metrics", {})
        
        for metric_name, metric_data in metrics.items():
            data_points = metric_data.get("data_points", [])
            
            if len(data_points) < 10:
                continue
            
            # Calculate trend metrics
            values = [point["value"] for point in data_points]
            trend_info = self._calculate_trend_metrics(values, metric_name)
            
            trend_analysis["trend_strength_summary"][metric_name] = {
                "direction": trend_info["direction"],
                "strength": trend_info["strength"],
                "acceleration": trend_info["acceleration"],
                "volatility": trend_info["volatility"]
            }
            
            # Categorize trends
            if trend_info["strength"] > 0.3:  # Strong trend
                if self._is_positive_trend(metric_name, trend_info["direction"]):
                    trend_analysis["positive_trends"].append({
                        "metric": metric_name,
                        "direction": trend_info["direction"],
                        "strength": trend_info["strength"]
                    })
                else:
                    trend_analysis["negative_trends"].append({
                        "metric": metric_name,
                        "direction": trend_info["direction"],
                        "strength": trend_info["strength"]
                    })
            
            # Check for concerning accelerations
            if trend_info["acceleration"] > 0.5 and not self._is_positive_trend(metric_name, trend_info["direction"]):
                trend_analysis["concerning_accelerations"].append({
                    "metric": metric_name,
                    "acceleration": trend_info["acceleration"],
                    "current_trend": trend_info["direction"]
                })
        
        print(f"Trend analysis: {len(trend_analysis['positive_trends'])} positive, "
              f"{len(trend_analysis['negative_trends'])} negative trends")
        
        return trend_analysis
    
    def _calculate_trend_metrics(self, values: List[float], metric_name: str) -> Dict[str, Any]:
        """Calculate detailed trend metrics for a time series."""
        
        if len(values) < 3:
            return {"direction": "unknown", "strength": 0, "acceleration": 0, "volatility": 0}
        
        # Simple linear regression for trend
        n = len(values)
        x_values = list(range(n))
        
        # Calculate slope
        sum_x = sum(x_values)
        sum_y = sum(values)
        sum_xy = sum(x * y for x, y in zip(x_values, values))
        sum_x2 = sum(x * x for x in x_values)
        
        if n * sum_x2 - sum_x * sum_x == 0:
            slope = 0
        else:
            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
        
        # Determine direction and strength
        avg_value = sum_y / n
        if avg_value != 0:
            normalized_slope = abs(slope) / avg_value
            strength = min(normalized_slope * 100, 1.0)
        else:
            strength = 0
        
        direction = "increasing" if slope > 0 else "decreasing" if slope < 0 else "stable"
        
        # Calculate acceleration (trend in recent vs earlier periods)
        mid_point = n // 2
        recent_values = values[mid_point:]
        earlier_values = values[:mid_point]
        
        recent_avg = sum(recent_values) / len(recent_values)
        earlier_avg = sum(earlier_values) / len(earlier_values)
        
        if earlier_avg != 0:
            acceleration = abs((recent_avg - earlier_avg) / earlier_avg)
        else:
            acceleration = 0
        
        # Calculate volatility (coefficient of variation)
        if avg_value != 0:
            std_dev = (sum((v - avg_value) ** 2 for v in values) / n) ** 0.5
            volatility = std_dev / avg_value
        else:
            volatility = 0
        
        return {
            "direction": direction,
            "strength": strength,
            "acceleration": acceleration,
            "volatility": volatility,
            "slope": slope
        }
    
    def _is_positive_trend(self, metric_name: str, direction: str) -> bool:
        """Determine if a trend direction is positive for a given metric."""
        
        # For error rates, latency, tickets - decreasing is positive
        if any(term in metric_name.lower() for term in ["error", "latency", "ticket"]):
            return direction == "decreasing"
        
        # For conversion, retention, adoption, DAU - increasing is positive
        else:
            return direction == "increasing"
    
    def _benchmark_performance(self, metrics_data: Dict[str, Any]) -> Dict[str, Any]:
        """Benchmark current performance against baselines and targets."""
        
        benchmark = {
            "metrics_vs_baseline": {},
            "metrics_vs_target": {},
            "performance_summary": {
                "exceeding_targets": 0,
                "meeting_baselines": 0,
                "below_baselines": 0,
                "critical_deviations": []
            }
        }
        
        metrics = metrics_data.get("metrics", {})
        
        for metric_name, metric_data in metrics.items():
            data_points = metric_data.get("data_points", [])
            if not data_points:
                continue
            
            current_value = data_points[-1]["value"]
            baseline = metric_data.get("baseline")
            target = metric_data.get("target")
            
            # Compare to baseline
            if baseline is not None and baseline != 0:
                baseline_deviation = ((current_value - baseline) / baseline) * 100
                benchmark["metrics_vs_baseline"][metric_name] = {
                    "current": current_value,
                    "baseline": baseline,
                    "deviation_percent": baseline_deviation,
                    "status": "above" if baseline_deviation > 0 else "below" if baseline_deviation < 0 else "equal"
                }
                
                # Check if deviation is concerning
                if abs(baseline_deviation) > 20:  # 20% deviation
                    benchmark["performance_summary"]["critical_deviations"].append({
                        "metric": metric_name,
                        "deviation": baseline_deviation,
                        "type": "baseline"
                    })
                
                # Count performance categories
                if self._is_positive_deviation(metric_name, baseline_deviation):
                    benchmark["performance_summary"]["meeting_baselines"] += 1
                else:
                    benchmark["performance_summary"]["below_baselines"] += 1
            
            # Compare to target
            if target is not None and target != 0:
                target_deviation = ((current_value - target) / target) * 100
                benchmark["metrics_vs_target"][metric_name] = {
                    "current": current_value,
                    "target": target,
                    "deviation_percent": target_deviation,
                    "status": "above" if target_deviation > 0 else "below" if target_deviation < 0 else "equal"
                }
                
                # Check if exceeding target
                if self._is_positive_deviation(metric_name, target_deviation):
                    benchmark["performance_summary"]["exceeding_targets"] += 1
        
        print(f"Performance benchmark: {benchmark['performance_summary']['exceeding_targets']} exceeding targets, "
              f"{benchmark['performance_summary']['below_baselines']} below baselines")
        
        return benchmark
    
    def _is_positive_deviation(self, metric_name: str, deviation_percent: float) -> bool:
        """Determine if a deviation is positive for a given metric."""
        
        # For error rates, latency, tickets - negative deviation is positive
        if any(term in metric_name.lower() for term in ["error", "latency", "ticket"]):
            return deviation_percent < 0
        
        # For conversion, retention, adoption, DAU - positive deviation is positive
        else:
            return deviation_percent > 0
    
    def _assess_data_quality_detailed(self, metrics_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform detailed data quality assessment."""
        
        quality_assessment = {
            "overall_score": 0.0,
            "completeness": {},
            "consistency": {},
            "timeliness": {},
            "accuracy_indicators": {},
            "recommendations": []
        }
        
        metrics = metrics_data.get("metrics", {})
        total_metrics = len(metrics)
        
        if total_metrics == 0:
            quality_assessment["overall_score"] = 0.0
            quality_assessment["recommendations"].append("No metrics data available")
            return quality_assessment
        
        completeness_score = 0
        consistency_score = 0
        timeliness_score = 0
        
        for metric_name, metric_data in metrics.items():
            data_points = metric_data.get("data_points", [])
            
            # Assess completeness
            expected_points = 14 * 24  # 14 days * 24 hours
            actual_points = len(data_points)
            completeness_ratio = min(1.0, actual_points / expected_points)
            completeness_score += completeness_ratio
            
            quality_assessment["completeness"][metric_name] = {
                "expected": expected_points,
                "actual": actual_points,
                "ratio": completeness_ratio
            }
            
            if completeness_ratio < 0.8:
                quality_assessment["recommendations"].append(
                    f"Incomplete data for {metric_name}: {actual_points}/{expected_points} points"
                )
            
            # Assess consistency (check for gaps)
            if len(data_points) >= 2:
                timestamps = [datetime.fromisoformat(p["timestamp"]) for p in data_points]
                gaps = []
                for i in range(1, len(timestamps)):
                    gap = (timestamps[i] - timestamps[i-1]).total_seconds() / 3600  # hours
                    if gap > 2:  # More than 2 hours gap
                        gaps.append(gap)
                
                consistency_ratio = 1.0 - min(1.0, len(gaps) / len(data_points))
                consistency_score += consistency_ratio
                
                quality_assessment["consistency"][metric_name] = {
                    "gaps_found": len(gaps),
                    "largest_gap_hours": max(gaps) if gaps else 0,
                    "consistency_ratio": consistency_ratio
                }
            else:
                consistency_score += 0.5  # Partial score for insufficient data
            
            # Assess timeliness (how recent is the latest data)
            if data_points:
                latest_timestamp = datetime.fromisoformat(data_points[-1]["timestamp"])
                hours_since_latest = (datetime.now() - latest_timestamp).total_seconds() / 3600
                
                if hours_since_latest <= 1:
                    timeliness_ratio = 1.0
                elif hours_since_latest <= 6:
                    timeliness_ratio = 0.8
                elif hours_since_latest <= 24:
                    timeliness_ratio = 0.6
                else:
                    timeliness_ratio = 0.3
                
                timeliness_score += timeliness_ratio
                
                quality_assessment["timeliness"][metric_name] = {
                    "hours_since_latest": hours_since_latest,
                    "timeliness_ratio": timeliness_ratio
                }
                
                if hours_since_latest > 6:
                    quality_assessment["recommendations"].append(
                        f"Stale data for {metric_name}: {hours_since_latest:.1f} hours old"
                    )
        
        # Calculate overall score
        quality_assessment["overall_score"] = (
            completeness_score / total_metrics * 0.4 +
            consistency_score / total_metrics * 0.3 +
            timeliness_score / total_metrics * 0.3
        )
        
        print(f"Data quality assessment: {quality_assessment['overall_score']:.2f} overall score")
        
        return quality_assessment
    
    def _assess_data_risks(self, metric_insights: Dict[str, Any], 
                          anomaly_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Assess risks based on data analysis."""
        
        risk_assessment = {
            "overall_risk_level": "medium",
            "critical_risks": [],
            "high_risks": [],
            "medium_risks": [],
            "risk_score": 0.5,  # 0-1 scale
            "mitigation_recommendations": []
        }
        
        risk_factors = []
        
        # Assess metric-based risks
        critical_metrics = metric_insights.get("critical_metrics", [])
        warning_metrics = metric_insights.get("warning_metrics", [])
        
        for metric in critical_metrics:
            risk_assessment["critical_risks"].append({
                "type": "metric_threshold",
                "description": f"{metric.metric_name} in critical state: {metric.current_value} {metric.unit}",
                "severity": "critical",
                "metric": metric.metric_name
            })
            risk_factors.append(0.9)  # High risk factor
        
        for metric in warning_metrics:
            risk_assessment["high_risks"].append({
                "type": "metric_threshold", 
                "description": f"{metric.metric_name} in warning state: {metric.current_value} {metric.unit}",
                "severity": "high",
                "metric": metric.metric_name
            })
            risk_factors.append(0.7)  # Moderate risk factor
        
        # Assess anomaly-based risks
        critical_anomalies = anomaly_summary.get("critical_anomalies", 0)
        recent_anomalies = anomaly_summary.get("recent_anomalies_24h", 0)
        
        if critical_anomalies > 0:
            risk_assessment["critical_risks"].append({
                "type": "anomaly",
                "description": f"{critical_anomalies} critical anomalies detected",
                "severity": "critical"
            })
            risk_factors.append(0.85)
        
        if recent_anomalies > 3:
            risk_assessment["high_risks"].append({
                "type": "anomaly",
                "description": f"{recent_anomalies} anomalies in last 24 hours",
                "severity": "high"
            })
            risk_factors.append(0.6)
        
        # Assess trend-based risks
        negative_trends = metric_insights.get("negative_trends", [])
        if len(negative_trends) > 3:
            risk_assessment["medium_risks"].append({
                "type": "trend",
                "description": f"{len(negative_trends)} metrics showing negative trends",
                "severity": "medium"
            })
            risk_factors.append(0.5)
        
        # Calculate overall risk score
        if risk_factors:
            risk_assessment["risk_score"] = max(risk_factors)
        else:
            risk_assessment["risk_score"] = 0.3  # Low risk if no factors identified
        
        # Determine overall risk level
        if risk_assessment["risk_score"] > 0.8:
            risk_assessment["overall_risk_level"] = "critical"
        elif risk_assessment["risk_score"] > 0.6:
            risk_assessment["overall_risk_level"] = "high"
        elif risk_assessment["risk_score"] > 0.4:
            risk_assessment["overall_risk_level"] = "medium"
        else:
            risk_assessment["overall_risk_level"] = "low"
        
        # Generate mitigation recommendations
        if critical_metrics:
            risk_assessment["mitigation_recommendations"].append(
                "Immediate investigation of critical metrics required"
            )
        
        if critical_anomalies > 0:
            risk_assessment["mitigation_recommendations"].append(
                "Investigate root cause of critical anomalies"
            )
        
        if recent_anomalies > 2:
            risk_assessment["mitigation_recommendations"].append(
                "Increase monitoring frequency for anomaly detection"
            )
        
        print(f"Data risk assessment: {risk_assessment['overall_risk_level']} risk level "
              f"(score: {risk_assessment['risk_score']:.2f})")
        
        return risk_assessment
    
    def _calculate_confidence_intervals(self, metrics_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate statistical confidence intervals for key metrics."""
        
        confidence_analysis = {
            "confidence_intervals": {},
            "prediction_accuracy": {},
            "statistical_significance": {}
        }
        
        metrics = metrics_data.get("metrics", {})
        
        for metric_name, metric_data in metrics.items():
            data_points = metric_data.get("data_points", [])
            
            if len(data_points) < 10:
                continue
            
            values = [point["value"] for point in data_points]
            
            # Calculate basic statistics
            n = len(values)
            mean = sum(values) / n
            variance = sum((x - mean) ** 2 for x in values) / (n - 1)
            std_dev = variance ** 0.5
            
            # 95% confidence interval for the mean
            margin_of_error = 1.96 * (std_dev / (n ** 0.5))  # Assuming normal distribution
            
            confidence_analysis["confidence_intervals"][metric_name] = {
                "mean": mean,
                "std_dev": std_dev,
                "confidence_95_lower": mean - margin_of_error,
                "confidence_95_upper": mean + margin_of_error,
                "sample_size": n
            }
        
        print(f"Calculated confidence intervals for {len(confidence_analysis['confidence_intervals'])} metrics")
        
        return confidence_analysis
    
    def _generate_data_findings(self, metric_insights: Dict[str, Any], 
                              anomaly_summary: Dict[str, Any],
                              trend_analysis: Dict[str, Any],
                              performance_benchmark: Dict[str, Any]) -> List[str]:
        """Generate key data findings from analysis."""
        
        findings = []
        
        # Overall health findings
        health_score = metric_insights.get("overall_health_score", 0.5)
        if health_score < 0.3:
            findings.append(f"Critical: Overall system health score is {health_score:.2f}")
        elif health_score < 0.6:
            findings.append(f"Concerning: Overall system health score is {health_score:.2f}")
        else:
            findings.append(f"Healthy: Overall system health score is {health_score:.2f}")
        
        # Critical metrics findings
        critical_count = len(metric_insights.get("critical_metrics", []))
        if critical_count > 0:
            findings.append(f"Alert: {critical_count} metrics in critical state")
        
        # Anomaly findings
        critical_anomalies = anomaly_summary.get("critical_anomalies", 0)
        recent_anomalies = anomaly_summary.get("recent_anomalies_24h", 0)
        
        if critical_anomalies > 0:
            findings.append(f"Critical: {critical_anomalies} critical anomalies detected")
        
        if recent_anomalies > 3:
            findings.append(f"Alert: {recent_anomalies} anomalies in last 24 hours")
        
        # Trend findings
        negative_trends = len(trend_analysis.get("negative_trends", []))
        positive_trends = len(trend_analysis.get("positive_trends", []))
        
        if negative_trends > positive_trends:
            findings.append(f"Concerning: {negative_trends} negative vs {positive_trends} positive trends")
        elif positive_trends > negative_trends:
            findings.append(f"Positive: {positive_trends} positive vs {negative_trends} negative trends")
        
        # Performance benchmark findings
        exceeding_targets = performance_benchmark.get("performance_summary", {}).get("exceeding_targets", 0)
        below_baselines = performance_benchmark.get("performance_summary", {}).get("below_baselines", 0)
        
        if below_baselines > 2:
            findings.append(f"Performance issue: {below_baselines} metrics below baseline")
        
        if exceeding_targets > 2:
            findings.append(f"Strong performance: {exceeding_targets} metrics exceeding targets")
        
        return findings
    
    def get_recommendation(self) -> AgentRecommendation:
        """Generate Data Analyst recommendation based on statistical analysis."""
        
        if not self.analysis_results:
            return AgentRecommendation(
                agent_name=self.agent_name,
                recommendation=DecisionType.PAUSE,
                confidence=0.3,
                rationale="Insufficient data for statistical analysis",
                key_findings=["No analysis performed"],
                concerns=["Missing analysis data"]
            )
        
        # Extract key analysis results
        metric_insights = self.analysis_results["metric_insights"]
        anomaly_summary = self.analysis_results["anomaly_summary"]
        risk_assessment = self.analysis_results["risk_assessment"]
        data_quality = self.analysis_results["data_quality"]
        key_findings = self.analysis_results["key_findings"]
        
        concerns = []
        
        # Decision logic based on data analysis
        health_score = metric_insights.get("overall_health_score", 0.5)
        critical_anomalies = anomaly_summary.get("critical_anomalies", 0)
        recent_anomalies = anomaly_summary.get("recent_anomalies_24h", 0)
        risk_level = risk_assessment.get("overall_risk_level", "medium")
        critical_metrics_count = len(metric_insights.get("critical_metrics", []))
        
        # Critical conditions requiring rollback
        if critical_anomalies > 2 or critical_metrics_count > 2:
            decision = DecisionType.ROLL_BACK
            confidence = 0.9
            rationale = f"Multiple critical issues: {critical_anomalies} critical anomalies, {critical_metrics_count} critical metrics"
            concerns.extend([
                f"{critical_anomalies} critical anomalies detected",
                f"{critical_metrics_count} metrics in critical state"
            ])
        
        elif health_score < 0.25:
            decision = DecisionType.ROLL_BACK
            confidence = 0.85
            rationale = f"System health critically low: {health_score:.2f}"
            concerns.append("Critical system health score")
        
        # High risk conditions requiring pause
        elif risk_level == "critical" or recent_anomalies > 5:
            decision = DecisionType.PAUSE
            confidence = 0.8
            rationale = f"High risk detected: {risk_level} risk level, {recent_anomalies} recent anomalies"
            concerns.extend([
                f"Risk level: {risk_level}",
                f"{recent_anomalies} anomalies in 24h"
            ])
        
        elif health_score < 0.4 or critical_metrics_count > 0:
            decision = DecisionType.PAUSE
            confidence = 0.75
            rationale = f"Moderate concerns: health score {health_score:.2f}, {critical_metrics_count} critical metrics"
            concerns.append("Below-average system health")
        
        # Proceed conditions
        elif health_score > 0.7 and critical_anomalies == 0 and risk_level in ["low", "medium"]:
            decision = DecisionType.PROCEED
            confidence = 0.8
            rationale = f"Strong data indicators: health score {health_score:.2f}, {risk_level} risk"
        
        else:
            decision = DecisionType.PROCEED
            confidence = 0.6
            rationale = f"Mixed indicators: health score {health_score:.2f}, manageable risk level"
            concerns.append("Mixed performance indicators")
        
        # Adjust confidence based on data quality
        data_quality_score = data_quality.get("overall_score", 0.7)
        confidence *= (0.5 + 0.5 * data_quality_score)  # Reduce confidence for poor data quality
        
        if data_quality_score < 0.6:
            concerns.append(f"Data quality concerns: {data_quality_score:.2f} score")
        
        recommendation = AgentRecommendation(
            agent_name=self.agent_name,
            recommendation=decision,
            confidence=confidence,
            rationale=rationale,
            key_findings=key_findings,
            concerns=concerns if concerns else None
        )
        
        print(f"Data Analyst Recommendation: {decision.value} (confidence: {confidence:.2f})")
        print(f"Rationale: {rationale}")
        
        return recommendation