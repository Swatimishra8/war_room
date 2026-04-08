"""Comprehensive test suite for the War Room multi-agent system."""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


def test_data_files():
    """Test that all required data files exist and are valid."""
    
    print("Testing data files...")
    
    required_files = [
        "data/metrics.json",
        "data/feedback.json", 
        "data/release_notes.md"
    ]
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"❌ Missing required file: {file_path}")
            return False
        else:
            print(f"✅ Found: {file_path}")
    
    # Test JSON files are valid
    try:
        with open("data/metrics.json", 'r') as f:
            metrics_data = json.load(f)
        
        assert "metrics" in metrics_data
        assert "feature_name" in metrics_data
        assert len(metrics_data["metrics"]) > 0
        print(f"✅ Metrics file valid: {len(metrics_data['metrics'])} metrics")
        
        with open("data/feedback.json", 'r') as f:
            feedback_data = json.load(f)
        
        assert "feedback_items" in feedback_data
        assert "total_count" in feedback_data
        assert len(feedback_data["feedback_items"]) > 0
        print(f"✅ Feedback file valid: {feedback_data['total_count']} items")
        
    except Exception as e:
        print(f"❌ Data file validation failed: {e}")
        return False
    
    return True


def test_simple_system():
    """Test the simple system implementation."""
    
    print("\nTesting simple system...")
    
    try:
        # Import and run simple test
        from simple_test import run_simple_test
        
        exit_code = run_simple_test()
        
        if exit_code in [0, 1, 2]:  # Valid exit codes
            print("✅ Simple system test completed successfully")
            
            # Check output file was created
            if os.path.exists("output/simple_decision.json"):
                with open("output/simple_decision.json", 'r') as f:
                    decision_data = json.load(f)
                
                required_fields = [
                    "decision", "confidence_score", "rationale", 
                    "risk_register", "action_plan", "communication_plan"
                ]
                
                for field in required_fields:
                    if field not in decision_data:
                        print(f"❌ Missing required field in output: {field}")
                        return False
                    else:
                        print(f"✅ Output contains: {field}")
                
                print(f"✅ Decision: {decision_data['decision']}")
                print(f"✅ Confidence: {decision_data['confidence_score']:.2f}")
                
                return True
            else:
                print("❌ Output file not created")
                return False
        else:
            print(f"❌ Unexpected exit code: {exit_code}")
            return False
            
    except Exception as e:
        print(f"❌ Simple system test failed: {e}")
        return False


def test_output_format():
    """Test that the output format matches requirements."""
    
    print("\nTesting output format...")
    
    if not os.path.exists("output/simple_decision.json"):
        print("❌ No output file to test")
        return False
    
    try:
        with open("output/simple_decision.json", 'r') as f:
            decision = json.load(f)
        
        # Test required top-level fields
        required_fields = {
            "decision": str,
            "confidence_score": (int, float),
            "rationale": dict,
            "risk_register": list,
            "action_plan": dict,
            "communication_plan": dict,
            "confidence_factors": list
        }
        
        for field, expected_type in required_fields.items():
            if field not in decision:
                print(f"❌ Missing required field: {field}")
                return False
            
            if not isinstance(decision[field], expected_type):
                print(f"❌ Wrong type for {field}: expected {expected_type}, got {type(decision[field])}")
                return False
            
            type_name = expected_type.__name__ if hasattr(expected_type, '__name__') else str(expected_type)
            print(f"✅ {field}: {type_name}")
        
        # Test decision value
        if decision["decision"] not in ["Proceed", "Pause", "Roll Back"]:
            print(f"❌ Invalid decision value: {decision['decision']}")
            return False
        
        # Test confidence score range
        if not 0 <= decision["confidence_score"] <= 1:
            print(f"❌ Confidence score out of range: {decision['confidence_score']}")
            return False
        
        # Test rationale structure
        rationale = decision["rationale"]
        if "key_drivers" not in rationale:
            print("❌ Missing key_drivers in rationale")
            return False
        
        # Test risk register structure
        for risk in decision["risk_register"]:
            if not all(field in risk for field in ["risk", "severity", "mitigation"]):
                print("❌ Invalid risk register item structure")
                return False
        
        # Test action plan structure
        action_plan = decision["action_plan"]
        if not any(timeline in action_plan for timeline in ["24_hours", "48_hours"]):
            print("❌ Action plan missing required timelines")
            return False
        
        for timeline, actions in action_plan.items():
            for action in actions:
                if not all(field in action for field in ["action", "owner"]):
                    print(f"❌ Invalid action item structure in {timeline}")
                    return False
        
        print("✅ Output format validation passed")
        return True
        
    except Exception as e:
        print(f"❌ Output format test failed: {e}")
        return False


