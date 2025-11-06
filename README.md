# 🤖 OSINT Agent

**AI-driven open source intelligence gathering and analysis system.**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 🌟 Overview

This is a **autonomous AI-powered OSINT (Open Source Intelligence) agent** that handles the complete intelligence lifecycle with **zero manual intervention**. The AI makes all decisions about:

- 📋 **Planning**: What to investigate and how
- 🔍 **Collection**: Which sources to query and when
- 🔄 **Processing**: How to clean and normalize data
- 🧠 **Analysis**: What findings are significant
- 📊 **Reporting**: How to present intelligence
- ✅ **Evaluation**: Assess investigation quality

**No human input needed** - just provide an objective and the AI does everything.

## 🚀 Key Features

### 🤖 Autonomous AI Agent
- **AI-Driven Decision Making**: LLM-powered planning, analysis, and adaptation
- **Self-Directed Investigation**: Agent decides which tools to use and when
- **Adaptive Strategy**: Dynamically adjusts approach based on findings
- **Continuous Learning**: Improves investigation quality through feedback

### 🔄 Automated Workflows
- **One-Time Investigations**: Run single automated investigations
- **Continuous Monitoring**: Set-and-forget surveillance with change detection
- **Scheduled Tasks**: Periodic investigations on autopilot
- **Multi-Target Campaigns**: Investigate multiple targets simultaneously

### 🛠️ Comprehensive OSINT Toolkit
- **15+ Built-in Tools**: Web search, DNS, WHOIS, SSL, social media, and more
- **Automatic Tool Selection**: AI chooses optimal tools for each objective
- **Extensible Architecture**: Easy to add custom tools
- **API Integration Ready**: Connect to VirusTotal, Shodan, SecurityTrails, etc.

### 📊 Intelligence Lifecycle Implementation
1. **Planning & Direction**: AI creates investigation strategy
2. **Collection**: Automated multi-source data gathering
3. **Processing**: AI-powered data normalization and structuring
4. **Analysis**: Deep intelligence analysis with confidence scoring
5. **Dissemination**: Multi-format report generation (Markdown, HTML, JSON, CSV, **Obsidian Canvas**)
6. **Feedback**: Self-evaluation and quality assessment

### 🗺️ Obsidian Canvas Mind Maps
- **Interactive Visualizations**: Generate beautiful mind maps from investigations
- **4 Canvas Types**: Overview, Entity Map, Timeline, Findings Hierarchy
- **Auto-Generated**: Canvases created automatically alongside reports
- **Obsidian Integration**: Open directly in Obsidian for interactive exploration
- **[Full Guide](OBSIDIAN_INTEGRATION.md)**

### 🎯 Advanced Capabilities
- **Entity Extraction**: Automatically identify people, organizations, domains, IPs
- **Relationship Mapping**: Discover connections between entities
- **Timeline Construction**: Build chronological event sequences
- **Risk Assessment**: AI-driven threat and risk analysis
- **Alert Generation**: Configurable intelligent alerting
- **Comparative Analysis**: Cross-target intelligence correlation

## 📋 Quick Start

### Installation

```bash
# Clone repository
git clone <repo-url>
cd OSINT

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your API keys (minimum: OpenAI or Anthropic)
```

### Your First AI-Powered Investigation

```bash
# Interactive mode
python main.py

# Direct investigation
python main.py "Investigate github.com for security and infrastructure intelligence"

# Using CLI
python -m src.cli investigate "Investigate example.com"
```

That's it! The AI handles everything automatically.

## 🎯 Usage Examples

### Example 1: Autonomous Investigation (Python)

```python
import asyncio
from src.agents.llm_client import create_llm_client
from src.agents.osint_agent import OSINTAgent
from src.memory.memory_store import MemoryStore
from src.tools.osint_tools import get_all_tools

async def main():
    # Initialize AI-powered components
    llm = create_llm_client()          # AI brain
    memory = MemoryStore()              # Persistent storage
    tools = get_all_tools()             # OSINT toolkit

    # Create autonomous agent
    agent = OSINTAgent(llm, tools, memory)

    # AI does EVERYTHING autonomously
    result = await agent.investigate(
        objective="Investigate example.com for security intelligence"
    )

    # Access results
    print(f"Findings: {len(result['analysis']['key_findings'])}")
    print(f"Entities: {len(result['processed_data']['entities'])}")
    print(f"Report: {result['report'][:500]}...")

asyncio.run(main())
```

