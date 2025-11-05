# Building Your Own OSINT Agent: Complete Tutorial

## Table of Contents
1. [Introduction](#introduction)
2. [Architecture Overview](#architecture)
3. [Prerequisites](#prerequisites)
4. [Building the Agent Step-by-Step](#building)
5. [Advanced Features](#advanced)
6. [Deployment Guide](#deployment)
7. [Best Practices](#practices)

---

## Introduction {#introduction}

This tutorial will teach you to build an autonomous OSINT agent that can:
- Accept investigation objectives
- Plan multi-step collection strategies
- Execute searches across platforms
- Analyze and synthesize findings
- Generate intelligence reports
- Monitor sources continuously

**What You'll Learn:**
- Agentic AI architecture patterns
- Tool integration for OSINT
- Autonomous decision-making logic
- Memory and state management
- Report generation
- Ethical implementation

---

## Architecture Overview {#architecture}

### Core Components and Data Flow

1. **User Input** → Objective & constraints
2. **Planner** → Creates investigation strategy
3. **Executor** → Runs searches and collects data
4. **Memory** → Stores findings and context
5. **Analyzer** → Synthesizes information
6. **Reporter** → Generates output

---

## Prerequisites {#prerequisites}

### Required Knowledge
- Python 3.9+ basics
- Understanding of APIs
- Basic async programming
- JSON data structures

### Tools & Libraries

```bash
# Core AI Framework
pip install openai anthropic langchain

# Data Processing
pip install pandas beautifulsoup4 requests

# OSINT Tools
pip install python-whois dnspython shodan

# Utilities
pip install aiohttp asyncio python-dotenv
```

### API Keys Needed
- OpenAI or Anthropic API key
- Google Custom Search API (optional)
- Shodan API (optional)
- News API (optional)

---

## Building the Agent Step-by-Step {#building}

### Step 1: Define the Agent Class

```python
import asyncio
from typing import List, Dict, Any
from datetime import datetime
import json

class OSINTAgent:
    """
    Autonomous OSINT Investigation Agent
    """
    
    def __init__(self, llm_client, tools: List[callable]):
        """
        Initialize the agent with LLM and tools
        
        Args:
            llm_client: LLM API client (OpenAI/Anthropic)
            tools: List of callable functions the agent can use
        """
        self.llm = llm_client
        self.tools = {tool.__name__: tool for tool in tools}
        self.memory = []
        self.objective = None
        self.max_iterations = 10
        
    def log_action(self, action: str, result: Any):
        """Store action and result in memory"""
        self.memory.append({
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'result': result
        })
```

### Step 2: Create the Planner

```python
    async def plan_investigation(self, objective: str) -> List[Dict]:
        """
        Create investigation plan based on objective
        
        Returns:
            List of planned actions
        """
        self.objective = objective
        
        planning_prompt = f"""
You are an OSINT investigation planner. Given the objective below, 
create a step-by-step investigation plan.

OBJECTIVE: {objective}

AVAILABLE TOOLS:
{', '.join(self.tools.keys())}

Create a plan with 5-8 specific actions. For each action, specify:
1. Tool to use
2. Query/parameters
3. Expected information type
4. Why this step is important

Output as JSON array of actions.
"""
        
        response = await self.llm.complete(planning_prompt)
        plan = json.loads(response)
        
        self.log_action("plan_created", plan)
        return plan
```

### Step 3: Build the Executor

```python
    async def execute_action(self, action: Dict) -> Any:
        """
        Execute a single action using appropriate tool
        
        Args:
            action: Action dictionary with tool and parameters
            
        Returns:
            Result from tool execution
        """
        tool_name = action.get('tool')
        parameters = action.get('parameters', {})
        
        if tool_name not in self.tools:
            return {"error": f"Tool {tool_name} not found"}
        
        try:
            tool = self.tools[tool_name]
            result = await tool(**parameters)
            
            self.log_action(f"executed_{tool_name}", {
                "parameters": parameters,
                "result": result
            })
            
            return result
            
        except Exception as e:
            error_result = {"error": str(e)}
            self.log_action(f"error_{tool_name}", error_result)
            return error_result
```

### Step 4: Implement the Analyzer

```python
    async def analyze_findings(self) -> Dict:
        """
        Analyze all collected information and synthesize insights
        
        Returns:
            Analysis dictionary with key findings
        """
        # Compile all findings from memory
        findings = [m for m in self.memory if 'result' in m]
        
        analysis_prompt = f"""
Analyze the following OSINT investigation findings and provide:

OBJECTIVE: {self.objective}

FINDINGS:
{json.dumps(findings, indent=2)}

Provide:
1. Key discoveries (what we learned)
2. Confidence levels (how reliable)
3. Gaps (what's missing)
4. Conflicts (any contradictions)
5. Risk indicators (red flags)
6. Recommendations (next steps)

Output as structured JSON.
"""
        
        response = await self.llm.complete(analysis_prompt)
        analysis = json.loads(response)
        
        self.log_action("analysis_completed", analysis)
        return analysis
```

### Step 5: Create Adaptive Decision Logic

```python
    async def should_continue(self, iteration: int) -> bool:
        """
        Decide whether to continue investigation
        
        Returns:
            True if should continue, False otherwise
        """
        if iteration >= self.max_iterations:
            return False
            
        # Ask LLM if objective is met
        decision_prompt = f"""
Based on the investigation so far, determine if we have enough 
information to answer the objective.

OBJECTIVE: {self.objective}

FINDINGS SO FAR:
{json.dumps(self.memory[-3:], indent=2)}

Answer: YES (sufficient) or NO (need more) or PIVOT (change approach)
Explain your reasoning.
"""
        
        response = await self.llm.complete(decision_prompt)
        
        return "NO" in response.upper() or "PIVOT" in response.upper()
    
    async def adapt_strategy(self) -> List[Dict]:
        """
        Dynamically adjust investigation strategy based on findings
        
        Returns:
            New actions to take
        """
        adaptation_prompt = f"""
Review the investigation progress and suggest 2-3 new actions.

OBJECTIVE: {self.objective}

RECENT FINDINGS:
{json.dumps(self.memory[-5:], indent=2)}

What should we investigate next? Consider:
- Unexplored angles
- Contradictions to resolve
- Gaps to fill
- Leads to follow

Output as JSON array of new actions.
"""
        
        response = await self.llm.complete(adaptation_prompt)
        new_actions = json.loads(response)
        
        return new_actions
```

### Step 6: Main Investigation Loop

```python
    async def investigate(self, objective: str) -> Dict:
        """
        Run complete autonomous investigation
        
        Args:
            objective: Investigation goal
            
        Returns:
            Complete investigation report
        """
        print(f"🔍 Starting investigation: {objective}")
        
        # Phase 1: Planning
        print("\n📋 Creating investigation plan...")
        plan = await self.plan_investigation(objective)
        
        # Phase 2: Execution with adaptation
        iteration = 0
        actions_queue = plan.copy()
        
        while actions_queue and iteration < self.max_iterations:
            print(f"\n⚡ Iteration {iteration + 1}")
            
            # Execute next action
            action = actions_queue.pop(0)
            print(f"   Executing: {action.get('tool')}")
            
            result = await self.execute_action(action)
            print(f"   Result: {len(str(result))} characters")
            
            # Check if should continue
            if not await self.should_continue(iteration):
                print("   ✅ Objective met, concluding...")
                break
            
            # Adapt if queue empty but should continue
            if not actions_queue:
                print("   🔄 Adapting strategy...")
                new_actions = await self.adapt_strategy()
                actions_queue.extend(new_actions)
            
            iteration += 1
        
        # Phase 3: Analysis
        print("\n🧠 Analyzing findings...")
        analysis = await self.analyze_findings()
        
        # Phase 4: Report Generation
        print("\n📄 Generating report...")
        report = await self.generate_report(analysis)
        
        print("\n✨ Investigation complete!")
        return report
```

### Step 7: Report Generator

```python
    async def generate_report(self, analysis: Dict) -> str:
        """
        Generate comprehensive investigation report
        
        Args:
            analysis: Analysis results
            
        Returns:
            Formatted report string
        """
        report_prompt = f"""
Generate a professional OSINT investigation report.

OBJECTIVE: {self.objective}

ANALYSIS:
{json.dumps(analysis, indent=2)}

INVESTIGATION TIMELINE:
{json.dumps(self.memory, indent=2)}

Create a report with:
1. Executive Summary
2. Methodology
3. Key Findings
4. Supporting Evidence
5. Confidence Assessments
6. Recommendations
7. Source Attribution

Format in clear markdown.
"""
        
        report = await self.llm.complete(report_prompt)
        
        self.log_action("report_generated", {"length": len(report)})
        return report
```

---

## Step 8: Building OSINT Tools

Now create the actual tools the agent will use:

```python
import aiohttp
import whois
from bs4 import BeautifulSoup

async def web_search(query: str, num_results: int = 10) -> List[Dict]:
    """
    Search the web for information
    """
    # Implementation using Google Custom Search API
    # or alternative search APIs
    pass

async def domain_lookup(domain: str) -> Dict:
    """
    Get WHOIS and DNS information for domain
    """
    try:
        w = whois.whois(domain)
        return {
            "domain": domain,
            "registrar": w.registrar,
            "creation_date": str(w.creation_date),
            "expiration_date": str(w.expiration_date),
            "name_servers": w.name_servers
        }
    except Exception as e:
        return {"error": str(e)}

async def fetch_webpage(url: str) -> Dict:
    """
    Fetch and parse webpage content
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            
            return {
                "url": url,
                "title": soup.title.string if soup.title else None,
                "text": soup.get_text()[:5000],  # First 5000 chars
                "links": [a['href'] for a in soup.find_all('a', href=True)][:50]
            }

async def social_media_search(platform: str, query: str) -> List[Dict]:
