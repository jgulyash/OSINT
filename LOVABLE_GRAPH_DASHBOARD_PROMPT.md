# Lovable Prompt: OSINT Agent Graph Visualization Dashboard

## Project Overview
Build an interactive, real-time dashboard for visualizing OSINT investigation knowledge graphs with React, TypeScript, and modern UI components.

---

## Core Requirements

### 1. Technology Stack
- **Framework**: React 18+ with TypeScript
- **Styling**: Tailwind CSS
- **Graph Visualization**: react-force-graph-2d or vis-network
- **State Management**: React Context API or Zustand
- **API Client**: Axios with real-time updates
- **UI Components**: Shadcn/ui or Headless UI
- **Icons**: Lucide React or Heroicons

### 2. Pages & Routes

```
/                       → Dashboard Overview
/investigations         → Investigation List
/investigations/:id     → Investigation Detail + Graph View
/graph                  → Global Knowledge Graph Explorer
/search                 → Entity Search
```

---

## Detailed Component Specifications

### Page 1: Dashboard Overview (`/`)

**Components:**
- Statistics Cards (4x grid)
  - Total Investigations
  - Active Investigations
  - Total Entities (from graph)
  - Average Confidence Score

- Recent Investigations Table
  - Columns: ID, Objective, Status, Findings, Confidence, Date
  - Click row → navigate to detail

- Graph Statistics Mini-View
  - Total Nodes by Type (pie/donut chart)
  - Total Relationships
  - Recent Growth (trend)

**API Endpoints:**
```typescript
GET /stats                    // Dashboard statistics
GET /investigations?limit=10  // Recent investigations
GET /graph/stats             // Graph statistics
```

**Sample Code:**
```typescript
interface DashboardStats {
  total_investigations: number;
  active_investigations: number;
  completed_investigations: number;
  failed_investigations: number;
  avg_confidence: number;
  total_findings: number;
  graph_stats: {
    total_nodes: number;
    total_relationships: number;
    nodes: Record<string, number>;
  };
}

const DashboardPage = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);

  useEffect(() => {
    axios.get('http://YOUR_NAS_IP:8081/stats')
      .then(res => setStats(res.data));
  }, []);

  // Render stats cards and charts
};
```

---

### Page 2: Investigation Detail + Graph View (`/investigations/:id`)

**Layout:**
- Left Sidebar (30%): Investigation details
- Right Panel (70%): Interactive graph visualization

**Investigation Details Panel:**
```
• Investigation ID
• Objective
• Status (badge with color)
• Created/Completed dates
• Findings count
• Confidence score (progress bar)
• Action buttons (Re-run, Export, Delete)
```

**Graph Visualization Panel:**
- **Interactive Force-Directed Graph** using react-force-graph-2d
- Node Types (color-coded):
  - Investigation (purple, larger)
  - Domain (blue)
  - IP Address (green)
  - Organization (orange)
  - Threat Actor (red)
  - Indicator (yellow)

- **Node Interactions:**
  - Click → Show details panel
  - Hover → Tooltip with key info
  - Double-click → Expand connections

- **Controls:**
  - Zoom in/out
  - Reset view
  - Filter by node type
  - Search entity
  - Export PNG/SVG

**API Endpoints:**
```typescript
GET /investigations/:id              // Investigation details
GET /graph/investigation/:id         // Graph data
GET /graph/entity/:type/:id/connections  // Entity connections
```

