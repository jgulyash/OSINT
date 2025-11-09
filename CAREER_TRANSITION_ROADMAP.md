# Intelligence Analyst → AI Engineer Career Transition Roadmap

**Your Profile:**
- 20+ years Senior Threat Intelligence Analyst experience
- Expert in identifying, characterizing, and disrupting threat actors
- TS/SCI clearance
- Strong operational intelligence background

**Career Goal:**
- **65% AI Native Engineer** + **35% Cyber Threat Intelligence**
- Remote-only with ~25% travel
- Salary: $140K-180K range
- Build working AI systems, not just analysis

**Timeline:** 3-6 months intensive learning + portfolio building

---

## 🎯 Learning Philosophy

**Leverage Your Strengths:**
- You already understand threat intelligence deeply
- You know what intelligence products SHOULD look like
- You understand the customer (analysts, operators, decision-makers)
- **Learn to BUILD what you've been USING**

**Focus Areas:**
1. **Python & AI/ML Fundamentals** (replace Excel/Maltego/i2)
2. **LangChain & Agent Development** (automate analyst workflows)
3. **Graph Databases** (relationship mapping at scale)
4. **Production Systems** (deploy tools others can use)
5. **Portfolio Building** (prove you can ship code)

---

## 📊 3-Month Overview

### Month 1: Foundation & First AI Agent
- **Week 1:** Python basics + Infrastructure setup
- **Week 2:** First AI agent (LangChain) + Database
- **Week 3:** Multi-agent system + Knowledge graphs
- **Week 4:** MCP integration + Portfolio v1

### Month 2: Advanced AI Engineering
- **Week 5:** RAG (Retrieval Augmented Generation)
- **Week 6:** LLM Security & Prompt Engineering
- **Week 7:** Production deployment + DevOps
- **Week 8:** Advanced orchestration + Testing

### Month 3: Specialization & Job Search
- **Week 9:** Threat-specific AI tools
- **Week 10:** Open source contributions
- **Week 11:** Portfolio finalization
- **Week 12:** Interviews + Job applications

---

## 📅 MONTH 1: FOUNDATION & FIRST SYSTEMS

### WEEK 1: Python Fundamentals & Infrastructure (Days 1-7)

#### Day 1: Python Environment Setup & Basics
**Time:** 4-6 hours
**Goal:** Get Python working and understand basics

**Morning (2-3 hours): Setup**
1. Install Python 3.11+ on your Mac
   ```bash
   brew install python@3.11
   python3 --version
   ```
2. Create project directory
   ```bash
   mkdir -p ~/ai-threat-intel
   cd ~/ai-threat-intel
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install initial packages
   ```bash
   pip install jupyter notebook ipython
   ```

**Afternoon (2-3 hours): Python Basics**
1. Launch Jupyter: `jupyter notebook`
2. Create notebook: "Python Basics for AI"
3. Work through these concepts (type code, don't copy):
   - Variables and data types
   - Lists, dictionaries, sets
   - For loops and list comprehensions
   - Functions
   - Reading/writing files

**Practice Exercise:**
```python
# Write a script that:
# 1. Reads a list of domains from a text file
# 2. Filters out duplicates
# 3. Sorts them alphabetically
# 4. Writes to new file

domains = []
with open('domains.txt', 'r') as f:
    domains = [line.strip() for line in f]

unique_domains = sorted(set(domains))

with open('clean_domains.txt', 'w') as f:
    for domain in unique_domains:
        f.write(f"{domain}\n")
```

**Evening: Documentation**
- Create README.md for your learning journey
- Document what you learned today

**✅ Success Criteria:**
- Python environment working
- Can write basic Python scripts
- Understand lists, dicts, loops, functions

---

#### Day 2: Advanced Python for Data Processing
**Time:** 4-6 hours
**Goal:** Handle data like threat intel feeds

**Morning: Async Programming**
Why: AI agents need to call multiple APIs concurrently

```python
import asyncio
import aiohttp

