# TokenTracker - Integration Plan

## 🎯 INTEGRATION GOALS

This document outlines how TokenTracker integrates with:
1. Team Brain agents (Forge, Atlas, Clio, Nexus, Bolt)
2. Existing Team Brain tools
3. BCH (Beacon Command Hub) - future potential
4. Logan's workflows and budget management

---

## 📖 ABOUT THIS DOCUMENT

**Document Purpose:** Complete integration guide for adopting TokenTracker across Team Brain ecosystem

**Target Audience:** AI agents, human operators, automation developers

**Last Updated:** January 22, 2026

**Maintained By:** Atlas (Team Brain)

---

## 📦 BCH INTEGRATION

### Overview

TokenTracker has **significant BCH integration potential** as the cost monitoring backbone for all AI agent operations.

**Current Status:** Not yet integrated with BCH  
**Planned Integration:** Phase 3 (BCH as Control Center)

### BCH Integration Architecture

```
BCH Desktop/Mobile
    │
    ├── Token Dashboard Panel
    │   ├── Real-time spend counter
    │   ├── Budget progress bar
    │   ├── Per-agent breakdown chart
    │   └── Cost alert notifications
    │
    ├── Agent Panels
    │   ├── Each agent shows token usage
    │   └── "Log Session" button for manual entry
    │
    └── Admin Panel
        ├── Set/modify budgets
        ├── View historical reports
        └── Export usage data
```

### Proposed BCH Commands

Once integrated, users could interact via BCH:

```
# View budget status
@tokentracker budget

# Log usage manually
@tokentracker log ATLAS sonnet-4.5 50000 15000 "Task description"

# Generate report
@tokentracker report month

# Set budget
@tokentracker set-budget 2026-02 75.00
```

### Implementation Steps (Future)

1. **Phase 3 Milestone:** Add TokenTracker to BCH backend API
2. **REST Endpoints:**
   - `GET /api/tokens/budget` - Current budget status
   - `POST /api/tokens/log` - Log usage
   - `GET /api/tokens/summary/{period}` - Usage summary
   - `GET /api/tokens/report/{period}` - Full report
3. **UI Components:**
   - Token dashboard widget
   - Budget progress bar
   - Agent usage chart
4. **Notifications:**
   - Push alerts when budget > 80%
   - Critical alerts at 95%

### Why BCH Integration Matters

- **Centralized Monitoring:** Logan can see all agent spending from one place
- **Real-time Visibility:** Live updates as agents use tokens
- **Proactive Alerts:** Mobile notifications before budget overrun
- **Historical Analysis:** Trend analysis in BCH dashboard

---

## 🤖 AI AGENT INTEGRATION

### Integration Matrix

| Agent | Primary Use Case | Integration Method | Priority | Status |
|-------|------------------|-------------------|----------|--------|
| **FORGE** | Cost oversight during orchestration | Python API + CLI | HIGH | Ready |
| **ATLAS** | Log builds, track project costs | Python API | HIGH | Ready |
| **CLIO** | Log Ubuntu/Linux sessions | CLI | MEDIUM | Ready |
| **NEXUS** | Cross-platform tracking | Python API + CLI | MEDIUM | Ready |
| **BOLT** | Track free tier usage | CLI | LOW | Ready |
| **GEMINI** | Track extension usage | CLI | LOW | Ready |

### Agent-Specific Workflows

---

#### FORGE (Orchestrator / Reviewer)

**Primary Use Case:** Monitor team budget, review costs before approving expensive tasks

**Why FORGE Needs TokenTracker:**
- FORGE uses Opus 4.5 ($15/$75 per 1M tokens) - most expensive model
- As orchestrator, FORGE approves work that consumes budget
- Budget awareness enables smarter task delegation

**Integration Steps:**

1. **Add to session startup:**
```python
from tokentracker import TokenTracker

def forge_startup():
    tracker = TokenTracker()
    budget = tracker.get_budget_status()
    
    print(f"[FORGE] Budget Status: ${budget['spent']:.2f} / ${budget['budget']:.2f}")
    print(f"[FORGE] Remaining: ${budget['remaining']:.2f} ({100 - budget['percent_used']:.1f}%)")
    
    if not budget['on_track']:
        print("[!] WARNING: Budget > 80% - Consider delegating to cheaper agents")
```