**Graph Component Example:**
```typescript
import ForceGraph2D from 'react-force-graph-2d';

interface GraphNode {
  id: string;
  label: string;
  type: string;
  properties: any;
}

interface GraphEdge {
  source: string;
  target: string;
  type: string;
  properties: any;
}

const InvestigationGraphView = ({ investigationId }: { investigationId: string }) => {
  const [graphData, setGraphData] = useState<{ nodes: GraphNode[]; edges: GraphEdge[] }>({
    nodes: [],
    edges: []
  });

  useEffect(() => {
    axios.get(`http://YOUR_NAS_IP:8081/graph/investigation/${investigationId}`)
      .then(res => setGraphData({
        nodes: res.data.nodes,
        edges: res.data.edges.map((e: any) => ({
          ...e,
          source: e.source,
          target: e.target
        }))
      }));
  }, [investigationId]);

  const NODE_COLORS = {
    Investigation: '#8b5cf6',
    Domain: '#3b82f6',
    IPAddress: '#10b981',
    Organization: '#f59e0b',
    ThreatActor: '#ef4444',
    Indicator: '#eab308'
  };

  return (
    <ForceGraph2D
      graphData={graphData}
      nodeLabel="label"
      nodeColor={node => NODE_COLORS[node.type] || '#gray'}
      nodeRelSize={8}
      linkDirectionalArrowLength={3.5}
      linkDirectionalArrowRelPos={1}
      linkCurvature={0.25}
      onNodeClick={handleNodeClick}
      onNodeHover={handleNodeHover}
      width={800}
      height={600}
    />
  );
};
```

---

### Page 3: Global Knowledge Graph Explorer (`/graph`)

**Features:**
- Full knowledge graph visualization (all nodes and edges)
- Advanced filtering:
  - By entity type (checkboxes)
  - By investigation
  - By date range
  - By confidence threshold

- Search bar (highlights matching nodes)
- Statistics panel (live updates)
- Legend (node types and colors)

**Graph Controls:**
- Layout algorithm selector (force, hierarchical, circular)
- Node size by (degree, confidence, findings)
- Show/hide labels
- Cluster by type

**API Endpoints:**
```typescript
GET /graph/overview              // Full graph overview
GET /graph/search?query=...      // Search entities
GET /graph/stats                 // Graph statistics
```

---

### Page 4: Entity Search (`/search`)

**Search Interface:**
- Search input with autocomplete
- Entity type filters (multi-select)
- Results as cards:
  - Entity type icon
  - Entity value
  - Associated investigations count
  - Click → Show entity detail modal

**Entity Detail Modal:**
- Entity information (all properties)
- Associated investigations list
- Connection graph (1-2 hops)
- Action: "View in Full Graph"

**API Endpoints:**
```typescript
GET /graph/search?query=example&entity_types=Domain,IPAddress
GET /graph/entity/:type/:id/investigations
GET /graph/entity/:type/:id/connections?max_depth=2
```

---

## Real-Time Updates

### WebSocket Integration
```typescript
const useInvestigationUpdates = (investigationId: string) => {
  const [status, setStatus] = useState('');

  useEffect(() => {
    const ws = new WebSocket(`ws://YOUR_NAS_IP:8081/ws/investigations/${investigationId}`);

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'status_update') {
        setStatus(data.status);
      } else if (data.type === 'completed') {
        setStatus('completed');
        // Refresh graph data
      }
    };

    return () => ws.close();
  }, [investigationId]);

  return status;
};
```

---

## Design System

### Color Palette
```css
/* Primary */
--purple-600: #8b5cf6;  /* Investigation */
--blue-600: #3b82f6;    /* Domain */
--green-600: #10b981;   /* IP */
--orange-600: #f59e0b;  /* Organization */
--red-600: #ef4444;     /* Threat Actor */
--yellow-600: #eab308;  /* Indicator */

