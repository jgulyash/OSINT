# AI-Powered OSINT Agent - Usage Guide

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd OSINT

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API keys
nano .env

# Minimum required:
# - OPENAI_API_KEY or ANTHROPIC_API_KEY
```

### 3. Run Your First Investigation

```bash
# Interactive mode
python main.py

# Direct investigation
python main.py "Investigate github.com for security intelligence"

# Using CLI
python -m src.cli investigate "Investigate example.com"
```

## AI-Powered Features

### 🤖 Autonomous Investigation

The AI agent makes ALL decisions:

```python
from src.agents.llm_client import create_llm_client
from src.agents.osint_agent import OSINTAgent
from src.memory.memory_store import MemoryStore
from src.tools.osint_tools import get_all_tools

# Initialize
llm = create_llm_client()
memory = MemoryStore()
tools = get_all_tools()

agent = OSINTAgent(llm, tools, memory)

# AI does everything autonomously
result = await agent.investigate("Investigate target.com")
```

**What the AI decides:**
- Investigation strategy and plan
- Which tools to use and when
- How to process and normalize data
- When to continue or stop
- What findings are significant
- Report content and structure

### 🔄 Automated Workflows

Set-and-forget automation:

```python
from src.agents.workflow_orchestrator import WorkflowOrchestrator, WorkflowType

orchestrator = WorkflowOrchestrator(agent, memory)

# Create continuous monitoring
workflow_id = await orchestrator.create_workflow(
    name="security_monitoring",
    workflow_type=WorkflowType.CONTINUOUS,
    objective="Monitor target.com for security changes",
    alert_conditions=[
        {'type': 'risk_indicator', 'severity': 'high'},
        {'type': 'change_detected'}
    ]
)

# Runs forever, autonomously
await orchestrator.continuous_monitoring(workflow_id)
```

### 🎯 Multi-Target Campaigns

Investigate multiple targets automatically:

```bash
# CLI
python -m src.cli campaign github.com gitlab.com bitbucket.org \
  --objective-template "Investigate {target} for security intel" \
  --parallel
```

```python
# Python
result = await orchestrator.run_campaign(
    campaign_name="code_hosting_security",
    targets=[{'name': 'github.com'}, {'name': 'gitlab.com'}],
    objective_template="Investigate {target}",
    parallel=True
)
```

## CLI Commands

### Basic Investigation

```bash
# Simple investigation
python -m src.cli investigate "Investigate example.com"

# With options
python -m src.cli investigate "Investigate example.com" \
  --format html \
  --max-iterations 20 \
  --output report.html \
  --classification UNCLASSIFIED
```

### Workflows

```bash
# One-time workflow
python -m src.cli workflow "scan_target" "Investigate target.com" --type one_time

# Continuous monitoring (runs forever)
python -m src.cli workflow "monitor" "Monitor target.com" \
  --type continuous \
  --interval 3600

# Scheduled workflow
python -m src.cli workflow "daily_scan" "Investigate target.com" \
  --type scheduled \
  --schedule "daily at 09:00"
```

### Campaign Mode

```bash
# Sequential campaign
python -m src.cli campaign target1.com target2.com target3.com \
  --objective-template "Investigate {target} for security issues"

# Parallel campaign (faster)
python -m src.cli campaign target1.com target2.com target3.com \
  --objective-template "Investigate {target}" \
  --parallel \
  --output-dir ./campaign_reports
```

### Utility Commands

```bash
# View investigation history
python -m src.cli history --limit 20

# Generate report from past investigation
python -m src.cli report <investigation_id>

# List available tools
python -m src.cli tools

# Check system health
python -m src.cli health

# View configuration
python -m src.cli config
```

## Python API Examples

### Example 1: Simple Automated Investigation

```python
import asyncio
from src.agents.llm_client import create_llm_client
from src.agents.osint_agent import OSINTAgent
from src.memory.memory_store import MemoryStore
from src.tools.osint_tools import get_all_tools

