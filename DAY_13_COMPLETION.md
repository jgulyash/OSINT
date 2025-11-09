# Day 13: Graph Visualization Dashboard - COMPLETED ✅

**Week 3, Day 13 | Knowledge Graph Visualization**

---

## 🎯 What We Built Today

Today we completed the knowledge graph visualization system by creating:

1. **Neo4j Knowledge Graph Store** (`src/memory/graph_store.py`)
   - Complete Neo4j integration with async operations
   - Entity node management (Domain, IP, Organization, ThreatActor, Indicator)
   - Relationship creation and traversal
   - Advanced query methods for graph exploration
   - 600+ lines of production-ready code

2. **LLM Entity Extractor** (`src/utils/entity_extractor.py`)
   - GPT-4 powered entity extraction from investigation text
   - Automatic confidence scoring
   - Fallback regex-based extraction
   - Support for 5 entity types

3. **Complete Dashboard API** (`dashboard_api.py`)
   - FastAPI backend with 15+ endpoints
   - WebSocket support for real-time updates
   - Basic dashboard endpoints (stats, investigations, health)
   - **Graph visualization endpoints** (NEW TODAY):
     - `/graph/investigation/:id` - Get investigation graph
     - `/graph/entity/:type/:id/connections` - Find entity connections
     - `/graph/entity/:type/:id/investigations` - Find related investigations
     - `/graph/stats` - Graph statistics
     - `/graph/search` - Entity search
     - `/graph/overview` - Comprehensive overview

4. **Lovable Integration Guide** (`LOVABLE_GRAPH_DASHBOARD_PROMPT.md`)
   - Complete prompt for building the React dashboard in Lovable
   - 4 page specifications (Dashboard, Investigation Detail, Graph Explorer, Search)
   - Graph visualization implementation with react-force-graph-2d
   - Real-time WebSocket integration
   - API integration examples
   - Design system and color palette
   - Deployment instructions

---

## 📁 Files Created/Modified

### New Files
```
src/memory/graph_store.py                 (621 lines) - Neo4j integration
src/utils/__init__.py                     (1 line)    - Utils module
src/utils/entity_extractor.py             (186 lines) - Entity extraction
dashboard_api.py                          (573 lines) - Complete API
LOVABLE_GRAPH_DASHBOARD_PROMPT.md         (700 lines) - Lovable guide
DAY_13_COMPLETION.md                      (this file)
test_dashboard_api.sh                     (40 lines)  - API test script
```

### Modified Files
```
requirements.txt                          - Added FastAPI, uvicorn, neo4j, websockets
```

**Total New Code:** ~2,100 lines of production-ready Python and documentation

---

## 🚀 How to Run the Dashboard API

### 1. Install Dependencies

```bash
# From OSINT project root
pip install fastapi uvicorn neo4j websockets pydantic
```

### 2. Set Up Neo4j (Optional but Recommended)

**Option A: Docker (Easiest)**
```bash
docker run -d \
  --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  -v $HOME/neo4j/data:/data \
  neo4j:latest
```

**Option B: Synology NAS Docker**
1. Open Docker app on NAS
2. Search for "neo4j" and download
3. Configure:
   - Port 7474 (HTTP)
   - Port 7687 (Bolt)
   - Environment: `NEO4J_AUTH=neo4j/password`
   - Volume: `/data` → `/volume1/docker/neo4j/data`
4. Start container

**Access Neo4j Browser:** http://YOUR_NAS_IP:7474
- Username: `neo4j`
- Password: `password` (change in production!)

### 3. Configure Environment

Create `.env` file in project root:
```bash
# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password

# Dashboard Configuration
DASHBOARD_PORT=8081

# OpenAI for Entity Extraction
OPENAI_API_KEY=sk-...
```

### 4. Start Dashboard API

```bash
# From OSINT project root
python dashboard_api.py
```

Expected output:
```
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║              OSINT Agent Dashboard API                        ║
    ║                                                               ║
    ║  Running on: http://0.0.0.0:8081                         ║
    ║  Docs: http://0.0.0.0:8081/docs                          ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝

🚀 Starting OSINT Dashboard API...
✓ Neo4j connection verified
✓ Graph schema initialized
✓ Dashboard API ready
```

### 5. Test API Endpoints

```bash
# Run test script
./test_dashboard_api.sh

# Or manually test
curl http://localhost:8081/health
curl http://localhost:8081/stats
curl http://localhost:8081/graph/stats
curl http://localhost:8081/graph/overview
```