/* Status Colors */
--status-running: #3b82f6;
--status-completed: #10b981;
--status-failed: #ef4444;
--status-pending: #6b7280;
```

### Typography
```
Headings: Inter or system-ui
Body: -apple-system, BlinkMacSystemFont, 'Segoe UI', ...
Code: 'Fira Code', monospace
```

---

## Sample API Configuration

```typescript
// src/config/api.ts
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8081';

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});
```

---

## Key Features to Implement

### 1. Investigation List with Filters
```typescript
const InvestigationList = () => {
  const [investigations, setInvestigations] = useState([]);
  const [statusFilter, setStatusFilter] = useState('all');

  const fetchInvestigations = () => {
    const params = statusFilter !== 'all' ? { status: statusFilter } : {};
    api.get('/investigations', { params }).then(res => setInvestigations(res.data));
  };

  // Filter buttons: All, In Progress, Completed, Failed
};
```

### 2. Graph Filtering UI
```typescript
const GraphFilters = ({ onChange }: { onChange: (filters: any) => void }) => {
  const [nodeTypes, setNodeTypes] = useState({
    Domain: true,
    IPAddress: true,
    Organization: true,
    ThreatActor: true,
    Indicator: true
  });

  return (
    <div className="filter-panel">
      {Object.keys(nodeTypes).map(type => (
        <label key={type}>
          <input
            type="checkbox"
            checked={nodeTypes[type]}
            onChange={e => {
              const updated = { ...nodeTypes, [type]: e.target.checked };
              setNodeTypes(updated);
              onChange(updated);
            }}
          />
          {type}
        </label>
      ))}
    </div>
  );
};
```

### 3. Entity Detail Panel
```typescript
const EntityDetailPanel = ({ entity }: { entity: GraphNode }) => {
  const [connections, setConnections] = useState([]);

  useEffect(() => {
    api.get(`/graph/entity/${entity.type}/${entity.id}/connections?max_depth=2`)
      .then(res => setConnections(res.data.connections));
  }, [entity]);

  return (
    <div className="entity-panel">
      <h3>{entity.label}</h3>
      <div className="entity-type-badge">{entity.type}</div>
      <dl>
        {Object.entries(entity.properties).map(([key, value]) => (
          <div key={key}>
            <dt>{key}</dt>
            <dd>{String(value)}</dd>
          </div>
        ))}
      </dl>
      <h4>Connected Entities ({connections.length})</h4>
      <ul>
        {connections.map(conn => (
          <li key={conn.data.id}>{conn.type}: {conn.data.name || conn.data.address || conn.data.value}</li>
        ))}
      </ul>
    </div>
  );
};
```

---

## Deployment Instructions

### 1. Configure API URL
Create `.env` file:
```bash
REACT_APP_API_URL=http://YOUR_NAS_IP:8081
```

### 2. Build for Production
Lovable will handle deployment, but for manual:
```bash
npm run build
```

### 3. Deploy Options
- **Lovable Hosting** (recommended): Automatic via Lovable platform
- **Vercel**: Connect to GitHub repo, auto-deploy
- **NAS Static Hosting**: Copy build folder to `/var/www/dashboard`

---

## Lovable-Specific Instructions

When you create this project in Lovable:

1. **Start with the prompt:**
   "Create a React TypeScript dashboard for OSINT investigation visualization with the following pages: Dashboard Overview, Investigation List, Investigation Detail with graph visualization, Global Knowledge Graph Explorer, and Entity Search. Use Tailwind CSS, react-force-graph-2d for graph visualization, and connect to a FastAPI backend at http://YOUR_NAS_IP:8081"

2. **Iterate with specific requests:**
   - "Add the Dashboard Overview page with stats cards showing total investigations, active investigations, total entities, and average confidence score"
   - "Create the Investigation Detail page with a split view: left sidebar for details, right panel for interactive graph visualization using react-force-graph-2d"
   - "Implement real-time updates using WebSocket connection to ws://YOUR_NAS_IP:8081/ws/investigations/:id"
   - "Add entity search with autocomplete and filters"
   - "Create graph filtering controls for node types with checkboxes"

3. **Customize the graph visualization:**
   - "Make nodes color-coded by type: Investigation (purple), Domain (blue), IP (green), Organization (orange), Threat Actor (red), Indicator (yellow)"
   - "Add click handlers to show entity details in a side panel"
   - "Implement zoom controls and reset view button"
   - "Add node search that highlights matching nodes"

4. **Polish the UI:**
   - "Add loading skeletons for all async data"
   - "Implement error boundaries and error messages"
   - "Add toast notifications for investigation updates"
   - "Create responsive layout for mobile/tablet"

---

## Example Full Lovable Prompt

Copy this into Lovable to start:

```
Create a modern, interactive dashboard for visualizing OSINT investigation knowledge graphs using React, TypeScript, and Tailwind CSS.