### Example 2: Continuous Monitoring (CLI)

```bash
# AI-powered continuous monitoring with automatic alerts
python -m src.cli workflow "monitor_target" "Monitor example.com for security changes" \
  --type continuous \
  --interval 3600

# Runs forever, alerts on changes automatically
```

### Example 3: Multi-Target Campaign

```bash
# Investigate multiple targets in parallel
python -m src.cli campaign github.com gitlab.com bitbucket.org \
  --objective-template "Investigate {target} for security issues" \
  --parallel \
  --output-dir ./campaign_results
```

### Example 4: Obsidian Canvas Mind Maps

```bash
# Generate interactive mind maps from investigation
python -m src.cli canvas <investigation_id> --type all

# Create Obsidian vault structure
python -m src.cli create-vault

# Run example with automatic canvas generation
python examples/obsidian_canvas_generation.py
```

```python
# Python: Generate canvases alongside reports
from src.reporters.report_generator import ReportGenerator

reporter = ReportGenerator()

# Generate all canvas types
reporter.generate_obsidian_canvas(
    investigation_data,
    canvas_type='all',  # overview, entity_map, timeline, findings, or all
    save=True
)
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   AI-Powered OSINT Agent                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐      ┌──────────────────────────┐    │
│  │   LLM Core  │◄────►│  Intelligence Lifecycle  │    │
│  │  (AI Brain) │      │                          │    │
│  └─────────────┘      │  1. Planning             │    │
│         ▲             │  2. Collection           │    │
│         │             │  3. Processing           │    │
│         │             │  4. Analysis             │    │
│         │             │  5. Dissemination        │    │
│         ▼             │  6. Feedback             │    │
│  ┌─────────────┐      └──────────────────────────┘    │
│  │   Memory    │                                        │
│  │   Store     │      ┌──────────────────────────┐    │
│  └─────────────┘      │    OSINT Tools (15+)     │    │
│                       │                          │    │
│  ┌─────────────┐      │  • Web Search            │    │
│  │  Workflow   │      │  • Domain Intelligence   │    │
│  │ Orchestrator│      │  • Social Media OSINT    │    │
│  └─────────────┘      │  • Infrastructure Recon  │    │
│                       │  • Threat Intelligence   │    │
│  ┌─────────────┐      └──────────────────────────┘    │
│  │   Report    │                                        │
│  │  Generator  │      ┌──────────────────────────┐    │
│  └─────────────┘      │   Output Formats         │    │
│                       │                          │    │
│                       │  • Markdown  • HTML      │    │
│                       │  • JSON      • CSV       │    │
│                       └──────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

## 🧠 How the AI Works

### 1. Planning Phase (AI-Driven)
```
AI receives objective → Analyzes requirements → Creates investigation plan
→ Selects tools → Prioritizes actions → Sets success criteria
```

### 2. Collection Phase (Autonomous)
```
AI executes plan → Uses multiple tools → Gathers intelligence
→ Adapts strategy → Handles failures → Continues until complete
```

### 3. Analysis Phase (AI-Powered)
```
AI processes data → Extracts entities → Maps relationships
→ Builds timeline → Assesses confidence → Identifies risks
```

### 4. Reporting Phase (Automated)
```
AI synthesizes findings → Generates reports → Creates visualizations
→ Provides recommendations → Evaluates quality
```

## 📊 Intelligence Lifecycle

The agent implements the complete intelligence cycle:

1. **Planning & Direction**
   - AI creates comprehensive investigation strategy
   - Defines information requirements
   - Selects optimal tools and sources

2. **Collection**
   - Autonomous multi-source data gathering
   - Parallel tool execution
   - Automatic retry and error handling

3. **Processing**
   - AI-powered data cleaning and normalization
   - Deduplication and structuring
   - Cross-referencing and validation

4. **Analysis**
   - Deep intelligence synthesis
   - Entity and relationship extraction
   - Timeline construction
   - Confidence scoring
   - Risk assessment

5. **Dissemination**
   - Multi-format report generation
   - Executive briefings
   - Technical appendices
   - Dashboard data

6. **Feedback**
   - Self-evaluation
   - Quality metrics
   - Improvement recommendations

## 🛠️ Available OSINT Tools

The AI can autonomously use these tools:

### Web & Domain Intelligence
- `web_search` - AI-driven web search
- `domain_lookup` - WHOIS, DNS, registration info
- `fetch_webpage` - Page scraping and analysis
- `subdomain_enum` - Subdomain discovery
- `ssl_certificate_info` - SSL/TLS certificate analysis

### Social Media & People
- `social_media_search` - Multi-platform social OSINT
- `email_investigation` - Email intelligence gathering
- `username_search` - Username enumeration across platforms

### Infrastructure & Network
- `ip_lookup` - IP geolocation and ASN info
- `phone_number_lookup` - Phone number analysis

### Analysis & Processing
- `analyze_url_patterns` - URL pattern extraction
- `hash_file_content` - Content fingerprinting
- `extract_iocs` - Indicator of Compromise extraction

### Threat Intelligence
- `check_reputation` - Multi-source reputation checking
- `passive_dns_lookup` - Historical DNS data

## 📁 Project Structure

```
OSINT/
├── src/
│   ├── agents/
│   │   ├── osint_agent.py          # Main AI agent (intelligence lifecycle)
│   │   ├── llm_client.py           # LLM integration (OpenAI/Anthropic)
│   │   └── workflow_orchestrator.py # Automation & scheduling
│   ├── tools/
│   │   └── osint_tools.py          # 15+ OSINT tools
│   ├── memory/
│   │   └── memory_store.py         # SQLite persistence
│   ├── reporters/
│   │   └── report_generator.py     # Multi-format reporting
│   └── cli.py                      # Command-line interface
├── examples/
│   ├── automated_investigation.py   # Full autonomous investigation demo
│   ├── continuous_monitoring.py     # Continuous monitoring demo
│   └── multi_target_campaign.py     # Campaign demo
├── config/
│   └── config.yaml                  # Configuration
├── data/
│   ├── reports/                     # Generated reports
│   ├── investigations/              # Investigation data
│   └── osint_memory.db              # SQLite database
├── main.py                          # Main entry point
├── requirements.txt                 # Dependencies
├── .env.example                     # Environment template
└── README.md                        # This file
```

## ⚙️ Configuration

### Environment Variables (.env)

```bash
# LLM Provider (required)
DEFAULT_LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...              # OpenAI API key
# OR
ANTHROPIC_API_KEY=sk-ant-...       # Anthropic API key

