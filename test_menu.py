"""Interactive menu for testing different War Room scenarios."""

import sys
import os
from test_proceed_scenario import run_proceed_test
from test_pause_scenario import run_pause_test  
from test_rollback_scenario import run_rollback_test

def print_menu():
    """Display the test menu."""
    print("\n" + "="*60)
    print("    WAR ROOM MULTI-AGENT SYSTEM - TEST MENU")
    print("="*60)
    print("Choose a scenario to test:")
    print()
    print("1. 🚀 PROCEED Scenario  (Exit Code 0)")
    print("   - Excellent metrics, 90%+ positive feedback")
    print("   - All agents recommend: Proceed")
    print()
    print("2. ⏸️  PAUSE Scenario    (Exit Code 1)")
    print("   - Mixed metrics, moderate negative feedback")
    print("   - Most agents recommend: Pause")
    print()
    print("3. 🔴 ROLLBACK Scenario (Exit Code 2)")
    print("   - Critical metrics, 70%+ negative feedback")
    print("   - Agents recommend: Roll Back")
    print()
    print("4. 📊 Test ALL Scenarios")
    print("   - Generate and test all three scenarios")
    print()
    print("5. 📁 Use Original Data (Current behavior)")
    print("   - Test with the existing mock data")
    print()
    print("0. ❌ Exit")
    print("="*60)

def run_war_room_test(metrics_file, feedback_file, scenario_name):
    """Run the war room system with specified data files."""
    print(f"\n🧪 Running {scenario_name} scenario...")
    print("-" * 40)
    
    # Check if virtual environment exists
    venv_python = "venv/bin/python"
    python_cmd = venv_python if os.path.exists(venv_python) else "python"
    
    cmd = f"{python_cmd} main.py --metrics {metrics_file} --feedback {feedback_file} --verbose"
    print(f"🔧 Command: {cmd}")
    print("-" * 40)
    
    # Run the command
    exit_code = os.system(cmd)
    
    print("-" * 40)
    print(f"📊 Exit Code: {exit_code >> 8}")  # os.system returns exit code << 8
    
    return exit_code >> 8

def main():
    """Main menu loop."""
    
    while True:
        print_menu()
        
        try:
            choice = input("\nEnter your choice (0-5): ").strip()
            
            if choice == "0":
                print("\n👋 Goodbye!")
                break
                
            elif choice == "1":
                print("\n🚀 Generating PROCEED scenario...")
                run_proceed_test()
                run_war_room_test("data/metrics_proceed.json", "data/feedback_proceed.json", "PROCEED")
                
            elif choice == "2":
                print("\n⏸️  Generating PAUSE scenario...")
                run_pause_test()
                run_war_room_test("data/metrics_pause.json", "data/feedback_pause.json", "PAUSE")
                
            elif choice == "3":
                print("\n🔴 Generating ROLLBACK scenario...")
                run_rollback_test()
                run_war_room_test("data/metrics_rollback.json", "data/feedback_rollback.json", "ROLLBACK")
                
            elif choice == "4":
                print("\n📊 Testing ALL scenarios...")
                from test_all_scenarios import main as run_all_tests
                run_all_tests()
                
            elif choice == "5":
                print("\n📁 Using original data...")
                run_war_room_test("data/metrics.json", "data/feedback.json", "ORIGINAL")
                
            else:
                print("\n❌ Invalid choice. Please enter 0-5.")
                continue
                
            input("\n⏎ Press Enter to continue...")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("\n⏎ Press Enter to continue...")

if __name__ == "__main__":
    main()