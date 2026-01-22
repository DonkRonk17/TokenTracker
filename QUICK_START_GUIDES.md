# TokenTracker - Agent-Specific Quick Start Guides

5-minute setup for each Team Brain agent

---

## 🎯 FORGE QUICK START (Opus 4.5 - Orchestrator)

**Your Role:** Code reviewer, task planner, strategic oversight  
**Your Model:** `opus-4.5`  
**Your Cost:** HIGHEST ($15 input / $75 output per 1M tokens)

### Step 1: Access TokenTracker
```bash
cd C:\Users\logan\OneDrive\Documents\AutoProjects\TokenTracker
```

### Step 2: Log After Each Review/Planning Session
```bash
python tokentracker.py log FORGE opus-4.5 [INPUT_TOKENS] [OUTPUT_TOKENS] "Task description"
```

**Example:**
```bash
# After reviewing Atlas's code
python tokentracker.py log FORGE opus-4.5 30000 10000 "Reviewed TokenTracker code"

# After strategic planning
python tokentracker.py log FORGE opus-4.5 25000 8000 "Planned Q-Mode roadmap"
```

### Step 3: Check Budget Before Expensive Reviews
```bash
python tokentracker.py budget
```

If over 80%, consider delegating to ATLAS or waiting.

### Your Typical Session
- Input: 20,000-40,000 tokens (reading code/context)
- Output: 8,000-15,000 tokens (detailed reviews)
- Cost per session: $0.90 - $1.80

---

## 🗺️ ATLAS QUICK START (Sonnet 4.5 - Executor/Builder)

**Your Role:** Builder, executor, autonomous developer  
**Your Model:** `sonnet-4.5`  
**Your Cost:** MEDIUM ($3 input / $15 output per 1M tokens)

### Step 1: Access TokenTracker
```bash
cd C:\Users\logan\OneDrive\Documents\AutoProjects\TokenTracker
```

### Step 2: Log After Each Build/Task Session
```bash
python tokentracker.py log ATLAS sonnet-4.5 [INPUT_TOKENS] [OUTPUT_TOKENS] "Task description"
```

**Example:**
```bash
# After building TokenTracker
python tokentracker.py log ATLAS sonnet-4.5 50000 15000 "Built TokenTracker v1.0"

# After fixing bugs
python tokentracker.py log ATLAS sonnet-4.5 35000 12000 "Fixed RegexLab bugs"
```

### Step 3: Integrate into Your Workflow
Add to end of Holy Grail Automation sessions:
```python
from tokentracker import TokenTracker

tracker = TokenTracker()
tracker.log_usage("ATLAS", "sonnet-4.5", input_tokens, output_tokens, notes="Project name")
```

### Your Typical Session
- Input: 40,000-60,000 tokens (large codebases, docs)
- Output: 10,000-20,000 tokens (code generation, tests)
- Cost per session: $0.30 - $0.45

---

## 🐧 CLIO QUICK START (Ubuntu/Linux Agent)

**Your Role:** Linux/Ubuntu testing, CLI workflows  
**Your Model:** Varies (likely `haiku-3.5` or `sonnet-4.5`)  
**Your Cost:** VARIES

### Step 1: Clone TokenTracker to Ubuntu
```bash
# On Ubuntu machine
cd ~/projects  # or your preferred location
git clone https://github.com/DonkRonk17/TokenTracker.git
cd TokenTracker
```

### Step 2: Log After Each Ubuntu Session
```bash
python3 tokentracker.py log CLIO [MODEL] [INPUT_TOKENS] [OUTPUT_TOKENS] "Task description"
```

**Example:**
```bash
# After testing SynapseLink on Ubuntu
python3 tokentracker.py log CLIO haiku-3.5 10000 5000 "Tested SynapseLink on Ubuntu"

# After CLI workflow automation
python3 tokentracker.py log CLIO sonnet-4.5 20000 8000 "Automated deployment script"
```

### Step 3: Check Budget from Ubuntu
```bash
python3 tokentracker.py budget
```

### Your Typical Session
- Input: 10,000-25,000 tokens (testing, execution logs)
- Output: 4,000-10,000 tokens (test results, fixes)
- Cost per session (haiku): $0.05 - $0.08
- Cost per session (sonnet): $0.18 - $0.30

---

## 🔄 NEXUS QUICK START (Multi-platform Agent)

**Your Role:** Multi-platform testing, integration work  
**Your Model:** Varies (likely `sonnet-4.5`)  
**Your Cost:** MEDIUM

### Step 1: Access TokenTracker (Platform-Specific)
**Windows:**
```bash
cd C:\Users\logan\OneDrive\Documents\AutoProjects\TokenTracker
```

**Linux/Mac:**
```bash
git clone https://github.com/DonkRonk17/TokenTracker.git
cd TokenTracker
```

### Step 2: Log After Multi-Platform Testing
```bash
python tokentracker.py log NEXUS sonnet-4.5 [INPUT_TOKENS] [OUTPUT_TOKENS] "Task description"
```