PAGES:
1. Dashboard (/) - Stats cards, recent investigations table, graph statistics
2. Investigation Detail (/investigations/:id) - Split view with details sidebar and interactive graph
3. Global Graph Explorer (/graph) - Full knowledge graph with advanced filtering
4. Entity Search (/search) - Search entities with autocomplete and detail view

GRAPH VISUALIZATION:
- Use react-force-graph-2d for interactive force-directed graphs
- Node types (color-coded): Investigation (purple), Domain (blue), IPAddress (green), Organization (orange), ThreatActor (red), Indicator (yellow)
- Node interactions: click for details, hover for tooltip, double-click to expand
- Graph controls: zoom, reset, filter by type, search, export

API INTEGRATION:
Backend: http://YOUR_NAS_IP:8081
Endpoints:
- GET /stats - Dashboard statistics
- GET /investigations - List investigations
- GET /investigations/:id - Investigation details
- GET /graph/investigation/:id - Graph data for visualization
- GET /graph/stats - Graph statistics
- GET /graph/search?query=... - Search entities
- GET /graph/entity/:type/:id/connections - Entity connections
- WebSocket: ws://YOUR_NAS_IP:8081/ws/investigations/:id for real-time updates

REAL-TIME FEATURES:
- WebSocket connection for live investigation status updates
- Auto-refresh graph when investigation completes
- Toast notifications for status changes

UI/UX:
- Modern, clean design with Tailwind CSS
- Responsive layout
- Loading skeletons
- Error boundaries
- Dark mode support (optional but nice)
- Smooth animations

Create the Dashboard Overview page first with:
1. Four statistics cards in a grid layout showing total investigations, active investigations, total entities from graph, and average confidence score
2. Recent investigations table with columns: ID, Objective, Status (colored badge), Findings, Confidence (progress bar), Date
3. Graph statistics section showing total nodes by type as a simple bar chart

Connect to the API at http://YOUR_NAS_IP:8081/stats for the statistics data.
```

---

## Testing Checklist

After Lovable builds the dashboard:

- [ ] Dashboard loads and shows statistics from API
- [ ] Investigation list displays and filters work
- [ ] Investigation detail page loads graph data
- [ ] Graph visualization renders correctly with color-coded nodes
- [ ] Node click shows entity details
- [ ] Graph zoom and pan work smoothly
- [ ] Entity search returns results
- [ ] WebSocket connects and receives updates
- [ ] All pages are responsive on mobile
- [ ] Loading states show properly
- [ ] Error handling works (test with API offline)

---

## Environment Variables

```bash
# .env.local
REACT_APP_API_URL=http://YOUR_NAS_IP:8081
REACT_APP_WS_URL=ws://YOUR_NAS_IP:8081
```

Replace `YOUR_NAS_IP` with your actual Synology NAS IP address (e.g., `192.168.1.100` or use TwinGate hostname).

---

## Next Steps After Building

1. **Deploy to Lovable Hosting**
   - Lovable provides free hosting
   - Custom domain supported

2. **Or Deploy to Vercel**
   - Connect GitHub repo
   - Auto-deploy on push
   - Add environment variables in Vercel dashboard

3. **Integrate with Home Lab**
   - Set up TwinGate access for secure remote access
   - Configure Nginx reverse proxy on NAS
   - Enable HTTPS with Let's Encrypt

4. **Add Advanced Features** (Future)
   - Export graphs as PNG/SVG
   - PDF report generation
   - Email alerts for high-priority findings
   - Scheduled investigations
   - Multi-user authentication

---

## Support Resources

- **react-force-graph**: https://github.com/vasturiano/react-force-graph
- **FastAPI WebSocket**: https://fastapi.tiangolo.com/advanced/websockets/
- **Tailwind CSS**: https://tailwindcss.com/docs
- **Lovable Docs**: https://docs.lovable.dev

---

**Good luck building your OSINT visualization dashboard! 🚀**