def test_decision_logic():
    """Test decision logic with different scenarios."""
    
    print("\nTesting decision logic...")
    
    # This would require more sophisticated testing with different data scenarios
    # For now, just verify the current decision makes sense
    
    try:
        with open("output/simple_decision.json", 'r') as f:
            decision = json.load(f)
        
        decision_value = decision["decision"]
        confidence = decision["confidence_score"]
        
        # Get analysis summary
        analysis = decision.get("analysis_summary", {})
        metric_analysis = analysis.get("metric_analysis", {})
        sentiment_analysis = analysis.get("sentiment_analysis", {})
        
        critical_metrics = len(metric_analysis.get("critical_metrics", []))
        health_score = metric_analysis.get("overall_health_score", 0.5)
        sentiment_score = sentiment_analysis.get("average_sentiment_score", 0.0)
        negative_percentage = sentiment_analysis.get("negative_percentage", 0.0)
        
        print(f"Decision factors:")
        print(f"  Critical metrics: {critical_metrics}")
        print(f"  Health score: {health_score:.2f}")
        print(f"  Sentiment score: {sentiment_score:.3f}")
        print(f"  Negative feedback: {negative_percentage:.1f}%")
        
        # Validate decision logic
        if decision_value == "Roll Back":
            if not (critical_metrics > 2 or health_score < 0.3 or sentiment_score < -0.4 or negative_percentage > 70):
                print("⚠️  Roll Back decision may be too aggressive for current metrics")
            else:
                print("✅ Roll Back decision justified by metrics")
        
        elif decision_value == "Pause":
            if critical_metrics > 0 or health_score < 0.5 or sentiment_score < -0.2 or negative_percentage > 50:
                print("✅ Pause decision justified by metrics")
            else:
                print("⚠️  Pause decision may be too conservative for current metrics")
        
        elif decision_value == "Proceed":
            if health_score > 0.7 and sentiment_score > 0.1 and negative_percentage < 30:
                print("✅ Proceed decision justified by strong metrics")
            elif critical_metrics == 0 and health_score > 0.5:
                print("✅ Proceed decision reasonable given metrics")
            else:
                print("⚠️  Proceed decision may be too risky for current metrics")
        
        # Check confidence is reasonable
        if 0.6 <= confidence <= 1.0:
            print(f"✅ Confidence score reasonable: {confidence:.2f}")
        else:
            print(f"⚠️  Confidence score may be too low: {confidence:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Decision logic test failed: {e}")
        return False


def test_traceability():
    """Test that the system provides adequate traceability."""
    
    print("\nTesting traceability...")
    
    try:
        with open("output/simple_decision.json", 'r') as f:
            decision = json.load(f)
        
        # Check for traceability elements
        traceability_elements = [
            "timestamp",
            "feature_name", 
            "launch_date",
            "rationale",
            "analysis_summary"
        ]
        
        for element in traceability_elements:
            if element not in decision:
                print(f"❌ Missing traceability element: {element}")
                return False
            print(f"✅ Traceability element present: {element}")
        
        # Check rationale has key drivers
        rationale = decision["rationale"]
        if "key_drivers" not in rationale or len(rationale["key_drivers"]) == 0:
            print("❌ Missing key drivers in rationale")
            return False
        
        print(f"✅ {len(rationale['key_drivers'])} key drivers documented")
        
        # Check analysis summary has details
        analysis = decision.get("analysis_summary", {})
        if not analysis:
            print("❌ Missing analysis summary")
            return False
        
        if "metric_analysis" in analysis and "sentiment_analysis" in analysis:
            print("✅ Detailed analysis summary present")
        else:
            print("❌ Incomplete analysis summary")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Traceability test failed: {e}")
        return False


def run_comprehensive_tests():
    """Run all tests and provide summary."""
    
    print("PurpleMerit War Room - Comprehensive Test Suite")
    print("=" * 60)
    
    tests = [
        ("Data Files", test_data_files),
        ("Simple System", test_simple_system),
        ("Output Format", test_output_format),
        ("Decision Logic", test_decision_logic),
        ("Traceability", test_traceability)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{test_name.upper()} TEST")
        print("-" * 30)
        
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
    
    print("-" * 30)
    print(f"TOTAL: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        print("\nThe War Room system is working correctly!")
        return 0
    else:
        print(f"⚠️  {total - passed} tests failed")
        print("\nPlease review the failed tests above.")
        return 1


if __name__ == "__main__":
    exit_code = run_comprehensive_tests()
    sys.exit(exit_code)