# Agent Configuration
MAX_ITERATIONS=15
MIN_CONFIDENCE=0.6

# Optional: Enhanced OSINT APIs
SHODAN_API_KEY=your_key
VIRUSTOTAL_API_KEY=your_key
GOOGLE_API_KEY=your_key
SECURITYTRAILS_API_KEY=your_key
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

workflows:
  enable_scheduling: true
  max_parallel: 3
```

## 📚 Documentation

- **[Usage Guide](USAGE_GUIDE.md)** - Comprehensive usage documentation
- **[Obsidian Integration](OBSIDIAN_INTEGRATION.md)** - Mind map and canvas generation guide
- **[Examples](examples/)** - Working code examples
- **[Configuration](config/config.yaml)** - Configuration options

## 🔐 Security & Ethics

### Responsible OSINT
- Only collect publicly available information
- Respect robots.txt and rate limits
- Do not access unauthorized systems
- Follow local laws and regulations

### Data Privacy
- All data stored locally
- No data sent to third parties (except LLM APIs)
- Configurable data retention
- Support for data redaction

### API Key Security
- Never commit .env files
- Use environment variables
- Rotate keys regularly
- Monitor API usage

## 🤝 Contributing

Contributions welcome! Areas of interest:

- Additional OSINT tools
- New LLM provider integrations
- Enhanced analysis capabilities
- Report format improvements
- Documentation and examples

## 📝 License

MIT License

## 🙏 Acknowledgments

Built with:
- OpenAI GPT-4 / Anthropic Claude for AI capabilities
- Python asyncio for concurrency
- SQLite for data persistence
- Rich for beautiful CLI output

---

**⚠️ Disclaimer**: This tool is for legitimate OSINT research and security assessments only. Users are responsible for compliance with applicable laws and regulations. Always obtain proper authorization before investigating targets you don't own.

---

Made with 🤖 by AI-powered automation
