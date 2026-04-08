# PurpleMerit War Room - Multi-Agent Launch Decision System

A sophisticated multi-agent system that simulates a cross-functional "war room" during product launches, analyzing metrics and user feedback to make structured launch decisions.

## Overview

This system simulates coordinated decision-making among multiple specialized agents:
- **Product Manager Agent**: Defines success criteria and go/no-go decisions
- **Data Analyst Agent**: Analyzes quantitative metrics and trends
- **Marketing/Communications Agent**: Assesses messaging and customer perception
- **Risk/Critic Agent**: Challenges assumptions and highlights risks
- **Orchestrator**: Coordinates the workflow and produces final decisions

## Features

- **Multi-agent orchestration** with clear separation of responsibilities
- **Tool usage** including metric aggregation, anomaly detection, and sentiment analysis
- **Structured output** with decision rationale, risk register, and action plans
- **Full traceability** with detailed logs of agent interactions
- **Realistic mock data** including metrics, user feedback, and release notes

## Setup Instructions

### Prerequisites
- Python 3.8+ (Python 3.9+ recommended)
- pip package manager
- Git (for cloning the repository)

### Step-by-Step Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd war_room
```

2. **Create and activate a virtual environment:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

3. **Install all dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables (optional):**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env file with your preferred settings
# Note: All environment variables are optional - system works with defaults
```

5. **Verify installation:**
```bash
# Test that all imports work correctly
python -c "from orchestrator import WarRoomOrchestrator; print('✅ Installation successful!')"

# Run help to see all available options
python main.py --help
```

## How to Run the Program End-to-End

### Quick Start (Basic Usage)

**Step 1:** Ensure your virtual environment is activated:
```bash
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows
```

**Step 2:** Run the complete war room simulation:
```bash
python main.py
```

This will:
- Load default mock data from `data/` directory
- Run all 4 agents (Product Manager, Data Analyst, Marketing, Risk/Critic)
- Produce a structured decision in `output/decision.json`
- Exit with semantic exit codes (0=Proceed, 1=Pause, 2=Roll Back)

### Advanced Usage Options

**Run with detailed logging:**
```bash
python main.py --verbose
```

**Specify custom data files:**
```bash
python main.py --metrics data/custom_metrics.json --feedback data/custom_feedback.json
```

**Change output format to YAML:**
```bash
python main.py --output-format yaml --output output/decision.yaml
```

**Use custom configuration:**
```bash
python main.py --config config/custom_config.yaml
```

### Complete Example Commands to Reproduce Output

**Example 1: Basic run with default data**
```bash
# Activate environment
source venv/bin/activate

# Run with verbose logging to see full agent workflow
python main.py --verbose

# Check the output
cat output/decision.json
```

**Example 2: Generate fresh mock data and analyze**
```bash
# Generate new mock data
python generate_mock_data.py

# Run analysis on the new data
python main.py --verbose --output output/fresh_analysis.json

# View results
python -m json.tool output/fresh_analysis.json
```

**Example 3: Test different decision scenarios**
```bash
# Test a "Proceed" scenario
python test_proceed_scenario.py
python main.py --verbose
echo "Exit code: $?"  # Should be 0

# Test a "Pause" scenario  
python test_pause_scenario.py
python main.py --verbose
echo "Exit code: $?"  # Should be 1

# Test a "Roll Back" scenario
python test_rollback_scenario.py  
python main.py --verbose
echo "Exit code: $?"  # Should be 2
```

**Example 4: Interactive testing menu**
```bash
# Use the interactive test menu to try different scenarios
python test_menu.py
```

## Project Structure

```
war_room/
├── main.py                 # Main entry point
├── orchestrator.py         # Central coordinator
├── agents/                 # Agent implementations
│   ├── __init__.py
│   ├── base_agent.py      # Base agent class
│   ├── product_manager.py  # PM agent
│   ├── data_analyst.py    # Data analysis agent
│   ├── marketing_agent.py # Marketing/comms agent
│   └── risk_agent.py      # Risk/critic agent
├── tools/                  # Analysis tools
│   ├── __init__.py
│   ├── metric_analyzer.py  # Metric aggregation & analysis
│   ├── sentiment_analyzer.py # Feedback sentiment analysis
│   └── anomaly_detector.py # Anomaly detection
├── data/                   # Mock data
│   ├── metrics.json       # Time series metrics
│   ├── feedback.json      # User feedback
│   └── release_notes.md   # Release information
├── models/                 # Pydantic models
│   ├── __init__.py
│   ├── metrics.py         # Metric data models
│   ├── feedback.py        # Feedback models
│   └── decision.py        # Decision output models
├── config/                 # Configuration files
│   └── default_config.yaml
├── tests/                  # Test files
└── output/                 # Generated decisions
```

