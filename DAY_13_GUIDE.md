# Day 13: Knowledge Graph Visualization Dashboard

**Week 3, Day 13 | Build Interactive Graph Visualization for OSINT Intelligence**

---

## 🎯 Today's Objectives

By the end of today, you will have:
1. Set up Neo4j graph database for storing investigation relationships
2. Created a GraphStore class to interact with Neo4j
3. Built an entity extractor that uses AI to find entities in investigation text
4. Created a FastAPI dashboard backend with graph endpoints
5. Learned how to build the frontend dashboard using Lovable

**Time Estimate:** 4-6 hours

---

## 📚 What You'll Learn

- Graph database concepts and Neo4j
- Cypher query language basics
- LLM-powered entity extraction
- FastAPI WebSocket for real-time updates
- Building interactive graph visualizations
- Connecting React frontends to Python backends

---

## Step 1: Install Neo4j with Docker (30 minutes)

### What is Neo4j?

Neo4j is a **graph database** that stores data as nodes (entities) and relationships (connections). Perfect for OSINT because we want to see how domains, IPs, organizations, and threat actors are connected.

### Task 1.1: Start Neo4j Container

On your Synology NAS (or local machine):

```bash
# Pull Neo4j image
docker pull neo4j:latest

# Run Neo4j container
docker run -d \
  --name neo4j \
  -p 7474:7474 \
  -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  -v $HOME/neo4j/data:/data \
  neo4j:latest

# Check if running
docker ps | grep neo4j
```

**What this does:**
- Port 7474: Web browser interface
- Port 7687: Bolt protocol for Python driver
- NEO4J_AUTH: Sets username/password
- Volume: Persists data even if container restarts

### Task 1.2: Access Neo4j Browser

1. Open browser: `http://YOUR_NAS_IP:7474`
2. Login:
   - Username: `neo4j`
   - Password: `password`
3. You should see the Neo4j Browser interface!

### Task 1.3: Run Your First Cypher Query

In the Neo4j Browser, try this query:

```cypher
CREATE (i:Investigation {id: 'test_001', objective: 'Test investigation'})
RETURN i
```

This creates a node of type "Investigation" with properties. You should see a graph visualization appear!

To see all nodes:
```cypher
MATCH (n) RETURN n
```

To delete test data:
```cypher
MATCH (n) DELETE n
```

**✅ Checkpoint:** Neo4j is running and you can execute Cypher queries in the browser.

---

## Step 2: Build GraphStore Class (1.5 hours)

### Task 2.1: Install Python Neo4j Driver

```bash
cd ~/OSINT
source venv/bin/activate  # Activate your virtual environment
pip install neo4j
```

### Task 2.2: Create the GraphStore Class

Create a new file: `src/memory/graph_store.py`

Your task is to implement a Python class that connects to Neo4j. Here's the structure to follow:

```python
"""
Neo4j Knowledge Graph Store for OSINT Agent
"""

import os
from typing import Dict, List, Optional
from neo4j import AsyncGraphDatabase

class GraphStore:
    """Knowledge graph storage using Neo4j"""

    def __init__(self, uri: str = None, user: str = None, password: str = None):
        """Initialize Neo4j connection"""
        # TODO: Set connection parameters from args or environment
        # Default: bolt://localhost:7687, neo4j, password
        pass

    async def connect(self):
        """Establish connection to Neo4j"""
        # TODO: Create AsyncGraphDatabase.driver
        pass

    async def close(self):
        """Close Neo4j connection"""
        # TODO: Close the driver
        pass

    async def verify_connection(self) -> bool:
        """Verify Neo4j connection is working"""
        # TODO: Run a simple query like "RETURN 1" to test connection
        # Return True if successful, False otherwise
        pass
```

**Hints:**
- Use `AsyncGraphDatabase.driver(uri, auth=(user, password))`
- Store the driver in `self.driver`
- Use `async with self.driver.session() as session:` for queries

### Task 2.3: Add Investigation Node Methods

Add these methods to create and update Investigation nodes:

```python
async def create_investigation_node(
    self,
    investigation_id: str,
    objective: str,
    status: str = "in_progress"
) -> Dict:
    """Create Investigation node in Neo4j"""
    # TODO: Write Cypher query to CREATE an Investigation node
    # Query template:
    # CREATE (i:Investigation {id: $id, objective: $objective, status: $status, created_at: datetime()})
    # RETURN i
    pass

async def update_investigation_node(
    self,
    investigation_id: str,
    status: str = None,
    findings_count: int = None
) -> Dict:
    """Update Investigation node"""
    # TODO: Write Cypher query to MATCH and SET properties
    # Query template:
    # MATCH (i:Investigation {id: $id})
    # SET i.status = $status, i.findings_count = $findings_count
    # RETURN i
    pass
```