async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def main():
    # Fetch multiple URLs concurrently
    urls = ['https://example.com', 'https://google.com']
    tasks = [fetch_url(url) for url in urls]
    results = await asyncio.gather(*tasks)
    print(results)

asyncio.run(main())
```

**Afternoon: Working with JSON & APIs**
```python
import requests
import json

# Practice with a threat intel feed
response = requests.get('https://otx.alienvault.com/api/v1/pulses/subscribed')
data = response.json()

# Extract IOCs
for pulse in data['results']:
    print(f"Threat: {pulse['name']}")
    for ioc in pulse['indicators']:
        print(f"  - {ioc['type']}: {ioc['indicator']}")
```

**Practice Exercise:**
Build a simple IOC aggregator:
1. Fetch data from 2-3 public threat feeds
2. Parse JSON responses
3. Extract IOCs (domains, IPs, hashes)
4. Save to structured JSON file

**✅ Success Criteria:**
- Understand async/await
- Can call APIs and parse JSON
- Built a working IOC aggregator script

---

#### Day 3: Infrastructure Setup (Docker, NAS, TwinGate)
**Time:** 5-7 hours
**Goal:** Production-ready infrastructure

**Morning: Docker Basics (2 hours)**
On your Synology NAS:

1. Install Docker via Package Center
2. Learn Docker basics:
   ```bash
   # Pull an image
   docker pull postgres:15

   # Run a container
   docker run -d --name my-postgres \
     -e POSTGRES_PASSWORD=password \
     -p 5432:5432 \
     postgres:15

   # Check running containers
   docker ps

   # View logs
   docker logs my-postgres
   ```

**Afternoon: Docker Compose (2 hours)**
Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: changeme
      POSTGRES_DB: threat_intel
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    restart: unless-stopped

volumes:
  postgres_data:
```

Run it: `docker-compose up -d`

**Evening: TwinGate Setup (1-2 hours)**
1. Create TwinGate account (free tier)
2. Install TwinGate connector on NAS
3. Configure access to NAS services
4. Test remote access

**Practice Exercise:**
- Deploy a simple web app in Docker
- Access it via TwinGate from laptop
- Verify database connectivity

**✅ Success Criteria:**
- Docker running on NAS
- PostgreSQL and Redis accessible
- TwinGate configured for remote access

---

#### Day 4: Git, GitHub, and n8n Setup
**Time:** 4-5 hours
**Goal:** Version control and automation platform

**Morning: Git & GitHub (2 hours)**
```bash
# Configure Git
git config --global user.name "Your Name"
git config --global user.email "you@furywrenlabs.io"

# Create first repo
cd ~/ai-threat-intel
git init
git add .
git commit -m "Initial commit: Learning journey begins"

# Push to GitHub
# (Create repo on GitHub first)
git remote add origin https://github.com/yourusername/ai-threat-intel.git
git push -u origin main
```

**Afternoon: n8n Automation Platform (2-3 hours)**

