# TokenTracker - Integration Examples

How to integrate TokenTracker into existing Team Brain workflows

---

## 🎯 INTEGRATION PATTERN 1: End-of-Session Logging

### Scenario
Agent completes a task and needs to log token usage before ending session.

### Implementation

**Manual (CLI):**
```bash
# At end of your session
python tokentracker.py log YOUR_AGENT YOUR_MODEL INPUT_TOKENS OUTPUT_TOKENS "Task completed"

# Example
python tokentracker.py log ATLAS sonnet-4.5 50000 15000 "Built TokenTracker v1.0"
```

**Automated (Python):**
```python
# Add to your session cleanup code
from tokentracker import TokenTracker

def log_and_exit(agent, model, input_tokens, output_tokens, task_summary):
    tracker = TokenTracker()
    tracker.log_usage(agent, model, input_tokens, output_tokens, notes=task_summary)
    print(f"[Session Complete] Logged {input_tokens + output_tokens:,} tokens")

# Call before exiting
log_and_exit("ATLAS", "sonnet-4.5", 50000, 15000, "Built TokenTracker v1.0")
```

---

## 🎯 INTEGRATION PATTERN 2: Pre-Task Budget Check

### Scenario
Agent wants to check if there's enough budget before starting an expensive task.

### Implementation

```python
from tokentracker import TokenTracker

def should_proceed_with_task(estimated_cost_usd):
    tracker = TokenTracker()
    budget = tracker.get_budget_status()
    
    if budget['remaining'] < estimated_cost_usd:
        print(f"[BUDGET WARNING] Only ${budget['remaining']:.2f} remaining, task costs ~${estimated_cost_usd:.2f}")
        print(f"Current usage: {budget['percent_used']:.1f}%")
        return False
    
    return True

# Before expensive operation
if should_proceed_with_task(5.00):  # Task estimated at $5
    # Proceed with task
    do_expensive_operation()
else:
    print("Deferring task due to budget constraints")
```

**Usage Example:**
```python
# FORGE before large code review
if should_proceed_with_task(2.00):  # Review costs ~$2
    review_atlas_code()
    log_and_exit("FORGE", "opus-4.5", 30000, 10000, "Code review")
else:
    defer_review_to_atlas()  # Use cheaper Sonnet instead
```

---

## 🎯 INTEGRATION PATTERN 3: Holy Grail Automation Integration

### Scenario
Atlas runs Holy Grail Automation and wants to automatically log each project build.

### Implementation

Add to `auto_cursor_prompt_v2.py` (or equivalent):

```python
import sys
sys.path.insert(0, r'C:\Users\logan\OneDrive\Documents\AutoProjects\TokenTracker')
from tokentracker import TokenTracker

def log_project_build(project_name, input_tokens, output_tokens):
    """Log token usage for automated project builds."""
    tracker = TokenTracker()
    tracker.log_usage(
        agent="ATLAS",
        model="sonnet-4.5",
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        session_id=f"holy_grail_{project_name}",
        notes=f"Holy Grail: Built {project_name}"
    )
    print(f"[TokenTracker] Logged {project_name} build: {input_tokens + output_tokens:,} tokens")

# Call at end of each project build
log_project_build("TokenTracker", 50000, 15000)
```

---

## 🎯 INTEGRATION PATTERN 4: Weekly Team Report

### Scenario
Generate and share weekly token usage report with team.

### Implementation

**Script: `weekly_report.py`**
```python
from tokentracker import TokenTracker
import sys
sys.path.insert(0, r'C:\Users\logan\OneDrive\Documents\AutoProjects\SynapseLink')
from synapselink import quick_send

def generate_and_send_weekly_report():
    tracker = TokenTracker()
    budget = tracker.get_budget_status()
    summary = tracker.get_usage_summary("week")
    
    # Build report
    report = f"""
    📊 TEAM BRAIN - WEEKLY TOKEN USAGE REPORT
    
    Budget Status:
    - Monthly Budget: ${budget['budget']:.2f}
    - Spent This Month: ${budget['spent']:.2f}
    - Remaining: ${budget['remaining']:.2f}
    - Usage: {budget['percent_used']:.1f}%
    
    This Week's Usage:
    - Total Tokens: {summary['total_tokens']:,}
    - Total Cost: ${summary['total_cost']:.2f}
    - Sessions: {summary['sessions']}
    
    By Agent:
    """
    
    for agent in summary['agents']:
        report += f"\n    {agent['agent']}: {agent['tokens']:,} tokens (${agent['cost']:.2f})"
    
    # Send via SynapseLink
    quick_send('ALL', 'Weekly Token Usage Report', report, priority='NORMAL', agent='ATLAS')
    print("[OK] Weekly report sent to Team Brain")

# Run weekly (e.g., Sunday night)
generate_and_send_weekly_report()
```

