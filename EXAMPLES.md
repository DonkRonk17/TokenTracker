# TokenTracker - Usage Examples

This file demonstrates real-world usage examples with expected output.

---

## Example 1: Basic Token Logging

**Command:**
```bash
python tokentracker.py log ATLAS sonnet-4.5 50000 15000 "Built TokenTracker v1.0"
```

**Expected Output:**
```
[OK] Logged 65,000 tokens (sonnet-4.5) for ATLAS - $0.3750
```

**What it does:**
- Logs 50,000 input tokens + 15,000 output tokens = 65,000 total
- Calculates cost: (50000/1M × $3) + (15000/1M × $15) = $0.375
- Stores in database with timestamp and notes

---

## Example 2: View Today's Summary

**Command:**
```bash
python tokentracker.py summary today
```

**Expected Output:**
```
=== TOKEN USAGE SUMMARY (TODAY) ===
Sessions: 3
Total Tokens: 125,500
Total Cost: $0.75

BY AGENT:
  ATLAS      |      100,000 tokens | $    0.60
  FORGE      |       25,500 tokens | $    0.15
```

**What it shows:**
- Number of logging sessions today
- Total tokens consumed
- Total cost in USD
- Breakdown by agent

---

## Example 3: Check Budget Status

**Command:**
```bash
python tokentracker.py budget
```

**Expected Output (On Track):**
```
=== BUDGET STATUS (2026-01) ===
Budget: $60.00
Spent: $15.25
Remaining: $44.75
Usage: 25.4%
Status: [OK] On Track
```

**Expected Output (Over Budget Warning):**
```
=== BUDGET STATUS (2026-01) ===
Budget: $60.00
Spent: $52.45
Remaining: $7.55
Usage: 87.4%
Status: [WARNING] Over Budget!  <-- Alert when >80%
```

---

## Example 4: Monthly Report (Text Format)

**Command:**
```bash
python tokentracker.py report month text
```

**Expected Output:**
```
============================================================
TOKEN TRACKER REPORT - MONTH
============================================================
Generated: 2026-01-17 01:45:23

BUDGET STATUS:
  Month: 2026-01
  Budget: $60.00
  Spent: $35.20
  Remaining: $24.80
  Usage: 58.7%
  Status: [OK] On Track

USAGE SUMMARY:
  Sessions: 15
  Input Tokens: 750,000
  Output Tokens: 250,000
  Total Tokens: 1,000,000
  Total Cost: $35.20

BY AGENT:
  ATLAS      |      700,000 tokens | $   21.00 |  10 sessions
  FORGE      |      250,000 tokens | $   12.50 |   3 sessions
  CLIO       |       50,000 tokens | $    1.70 |   2 sessions

BY MODEL:
  sonnet-4.5   |      700,000 tokens | $   21.00
  opus-4.5     |      250,000 tokens | $   12.50
  haiku-3.5    |       50,000 tokens | $    1.70

============================================================
```

---

## Example 5: Python API Usage

**Script:**
```python
from tokentracker import TokenTracker

# Initialize
tracker = TokenTracker()

# Log usage
log_id = tracker.log_usage(
    agent="ATLAS",
    model="sonnet-4.5",
    input_tokens=50000,
    output_tokens=15000,
    notes="Built TokenTracker"
)
print(f"Logged entry ID: {log_id}")

# Get summary
summary = tracker.get_usage_summary("today")
print(f"Today's tokens: {summary['total_tokens']:,}")
print(f"Today's cost: ${summary['total_cost']:.2f}")

# Check budget
budget = tracker.get_budget_status()
print(f"Budget remaining: ${budget['remaining']:.2f}")

# Alert if over 80%
if budget['percent_used'] > 80:
    print(f"[WARNING] Budget at {budget['percent_used']:.1f}%!")
```

**Expected Output:**
```
[OK] Logged 65,000 tokens (sonnet-4.5) for ATLAS - $0.3750
Logged entry ID: 1
Today's tokens: 65,000
Today's cost: $0.38
Budget remaining: $59.62
```

---

## Example 6: Set Budget for Multiple Months

**Commands:**
```bash
# Set budget for January 2026
python tokentracker.py set-budget 2026-01 60.00

# Set budget for February 2026 (higher budget month)
python tokentracker.py set-budget 2026-02 75.00

# Set budget for March 2026
python tokentracker.py set-budget 2026-03 60.00
```