## Environment Variables

All environment variables are **optional**. The system works perfectly with default settings.

Create a `.env` file (copy from `.env.example`) with any of these variables:

```env
# Optional: OpenAI API key for enhanced LLM analysis
# Note: System works without this - uses built-in analysis algorithms
OPENAI_API_KEY=your_api_key_here

# System configuration
LOG_LEVEL=INFO                    # DEBUG, INFO, WARNING, ERROR
OUTPUT_FORMAT=json               # json or yaml
ENABLE_PLOTS=false              # true/false - generate visualization plots
ERROR_THRESHOLD=0.03            # Error rate threshold (0.0-1.0)
CONFIDENCE_THRESHOLD=0.7        # Minimum confidence for decisions (0.0-1.0)
```

### Environment Variable Details

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | None | Optional OpenAI API key for enhanced analysis. System uses built-in algorithms if not provided. |
| `LOG_LEVEL` | INFO | Controls logging verbosity. Use DEBUG for maximum detail. |
| `OUTPUT_FORMAT` | json | Output format for decision files. Options: json, yaml |
| `ENABLE_PLOTS` | false | Generate matplotlib visualizations of metrics (requires display) |
| `ERROR_THRESHOLD` | 0.03 | Maximum acceptable error rate (3%) before triggering warnings |
| `CONFIDENCE_THRESHOLD` | 0.7 | Minimum confidence score (70%) required for high-confidence decisions |

**Important:** The system is designed to work completely offline without any external API keys. All core analysis is performed using built-in statistical and sentiment analysis tools.

## Expected Output Format

The system produces a comprehensive structured decision in JSON format with all required fields:

### Sample Output Structure
```json
{
  "decision": "Pause",
  "feature_name": "Smart Recommendations Engine",
  "launch_date": "2026-04-08",
  "timestamp": "2026-04-08T21:09:17.173179",
  "rationale": {
    "key_drivers": [
      "High negative sentiment (45% negative feedback)",
      "Critical customer issues identified (11 issues)",
      "Medium risk level detected by data analysis"
    ],
    "metric_references": {
      "daily_active_users": "51.5% decline from baseline",
      "error_rate": "0.43% (within acceptable range)",
      "feature_adoption_rate": "24.4% (meets minimum threshold)"
    },
    "feedback_summary": "Mixed sentiment with 45.1% negative, 35.3% positive feedback. Critical issues around bugs and performance."
  },
  "risk_register": [
    {
      "risk": "Brand reputation and public perception risks",
      "severity": "High",
      "mitigation": "Implement targeted communication strategy and address critical user issues"
    },
    {
      "risk": "Operational capacity and process execution risks", 
      "severity": "Critical",
      "mitigation": "Immediate process review and capacity assessment"
    }
  ],
  "action_plan": {
    "24_hours": [
      {
        "action": "Halt new user onboarding to feature",
        "owner": "Product/Engineering",
        "priority": "Critical"
      },
      {
        "action": "Convene emergency stakeholder meeting",
        "owner": "Product Manager", 
        "priority": "High"
      }
    ],
    "48_hours": [
      {
        "action": "Conduct root cause analysis of issues",
        "owner": "Engineering/Product",
        "priority": "High"
      }
    ]
  },
  "communication_plan": {
    "internal": "Stakeholder notification of pause decision within 4 hours...",
    "external": "Targeted communication to affected users about temporary pause..."
  },
  "confidence_score": 0.76,
  "confidence_factors": [
    "High agent agreement (75% consensus)",
    "Strong data quality (1.00 score)",
    "Comprehensive risk analysis completed"
  ],
  "agent_recommendations": [
    {
      "agent": "product_manager",
      "decision": "Roll Back",
      "confidence": 0.63,
      "rationale": "Critical success criteria failures require immediate rollback"
    },
    {
      "agent": "data_analyst", 
      "decision": "Pause",
      "confidence": 0.80,
      "rationale": "High risk detected: medium risk level, 13 recent anomalies"
    }
  ]
}
```

### Exit Codes for CI/CD Integration
The system uses semantic exit codes for automated decision handling:
- **Exit Code 0**: Proceed with launch
- **Exit Code 1**: Pause launch (investigate and address issues)  
- **Exit Code 2**: Roll back launch (immediate action required)

### Output Files
- **Primary Output**: `output/decision.json` (or `.yaml` if specified)
- **Backup Outputs**: Previous decisions are preserved with timestamps
- **Logs**: All agent interactions and tool calls are logged to console

## Architecture