2. **Pre-task cost estimation:**
```python
def estimate_task_cost(estimated_input, estimated_output, model="opus-4.5"):
    tracker = TokenTracker()
    cost = tracker._calculate_cost(model, estimated_input, estimated_output)
    
    budget = tracker.get_budget_status()
    if cost > budget['remaining']:
        return {"approved": False, "reason": "Exceeds remaining budget"}
    
    return {"approved": True, "estimated_cost": cost}
```

3. **Session end logging:**
```python
def forge_session_end(input_tokens, output_tokens, task_summary):
    tracker = TokenTracker()
    tracker.log_usage(
        agent="FORGE",
        model="opus-4.5",
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        notes=f"[Orchestration] {task_summary}"
    )
```

**Typical FORGE Session:**
- Input: 20,000-40,000 tokens (reading code, context)
- Output: 8,000-15,000 tokens (detailed reviews)
- Cost per session: $0.90 - $1.80

---

#### ATLAS (Executor / Builder)

**Primary Use Case:** Log all tool builds, track Holy Grail automation costs

**Why ATLAS Needs TokenTracker:**
- ATLAS is the primary executor - highest volume of work
- Builds tools that consume consistent token budgets
- Holy Grail automation benefits from automatic logging

**Integration Steps:**

1. **Import in tool-building sessions:**
```python
import sys
sys.path.insert(0, r'C:\Users\logan\OneDrive\Documents\AutoProjects\TokenTracker')
from tokentracker import TokenTracker
```

2. **Holy Grail Automation integration:**
```python
# In auto_cursor_prompt_v2.py or equivalent

def log_project_build(project_name, input_tokens, output_tokens):
    """Log token usage for automated project builds."""
    tracker = TokenTracker()
    tracker.log_usage(
        agent="ATLAS",
        model="sonnet-4.5",
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        session_id=f"holy_grail_{datetime.now().strftime('%Y%m%d')}",
        notes=f"Holy Grail: {project_name}"
    )
    print(f"[TokenTracker] Logged {project_name} build: {input_tokens + output_tokens:,} tokens")

# Call at end of each project
log_project_build("TokenTracker", 50000, 15000)
```

3. **Budget check before expensive operations:**
```python
def atlas_should_proceed(estimated_cost):
    tracker = TokenTracker()
    budget = tracker.get_budget_status()
    
    if budget['remaining'] < estimated_cost:
        print(f"[ATLAS] Insufficient budget: ${budget['remaining']:.2f} < ${estimated_cost:.2f}")
        print(f"[ATLAS] Consider using BOLT (free) for this task")
        return False
    
    return True
```

**Typical ATLAS Session:**
- Input: 40,000-60,000 tokens (large codebases, docs)
- Output: 10,000-20,000 tokens (code generation, tests)
- Cost per session: $0.30 - $0.45

---

#### CLIO (Linux / Ubuntu Agent)

**Primary Use Case:** Log Ubuntu testing sessions, CLI automation

**Platform Considerations:**
- CLIO runs on Linux - may need to clone TokenTracker from GitHub
- Database path should use Linux conventions
- Shell scripts for automation

**Integration Steps:**

1. **Clone to Ubuntu:**
```bash
cd ~/projects
git clone https://github.com/DonkRonk17/TokenTracker.git
cd TokenTracker
```

2. **Bash wrapper for easy logging:**
```bash
#!/bin/bash
# save as ~/bin/ttlog

cd ~/projects/TokenTracker
python3 tokentracker.py log CLIO "$1" "$2" "$3" "$4"
```

Usage:
```bash
# After session
ttlog haiku-3.5 10000 5000 "Tested SynapseLink on Ubuntu"
```

3. **Budget check alias:**
```bash
# Add to ~/.bashrc
alias ttbudget='python3 ~/projects/TokenTracker/tokentracker.py budget'
alias ttsummary='python3 ~/projects/TokenTracker/tokentracker.py summary today'
```