**Schedule with cron (Linux) or Task Scheduler (Windows):**
```bash
# Run every Sunday at 11:59 PM
0 23 * * 0 python /path/to/weekly_report.py
```

---

## 🎯 INTEGRATION PATTERN 5: Budget Alert Automation

### Scenario
Automatically alert Team Brain when budget reaches 80%.

### Implementation

**Script: `budget_monitor.py`**
```python
from tokentracker import TokenTracker
import sys
sys.path.insert(0, r'C:\Users\logan\OneDrive\Documents\AutoProjects\SynapseLink')
from synapselink import quick_send

def check_and_alert_budget():
    tracker = TokenTracker()
    budget = tracker.get_budget_status()
    
    if budget['percent_used'] >= 80 and budget['percent_used'] < 85:
        # First alert at 80%
        alert = f"""
        ⚠️ BUDGET ALERT: 80% Threshold Reached
        
        We've used {budget['percent_used']:.1f}% of our monthly budget.
        
        Details:
        - Budget: ${budget['budget']:.2f}
        - Spent: ${budget['spent']:.2f}
        - Remaining: ${budget['remaining']:.2f}
        
        Recommended Actions:
        1. Defer non-urgent tasks
        2. Use BOLT (free tier) for simple tasks
        3. Optimize expensive operations
        4. Review usage patterns for waste
        
        Check details: python tokentracker.py report month text
        """
        quick_send('ALL', '⚠️ BUDGET ALERT: 80% Used', alert, priority='HIGH', agent='TOKENTRACKER')
        
    elif budget['percent_used'] >= 95:
        # Critical alert at 95%
        alert = f"""
        🚨 CRITICAL BUDGET ALERT: 95% Used!
        
        We've used {budget['percent_used']:.1f}% of our monthly budget.
        Only ${budget['remaining']:.2f} remaining!
        
        IMMEDIATE ACTIONS REQUIRED:
        1. STOP all non-critical operations
        2. Defer ALL tasks until next month
        3. Logan needs to approve any additional usage
        
        Current spend: ${budget['spent']:.2f} / ${budget['budget']:.2f}
        """
        quick_send('ALL', '🚨 CRITICAL: 95% Budget Used!', alert, priority='CRITICAL', agent='TOKENTRACKER')

# Run every hour
check_and_alert_budget()
```

**Schedule:**
```bash
# Run every hour
0 * * * * python /path/to/budget_monitor.py
```

---

## 🎯 INTEGRATION PATTERN 6: Session Token Estimation

### Scenario
Agent doesn't have exact token counts but wants to estimate.

### Implementation

```python
def estimate_tokens(text_length_chars):
    """Estimate tokens from character count (rough approximation)."""
    # Average: 1 token ≈ 4 characters (varies by language/content)
    return text_length_chars // 4

def estimate_session_cost(input_text, output_text, model):
    """Estimate cost for a session based on text length."""
    from tokentracker import TokenTracker
    
    input_tokens = estimate_tokens(len(input_text))
    output_tokens = estimate_tokens(len(output_text))
    
    tracker = TokenTracker()
    cost = tracker._calculate_cost(model, input_tokens, output_tokens)
    
    return input_tokens, output_tokens, cost

# Usage
input_text = "... all your input context ..."
output_text = "... all your generated output ..."

input_est, output_est, cost_est = estimate_session_cost(input_text, output_text, "sonnet-4.5")
print(f"Estimated: {input_est:,} input + {output_est:,} output = ${cost_est:.2f}")

# Log estimated values
tracker = TokenTracker()
tracker.log_usage("ATLAS", "sonnet-4.5", input_est, output_est, notes="Estimated tokens")
```

---

## 🎯 INTEGRATION PATTERN 7: Multi-Session Tracking

### Scenario
Agent works on a long task across multiple sessions, wants to track total.

### Implementation