### 6. View Interactive API Docs

Open in browser: **http://localhost:8081/docs**

FastAPI provides automatic interactive documentation where you can:
- See all endpoints
- Test endpoints directly
- View request/response schemas
- Download OpenAPI spec

---

## 🎨 Building the Lovable Dashboard

### Quick Start

1. **Go to Lovable**: https://lovable.dev
2. **Create New Project**: "OSINT Dashboard"
3. **Copy the prompt** from `LOVABLE_GRAPH_DASHBOARD_PROMPT.md`
4. **Paste into Lovable** and let it build!

### Step-by-Step with Lovable

**Phase 1: Dashboard Overview**
```
Prompt: Create a React TypeScript dashboard overview page with Tailwind CSS.
Show 4 statistics cards (total investigations, active, entities, avg confidence)
and a recent investigations table. Connect to API at http://YOUR_NAS_IP:8081/stats
```

**Phase 2: Investigation Detail + Graph**
```
Prompt: Add an investigation detail page at /investigations/:id with a split layout.
Left sidebar shows investigation details. Right panel shows an interactive force-directed
graph using react-force-graph-2d. Fetch data from /graph/investigation/:id.
Color-code nodes: Investigation (purple), Domain (blue), IP (green),
Organization (orange), ThreatActor (red), Indicator (yellow).
```

**Phase 3: Real-Time Updates**
```
Prompt: Add WebSocket connection at ws://YOUR_NAS_IP:8081/ws/investigations/:id
for real-time investigation status updates. Show toast notifications when status changes.
```

**Phase 4: Entity Search**
```
Prompt: Create entity search page with autocomplete, filters by entity type,
and results as cards. Connect to /graph/search endpoint. Clicking an entity
shows a modal with details and a mini connection graph.
```

### Configuration

Before deploying, create `.env.local`:
```bash
REACT_APP_API_URL=http://YOUR_NAS_IP:8081
REACT_APP_WS_URL=ws://YOUR_NAS_IP:8081
```

Replace `YOUR_NAS_IP` with:
- Local: `192.168.1.100` (your actual NAS IP)
- TwinGate: `nas.furywrenlabs` (or your TwinGate hostname)
- Public: `api.furywrenlabs.io` (if exposed via Nginx)

---

## 🔧 Deploying to Production

### Option 1: Lovable Hosting (Easiest)
1. Build in Lovable
2. Click "Deploy"
3. Lovable provides free hosting with custom domain support
4. Done! ✨

### Option 2: Vercel
1. Connect Lovable project to GitHub
2. Import to Vercel
3. Add environment variables in Vercel dashboard
4. Auto-deploy on every push

### Option 3: Synology NAS
```bash
# Build locally
npm run build

# Copy to NAS
scp -r build/* user@nas.local:/var/www/dashboard/

# Configure Nginx
sudo nano /etc/nginx/sites-available/dashboard

# Add:
server {
    listen 80;
    server_name dashboard.furywrenlabs.io;

    location / {
        root /var/www/dashboard;
        try_files $uri /index.html;
    }

    location /api {
        proxy_pass http://localhost:8081;
    }

    location /ws {
        proxy_pass http://localhost:8081;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}

# Enable and restart
sudo ln -s /etc/nginx/sites-available/dashboard /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## 📊 API Endpoints Reference

### Basic Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API root |
| GET | `/health` | Health check |
| GET | `/stats` | Dashboard statistics |
| GET | `/investigations` | List investigations |
| GET | `/investigations/:id` | Investigation detail |
| POST | `/investigate` | Start new investigation |
| GET | `/active-investigations` | Currently running |
| WS | `/ws/investigations/:id` | Real-time updates |

### Graph Endpoints (NEW)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/graph/investigation/:id` | Get investigation graph |
| GET | `/graph/entity/:type/:id/connections` | Find entity connections |
| GET | `/graph/entity/:type/:id/investigations` | Related investigations |
| GET | `/graph/stats` | Graph statistics |
| GET | `/graph/search?query=...` | Search entities |
| GET | `/graph/overview` | Comprehensive overview |
| POST | `/graph/initialize` | Initialize schema |

---

## 🎯 What the System Does Now

### End-to-End Workflow

1. **User Starts Investigation**
   ```
   POST /investigate
   { "target": "example.com", "objective": "Security assessment" }
   ```

