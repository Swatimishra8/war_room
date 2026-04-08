"""Main entry point for the War Room multi-agent system."""

import argparse
import sys
import os
from datetime import datetime
from pathlib import Path

from orchestrator import WarRoomOrchestrator


def main():
    """Main function to run the War Room analysis."""
    
    parser = argparse.ArgumentParser(
        description="War Room Multi-Agent Launch Decision System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py
  python main.py --verbose
  python main.py --output-format yaml
  python main.py --metrics data/custom_metrics.json
        """
    )
    
    parser.add_argument(
        "--metrics",
        default="data/metrics.json",
        help="Path to metrics JSON file (default: data/metrics.json)"
    )
    
    parser.add_argument(
        "--feedback", 
        default="data/feedback.json",
        help="Path to feedback JSON file (default: data/feedback.json)"
    )
    
    parser.add_argument(
        "--release-notes",
        default="data/release_notes.md",
        help="Path to release notes file (default: data/release_notes.md)"
    )
    
    parser.add_argument(
        "--output",
        default="output/decision.json",
        help="Output file path (default: output/decision.json)"
    )
    
    parser.add_argument(
        "--output-format",
        choices=["json", "yaml"],
        default="json",
        help="Output format (default: json)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    parser.add_argument(
        "--config",
        help="Path to configuration file (optional)"
    )
    
    args = parser.parse_args()
    
    # Validate input files exist
    for file_path, name in [
        (args.metrics, "metrics"),
        (args.feedback, "feedback"), 
        (args.release_notes, "release notes")
    ]:
        if not os.path.exists(file_path):
            print(f"Error: {name} file not found: {file_path}")
            print(f"Please ensure the file exists or specify a different path with --{name.replace(' ', '-')}")
            sys.exit(1)
    
    # Create output directory if it doesn't exist
    output_dir = Path(args.output).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load configuration if provided
    config = None
    if args.config:
        import json
        with open(args.config, 'r') as f:
            config = json.load(f)
    
    # Override config with command line arguments
    # Only override specific fields, don't replace entire config
    if config:
        config["output_format"] = args.output_format
        config["enable_detailed_logging"] = args.verbose
    else:
        # Let orchestrator use its default config and just override these fields
        config = {
            "output_format": args.output_format,
            "enable_detailed_logging": args.verbose
        }
    
    print("PurpleMerit War Room - Multi-Agent Launch Decision System")
    print("=" * 60)
    print(f"Metrics file: {args.metrics}")
    print(f"Feedback file: {args.feedback}")
    print(f"Release notes: {args.release_notes}")
    print(f"Output file: {args.output}")
    print(f"Output format: {args.output_format}")
    print(f"Verbose logging: {args.verbose}")
    print("=" * 60)
    
    try:
        # Initialize orchestrator
        print("Initializing War Room Orchestrator...")
        orchestrator = WarRoomOrchestrator(config)
        
        # Run analysis
        print("Starting multi-agent analysis...")
        decision = orchestrator.run_war_room_analysis(
            args.metrics,
            args.feedback, 
            args.release_notes
        )
        
        # Save decision
        print(f"Saving decision to {args.output}...")
        orchestrator.save_decision(decision, args.output)
        
        # Print summary
        print("\n" + "=" * 60)
        print("FINAL DECISION SUMMARY")
        print("=" * 60)
        print(f"Decision: {decision.decision.value}")
        print(f"Confidence Score: {decision.confidence_score:.2f}")
        print(f"Feature: {decision.feature_name}")
        print(f"Analysis Duration: {decision.analysis_duration_seconds:.1f} seconds")
        print(f"Risks Identified: {len(decision.risk_register)}")
        print(f"Action Items: {sum(len(actions) for actions in decision.action_plan.values())}")
        
        print("\nAgent Recommendations:")
        for rec in decision.agent_recommendations:
            print(f"  {rec.agent_name}: {rec.recommendation.value} (confidence: {rec.confidence:.2f})")
        
        print(f"\nKey Risk Factors:")
        critical_risks = [r for r in decision.risk_register if r.severity.value == "Critical"]
        high_risks = [r for r in decision.risk_register if r.severity.value == "High"]
        
        if critical_risks:
            print(f"  Critical Risks: {len(critical_risks)}")
            for risk in critical_risks[:3]:  # Show top 3
                print(f"    - {risk.risk}")
        
        if high_risks:
            print(f"  High Risks: {len(high_risks)}")
            for risk in high_risks[:3]:  # Show top 3
                print(f"    - {risk.risk}")
        
        print(f"\nNext Steps (24 hours):")
        if "24 hours" in decision.action_plan:
            for action in decision.action_plan["24 hours"][:3]:  # Show top 3
                print(f"  - {action.action} (Owner: {action.owner})")
        
        print(f"\nCommunication Plan:")
        print(f"  Internal: {decision.communication_plan.get('internal', 'N/A')[:100]}...")
        print(f"  External: {decision.communication_plan.get('external', 'N/A')[:100]}...")
        
        print("\n" + "=" * 60)
        print(f"Analysis complete! Full decision saved to: {args.output}")
        print("=" * 60)
        
        # Exit with appropriate code based on decision
        if decision.decision.value == "Roll Back":
            sys.exit(2)  # Critical issues
        elif decision.decision.value == "Pause":
            sys.exit(1)  # Warning issues
        else:
            sys.exit(0)  # Success
            
    except KeyboardInterrupt:
        print("\nAnalysis interrupted by user.")
        sys.exit(130)
        
    except Exception as e:
        print(f"\nError during analysis: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()