```python
from tokentracker import TokenTracker
import uuid

# Generate session ID at start of task
task_id = f"tokentracker_build_{uuid.uuid4().hex[:8]}"

# Log each sub-session with same session_id
tracker = TokenTracker()

# Session 1: Initial build
tracker.log_usage("ATLAS", "sonnet-4.5", 50000, 15000, session_id=task_id, notes="Initial build")

# Session 2: Testing
tracker.log_usage("ATLAS", "sonnet-4.5", 35000, 12000, session_id=task_id, notes="Testing phase")

# Session 3: Documentation
tracker.log_usage("ATLAS", "sonnet-4.5", 40000, 14000, session_id=task_id, notes="Documentation")

# Query total for this task
import sqlite3
conn = sqlite3.connect("token_usage.db")
cursor = conn.cursor()
cursor.execute("""
    SELECT SUM(total_tokens), SUM(cost_usd) 
    FROM usage_log 
    WHERE session_id = ?
""", (task_id,))
total_tokens, total_cost = cursor.fetchone()
print(f"Total for {task_id}: {total_tokens:,} tokens, ${total_cost:.2f}")
conn.close()
```

---

## 🎯 INTEGRATION PATTERN 8: Export to Spreadsheet

### Scenario
Logan wants to analyze usage in Excel/Google Sheets.

### Implementation

```bash
# Export monthly usage to JSON
python tokentracker.py report month json > usage_jan_2026.json

# Convert to CSV (Python script)
```

**Script: `json_to_csv.py`**
```python
import json
import csv

with open("usage_jan_2026.json") as f:
    data = json.load(f)

# Export agent summary to CSV
with open("usage_by_agent.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Agent", "Sessions", "Tokens", "Cost USD"])
    
    for agent in data['usage']['agents']:
        writer.writerow([
            agent['agent'],
            agent['sessions'],
            agent['tokens'],
            agent['cost']
        ])

print("Exported to usage_by_agent.csv")
```

---

## 🎯 INTEGRATION PATTERN 9: SynapseLink + TokenTracker Combo

### Scenario
Agent logs usage AND notifies team via Synapse in one action.

### Implementation

```python
import sys
sys.path.insert(0, r'C:\Users\logan\OneDrive\Documents\AutoProjects\TokenTracker')
sys.path.insert(0, r'C:\Users\logan\OneDrive\Documents\AutoProjects\SynapseLink')
from tokentracker import TokenTracker
from synapselink import quick_send

def log_and_notify(agent, model, input_tokens, output_tokens, task, notify_team=False):
    """Log usage and optionally notify team."""
    # Log usage
    tracker = TokenTracker()
    tracker.log_usage(agent, model, input_tokens, output_tokens, notes=task)
    
    cost = tracker._calculate_cost(model, input_tokens, output_tokens)
    
    # Notify team if significant usage
    if notify_team or cost > 1.00:  # Notify if over $1
        quick_send(
            'ALL',
            f'{agent} completed: {task}',
            f'Task completed using {input_tokens + output_tokens:,} tokens (${cost:.2f})',
            priority='NORMAL',
            agent=agent
        )

# Usage
log_and_notify("ATLAS", "sonnet-4.5", 50000, 15000, "Built TokenTracker v1.0", notify_team=True)
```

---

## 🎯 INTEGRATION PATTERN 10: Automatic Token Capture (Advanced)

### Scenario
Automatically capture token usage from AI API responses.

### Implementation

**For agents with API access:**
```python
import anthropic
from tokentracker import TokenTracker

def claude_api_call_with_logging(prompt, agent_name):
    """Make Claude API call and automatically log usage."""
    client = anthropic.Anthropic(api_key="your-api-key")
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Extract token usage from response
    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens
    
    # Automatically log to TokenTracker
    tracker = TokenTracker()
    tracker.log_usage(
        agent=agent_name,
        model="sonnet-4.5",
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        notes=f"API call: {prompt[:50]}..."
    )
    
    return response.content[0].text

# Usage
result = claude_api_call_with_logging("Build a new AutoProject", "ATLAS")
```

---

## 📊 RECOMMENDED INTEGRATION PRIORITY

1. **Immediate** (Day 1):
   - End-of-session logging (Pattern 1) ← START HERE
   - Pre-task budget check (Pattern 2)

2. **Short-term** (Week 1):
   - Budget alert automation (Pattern 5)
   - Weekly team report (Pattern 4)

3. **Medium-term** (Month 1):
   - Holy Grail integration (Pattern 3)
   - Multi-session tracking (Pattern 7)

4. **Long-term** (As needed):
   - Automatic token capture (Pattern 10)
   - Export to spreadsheet (Pattern 8)
   - SynapseLink combo (Pattern 9)

---

**Created:** January 17, 2026  
**By:** Atlas (Sonnet 4.5) - Team Brain  
**Version:** 1.0
