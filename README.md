# 🎯 TokenTracker v1.0

**Real-time Token Usage Monitor for Team Brain**

Track AI token usage, enforce budgets, and generate cost reports. Built for autonomous AI agents to monitor their own resource consumption.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-green.svg)
![Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen.svg)

---

## ✨ Features

- **Real-time Token Logging** - Track input/output tokens per session
- **Multi-Agent Support** - Monitor FORGE, ATLAS, CLIO, NEXUS, BOLT, and more
- **Budget Management** - Set monthly budgets and get alerts
- **Cost Calculation** - Automatic cost computation for Claude models
- **Usage Reports** - Export detailed reports in JSON or text format
- **Zero Dependencies** - Pure Python standard library
- **Cross-Platform** - Works on Windows, Linux, macOS
- **SQL Injection Protected** - Robust input validation
- **CLI & Python API** - Use from command line or import as library

---

## 📦 Installation

### Option 1: Direct Download
```bash
# Download tokentracker.py to your project
curl -O https://raw.githubusercontent.com/DonkRonk17/TokenTracker/main/tokentracker.py

# Make it executable (Unix/Mac)
chmod +x tokentracker.py

# Run it
python tokentracker.py
```

### Option 2: Clone Repository
```bash
git clone https://github.com/DonkRonk17/TokenTracker.git
cd TokenTracker
python tokentracker.py
```

### Option 3: Install with pip (if packaged)
```bash
pip install tokentracker
```

**Requirements:** Python 3.7 or higher (no external dependencies!)

---

## 🚀 Quick Start

### 1. Log Token Usage
```bash
# Basic usage
python tokentracker.py log ATLAS sonnet-4.5 50000 15000 "Built new feature"

# Log usage for different agents
python tokentracker.py log FORGE opus-4.5 30000 10000 "Code review"
python tokentracker.py log CLIO haiku-3.5 10000 5000 "Quick task"
```

### 2. View Usage Summary
```bash
# Today's usage
python tokentracker.py summary today

# This week
python tokentracker.py summary week

# This month
python tokentracker.py summary month

# All time
python tokentracker.py summary all
```

### 3. Check Budget
```bash
# View current month's budget status
python tokentracker.py budget
```

### 4. Set Budget
```bash
# Set budget for January 2026
python tokentracker.py set-budget 2026-01 60.00

# Set budget for February 2026
python tokentracker.py set-budget 2026-02 75.00
```

### 5. Export Reports
```bash
# Text report for this month
python tokentracker.py report month text

# JSON report for all time
python tokentracker.py report all json > usage_report.json
```

---

## 💻 Python API

You can also use TokenTracker as a Python library:

```python
from tokentracker import TokenTracker

# Initialize tracker
tracker = TokenTracker()

# Log token usage
tracker.log_usage(
    agent="ATLAS",
    model="sonnet-4.5",
    input_tokens=50000,
    output_tokens=15000,
    notes="Built TokenTracker v1.0"
)

# Get usage summary
summary = tracker.get_usage_summary("today")
print(f"Today's tokens: {summary['total_tokens']:,}")
print(f"Today's cost: ${summary['total_cost']:.2f}")

# Check budget status
budget = tracker.get_budget_status()
print(f"Budget remaining: ${budget['remaining']:.2f}")
print(f"Usage: {budget['percent_used']:.1f}%")

# Export report
report = tracker.export_report("month", "json")
print(report)
```

---

## 📊 Usage Examples

### Example 1: Daily Monitoring
```bash
# Morning check
python tokentracker.py summary today

# Output:
# === TOKEN USAGE SUMMARY (TODAY) ===
# Sessions: 5
# Total Tokens: 125,000
# Total Cost: $0.75
#
# BY AGENT:
#   ATLAS      |      100,000 tokens | $    0.60
#   FORGE      |       25,000 tokens | $    0.15
```

### Example 2: Budget Alert
```bash
python tokentracker.py budget

# Output:
# === BUDGET STATUS (2026-01) ===
# Budget: $60.00
# Spent: $52.45
# Remaining: $7.55
# Usage: 87.4%
# Status: [WARNING] Over Budget!  <-- Alert when >80%
```

### Example 3: Monthly Report
```bash
python tokentracker.py report month text > monthly_report.txt

# Generates detailed report with:
# - Budget status
# - Total usage by agent
# - Total usage by model
# - Cost breakdown
```

---

## 🎛️ Supported Models & Pricing

TokenTracker automatically calculates costs based on current Claude pricing (January 2026):

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|------------------------|
| `opus-4.5` | $15.00 | $75.00 |
| `sonnet-4.5` | $3.00 | $15.00 |
| `sonnet-3.5` | $3.00 | $15.00 |
| `haiku-3.5` | $0.80 | $4.00 |
| `grok` | $0.00 | $0.00 (Free tier) |
| `gemini` | $0.00 | $0.00 (Extension) |

**Note:** Pricing is configurable in `tokentracker.py` (see `TOKEN_COSTS` dictionary).

---

## 👥 Supported Agents

TokenTracker recognizes these Team Brain agents:

- **FORGE** - Opus 4.5 (Orchestrator)
- **ATLAS** - Sonnet 4.5 (Executor/Builder)
- **CLIO** - Linux/Ubuntu Agent
- **NEXUS** - Multi-platform Agent
- **BOLT** - Cline/Grok (Free Executor)
- **GEMINI** - Extension Agent
- **LOGAN** - Human oversight

**Note:** You can log usage for any agent name, but unknown agents will trigger a warning.

---

## 🛡️ Security Features

TokenTracker includes robust validation to prevent misuse:

- ✅ **Input Validation** - Rejects negative or excessive token counts
- ✅ **SQL Injection Protection** - Blocks malicious agent names
- ✅ **Budget Limits** - Prevents unreasonable budget values
- ✅ **Month Format Validation** - Ensures correct YYYY-MM format
- ✅ **Token Caps** - Maximum 10M tokens per session

---

## 📁 Data Storage

TokenTracker uses SQLite for local storage:

- **Location:** `token_usage.db` (same directory as script)
- **Tables:**
  - `usage_log` - All token usage entries
  - `budget` - Monthly budget tracking
  - `agents` - Agent profiles (future use)

### Backup Your Data
```bash
# Backup database
cp token_usage.db token_usage_backup_$(date +%Y%m%d).db

# View database directly
sqlite3 token_usage.db "SELECT * FROM usage_log LIMIT 10;"
```

---

## 🔧 Advanced Usage

### Custom Database Location
```python
from tokentracker import TokenTracker
from pathlib import Path

# Use custom database path
tracker = TokenTracker(db_path=Path("/path/to/custom/tokens.db"))
```

### Session Tracking
```python
# Track a specific session
session_id = "atlas_2026-01-17_session1"

tracker.log_usage(
    agent="ATLAS",
    model="sonnet-4.5",
    input_tokens=25000,
    output_tokens=8000,
    session_id=session_id,
    notes="Built SynapseLink integration"
)
```

### Batch Import
```python
import json

# Import usage from external log
with open("external_usage.json") as f:
    entries = json.load(f)

for entry in entries:
    tracker.log_usage(
        agent=entry["agent"],
        model=entry["model"],
        input_tokens=entry["input"],
        output_tokens=entry["output"],
        notes=entry.get("notes")
    )
```

---

## 🎯 Use Cases

### For AI Agents
```bash
# Log at end of each session
python tokentracker.py log $AGENT_NAME $MODEL $INPUT_TOKENS $OUTPUT_TOKENS "$TASK_DESCRIPTION"

# Check if approaching budget limit before starting large task
python tokentracker.py budget | grep "Status"
```

### For Human Operators
```bash
# Daily cost review
python tokentracker.py summary today

# Weekly team review
python tokentracker.py report week text | mail -s "Weekly AI Usage Report" team@company.com

# Budget planning
python tokentracker.py set-budget $(date +%Y-%m -d "next month") 75.00
```

### For Automation
```python
from tokentracker import TokenTracker

tracker = TokenTracker()

# Auto-alert if over budget
budget = tracker.get_budget_status()
if budget['percent_used'] > 80:
    send_alert(f"AI budget at {budget['percent_used']:.1f}% - ${budget['remaining']:.2f} remaining")
```

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'tokentracker'"
**Solution:** Ensure you're running from the correct directory or add to PYTHONPATH:
```bash
export PYTHONPATH="/path/to/TokenTracker:$PYTHONPATH"
```

### Issue: "ValueError: Input tokens cannot be negative"
**Solution:** This is intentional validation. Check your token counts are positive integers.

### Issue: Database locked
**Solution:** Close any other processes accessing `token_usage.db`:
```bash
lsof token_usage.db  # Unix/Mac
# Kill the process if needed
```

### Issue: Budget shows wrong month
**Solution:** Set budget explicitly:
```bash
python tokentracker.py set-budget $(date +%Y-%m) 60.00
```

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built by **Team Brain** (Atlas/Sonnet 4.5)
- Part of the **Holy Grail Automation** project
- Inspired by the need for AI agents to self-monitor resource usage
- Follows the **Test-Break-Optimize** development methodology

---

## 📞 Support

- **Issues:** https://github.com/DonkRonk17/TokenTracker/issues
- **Discussions:** https://github.com/DonkRonk17/TokenTracker/discussions
- **Email:** [Your contact email]

---

## 🗺️ Roadmap

- [ ] Web dashboard for visualizing usage
- [ ] Integration with SynapseLink for AI-to-AI alerts
- [ ] Support for more AI models (OpenAI, Anthropic API updates)
- [ ] Cost prediction based on historical usage
- [ ] Multi-currency support
- [ ] Team/organization features
- [ ] Automated budget recommendations

---

## 🙏 Credits

Created by **Randell Logan Smith and Team Brain** at [Metaphy LLC](https://metaphysicsandcomputing.com)

Part of the HMSS (Heavenly Morning Star System) ecosystem.

---

**Built with ❤️ by Team Brain - Autonomous AI agents building tools for AI agents**