### Agent Workflow
1. **Orchestrator** loads mock data and initializes agents
2. **Data Analyst** analyzes metrics and identifies trends/anomalies
3. **Product Manager** evaluates against success criteria
4. **Marketing Agent** assesses customer sentiment and communication needs
5. **Risk Agent** challenges findings and identifies additional risks
6. **Orchestrator** synthesizes inputs and produces final decision

### Tool Integration
- **Metric Analyzer**: Aggregates time series data, calculates trends
- **Sentiment Analyzer**: Processes user feedback for sentiment scoring
- **Anomaly Detector**: Identifies statistical anomalies in metrics

## Testing and Verification

### Quick System Verification

**Test 1: Verify installation and imports**
```bash
python -c "from orchestrator import WarRoomOrchestrator; print('✅ All imports working')"
```

**Test 2: Run basic system test**
```bash
python test_system.py
```

**Test 3: Run full analysis with default data**
```bash
python main.py --verbose
echo "Exit code: $?"
```

### Testing All Decision Scenarios

The system includes dedicated test scripts for each possible decision outcome:

**Test "Proceed" Decision (Exit Code 0)**
```bash
# Generate data that leads to a "Proceed" decision
python test_proceed_scenario.py

# Run analysis - should exit with code 0
python main.py --verbose
echo "Exit code should be 0: $?"
```

**Test "Pause" Decision (Exit Code 1)**  
```bash
# Generate data that leads to a "Pause" decision
python test_pause_scenario.py

# Run analysis - should exit with code 1
python main.py --verbose  
echo "Exit code should be 1: $?"
```

**Test "Roll Back" Decision (Exit Code 2)**
```bash
# Generate data that leads to a "Roll Back" decision
python test_rollback_scenario.py

# Run analysis - should exit with code 2
python main.py --verbose
echo "Exit code should be 2: $?"
```

### Automated Testing

**Run all scenarios automatically:**
```bash
python test_all_scenarios.py
```

**Interactive testing menu:**
```bash
python test_menu.py
```

### Manual Testing Checklist

- [ ] System runs without errors: `python main.py`
- [ ] Verbose logging shows all agent steps: `python main.py --verbose`  
- [ ] JSON output is valid: `python -m json.tool output/decision.json`
- [ ] All three decision types work: Run scenario tests above
- [ ] Exit codes are correct: Check `echo $?` after each run
- [ ] Custom data files work: `python main.py --metrics custom.json`

### Troubleshooting

**Common Issues:**

1. **Import errors**: Ensure virtual environment is activated
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Missing data files**: Generate fresh mock data
   ```bash
   python generate_mock_data.py
   ```

3. **Permission errors**: Check file permissions in `data/` and `output/` directories

4. **YAML errors**: Install PyYAML if using YAML output
   ```bash
   pip install pyyaml
   ```

## Development

### Adding New Agents
1. Create new agent class inheriting from `BaseAgent`
2. Implement required methods: `analyze()`, `get_recommendation()`
3. Register agent in orchestrator configuration

### Adding New Tools
1. Create tool class in `tools/` directory
2. Implement tool interface with proper type hints
3. Register tool with relevant agents

## Quick Reference

### Most Common Commands
```bash
# Basic run with default data
python main.py

# Run with detailed logging  
python main.py --verbose

# Test specific scenario
python test_proceed_scenario.py && python main.py --metrics data/metrics_proceed.json --feedback data/feedback_proceed.json

# Interactive testing
python test_menu.py

# Generate fresh mock data
python generate_mock_data.py
```

### File Structure Overview
```
war_room/
├── main.py              # 🚀 Main entry point - START HERE
├── orchestrator.py      # 🎯 Central coordinator
├── agents/              # 🤖 Specialized decision agents  
├── tools/               # 🔧 Analysis tools (metrics, sentiment, anomaly)
├── models/              # 📋 Data structures (Pydantic models)
├── data/                # 📊 Mock dashboard data
├── output/              # 📄 Generated decisions
├── test_*.py            # 🧪 Scenario testing scripts
└── requirements.txt     # 📦 Dependencies
```

### Key Features Implemented ✅
- ✅ **Multi-agent orchestration** with 4 specialized agents
- ✅ **Tool usage** with 3 programmatic analysis tools  
- ✅ **Structured JSON/YAML output** with all required fields
- ✅ **Full traceability** with detailed agent interaction logs
- ✅ **Realistic mock data** with 7-14 day metrics and 20-50 feedback items
- ✅ **Semantic exit codes** for CI/CD integration (0/1/2)
- ✅ **Comprehensive testing** for all decision scenarios
- ✅ **Environment variable configuration** (all optional)
- ✅ **Offline operation** (no external API dependencies required)

## License

MIT License - see LICENSE file for details.