**Typical CLIO Session:**
- Input: 10,000-25,000 tokens (testing, execution logs)
- Output: 4,000-10,000 tokens (test results, fixes)
- Cost per session (haiku): $0.05 - $0.08

---

#### NEXUS (Multi-Platform Agent)

**Primary Use Case:** Track cross-platform testing, integration work

**Platform Considerations:**
- Runs on Windows, Linux, and macOS
- Should use platform-agnostic database paths
- Notes field useful for tracking platform

**Integration Steps:**

1. **Platform-aware initialization:**
```python
from tokentracker import TokenTracker
from pathlib import Path
import platform

def get_nexus_tracker():
    # Use platform-specific path if needed
    if platform.system() == "Windows":
        db_path = Path.home() / "Documents/AutoProjects/TokenTracker/token_usage.db"
    else:
        db_path = Path.home() / "projects/TokenTracker/token_usage.db"
    
    return TokenTracker(db_path=db_path)
```

2. **Platform-tagged logging:**
```python
def nexus_log(model, input_tokens, output_tokens, task):
    tracker = get_nexus_tracker()
    platform_name = platform.system()
    
    tracker.log_usage(
        agent="NEXUS",
        model=model,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        notes=f"[{platform_name}] {task}"
    )
```

**Typical NEXUS Session:**
- Input: 15,000-35,000 tokens (multi-platform docs, tests)
- Output: 6,000-14,000 tokens (platform-specific fixes)
- Cost per session: $0.18 - $0.36

---

#### BOLT (Cline / Free Executor)

**Primary Use Case:** Track free tier usage to demonstrate value

**Why Log Free Usage:**
- Shows BOLT's contribution to team productivity
- Helps identify tasks to offload (free = good!)
- Tracks total team token usage for reporting

**Integration Steps:**

1. **Simple CLI logging:**
```bash
# After completing task
python tokentracker.py log BOLT grok 15000 5000 "Generated branding images"
```

2. **Cline integration (if supported):**
```python
# Post-task hook
def bolt_task_complete(task_name, input_tokens, output_tokens):
    tracker = TokenTracker()
    tracker.log_usage(
        agent="BOLT",
        model="grok",
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        notes=f"[Cline] {task_name}"
    )
    # Note: cost will be $0.00
```

**Typical BOLT Session:**
- Input: 10,000-20,000 tokens (task instructions, context)
- Output: 4,000-8,000 tokens (execution logs, results)
- Cost per session: $0.00 (FREE!)

---

## 🔗 INTEGRATION WITH OTHER TEAM BRAIN TOOLS

### With SynapseLink

**Notification Use Case:** Automatic budget alerts and weekly reports to Team Brain

**Integration Pattern:**
```python
import sys
sys.path.insert(0, r'C:\Users\logan\OneDrive\Documents\AutoProjects\TokenTracker')
sys.path.insert(0, r'C:\Users\logan\OneDrive\Documents\AutoProjects\SynapseLink')
from tokentracker import TokenTracker
from synapselink import quick_send

def check_and_alert_budget():
    """Send Synapse alert if budget is critical."""
    tracker = TokenTracker()
    budget = tracker.get_budget_status()
    
    if budget['percent_used'] >= 80:
        alert = f"""
        [!] BUDGET ALERT: {budget['percent_used']:.1f}% Used
        
        Spent: ${budget['spent']:.2f}
        Remaining: ${budget['remaining']:.2f}
        
        Recommended: Defer non-urgent tasks or use BOLT
        """
        
        priority = "CRITICAL" if budget['percent_used'] >= 95 else "HIGH"
        quick_send('ALL', 'Budget Alert', alert, priority=priority, agent='TOKENTRACKER')

def send_weekly_report():
    """Send weekly token usage report via Synapse."""
    tracker = TokenTracker()
    summary = tracker.get_usage_summary("week")
    budget = tracker.get_budget_status()
    
    report = f"""
    WEEKLY TOKEN USAGE REPORT
    
    Budget: ${budget['spent']:.2f} / ${budget['budget']:.2f} ({budget['percent_used']:.1f}%)
    This Week: {summary['total_tokens']:,} tokens (${summary['total_cost']:.2f})
    Sessions: {summary['sessions']}
    """
    
    quick_send('ALL', 'Weekly Token Report', report, priority='NORMAL', agent='TOKENTRACKER')
```