**Example:**
```bash
# After cross-platform testing
python tokentracker.py log NEXUS sonnet-4.5 20000 8000 "Tested TokenTracker on Win/Linux"

# After integration work
python tokentracker.py log NEXUS sonnet-4.5 30000 12000 "Integrated SynapseLink with tools"
```

### Step 3: Track Platform-Specific Costs
Use notes field to track platform:
```bash
python tokentracker.py log NEXUS sonnet-4.5 20000 8000 "Windows testing"
python tokentracker.py log NEXUS sonnet-4.5 15000 6000 "Linux testing"
```

### Your Typical Session
- Input: 15,000-35,000 tokens (multi-platform docs, tests)
- Output: 6,000-14,000 tokens (platform-specific fixes)
- Cost per session: $0.18 - $0.36

---

## ⚡ BOLT QUICK START (Cline/Grok - Free Executor)

**Your Role:** Free execution, repetitive tasks, image generation  
**Your Model:** `grok`  
**Your Cost:** FREE ($0 / $0 per 1M tokens)

### Step 1: Access TokenTracker
```bash
cd C:\Users\logan\OneDrive\Documents\AutoProjects\TokenTracker
```

### Step 2: Log Free Sessions (Still Track Usage!)
```bash
python tokentracker.py log BOLT grok [INPUT_TOKENS] [OUTPUT_TOKENS] "Task description"
```

**Example:**
```bash
# After running branding automation
python tokentracker.py log BOLT grok 15000 5000 "Generated branding images"

# After repetitive task execution
python tokentracker.py log BOLT grok 10000 4000 "Batch file operations"
```

### Why Log if Free?
- Shows your contribution to team
- Helps identify tasks to offload to you (free = good!)
- Tracks total team token usage

### Your Typical Session
- Input: 10,000-20,000 tokens (task instructions, context)
- Output: 4,000-8,000 tokens (execution logs, results)
- Cost per session: $0.00 (FREE!)

---

## 🎨 GEMINI QUICK START (Extension Agent)

**Your Role:** Extension-based work, alternative execution  
**Your Model:** `gemini`  
**Your Cost:** FREE (via extension)

### Step 1: Access TokenTracker
```bash
cd C:\Users\logan\OneDrive\Documents\AutoProjects\TokenTracker
```

### Step 2: Log Extension Sessions
```bash
python tokentracker.py log GEMINI gemini [INPUT_TOKENS] [OUTPUT_TOKENS] "Task description"
```

**Example:**
```bash
# After extension-based work
python tokentracker.py log GEMINI gemini 12000 5000 "Alternative approach testing"
```

### Note
Tool calling issues may limit your usage, but still log when active!

---

## 🤖 LOGAN QUICK START (Human Oversight)

**Your Role:** Human operator, final reviewer  
**Your Model:** Varies (use agent you're operating as)  
**Your Cost:** Depends on model

### When to Log as LOGAN
Only when YOU (Logan) are directly using AI tools, not when agents are operating.

**Example:**
```bash
# If Logan manually uses Claude
python tokentracker.py log LOGAN sonnet-4.5 10000 4000 "Manual code review"
```

---

## ⚙️ AUTOMATION TIP (All Agents)

Add to your startup scripts or session-end hooks:

```python
import sys
sys.path.insert(0, r'C:\Users\logan\OneDrive\Documents\AutoProjects\TokenTracker')
from tokentracker import TokenTracker

def log_session(agent, model, input_tokens, output_tokens, task):
    tracker = TokenTracker()
    tracker.log_usage(agent, model, input_tokens, output_tokens, notes=task)
    print(f"[TokenTracker] Logged {input_tokens + output_tokens:,} tokens for {agent}")

# Call at end of session
log_session("YOUR_AGENT", "your-model", input_tokens, output_tokens, "Task description")
```

---

## 📊 TEAM BUDGET AWARENESS

**Monthly Budget:** $60.00  
**Current Status:** Check `python tokentracker.py budget`

**Typical Monthly Breakdown (Target):**
- FORGE: $25 (40%) - High-cost strategic work
- ATLAS: $20 (35%) - Primary executor
- CLIO: $5 (8%) - Low-cost testing
- NEXUS: $8 (13%) - Integration work
- BOLT: $0 (0%) - Free tier
- Buffer: $2 (4%) - Unexpected usage

**Alert Threshold:** 80% ($48 spent)

---

## 🎯 FIRST SESSION GOALS

1. **Log at least ONE session** within 24 hours
2. **Reply to Atlas's announcement** via SynapseLink
3. **Check budget status** to see baseline
4. **Identify integration points** in your workflow

---

## 📞 NEED HELP?

- **Questions:** Reply to ATLAS via SynapseLink
- **Bugs:** Report immediately
- **Can't access:** Let Logan know

---

**Created:** January 17, 2026  
**By:** Atlas (Sonnet 4.5) - Team Brain  
**Version:** 1.0
