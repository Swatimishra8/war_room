"""Master test script to generate and test all decision scenarios."""

import sys
import subprocess
from test_proceed_scenario import run_proceed_test
from test_pause_scenario import run_pause_test
from test_rollback_scenario import run_rollback_test

def print_header(title):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def run_scenario_test(scenario_name, metrics_file, feedback_file, output_file, expected_exit_code):
    """Run a specific scenario test."""
    print(f"\n🧪 Testing {scenario_name.upper()} scenario...")
    
    cmd = [
        "python", "main.py",
        "--metrics", metrics_file,
        "--feedback", feedback_file,
        "--output", output_file
    ]
    
    try:
        # Run in virtual environment if it exists
        venv_python = "venv/bin/python"
        import os
        if os.path.exists(venv_python):
            cmd[0] = venv_python
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=".")
        
        print(f"📊 Result: Exit Code {result.returncode}")
        
        if result.returncode == expected_exit_code:
            print(f"✅ SUCCESS: Got expected exit code {expected_exit_code}")
        else:
            print(f"❌ FAILED: Expected exit code {expected_exit_code}, got {result.returncode}")
        
        # Extract decision from output
        lines = result.stdout.split('\n')
        decision_line = [line for line in lines if "Final Decision:" in line]
        if decision_line:
            print(f"📋 {decision_line[0]}")
        
        confidence_line = [line for line in lines if "Confidence Score:" in line]
        if confidence_line:
            print(f"📈 {confidence_line[0]}")
        
        return result.returncode == expected_exit_code
        
    except Exception as e:
        print(f"❌ ERROR running test: {e}")
        return False

def main():
    """Run all scenario tests."""
    
    print_header("WAR ROOM MULTI-AGENT SYSTEM - ALL SCENARIOS TEST")
    
    print("🔧 Generating test scenarios...")
    
    # Generate all scenarios
    print("\n1️⃣  Generating PROCEED scenario...")
    run_proceed_test()
    
    print("\n2️⃣  Generating PAUSE scenario...")
    run_pause_test()
    
    print("\n3️⃣  Generating ROLL BACK scenario...")
    run_rollback_test()
    
    print_header("RUNNING ALL SCENARIO TESTS")
    
    results = []
    
    # Test all scenarios
    scenarios = [
        ("PROCEED", "data/metrics_proceed.json", "data/feedback_proceed.json", "output/proceed_test.json", 0),
        ("PAUSE", "data/metrics_pause.json", "data/feedback_pause.json", "output/pause_test.json", 1),
        ("ROLL BACK", "data/metrics_rollback.json", "data/feedback_rollback.json", "output/rollback_test.json", 2)
    ]
    
    for scenario_name, metrics_file, feedback_file, output_file, expected_exit_code in scenarios:
        success = run_scenario_test(scenario_name, metrics_file, feedback_file, output_file, expected_exit_code)
        results.append((scenario_name, success))
    
    # Summary
    print_header("TEST RESULTS SUMMARY")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for scenario_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{scenario_name:12} {status}")
    
    print(f"\n📊 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL SCENARIO TESTS PASSED!")
        print("\n📚 Usage Examples:")
        print("  🚀 Test PROCEED: python test_proceed_scenario.py")
        print("  ⏸️  Test PAUSE:   python test_pause_scenario.py")
        print("  🔴 Test ROLLBACK: python test_rollback_scenario.py")
        print("\n🎯 Run individual scenarios:")
        print("  python main.py --metrics data/metrics_proceed.json --feedback data/feedback_proceed.json")
        print("  python main.py --metrics data/metrics_pause.json --feedback data/feedback_pause.json")
        print("  python main.py --metrics data/metrics_rollback.json --feedback data/feedback_rollback.json")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)