---

### With AgentHealth

**Correlation Use Case:** Link token usage with agent health metrics

**Integration Pattern:**
```python
from agenthealth import AgentHealth
from tokentracker import TokenTracker

def complete_session_with_health(agent, model, input_tokens, output_tokens, task):
    """Log both token usage and health metrics."""
    tracker = TokenTracker()
    health = AgentHealth()
    
    # Shared session ID for correlation
    session_id = f"{agent.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Log token usage
    tracker.log_usage(
        agent=agent,
        model=model,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        session_id=session_id,
        notes=task
    )
    
    # Log health checkpoint
    health.heartbeat(agent, status="session_complete")
    health.log_activity(agent, "session_complete", {
        "session_id": session_id,
        "tokens": input_tokens + output_tokens,
        "task": task
    })
```

---

### With TaskQueuePro

**Task Cost Tracking Use Case:** Associate token costs with specific tasks

**Integration Pattern:**
```python
from taskqueuepro import TaskQueuePro
from tokentracker import TokenTracker

def complete_task_with_tokens(task_id, agent, model, input_tokens, output_tokens):
    """Complete task and log associated token cost."""
    tracker = TokenTracker()
    queue = TaskQueuePro()
    
    # Get task details
    task = queue.get_task(task_id)
    
    # Log usage with task reference
    tracker.log_usage(
        agent=agent,
        model=model,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        session_id=f"task_{task_id}",
        notes=f"[TaskQueue] {task['title']}"
    )
    
    # Update task with cost info
    cost = tracker._calculate_cost(model, input_tokens, output_tokens)
    queue.complete_task(task_id, result={
        "tokens": input_tokens + output_tokens,
        "cost": cost
    })
```

---

### With MemoryBridge

**Data Persistence Use Case:** Sync token usage to Memory Core

**Integration Pattern:**
```python
from memorybridge import MemoryBridge
from tokentracker import TokenTracker

def sync_tokens_to_memory():
    """Sync daily token summary to Memory Core."""
    tracker = TokenTracker()
    memory = MemoryBridge()
    
    summary = tracker.get_usage_summary("today")
    budget = tracker.get_budget_status()
    
    # Store in memory core
    memory.set("token_tracker_daily", {
        "date": datetime.now().isoformat(),
        "tokens": summary['total_tokens'],
        "cost": summary['total_cost'],
        "budget_percent": budget['percent_used'],
        "agents": summary['agents']
    })
    
    memory.sync()
```

---

### With SessionReplay

**Debugging Use Case:** Replay expensive sessions to understand costs

**Integration Pattern:**
```python
from sessionreplay import SessionReplay
from tokentracker import TokenTracker

def start_tracked_session(agent, task):
    """Start a session with both replay and token tracking."""
    replay = SessionReplay()
    tracker = TokenTracker()
    
    session_id = replay.start_session(agent, task)
    
    # Store session ID for later token logging
    return session_id

def end_tracked_session(session_id, agent, model, input_tokens, output_tokens, task):
    """End session and log both replay and tokens."""
    replay = SessionReplay()
    tracker = TokenTracker()
    
    # Log tokens with session reference
    tracker.log_usage(
        agent=agent,
        model=model,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        session_id=session_id,
        notes=task
    )
    
    # End replay session
    replay.end_session(session_id, status="COMPLETED")
```

---

### With ContextCompressor

**Token Optimization Use Case:** Measure savings from compression

**Integration Pattern:**
```python
from contextcompressor import ContextCompressor
from tokentracker import TokenTracker

def measure_compression_savings(text, agent, model):
    """Measure and log token savings from compression."""
    compressor = ContextCompressor()
    tracker = TokenTracker()
    
    # Compress the text
    compressed = compressor.compress_text(text, method="summary")
    
    # Calculate savings
    original_tokens = compressor.count_tokens(text)
    compressed_tokens = compressor.count_tokens(compressed.compressed_text)
    saved_tokens = original_tokens - compressed_tokens
    
    # Log the compressed (smaller) version
    tracker.log_usage(
        agent=agent,
        model=model,
        input_tokens=compressed_tokens,
        output_tokens=0,
        notes=f"[Compressed] Saved {saved_tokens:,} tokens ({compressed.compression_ratio:.1f}%)"
    )
    
    return compressed.compressed_text
```