async def investigate():
    # Setup
    llm = create_llm_client()
    memory = MemoryStore()
    tools = get_all_tools()
    agent = OSINTAgent(llm, tools, memory)

    # Run - AI does everything
    result = await agent.investigate(
        objective="Investigate example.com for security intelligence"
    )

    # Access results
    findings = result['analysis']['key_findings']
    entities = result['processed_data']['entities']
    report = result['report']

    print(f"Found {len(findings)} key findings")
    print(f"Identified {len(entities)} entities")

    return result

asyncio.run(investigate())
```

### Example 2: Continuous Monitoring with Alerts

```python
async def monitor():
    # Setup
    llm = create_llm_client()
    memory = MemoryStore()
    tools = get_all_tools()
    agent = OSINTAgent(llm, tools, memory)
    orchestrator = WorkflowOrchestrator(agent, memory)

    # Create monitoring workflow
    workflow_id = await orchestrator.create_workflow(
        name="threat_monitoring",
        workflow_type=WorkflowType.CONTINUOUS,
        objective="Monitor target.com for threats and changes",
        alert_conditions=[
            {
                'type': 'risk_indicator',
                'severity': 'high'
            },
            {
                'type': 'change_detected',
                'severity': 'medium'
            },
            {
                'type': 'keyword_match',
                'keywords': ['breach', 'vulnerability', 'exploit'],
                'severity': 'critical'
            }
        ]
    )

    # Start monitoring (runs indefinitely)
    await orchestrator.continuous_monitoring(
        workflow_id=workflow_id,
        check_interval=300  # Check every 5 minutes
    )

    # Get alerts
    alerts = orchestrator.get_alerts(severity='high', status='active')
    for alert in alerts:
        print(f"Alert: {alert['condition']['type']} - {alert['severity']}")

asyncio.run(monitor())
```

### Example 3: Multi-Target Campaign

```python
async def campaign():
    # Setup
    llm = create_llm_client()
    memory = MemoryStore()
    tools = get_all_tools()
    agent = OSINTAgent(llm, tools, memory)
    orchestrator = WorkflowOrchestrator(agent, memory)

    # Define targets
    targets = [
        {'name': 'target1.com', 'priority': 'high'},
        {'name': 'target2.com', 'priority': 'medium'},
        {'name': 'target3.com', 'priority': 'medium'}
    ]

    # Run campaign
    result = await orchestrator.run_campaign(
        campaign_name="security_assessment_campaign",
        targets=targets,
        objective_template="Perform security assessment of {target}",
        parallel=True  # Investigate all targets simultaneously
    )

    # Analyze results
    print(f"Completed: {result['completed']}/{len(targets)}")
    print(f"Duration: {result['end_time']} - {result['start_time']}")

    for target, target_result in zip(targets, result['results']):
        if 'error' not in target_result:
            findings = len(target_result['analysis']['key_findings'])
            print(f"{target['name']}: {findings} findings")

    return result

asyncio.run(campaign())
```

## Available OSINT Tools

The agent can autonomously use these tools:

**Web & Domain Intelligence:**
- `web_search` - Search the web
- `domain_lookup` - WHOIS and DNS information
- `fetch_webpage` - Scrape and analyze webpages
- `subdomain_enum` - Enumerate subdomains
- `ssl_certificate_info` - SSL/TLS certificate details

**Social Media & People:**
- `social_media_search` - Search social platforms
- `email_investigation` - Email intelligence
- `username_search` - Username across platforms

**Infrastructure:**
- `ip_lookup` - IP geolocation and info
- `phone_number_lookup` - Phone number analysis

**Document & Analysis:**
- `analyze_url_patterns` - URL pattern analysis
- `hash_file_content` - Content hashing
- `extract_iocs` - Extract indicators of compromise

**Threat Intelligence:**
- `check_reputation` - Reputation checking
- `passive_dns_lookup` - Historical DNS data

## Report Formats

Generate reports in multiple formats:

```python
from src.reporters.report_generator import ReportGenerator

reporter = ReportGenerator()

# Markdown (default)
report = reporter.generate_report(data, format='markdown')

# HTML (styled)
report = reporter.generate_report(data, format='html')

# JSON (machine-readable)
report = reporter.generate_report(data, format='json')

# CSV (data export)
report = reporter.generate_report(data, format='csv')

# Executive brief (concise)
brief = reporter.generate_executive_brief(data)