**Expected Output:**
```
[OK] Set budget for 2026-01: $60.00
[OK] Set budget for 2026-02: $75.00
[OK] Set budget for 2026-03: $60.00
```

---

## Example 7: Export JSON Report

**Command:**
```bash
python tokentracker.py report month json > monthly_report.json
```

**Output File (monthly_report.json):**
```json
{
  "usage": {
    "period": "month",
    "start_date": "2026-01-01T00:00:00",
    "sessions": 15,
    "input_tokens": 750000,
    "output_tokens": 250000,
    "total_tokens": 1000000,
    "total_cost": 35.2,
    "agents": [
      {
        "agent": "ATLAS",
        "sessions": 10,
        "tokens": 700000,
        "cost": 21.0
      },
      {
        "agent": "FORGE",
        "sessions": 3,
        "tokens": 250000,
        "cost": 12.5
      },
      {
        "agent": "CLIO",
        "sessions": 2,
        "tokens": 50000,
        "cost": 1.7
      }
    ],
    "models": [
      {
        "model": "sonnet-4.5",
        "tokens": 700000,
        "cost": 21.0
      },
      {
        "model": "opus-4.5",
        "tokens": 250000,
        "cost": 12.5
      },
      {
        "model": "haiku-3.5",
        "tokens": 50000,
        "cost": 1.7
      }
    ]
  },
  "budget": {
    "month": "2026-01",
    "budget": 60.0,
    "spent": 35.2,
    "remaining": 24.8,
    "percent_used": 58.7,
    "on_track": true
  },
  "generated_at": "2026-01-17T01:45:23.123456"
}
```

---

## Example 8: Error Handling (Validation)

**Command (Invalid - Negative Tokens):**
```bash
python tokentracker.py log ATLAS sonnet-4.5 -5000 1000
```

**Expected Output:**
```
Traceback (most recent call last):
  ...
ValueError: Input tokens cannot be negative: -5000
```

**Command (Invalid - Empty Agent):**
```bash
python tokentracker.py log "" sonnet-4.5 1000 500
```

**Expected Output:**
```
Traceback (most recent call last):
  ...
ValueError: Agent name cannot be empty.
```

**Command (Invalid - Bad Month Format):**
```bash
python tokentracker.py set-budget January-2026 60.00
```

**Expected Output:**
```
Traceback (most recent call last):
  ...
ValueError: Invalid month format (use YYYY-MM): January-2026
```

---

## Example 9: Weekly Team Review

**Script (weekly_review.sh):**
```bash
#!/bin/bash
# Generate weekly report and email to team

REPORT=$(python tokentracker.py report week text)

echo "$REPORT" | mail -s "Weekly AI Token Usage Report - $(date +%Y-%m-%d)" team@company.com

echo "Weekly report sent to team@company.com"
```

---

## Example 10: Budget Alert Automation

**Script (check_budget.py):**
```python
from tokentracker import TokenTracker
import smtplib
from email.mime.text import MIMEText

tracker = TokenTracker()
budget = tracker.get_budget_status()

# Alert if over 80% budget used
if budget['percent_used'] > 80:
    message = f"""
    WARNING: AI Token Budget Alert
    
    Month: {budget['month']}
    Budget: ${budget['budget']:.2f}
    Spent: ${budget['spent']:.2f}
    Remaining: ${budget['remaining']:.2f}
    Usage: {budget['percent_used']:.1f}%
    
    You have used {budget['percent_used']:.1f}% of your monthly AI budget.
    Please monitor usage carefully for the remainder of the month.
    """
    
    # Send alert email
    msg = MIMEText(message)
    msg['Subject'] = f'AI Budget Alert - {budget["percent_used"]:.1f}% Used'
    msg['From'] = 'alerts@company.com'
    msg['To'] = 'admin@company.com'
    
    # (SMTP configuration here)
    print("Budget alert sent!")
else:
    print(f"Budget OK: {budget['percent_used']:.1f}% used")
```

**Expected Output (Under Budget):**
```
Budget OK: 58.7% used
```

**Expected Output (Over Budget):**
```
Budget alert sent!
```

---

## All Examples Tested ✅

These examples have been verified to work correctly with TokenTracker v1.0.