---

### With ConfigManager

**Configuration Use Case:** Centralize TokenTracker settings

**Integration Pattern:**
```python
from configmanager import ConfigManager
from tokentracker import TokenTracker

def get_configured_tracker():
    """Get TokenTracker with settings from ConfigManager."""
    config = ConfigManager()
    
    # Get TokenTracker config
    tt_config = config.get("tokentracker", {
        "default_budget": 60.0,
        "alert_threshold": 0.8,
        "db_path": None  # Use default
    })
    
    tracker = TokenTracker(db_path=tt_config.get("db_path"))
    
    # Set budget if configured
    if tt_config.get("default_budget"):
        month = datetime.now().strftime("%Y-%m")
        tracker.set_budget(month, tt_config["default_budget"])
    
    return tracker
```

---

### With CollabSession

**Multi-Agent Tracking Use Case:** Track token usage across collaborative sessions

**Integration Pattern:**
```python
from collabsession import CollabSession
from tokentracker import TokenTracker

def collab_session_with_tracking(participants, task):
    """Start collaborative session with shared token tracking."""
    collab = CollabSession()
    tracker = TokenTracker()
    
    # Start collaboration
    session_id = collab.start_session(f"collab_{task}", participants)
    
    # Each agent logs with shared session_id
    def log_participant_usage(agent, model, input_tokens, output_tokens):
        tracker.log_usage(
            agent=agent,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            session_id=session_id,
            notes=f"[Collab:{task}] {agent} contribution"
        )
    
    return session_id, log_participant_usage
```

---

## 🚀 ADOPTION ROADMAP

### Phase 1: Core Adoption (Week 1)

**Goal:** All agents aware and can use basic features

**Steps:**
1. ✓ Tool deployed to GitHub
2. ☐ Quick-start guides sent via Synapse
3. ☐ Each agent tests basic workflow
4. ☐ Feedback collected

**Success Criteria:**
- All 5 agents have logged at least one session
- No blocking issues reported
- Budget status accessible to all

**Assigned To:** ATLAS (coordinator), All agents (participants)

---

### Phase 2: Integration (Week 2-3)

**Goal:** Integrated into daily workflows

**Steps:**
1. ☐ Add to agent startup routines
2. ☐ Create SynapseLink + TokenTracker automation
3. ☐ Implement budget alert system
4. ☐ Set up weekly report generation

**Success Criteria:**
- Used daily by at least 3 agents
- Budget alerts functioning
- Weekly reports automated

**Assigned To:** ATLAS (automation), FORGE (oversight)

---

### Phase 3: Optimization (Week 4+)

**Goal:** Optimized and fully adopted

**Steps:**
1. ☐ Collect efficiency metrics
2. ☐ Identify expensive operations to optimize
3. ☐ Create dashboard or report templates
4. ☐ Document cost patterns and recommendations

**Success Criteria:**
- Measurable cost insights
- Optimization recommendations documented
- Team using data to make decisions

**Assigned To:** FORGE (analysis), ATLAS (implementation)

---

### Phase 4: BCH Integration (Future)

**Goal:** Full BCH integration

**Steps:**
1. ☐ Add TokenTracker API to BCH backend
2. ☐ Build dashboard UI components
3. ☐ Implement real-time updates
4. ☐ Mobile notifications for alerts

**Success Criteria:**
- Logan can view budget from BCH Desktop/Mobile
- Real-time cost visibility
- Push notifications working

**Assigned To:** IRIS (Desktop), PORTER (Mobile), CLIO (Backend)

---

## 📊 SUCCESS METRICS

### Adoption Metrics

| Metric | Target | Tracking Method |
|--------|--------|-----------------|
| Agents logging daily | 3+ | Query usage_log table |
| Sessions logged per week | 20+ | Weekly report |
| Budget compliance | Stay under $60/mo | Budget status |