# Technical appendix (detailed)
appendix = reporter.generate_technical_appendix(data)
```

## Memory & Data Persistence

All investigations are automatically saved:

```python
from src.memory.memory_store import MemoryStore

memory = MemoryStore()

# List past investigations
investigations = await memory.list_investigations(limit=10)

# Get specific investigation
data = await memory.get_investigation_summary(investigation_id)

# Get findings
findings = await memory.get_findings(investigation_id, min_confidence=0.7)

# Get entities and relationships
entities = await memory.get_entities(investigation_id)
relationships = await memory.get_relationships(investigation_id)

# Export investigation
export = await memory.export_investigation(investigation_id, format='json')
```

## Configuration

### Environment Variables (.env)

```bash
# LLM Provider
DEFAULT_LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Agent Settings
MAX_ITERATIONS=15
MIN_CONFIDENCE=0.6

# Optional API Keys (for enhanced tools)
SHODAN_API_KEY=your_key
VIRUSTOTAL_API_KEY=your_key
GOOGLE_API_KEY=your_key
```

### YAML Configuration (config/config.yaml)

```yaml
agent:
  max_iterations: 15
  min_confidence: 0.6

llm:
  provider: openai
  temperature: 0.7
  max_tokens: 4000

tools:
  enabled:
    - web_search
    - domain_lookup
    - all_other_tools
```

## Best Practices

### 1. Start with Clear Objectives

```python
# Good
"Investigate example.com for security vulnerabilities and infrastructure details"

# Too vague
"Tell me about example.com"

# Too broad
"Find everything about everyone related to example.com"
```

### 2. Use Constraints for Focus

```python
result = await agent.investigate(
    objective="Investigate target.com",
    constraints={
        'time_limit': 600,
        'focus_areas': ['security', 'infrastructure'],
        'max_depth': 2
    }
)
```

### 3. Configure Alerts for Monitoring

```python
alert_conditions=[
    {'type': 'risk_indicator', 'severity': 'high'},
    {'type': 'change_detected', 'severity': 'medium'},
    {'type': 'finding_count', 'threshold': 5}
]
```

### 4. Use Campaigns for Multiple Targets

```python
# Instead of running separate investigations
result = await orchestrator.run_campaign(
    targets=multiple_targets,
    objective_template=template,
    parallel=True
)
```

## Troubleshooting

### No API Key Error

```bash
# Set API key
export OPENAI_API_KEY=sk-...
# Or
export ANTHROPIC_API_KEY=sk-ant-...
```

### Tools Not Working

```bash
# Check health
python -m src.cli health

# List tools
python -m src.cli tools

# Install missing dependencies
pip install -r requirements.txt
```

### Investigation Too Slow

```python
# Reduce iterations
agent = OSINTAgent(llm, tools, memory, config={'max_iterations': 10})

# Use quick scan
await agent.investigate(objective, constraints={'quick_scan': True})
```

### Memory Database Issues

```bash
# Check database
ls data/osint_memory.db

# Reset database (WARNING: deletes all data)
rm data/osint_memory.db

# Agent will recreate on next run
```

## Advanced Usage

### Custom Tools

```python
# Define custom tool
async def custom_osint_tool(target: str) -> dict:
    # Your custom OSINT logic
    return {"data": "custom intelligence"}

# Add to agent
tools = get_all_tools()
tools.append(custom_osint_tool)

agent = OSINTAgent(llm, tools, memory)
```

### Custom LLM Provider

```python
from src.agents.llm_client import LLMClient

# Use custom LLM
custom_llm = LLMClient(
    provider='openai',
    model='gpt-4-turbo',
    temperature=0.5,
    max_tokens=8000
)

agent = OSINTAgent(custom_llm, tools, memory)
```

### Export and Analysis

```python
# Export investigation
data = await memory.export_investigation(investigation_id, format='json')

# Analyze with pandas
import pandas as pd
df = pd.DataFrame(data['findings'])
df.groupby('confidence').count()
```

## Support

- Documentation: See `docs/` directory
- Examples: See `examples/` directory
- Issues: GitHub Issues
- Configuration: `.env.example` and `config/config.yaml`

## License

[Your License Here]