2. **System Creates Graph Node**
   - Investigation node created in Neo4j
   - WebSocket connection established
   - Background task starts

3. **Investigation Runs** (Mock for now, real in production)
   - Collects intelligence
   - Broadcasts status updates via WebSocket
   - Frontend shows real-time progress

4. **Entities Extracted**
   - GPT-4 analyzes investigation text
   - Extracts: domains, IPs, organizations, threat actors, indicators
   - Each entity stored as Neo4j node

5. **Graph Populated**
   - Relationships created: Investigation → Entity
   - Cross-investigation relationships discovered
   - Confidence scores assigned

6. **Dashboard Visualizes**
   - Interactive force-directed graph
   - Color-coded by entity type
   - Click to explore connections
   - Search across all entities

---

## 💡 Key Features Implemented

### Knowledge Graph
- ✅ Neo4j integration with async driver
- ✅ 6 node types (Investigation, Domain, IP, Organization, ThreatActor, Indicator)
- ✅ Relationship management
- ✅ Graph traversal (find connections up to N hops)
- ✅ Cross-investigation entity tracking
- ✅ Confidence scoring

### Entity Extraction
- ✅ GPT-4 powered extraction
- ✅ 5 entity types detected
- ✅ Regex fallback for reliability
- ✅ Deduplication
- ✅ Context preservation

### Dashboard API
- ✅ 15+ REST endpoints
- ✅ WebSocket real-time updates
- ✅ CORS enabled for frontend
- ✅ Auto-generated OpenAPI docs
- ✅ Health checks
- ✅ Error handling

### Lovable Integration
- ✅ Complete UI specifications
- ✅ Graph visualization guide
- ✅ API integration examples
- ✅ Design system
- ✅ Deployment instructions

---

## 📈 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Lovable Dashboard                       │
│  (React + TypeScript + react-force-graph-2d)                │
│                                                             │
│  Pages:                                                     │
│  • Dashboard Overview (stats, recent investigations)        │
│  • Investigation Detail (info + graph visualization)        │
│  • Global Graph Explorer (full knowledge graph)             │
│  • Entity Search (autocomplete + filters)                   │
│                                                             │
│  Real-Time: WebSocket ◄─┐                                   │
└─────────────────────────┼───────────────────────────────────┘
                          │
                          │ HTTP + WebSocket
                          │
┌─────────────────────────┼───────────────────────────────────┐
│                   Dashboard API (FastAPI)                    │
│                         Port 8081                            │
│                                                             │
│  Endpoints:                                                 │
│  • Basic: /stats, /investigations, /health                  │
│  • Graph: /graph/investigation/:id, /graph/search, etc.     │
│  • WebSocket: /ws/investigations/:id                        │
│                                                             │
│  Components:                                                │
│  • GraphStore (Neo4j client)                                │
│  • EntityExtractor (GPT-4 powered)                          │
│  • Active investigations tracker                            │
└─────────────────────────┬───────────────────────────────────┘
                          │
                ┌─────────┴─────────┐
                │                   │
        ┌───────▼──────┐    ┌──────▼────────┐
        │   Neo4j DB   │    │  OpenAI API   │
        │  (Knowledge  │    │  (GPT-4 for   │
        │    Graph)    │    │   entities)   │
        │  Port 7687   │    │               │
        └──────────────┘    └───────────────┘
```

---

## 🔍 Testing the Complete System

### 1. Test Neo4j Connection
```bash
curl http://localhost:8081/health
# Should show: "neo4j": "connected"
```

### 2. Initialize Graph Schema
```bash
curl -X POST http://localhost:8081/graph/initialize
```

### 3. Start Mock Investigation
```bash
curl -X POST http://localhost:8081/investigate \
  -H "Content-Type: application/json" \
  -d '{"target": "example.com", "objective": "Security assessment"}'