### Efficiency Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| FORGE cost per review | < $2.00 | Filter by agent + notes |
| ATLAS cost per build | < $0.50 | Filter by agent + notes |
| BOLT utilization | 20%+ of simple tasks | Compare BOLT vs ATLAS usage |

### Quality Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Budget overruns | 0 per month | Budget alerts triggered |
| Logging consistency | 90%+ sessions logged | Compare to expected sessions |
| Report accuracy | No discrepancies | Periodic audit |

---

## 🛠️ TECHNICAL INTEGRATION DETAILS

### Import Paths

```python
# Standard import (from TokenTracker directory)
from tokentracker import TokenTracker

# Import from another project
import sys
sys.path.insert(0, r'C:\Users\logan\OneDrive\Documents\AutoProjects\TokenTracker')
from tokentracker import TokenTracker

# Linux import
sys.path.insert(0, '/home/user/projects/TokenTracker')
from tokentracker import TokenTracker
```

### Configuration Integration

**Config File:** `token_usage.db` (SQLite, same directory as script)

**Shared Config with ConfigManager:**
```json
{
  "tokentracker": {
    "default_budget": 60.0,
    "alert_threshold": 0.8,
    "db_path": null,
    "models": {
      "opus-4.5": {"input": 15.00, "output": 75.00},
      "sonnet-4.5": {"input": 3.00, "output": 15.00}
    }
  }
}
```

### Error Handling Integration

**Standardized Error Codes:**
- 0: Success
- 1: General error
- 2: Validation error (invalid input)
- 3: Database error
- 4: Budget exceeded

**Error Response Format:**
```python
try:
    tracker.log_usage(...)
except ValueError as e:
    print(f"[ERROR] Validation failed: {e}")
    sys.exit(2)
except sqlite3.Error as e:
    print(f"[ERROR] Database error: {e}")
    sys.exit(3)
```

### Logging Integration

**Log Format:** Console output with status indicators

**Log Levels:**
- `[OK]` - Success
- `[WARNING]` - Non-critical issue
- `[ERROR]` - Operation failed

**Log Location:** stdout (can be redirected to file)

---

## 🔧 MAINTENANCE & SUPPORT

### Update Strategy

- **Minor updates (v1.x):** Monthly, as pricing changes
- **Major updates (v2.0+):** Quarterly, with BCH integration
- **Security patches:** Immediate

### Support Channels

- **GitHub Issues:** Bug reports and feature requests
- **Synapse:** Team Brain discussions
- **Direct to ATLAS:** Complex issues or integration help

### Known Limitations

1. **No real-time token capture:** Agents must manually log or estimate
2. **Local database:** Each machine has separate database (sync manually)
3. **Single currency:** USD only (multi-currency planned for v2)
4. **No web dashboard:** CLI and Python API only (BCH integration planned)

### Planned Improvements

1. **v1.1:** Auto-sync database across machines
2. **v1.2:** Token estimation from text length
3. **v2.0:** BCH integration with dashboard
4. **v2.1:** Historical trend analysis

---

## 📚 ADDITIONAL RESOURCES

- **Main Documentation:** [README.md](README.md)
- **Usage Examples:** [EXAMPLES.md](EXAMPLES.md)
- **Quick Start Guides:** [QUICK_START_GUIDES.md](QUICK_START_GUIDES.md)
- **Integration Examples:** [INTEGRATION_EXAMPLES.md](INTEGRATION_EXAMPLES.md)
- **Cheat Sheet:** [CHEAT_SHEET.txt](CHEAT_SHEET.txt)
- **GitHub:** https://github.com/DonkRonk17/TokenTracker

---

## 📝 CREDITS

**Built by:** Atlas (Team Brain)  
**For:** Logan Smith / Metaphy LLC  
**Requested by:** Self-initiated (Q-Mode Tool #6)  
**Why:** Enable AI agents to track and manage their own resource consumption against $60/mo budget  
**Part of:** Beacon HQ / Team Brain Ecosystem  
**Date:** January 17, 2026 (Original) / January 22, 2026 (Integration Plan)

---

**Last Updated:** January 22, 2026  
**Maintained By:** Atlas (Team Brain)  
**Document Version:** 1.0