**Example of running a Cypher query in Python:**

```python
async with self.driver.session() as session:
    result = await session.run(
        "CREATE (i:Investigation {id: $id, objective: $obj}) RETURN i",
        id=investigation_id,
        obj=objective
    )
    record = await result.single()
    return dict(record['i']) if record else {}
```

### Task 2.4: Test Your GraphStore

Create a test file: `test_graph.py`

```python
import asyncio
from src.memory.graph_store import GraphStore

async def test_graph():
    graph = GraphStore()

    # Test connection
    connected = await graph.verify_connection()
    print(f"Connected: {connected}")

    # Create investigation node
    inv = await graph.create_investigation_node(
        investigation_id="test_001",
        objective="Test investigation for learning"
    )
    print(f"Created: {inv}")

    # Update investigation
    updated = await graph.update_investigation_node(
        investigation_id="test_001",
        status="completed",
        findings_count=5
    )
    print(f"Updated: {updated}")

    await graph.close()

asyncio.run(test_graph())
```

Run it:
```bash
python test_graph.py
```

Check Neo4j Browser to see your node:
```cypher
MATCH (i:Investigation) RETURN i
```

**✅ Checkpoint:** You can create and update Investigation nodes in Neo4j from Python.

---

## Step 3: Add Entity Node Methods (1 hour)

Now add methods to create different entity types. You need to handle:
- **Domain** nodes (e.g., example.com)
- **IPAddress** nodes (e.g., 1.2.3.4)
- **Organization** nodes (e.g., Google Inc.)

### Task 3.1: Implement create_domain_node

```python
async def create_domain_node(self, domain: str, properties: Dict = None) -> Dict:
    """Create or merge Domain node"""
    # Use MERGE instead of CREATE to avoid duplicates
    # MERGE (d:Domain {name: $name})
    # ON CREATE SET d.created_at = datetime(), d.first_seen = $first_seen
    # ON MATCH SET d.last_seen = datetime()
    # RETURN d
    pass
```

**Key Concept - MERGE:**
- `MERGE` = "Create if doesn't exist, otherwise match existing"
- `ON CREATE SET` = Properties to set only when creating new node
- `ON MATCH SET` = Properties to update when node already exists

### Task 3.2: Add More Entity Types

Follow the same pattern to create:
- `create_ip_node(ip_address: str, properties: Dict = None)`
- `create_organization_node(org_name: str, properties: Dict = None)`

### Task 3.3: Create Relationships Between Nodes

Add this method to link Investigation nodes to Entity nodes:

```python
async def create_relationship(
    self,
    from_id: str,
    from_type: str,  # e.g., "Investigation"
    to_id: str,
    to_type: str,    # e.g., "Domain"
    rel_type: str    # e.g., "INVESTIGATES"
) -> Dict:
    """Create relationship between two nodes"""
    # Cypher query template:
    # MATCH (from:Investigation {id: $from_id})
    # MATCH (to:Domain {name: $to_id})
    # MERGE (from)-[r:INVESTIGATES]->(to)
    # ON CREATE SET r.created_at = datetime()
    # RETURN r
    pass
```

### Task 3.4: Test Entity Creation

Update `test_graph.py`:

```python
# Create domain
domain = await graph.create_domain_node(
    domain="example.com",
    properties={"registrar": "Example Registrar"}
)
print(f"Domain: {domain}")

# Create relationship
rel = await graph.create_relationship(
    from_id="test_001",
    from_type="Investigation",
    to_id="example.com",
    to_type="Domain",
    rel_type="INVESTIGATES"
)
print(f"Relationship: {rel}")
```

In Neo4j Browser, visualize:
```cypher
MATCH (i:Investigation)-[r:INVESTIGATES]->(d:Domain)
RETURN i, r, d
```

You should see a graph with Investigation node connected to Domain node!

**✅ Checkpoint:** You can create entities and relationships in the graph.

---

## Step 4: Build FastAPI Dashboard Backend (1.5 hours)

### Task 4.1: Install Dependencies

```bash
pip install fastapi uvicorn websockets pydantic
```

### Task 4.2: Create dashboard_api.py

Create file in project root: `dashboard_api.py`

Start with this skeleton:

```python
"""
OSINT Agent Dashboard API
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.memory.graph_store import GraphStore

# Initialize FastAPI
app = FastAPI(title="OSINT Dashboard API")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize graph store
graph_store = GraphStore()

# Pydantic models
class GraphData(BaseModel):
    nodes: List[Dict]
    edges: List[Dict]

# Root endpoint
@app.get("/")
async def root():
    return {"name": "OSINT Dashboard API", "version": "1.0.0"}

# Health check
@app.get("/health")
async def health():
    connected = await graph_store.verify_connection()
    return {
        "status": "healthy" if connected else "degraded",
        "neo4j": "connected" if connected else "disconnected"
    }

# TODO: Add more endpoints below
```