Deploy n8n on your Hostinger VPS:
```bash
# SSH to VPS
ssh user@your-vps-ip

# Install n8n with Docker
docker run -d --restart unless-stopped \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

Configure Nginx reverse proxy:
```nginx
server {
    listen 80;
    server_name n8n.furywrenlabs.io;

    location / {
        proxy_pass http://localhost:5678;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**First n8n Workflow:**
1. Login to n8n.furywrenlabs.io
2. Create workflow: "Daily Threat Feed Aggregator"
3. Add HTTP Request node → AlienVault OTX
4. Add Filter node → Extract only high-confidence IOCs
5. Add Webhook node → Send to your endpoint

**✅ Success Criteria:**
- Code in GitHub with daily commits
- n8n running and accessible
- First automation workflow working

---

#### Day 5: Python Classes & OOP for AI Agents
**Time:** 4-6 hours
**Goal:** Understand classes (foundation for agents)

**Morning: Class Basics (2 hours)**
```python
class ThreatActor:
    def __init__(self, name, attribution, ttps):
        self.name = name
        self.attribution = attribution
        self.ttps = ttps
        self.first_seen = None
        self.last_seen = None

    def add_ttp(self, ttp):
        """Add a new TTP to this actor"""
        self.ttps.append(ttp)

    def __repr__(self):
        return f"ThreatActor(name='{self.name}', ttps={len(self.ttps)})"

# Usage
apt29 = ThreatActor(
    name="APT29",
    attribution="Russia/SVR",
    ttps=["Spearphishing", "Credential Harvesting"]
)
apt29.add_ttp("Living off the Land")
print(apt29)
```

**Afternoon: Building an Intelligence Class (2-3 hours)**
```python
from datetime import datetime
from typing import List, Dict
import json

class IntelligenceReport:
    """Represents a threat intelligence report"""

    def __init__(self, title: str, classification: str):
        self.title = title
        self.classification = classification
        self.created_at = datetime.now()
        self.key_findings = []
        self.iocs = []
        self.confidence = None

    def add_finding(self, finding: str, confidence: float):
        """Add a key finding with confidence score"""
        self.key_findings.append({
            'finding': finding,
            'confidence': confidence,
            'timestamp': datetime.now().isoformat()
        })

    def add_ioc(self, ioc_type: str, value: str):
        """Add an indicator of compromise"""
        self.iocs.append({
            'type': ioc_type,
            'value': value,
            'source': 'analysis'
        })

    def calculate_confidence(self) -> float:
        """Calculate overall report confidence"""
        if not self.key_findings:
            return 0.0
        confidences = [f['confidence'] for f in self.key_findings]
        self.confidence = sum(confidences) / len(confidences)
        return self.confidence

    def to_json(self) -> str:
        """Export report as JSON"""
        return json.dumps({
            'title': self.title,
            'classification': self.classification,
            'created_at': self.created_at.isoformat(),
            'findings': self.key_findings,
            'iocs': self.iocs,
            'confidence': self.confidence
        }, indent=2)

# Usage
report = IntelligenceReport("APT29 Phishing Campaign", "TLP:AMBER")
report.add_finding("APT29 targeting defense contractors", 0.9)
report.add_finding("Using COVID-19 themed lures", 0.85)
report.add_ioc("domain", "fake-vaccine-info.com")
report.calculate_confidence()
print(report.to_json())
```

**Practice Exercise:**
Build a `ThreatIntelDatabase` class that:
- Stores multiple reports
- Searches reports by keyword
- Filters by confidence threshold
- Exports to JSON file

**✅ Success Criteria:**
- Comfortable with Python classes
- Built intelligence data structures
- Understand OOP concepts (inheritance, methods, attributes)

---

#### Day 6-7: LangChain Basics & First AI Agent
**Time:** 8-10 hours total (2 days)
**Goal:** Build your first AI-powered intelligence tool

**Day 6 Morning: LangChain Installation & Concepts (2-3 hours)**

```bash
pip install langchain langchain-community langchain-openai openai
```

Get OpenAI API key: https://platform.openai.com/api-keys

**Core LangChain Concepts:**
1. **LLMs** - Language models (GPT-4, Claude)
2. **Prompts** - Instructions to the LLM
3. **Chains** - Sequences of LLM calls
4. **Agents** - LLMs that can use tools
5. **Tools** - Functions the agent can call

**First LangChain Script:**
```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os

# Set API key
os.environ['OPENAI_API_KEY'] = 'sk-...'

# Initialize LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

# Create prompt template
prompt = ChatPromptTemplate.from_template(
    "You are a threat intelligence analyst. Analyze this IOC: {ioc}"
)

# Create chain
chain = prompt | llm

# Use it
result = chain.invoke({"ioc": "malicious-domain.com"})
print(result.content)
```

**Day 6 Afternoon: Building Tools (3-4 hours)**

```python
from langchain.tools import tool
import requests

@tool
def whois_lookup(domain: str) -> str:
    """Look up WHOIS information for a domain"""
    # Simple implementation (you'll improve this)
    try:
        response = requests.get(f"https://www.whois.com/whois/{domain}")
        return f"WHOIS data retrieved for {domain}"
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def reputation_check(indicator: str) -> str:
    """Check reputation of an indicator (domain/IP/hash)"""
    # Mock implementation - you'll add real APIs later
    reputation_score = 0.75  # Placeholder
    return f"Reputation score for {indicator}: {reputation_score}"

@tool
def extract_iocs(text: str) -> str:
    """Extract IOCs (domains, IPs) from text"""
    import re

    # Simple regex patterns
    domains = re.findall(r'\b(?:[a-z0-9]+\.)+[a-z]{2,}\b', text, re.I)
    ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', text)

    return f"Found {len(domains)} domains and {len(ips)} IPs"

# Test tools
print(whois_lookup.invoke("google.com"))
print(reputation_check.invoke("malicious-site.com"))
```

**Day 7: Build Complete AI Agent (4-5 hours)**

```python
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

# Initialize LLM
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Create tools list
tools = [whois_lookup, reputation_check, extract_iocs]

# Agent prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a threat intelligence analyst assistant.
    Your job is to investigate indicators and provide analysis.

    Use the available tools to gather information.
    Always provide confidence scores for your findings.
    Format your response as a professional intelligence report."""),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Create agent
agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Test it!
result = agent_executor.invoke({
    "input": "Investigate the domain malicious-site.com and provide a threat assessment"
})

print(result['output'])
```

**Practice Exercise - Build "Intel-Agent-1":**
Create a complete agent that:
1. Takes a domain/IP as input
2. Runs WHOIS lookup
3. Checks reputation
4. Analyzes findings with GPT-4
5. Generates formatted intel report
6. Saves report to file

**✅ Week 1 Success Criteria:**
- Python environment fully set up
- Infrastructure running (Docker, NAS, TwinGate, n8n)
- First AI agent working
- Daily Git commits
- Understanding of LangChain basics

---

### WEEK 2: Database Integration & Production Agent (Days 8-14)

#### Day 8: PostgreSQL + pgVector Setup
**Time:** 4-5 hours
**Goal:** Store intelligence data in database

**Morning: PostgreSQL Setup (2 hours)**

Already have PostgreSQL in Docker from Day 3. Now create schemas:

```sql
-- Connect to database
-- psql -h localhost -U postgres -d threat_intel

-- Intelligence reports table
CREATE TABLE intelligence_reports (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    classification VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    created_by VARCHAR(100),
    confidence FLOAT CHECK (confidence >= 0 AND confidence <= 1),
    content TEXT,
    metadata JSONB
);

-- IOCs table
CREATE TABLE indicators (
    id SERIAL PRIMARY KEY,
    type VARCHAR(50) NOT NULL, -- domain, ip, hash, email
    value TEXT NOT NULL,
    first_seen TIMESTAMP DEFAULT NOW(),
    last_seen TIMESTAMP,
    confidence FLOAT,
    tags TEXT[],
    source VARCHAR(100),
    report_id INTEGER REFERENCES intelligence_reports(id)
);

-- Threat actors table
CREATE TABLE threat_actors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    aliases TEXT[],
    attribution VARCHAR(200),
    first_seen TIMESTAMP,
    last_seen TIMESTAMP,
    ttps TEXT[],
    targets TEXT[],
    confidence FLOAT
);

-- Create indexes
CREATE INDEX idx_indicators_type ON indicators(type);
CREATE INDEX idx_indicators_value ON indicators(value);
CREATE INDEX idx_reports_created_at ON intelligence_reports(created_at);
```

**Afternoon: Python Database Connection (2-3 hours)**

```bash
pip install psycopg2-binary asyncpg
```

Create `src/database/db_manager.py`:
```python
import asyncpg
from typing import List, Dict, Optional
from datetime import datetime

class ThreatIntelDB:
    """Database manager for threat intelligence data"""

    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.pool = None

    async def connect(self):
        """Create connection pool"""
        self.pool = await asyncpg.create_pool(self.connection_string)

    async def close(self):
        """Close connection pool"""
        await self.pool.close()

    async def create_report(
        self,
        title: str,
        classification: str,
        content: str,
        confidence: float,
        metadata: Dict = None
    ) -> int:
        """Create new intelligence report"""
        query = """
        INSERT INTO intelligence_reports
        (title, classification, content, confidence, metadata)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING id
        """
        async with self.pool.acquire() as conn:
            report_id = await conn.fetchval(
                query, title, classification, content,
                confidence, metadata or {}
            )
        return report_id

    async def add_indicator(
        self,
        ioc_type: str,
        value: str,
        confidence: float,
        source: str,
        report_id: Optional[int] = None
    ) -> int:
        """Add IOC to database"""
        query = """
        INSERT INTO indicators (type, value, confidence, source, report_id)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING id
        """
        async with self.pool.acquire() as conn:
            ioc_id = await conn.fetchval(
                query, ioc_type, value, confidence, source, report_id
            )
        return ioc_id

    async def search_indicators(
        self,
        ioc_type: Optional[str] = None,
        min_confidence: float = 0.0
    ) -> List[Dict]:
        """Search for indicators"""
        query = """
        SELECT * FROM indicators
        WHERE ($1 IS NULL OR type = $1)
        AND confidence >= $2
        ORDER BY first_seen DESC
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, ioc_type, min_confidence)
            return [dict(row) for row in rows]

    async def get_report(self, report_id: int) -> Optional[Dict]:
        """Get report by ID with related IOCs"""
        query = """
        SELECT r.*,
               array_agg(i.value) as iocs
        FROM intelligence_reports r
        LEFT JOIN indicators i ON i.report_id = r.id
        WHERE r.id = $1
        GROUP BY r.id
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, report_id)
            return dict(row) if row else None

# Usage
async def main():
    db = ThreatIntelDB("postgresql://postgres:password@localhost/threat_intel")
    await db.connect()

    # Create report
    report_id = await db.create_report(
        title="APT29 Campaign Analysis",
        classification="TLP:AMBER",
        content="Analysis of recent APT29 activity...",
        confidence=0.85
    )

    # Add IOCs
    await db.add_indicator("domain", "evil.com", 0.9, "analysis", report_id)

    # Search
    results = await db.search_indicators(ioc_type="domain", min_confidence=0.8)
    print(f"Found {len(results)} high-confidence domains")

    await db.close()
```

**✅ Success Criteria:**
- PostgreSQL schema created
- Python can read/write to database
- Can store and query intelligence reports

---

#### Day 9: Integrate Database with AI Agent
**Time:** 4-6 hours
**Goal:** Agent stores findings in database

Update your agent from Day 7 to use the database:

```python
from langchain.tools import tool
from src.database.db_manager import ThreatIntelDB

# Initialize database
db = ThreatIntelDB("postgresql://postgres:password@localhost/threat_intel")

@tool
async def store_finding(
    title: str,
    content: str,
    confidence: float,
    iocs: List[str]
) -> str:
    """Store intelligence finding in database"""
    await db.connect()

    # Create report
    report_id = await db.create_report(
        title=title,
        classification="TLP:WHITE",
        content=content,
        confidence=confidence
    )

    # Store IOCs
    for ioc in iocs:
        await db.add_indicator(
            ioc_type="domain",  # Auto-detect type in production
            value=ioc,
            confidence=confidence,
            source="ai_analysis",
            report_id=report_id
        )

    await db.close()
    return f"Report {report_id} created with {len(iocs)} IOCs"

@tool
async def search_past_analysis(keyword: str) -> str:
    """Search previous intelligence reports"""
    await db.connect()

    query = """
    SELECT title, confidence, created_at
    FROM intelligence_reports
    WHERE content ILIKE $1
    ORDER BY created_at DESC
    LIMIT 5
    """
    async with db.pool.acquire() as conn:
        rows = await conn.fetch(query, f"%{keyword}%")

    results = "\n".join([
        f"- {row['title']} (confidence: {row['confidence']})"
        for row in rows
    ])

    await db.close()
    return f"Previous reports:\n{results}" if results else "No previous reports found"
```

**Practice Exercise:**
Build "Intel-Agent-2" that:
1. Investigates a threat actor
2. Searches database for previous reports on this actor
3. Conducts new analysis
4. Stores findings in database
5. Generates report showing historical context

**✅ Success Criteria:**
- Agent can write to database
- Agent can query previous intelligence
- Intelligence accumulates over time

---

#### Day 10-11: FastAPI Backend for Intelligence Platform
**Time:** 8-10 hours (2 days)
**Goal:** RESTful API to access your intelligence

**Day 10: FastAPI Basics (4-5 hours)**

```bash
pip install fastapi uvicorn pydantic
```

Create `api/main.py`:
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from src.database.db_manager import ThreatIntelDB

app = FastAPI(title="Threat Intelligence API")

# Initialize database
db = ThreatIntelDB("postgresql://postgres:password@localhost/threat_intel")

# Pydantic models
class CreateReportRequest(BaseModel):
    title: str
    classification: str
    content: str
    confidence: float

class ReportResponse(BaseModel):
    id: int
    title: str
    classification: str
    created_at: datetime
    confidence: float

class IOCRequest(BaseModel):
    type: str
    value: str
    confidence: float
    source: str

@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.close()

@app.get("/")
async def root():
    return {"message": "Threat Intelligence API v1.0"}

@app.post("/reports", response_model=ReportResponse)
async def create_report(request: CreateReportRequest):
    """Create new intelligence report"""
    report_id = await db.create_report(
        title=request.title,
        classification=request.classification,
        content=request.content,
        confidence=request.confidence
    )

    report = await db.get_report(report_id)
    return report

@app.get("/reports", response_model=List[ReportResponse])
async def list_reports(
    classification: Optional[str] = None,
    min_confidence: float = 0.0,
    limit: int = 50
):
    """List intelligence reports"""
    query = """
    SELECT id, title, classification, created_at, confidence
    FROM intelligence_reports
    WHERE ($1 IS NULL OR classification = $1)
    AND confidence >= $2
    ORDER BY created_at DESC
    LIMIT $3
    """
    async with db.pool.acquire() as conn:
        rows = await conn.fetch(query, classification, min_confidence, limit)

    return [dict(row) for row in rows]

@app.get("/reports/{report_id}")
async def get_report(report_id: int):
    """Get report details"""
    report = await db.get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

@app.post("/indicators")
async def create_indicator(request: IOCRequest):
    """Add new IOC"""
    ioc_id = await db.add_indicator(
        ioc_type=request.type,
        value=request.value,
        confidence=request.confidence,
        source=request.source
    )
    return {"id": ioc_id, "message": "IOC created"}

@app.get("/indicators")
async def search_indicators(
    type: Optional[str] = None,
    min_confidence: float = 0.0,
    limit: int = 100
):
    """Search IOCs"""
    results = await db.search_indicators(type, min_confidence)
    return results[:limit]

# Run with: uvicorn api.main:app --reload
```

**Day 11: AI Analysis Endpoint (4-5 hours)**

Add AI-powered analysis endpoint:

```python
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent

@app.post("/analyze")
async def analyze_threat(
    target: str,
    analysis_type: str = "domain"
):
    """AI-powered threat analysis"""

    # Initialize agent (from Day 7)
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    tools = [whois_lookup, reputation_check, extract_iocs, store_finding]
    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools)

    # Run analysis
    result = agent_executor.invoke({
        "input": f"Analyze this {analysis_type}: {target}. Store findings in database."
    })

    return {
        "target": target,
        "analysis": result['output'],
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test database
        async with db.pool.acquire() as conn:
            await conn.fetchval("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
```

**Test Your API:**
```bash
# Start server
uvicorn api.main:app --reload --port 8000

# Test endpoints
curl http://localhost:8000/
curl http://localhost:8000/health
curl http://localhost:8000/reports

# Trigger AI analysis
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"target": "suspicious-domain.com", "analysis_type": "domain"}'
```

**✅ Success Criteria:**
- FastAPI server running
- Can create/read reports via API
- AI analysis endpoint working
- Automatic API docs at /docs

---

#### Day 12-14: Build Simple Frontend Dashboard
**Time:** 10-12 hours (3 days)
**Goal:** Web UI to visualize intelligence

**Option 1: Use Lovable (Recommended - Faster)**

1. Go to https://lovable.dev
2. Create project: "Threat Intel Dashboard"
3. Use this prompt:

```
Create a threat intelligence dashboard with React and TypeScript.

Pages:
1. Dashboard - Recent reports, IOC statistics
2. Reports - List of intelligence reports with filters
3. IOCs - Search and browse indicators
4. Analyze - Input form to trigger AI analysis

Features:
- Dark theme (looks professional)
- Connect to API at http://localhost:8000
- Tables for data display
- Search and filter capabilities
- Charts showing trends (optional)

Use Tailwind CSS and shadcn/ui components.
```

**Option 2: Build Manually with React**

```bash
npx create-react-app threat-intel-dashboard --template typescript
cd threat-intel-dashboard
npm install axios react-router-dom
```

Create basic dashboard showing:
- Recent reports list
- IOC search
- Analysis submission form

**✅ Week 2 Success Criteria:**
- Database schema complete
- Agent stores findings in PostgreSQL
- FastAPI backend with 8+ endpoints
- Basic frontend dashboard
- Can trigger AI analysis via web UI

---

### WEEK 3: Knowledge Graphs & Advanced Agents (Days 15-21)

#### Day 15: Neo4j Graph Database Setup
**Time:** 4-5 hours
**Goal:** Map threat actor relationships

(Continue with detailed daily guides for Week 3...)

---

### WEEK 4: MCP & Production Deployment (Days 22-28)

(Continue with detailed daily guides for Week 4...)

---

## 📚 Learning Resources

### Essential Free Courses
- **LangChain Tutorials**: https://python.langchain.com/docs/get_started
- **FastAPI Course**: https://fastapi.tiangolo.com/tutorial/
- **Python Asyncio**: Real Python tutorials

### Books (Optional)
- "Building LLM Apps" - online resources
- "Python for Data Analysis" - pandas/data processing

### Communities
- LangChain Discord
- r/MachineLearning
- Threat Intel communities (leverage your network!)

---

## 💰 Cost Tracking

### Month 1 Estimated Costs
- **OpenAI API**: $30-50 (GPT-4 usage)
- **Infrastructure**: $0 (using NAS + free tiers)
- **Total**: ~$30-50

### Cost Optimization
- Use GPT-3.5-turbo for development
- Switch to GPT-4 only for production
- Cache API responses
- Use local models (Ollama) for testing

---

## ✅ Daily Commit Routine

Every day:
```bash
git add .
git commit -m "Day X: [What you built]"
git push origin main
```

Build your GitHub activity graph - employers look at this!

---

**This is your starting roadmap. I'll provide detailed guides for each day as you progress. Focus on Day 1 first - get Python set up and working through the basics.**

**Ready to start Day 1?**