```

### 4. View Graph Stats
```bash
curl http://localhost:8081/graph/stats
```

### 5. Search Entities
```bash
curl "http://localhost:8081/graph/search?query=example&limit=10"
```

### 6. Connect via WebSocket (JavaScript)
```javascript
const ws = new WebSocket('ws://localhost:8081/ws/investigations/inv_001');
ws.onmessage = (event) => console.log(JSON.parse(event.data));
```

---

## 🎓 What You Learned Today

### Technical Skills
- ✅ Neo4j graph database design and querying (Cypher)
- ✅ Async Python with Neo4j driver
- ✅ FastAPI WebSocket implementation
- ✅ LLM-powered entity extraction
- ✅ Graph algorithms (traversal, search, relationship mapping)
- ✅ React force-directed graph visualization
- ✅ Real-time data streaming with WebSockets

### AI Engineering Concepts
- ✅ Knowledge graph population from unstructured text
- ✅ Entity extraction with LLMs (structured output)
- ✅ Confidence scoring and uncertainty handling
- ✅ Multi-source intelligence correlation
- ✅ Visual intelligence analytics

### DevOps Skills
- ✅ Docker container management (Neo4j)
- ✅ API deployment and testing
- ✅ Environment configuration
- ✅ CORS and security basics
- ✅ WebSocket connection management

---

## 📚 Resources & Documentation

### Created Documentation
- `LOVABLE_GRAPH_DASHBOARD_PROMPT.md` - Complete Lovable guide
- `DAY_13_COMPLETION.md` - This file
- `test_dashboard_api.sh` - API test script
- FastAPI auto-docs: http://localhost:8081/docs

### External Resources
- **Neo4j Python Driver**: https://neo4j.com/docs/python-manual/current/
- **FastAPI WebSockets**: https://fastapi.tiangolo.com/advanced/websockets/
- **react-force-graph**: https://github.com/vasturiano/react-force-graph
- **Lovable Documentation**: https://docs.lovable.dev

---

## 🚧 Next Steps (Week 3, Day 14)

Tomorrow we'll wrap up Week 3 with:

### Portfolio Polish
- ✅ Screenshot your Lovable dashboard
- ✅ Update furywrenlabs.io projects page with dashboard link
- ✅ Write blog post: "Building a Knowledge Graph for OSINT Intelligence"
- ✅ Create GitHub README with architecture diagram

### Advanced Features (Time Permitting)
- ⏳ Connect real OSINT agent to dashboard API
- ⏳ Automatic entity extraction in investigation pipeline
- ⏳ Graph export (PNG, SVG, JSON)
- ⏳ Advanced graph analytics (centrality, community detection)

### Career Materials
- ⏳ Update LinkedIn with graph database skills
- ⏳ Add "Knowledge Graph Engineering" to resume
- ⏳ Prepare demo script for interviews

---

## 💰 Cost Tracking

### Week 3 Costs (Days 10-13)
- **GPT-4 API** (entity extraction, multi-agent): $5-8
- **Infrastructure** (Docker, NAS): $0 (existing)
- **Lovable**: $0 (free tier)
- **Neo4j**: $0 (Docker self-hosted)
- **Total Week 3**: ~$5-8

### Month 1 Total: ~$30-50

**Cost Optimization Tips:**
- Use GPT-3.5-turbo for entity extraction (80% cheaper, 90% as good)
- Cache entity extraction results
- Batch API calls when possible
- Neo4j Community Edition is free forever

---

## ✅ Day 13 Completion Checklist

- [x] Create GraphStore class with complete Neo4j integration
- [x] Implement EntityExtractor with GPT-4 and regex fallback
- [x] Build complete Dashboard API with 15+ endpoints
- [x] Add graph visualization endpoints
- [x] Implement WebSocket for real-time updates
- [x] Create comprehensive Lovable prompt and guide
- [x] Update requirements.txt with new dependencies
- [x] Write testing script
- [x] Document deployment instructions
- [x] Test all API endpoints
- [x] Create this completion document

**Status: ✅ COMPLETE**

---

## 🎉 Achievements Unlocked

Today you:
- 🏆 Built a production-ready knowledge graph system
- 🏆 Created 2,100+ lines of clean, documented code
- 🏆 Integrated 3 cutting-edge technologies (Neo4j, FastAPI, LLMs)
- 🏆 Designed a complete dashboard architecture
- 🏆 Learned graph database concepts from scratch
- 🏆 Created reusable components for future projects

---

**Tomorrow:** Week 3 wrap-up, portfolio polish, and career materials! 🚀

---

**Questions or Issues?**
- Check FastAPI docs at http://localhost:8081/docs
- Neo4j browser at http://localhost:7474
- Review `LOVABLE_GRAPH_DASHBOARD_PROMPT.md` for Lovable questions

**Great work today! The knowledge graph visualization is a powerful addition to your OSINT system and portfolio.** 🎯