### Task 4.3: Add Graph Endpoint

Add this endpoint to get graph data for an investigation:

```python
@app.get("/graph/investigation/{investigation_id}")
async def get_investigation_graph(investigation_id: str):
    """Get graph data for visualization"""
    # TODO: Query Neo4j to get all nodes and relationships for this investigation
    # Return format: {"nodes": [...], "edges": [...]}

    # You'll need to add a method to GraphStore like:
    # await graph_store.get_investigation_graph(investigation_id)
    pass
```

### Task 4.4: Implement get_investigation_graph in GraphStore

Back in `graph_store.py`, add:

```python
async def get_investigation_graph(self, investigation_id: str) -> Dict:
    """Get complete graph for an investigation"""
    # Cypher query to get investigation and all connected nodes:
    # MATCH path = (i:Investigation {id: $id})-[*1..2]-(n)
    # RETURN i, collect(DISTINCT n) as nodes, collect(DISTINCT relationships(path)) as rels

    # Format the result as:
    # {
    #   "nodes": [{"id": "...", "label": "...", "type": "Investigation"}, ...],
    #   "edges": [{"source": "...", "target": "...", "type": "INVESTIGATES"}, ...]
    # }
    pass
```

**Hint:** Neo4j returns complex objects. Extract properties with `dict(node)` and labels with `list(node.labels)`.

### Task 4.5: Test Your API

Run the API:

```bash
python dashboard_api.py
```

It should start on `http://localhost:8000`

Test with curl:

```bash
# Health check
curl http://localhost:8000/health

# Get investigation graph
curl http://localhost:8000/graph/investigation/test_001
```

Visit `http://localhost:8000/docs` to see interactive API documentation!

**✅ Checkpoint:** FastAPI server is running and graph endpoints return data.

---

## Step 5: Build Frontend with Lovable (1 hour)

### What is Lovable?

Lovable is an AI-powered tool that builds React apps from natural language prompts. Perfect for quickly creating professional UIs!

### Task 5.1: Plan Your Dashboard

Your dashboard needs these pages:
1. **Dashboard Overview** - Statistics and recent investigations
2. **Investigation Detail** - Show graph visualization for one investigation
3. **Search** - Search for entities

### Task 5.2: Create Lovable Project

1. Go to https://lovable.dev
2. Sign in with your account
3. Click "New Project"
4. Name it: "OSINT Investigation Dashboard"

### Task 5.3: Use This Prompt

Copy this prompt into Lovable:

```
Create a React TypeScript dashboard for OSINT investigations with Tailwind CSS.

PAGE 1: Dashboard Overview (/)
- Header with title "OSINT Investigation Dashboard"
- 4 statistics cards in a grid:
  - Total Investigations
  - Active Investigations
  - Total Entities
  - Average Confidence Score
- Recent investigations table with columns: ID, Objective, Status, Date
- Connect to API at http://localhost:8000/stats for the data

Use modern design with a dark theme. Make it look professional and clean.
```

### Task 5.4: Add Investigation Detail Page

After Lovable builds the first page, add:

```
Add a new page at /investigations/:id that shows:
- Investigation details in a left sidebar (30% width)
- Interactive graph visualization on the right (70% width)

For the graph, use react-force-graph-2d library.
Color-code nodes by type:
- Investigation: purple
- Domain: blue
- IPAddress: green
- Organization: orange

Fetch data from http://localhost:8000/graph/investigation/:id

The API returns:
{
  "nodes": [{"id": "...", "label": "...", "type": "..."}],
  "edges": [{"source": "...", "target": "...", "type": "..."}]
}
```

### Task 5.5: Configure API URL

In Lovable, create environment variable:
```
REACT_APP_API_URL=http://localhost:8000
```

### Task 5.6: Test Locally

Lovable will give you a preview URL. Open it and test:
1. Dashboard loads
2. Can navigate to investigation detail
3. Graph visualization renders

**✅ Checkpoint:** You have a working React dashboard that displays investigation graphs!

---

## Step 6: Integration Testing (30 minutes)

### Task 6.1: Create Test Data

Create `setup_test_data.py`:

```python
import asyncio
from src.memory.graph_store import GraphStore

async def setup():
    graph = GraphStore()

    # Create investigation
    await graph.create_investigation_node(
        "inv_001",
        "Investigate example.com security",
        "completed"
    )

    # Create entities
    await graph.create_domain_node("example.com", {"registrar": "Example Corp"})
    await graph.create_domain_node("test.com", {"registrar": "Test Inc"})
    await graph.create_ip_node("1.2.3.4", {"country": "US"})

    # Create relationships
    await graph.create_relationship("inv_001", "Investigation", "example.com", "Domain", "INVESTIGATES")
    await graph.create_relationship("inv_001", "Investigation", "1.2.3.4", "IPAddress", "INVESTIGATES")
    await graph.create_relationship("example.com", "Domain", "1.2.3.4", "IPAddress", "RESOLVES_TO")

    print("✅ Test data created!")
    await graph.close()

asyncio.run(setup())
```

Run it:
```bash
python setup_test_data.py
```

### Task 6.2: Test Full Flow

1. Start API: `python dashboard_api.py`
2. Open dashboard in browser
3. Navigate to investigation "inv_001"
4. You should see a graph with:
   - 1 Investigation node (purple)
   - 2 Domain nodes (blue)
   - 1 IP node (green)
   - Connections between them

**✅ Checkpoint:** End-to-end working! API → Neo4j → Dashboard visualization.

---

## Step 7: Deploy to Your NAS (30 minutes)

### Task 7.1: Add to Docker Compose

Update your `docker-compose.yml` on the NAS to include Neo4j:

```yaml
services:
  neo4j:
    image: neo4j:latest
    ports:
      - "7474:7474"
      - "7687:7687"
    environment:
      - NEO4J_AUTH=neo4j/YOUR_STRONG_PASSWORD
    volumes:
      - /volume1/docker/neo4j/data:/data
    restart: unless-stopped
```

### Task 7.2: Deploy Dashboard API

Copy your code to NAS:

```bash
scp -r ~/OSINT user@nas:/volume1/docker/osint/
```

Run the API in a Docker container or using systemd service.

### Task 7.3: Deploy Frontend

Option 1: Deploy via Lovable (easiest)
- Click "Deploy" in Lovable
- It provides free hosting!

Option 2: Deploy to Vercel
- Connect Lovable project to GitHub
- Import to Vercel
- Auto-deploys on every push

**✅ Checkpoint:** Your dashboard is deployed and accessible!

---

## 🎓 What You've Learned

### Technical Skills
- ✅ Graph database concepts (nodes, relationships, Cypher)
- ✅ Neo4j setup and querying
- ✅ Async Python with Neo4j driver
- ✅ FastAPI REST API development
- ✅ React dashboard with graph visualization
- ✅ Lovable AI-assisted development

### Architecture Concepts
- ✅ Knowledge graph modeling
- ✅ API design for graph data
- ✅ Real-time data visualization
- ✅ Full-stack integration

---

## 📝 Commit Your Work

When you're done, commit everything:

```bash
git add src/memory/graph_store.py dashboard_api.py test_graph.py setup_test_data.py
git commit -m "Add knowledge graph visualization with Neo4j and FastAPI dashboard"
git push origin claude/career-analysis-upskilling-011CUuhKsA47yaMS2oyDaNBL
```

---

## 🚀 Next Steps

**Optional Enhancements:**
- Add more entity types (ThreatActor, Indicator)
- Implement entity search endpoint
- Add WebSocket for real-time updates
- Create entity detail modal in dashboard

**Tomorrow (Day 14):**
- Portfolio polish
- Blog post about building a knowledge graph
- Update furywrenlabs.io
- Week 3 wrap-up

---

## 🆘 Troubleshooting

**Neo4j won't start:**
- Check Docker logs: `docker logs neo4j`
- Ensure ports 7474 and 7687 are not in use
- Verify Docker has enough resources

**Python connection fails:**
- Check Neo4j is running: `docker ps | grep neo4j`
- Verify URI is correct: `bolt://localhost:7687`
- Check username/password

**Dashboard can't connect to API:**
- Ensure API is running on port 8000
- Check CORS is enabled
- Verify API URL in environment variables

**Graph doesn't render:**
- Check browser console for errors
- Verify data format matches what react-force-graph expects
- Ensure nodes have `id` and edges have `source`/`target`

---

## 💡 Tips for Success

1. **Test incrementally** - Run test after each method you add
2. **Use Neo4j Browser** - Visualize your queries before coding
3. **Check FastAPI docs** - `/docs` endpoint is your friend
4. **Start simple** - Get basic graph working before adding complexity
5. **Ask Lovable to iterate** - You can refine the UI with follow-up prompts

---

**Good luck! Take your time and actually implement each step. Learning by doing is the best way to master these skills.** 🎯

Let me know when you complete each major step and I'll help troubleshoot or guide you to the next one!
