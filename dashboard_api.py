"""
OSINT Agent Dashboard API

FastAPI backend for the Lovable dashboard with real-time updates and graph visualization
"""

import asyncio
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.memory.graph_store import GraphStore
from src.utils.entity_extractor import EntityExtractor

# Initialize FastAPI
app = FastAPI(
    title="OSINT Agent Dashboard API",
    description="Real-time dashboard for AI-powered OSINT investigations",
    version="1.0.0"
)

# CORS middleware for Lovable frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
active_investigations: Dict[str, Dict] = {}
websocket_connections: Dict[str, List[WebSocket]] = {}

# Initialize graph store
graph_store = GraphStore()


# ========== Pydantic Models ==========

class InvestigationRequest(BaseModel):
    """Request to start new investigation"""
    target: str
    objective: str
    constraints: Optional[Dict] = None


class InvestigationResponse(BaseModel):
    """Investigation response"""
    investigation_id: str
    status: str
    message: str


class DashboardStats(BaseModel):
    """Dashboard statistics"""
    total_investigations: int
    active_investigations: int
    completed_investigations: int
    failed_investigations: int
    avg_confidence: float
    total_findings: int
    graph_stats: Dict


class Investigation(BaseModel):
    """Investigation summary"""
    id: str
    objective: str
    status: str
    created_at: str
    findings_count: int
    confidence: Optional[float]


class GraphNode(BaseModel):
    """Graph node for visualization"""
    id: str
    label: str
    type: str
    properties: Dict


class GraphEdge(BaseModel):
    """Graph edge for visualization"""
    source: str
    target: str
    type: str
    properties: Dict


class GraphData(BaseModel):
    """Complete graph data"""
    nodes: List[GraphNode]
    edges: List[GraphEdge]
    investigation_id: Optional[str] = None


class EntitySearchResult(BaseModel):
    """Entity search result"""
    type: str
    data: Dict


# ========== Helper Functions ==========

async def get_mock_investigations_data() -> List[Dict]:
    """
    Get investigations data
    In production, this would query PostgreSQL
    For now, returns mock data mixed with real graph data
    """
    # Mock data for demonstration
    investigations = [
        {
            "id": "inv_001",
            "objective": "Investigate example.com for security intelligence",
            "status": "completed",
            "created_at": datetime.now().isoformat(),
            "findings_count": 5,
            "confidence": 0.85
        },
        {
            "id": "inv_002",
            "objective": "Analyze github.com infrastructure",
            "status": "completed",
            "created_at": datetime.now().isoformat(),
            "findings_count": 8,
            "confidence": 0.92
        }
    ]

    # Add active investigations
    for inv_id, inv_data in active_investigations.items():
        investigations.append({
            "id": inv_id,
            "objective": inv_data.get("objective", ""),
            "status": inv_data.get("status", "in_progress"),
            "created_at": inv_data.get("started_at", datetime.now().isoformat()),
            "findings_count": inv_data.get("findings_count", 0),
            "confidence": inv_data.get("confidence")
        })

    return investigations


async def broadcast_to_websockets(investigation_id: str, message: Dict):
    """Broadcast message to all WebSocket clients for an investigation"""
    if investigation_id in websocket_connections:
        dead_connections = []
        for ws in websocket_connections[investigation_id]:
            try:
                await ws.send_json(message)
            except:
                dead_connections.append(ws)

        # Clean up dead connections
        for ws in dead_connections:
            websocket_connections[investigation_id].remove(ws)


# ========== Basic Dashboard Endpoints ==========

@app.get("/")
async def root():
    """API root"""
    return {
        "name": "OSINT Agent Dashboard API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "stats": "/stats",
            "investigations": "/investigations",
            "graph": "/graph/*"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    graph_connected = await graph_store.verify_connection()

    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "api": "running",
            "neo4j": "connected" if graph_connected else "disconnected"
        }
    }


@app.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats():
    """Get dashboard statistics"""
    investigations = await get_mock_investigations_data()

    total = len(investigations)
    active = sum(1 for inv in investigations if inv['status'] == 'in_progress')
    completed = sum(1 for inv in investigations if inv['status'] == 'completed')
    failed = sum(1 for inv in investigations if inv['status'] == 'failed')

    # Calculate average confidence
    confidences = [inv['confidence'] for inv in investigations if inv.get('confidence')]
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0

    # Total findings
    total_findings = sum(inv.get('findings_count', 0) for inv in investigations)

    # Get graph statistics
    try:
        graph_stats = await graph_store.get_graph_stats()
    except:
        graph_stats = {"total_nodes": 0, "total_relationships": 0}

    return DashboardStats(
        total_investigations=total,
        active_investigations=active,
        completed_investigations=completed,
        failed_investigations=failed,
        avg_confidence=round(avg_confidence, 2),
        total_findings=total_findings,
        graph_stats=graph_stats
    )


@app.get("/investigations", response_model=List[Investigation])
async def get_investigations(
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: int = Query(50, description="Maximum results")
):
    """Get list of investigations"""
    investigations = await get_mock_investigations_data()

    # Filter by status if provided
    if status:
        investigations = [inv for inv in investigations if inv['status'] == status]

    # Limit results
    investigations = investigations[:limit]

    return [Investigation(**inv) for inv in investigations]


@app.get("/investigations/{investigation_id}")
async def get_investigation_detail(investigation_id: str):
    """Get detailed investigation information"""
    investigations = await get_mock_investigations_data()

    investigation = next((inv for inv in investigations if inv['id'] == investigation_id), None)

    if not investigation:
        raise HTTPException(status_code=404, detail="Investigation not found")

    # Get graph data for this investigation
    try:
        graph_data = await graph_store.get_investigation_graph(investigation_id)
    except:
        graph_data = {"nodes": [], "edges": []}

    return {
        **investigation,
        "graph": graph_data
    }


@app.post("/investigate", response_model=InvestigationResponse)
async def start_investigation(request: InvestigationRequest):
    """
    Start new investigation (background task)

    In production, this would trigger the actual OSINT agent
    For now, creates a placeholder investigation
    """
    investigation_id = f"inv_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    # Store in active investigations
    active_investigations[investigation_id] = {
        "target": request.target,
        "objective": request.objective,
        "status": "in_progress",
        "started_at": datetime.now().isoformat(),
        "findings_count": 0
    }

    # Create investigation node in graph
    try:
        await graph_store.create_investigation_node(
            investigation_id=investigation_id,
            objective=request.objective,
            status="in_progress",
            metadata={"target": request.target}
        )
    except Exception as e:
        print(f"Graph creation error: {e}")

    # Start background task (mock for now)
    asyncio.create_task(run_investigation_background(investigation_id, request.target, request.objective))

    return InvestigationResponse(
        investigation_id=investigation_id,
        status="started",
        message=f"Investigation {investigation_id} started successfully"
    )


async def run_investigation_background(investigation_id: str, target: str, objective: str):
    """
    Background task to run investigation

    In production, this would call the OSINT agent
    """
    try:
        # Simulate investigation progress
        await asyncio.sleep(2)

        # Update status
        active_investigations[investigation_id]["status"] = "collecting"
        await broadcast_to_websockets(investigation_id, {
            "type": "status_update",
            "status": "collecting",
            "message": "Collecting intelligence from sources..."
        })

        await asyncio.sleep(3)

        # Simulate findings
        findings_count = 5
        confidence = 0.85

        active_investigations[investigation_id].update({
            "status": "completed",
            "findings_count": findings_count,
            "confidence": confidence,
            "completed_at": datetime.now().isoformat()
        })

        # Update graph
        try:
            await graph_store.update_investigation_node(
                investigation_id=investigation_id,
                status="completed",
                findings_count=findings_count,
                confidence=confidence
            )
        except Exception as e:
            print(f"Graph update error: {e}")

        # Broadcast completion
        await broadcast_to_websockets(investigation_id, {
            "type": "completed",
            "status": "completed",
            "findings_count": findings_count,
            "confidence": confidence
        })

    except Exception as e:
        print(f"Investigation error: {e}")
        active_investigations[investigation_id]["status"] = "failed"
        await broadcast_to_websockets(investigation_id, {
            "type": "error",
            "message": str(e)
        })


@app.get("/active-investigations")
async def get_active_investigations():
    """Get currently running investigations"""
    return {
        "active_count": len(active_investigations),
        "investigations": active_investigations
    }


# ========== WebSocket Endpoint ==========

@app.websocket("/ws/investigations/{investigation_id}")
async def websocket_endpoint(websocket: WebSocket, investigation_id: str):
    """WebSocket endpoint for real-time investigation updates"""
    await websocket.accept()

    # Add to connections
    if investigation_id not in websocket_connections:
        websocket_connections[investigation_id] = []
    websocket_connections[investigation_id].append(websocket)

    try:
        # Send initial status
        if investigation_id in active_investigations:
            await websocket.send_json({
                "type": "connected",
                "investigation_id": investigation_id,
                "status": active_investigations[investigation_id].get("status")
            })

        # Keep connection alive
        while True:
            data = await websocket.receive_text()
            # Echo back or handle commands
            await websocket.send_json({"type": "echo", "data": data})

    except WebSocketDisconnect:
        websocket_connections[investigation_id].remove(websocket)


# ========== Graph Visualization Endpoints (Day 13) ==========

@app.get("/graph/investigation/{investigation_id}", response_model=GraphData)
async def get_investigation_graph(investigation_id: str):
    """
    Get knowledge graph for an investigation

    Returns nodes and edges for visualization
    """
    try:
        graph_data = await graph_store.get_investigation_graph(investigation_id, depth=2)

        return GraphData(
            nodes=[GraphNode(**node) for node in graph_data['nodes']],
            edges=[GraphEdge(**edge) for edge in graph_data['edges']],
            investigation_id=investigation_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Graph retrieval failed: {str(e)}")


@app.get("/graph/entity/{entity_type}/{entity_id}/connections")
async def get_entity_connections(
    entity_type: str,
    entity_id: str,
    max_depth: int = Query(3, description="Maximum traversal depth")
):
    """
    Find entities connected to a specific entity

    Args:
        entity_type: Type of entity (Domain, IPAddress, Organization, etc.)
        entity_id: Entity identifier
        max_depth: Maximum graph traversal depth
    """
    try:
        connections = await graph_store.find_entity_connections(
            entity_type=entity_type,
            entity_id=entity_id,
            max_depth=max_depth
        )
        return connections
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection search failed: {str(e)}")


@app.get("/graph/entity/{entity_type}/{entity_id}/investigations")
async def get_entity_investigations(entity_type: str, entity_id: str):
    """
    Find all investigations involving a specific entity

    Args:
        entity_type: Type of entity
        entity_id: Entity identifier
    """
    try:
        investigations = await graph_store.find_related_investigations(
            entity_type=entity_type,
            entity_id=entity_id
        )
        return {
            "entity": {"type": entity_type, "id": entity_id},
            "investigations": investigations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Investigation search failed: {str(e)}")


@app.get("/graph/stats")
async def get_graph_statistics():
    """Get overall knowledge graph statistics"""
    try:
        stats = await graph_store.get_graph_stats()
        return {
            "timestamp": datetime.now().isoformat(),
            "statistics": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stats retrieval failed: {str(e)}")


@app.get("/graph/search", response_model=List[EntitySearchResult])
async def search_entities(
    query: str = Query(..., description="Search query"),
    entity_types: Optional[str] = Query(None, description="Comma-separated entity types"),
    limit: int = Query(20, description="Maximum results")
):
    """
    Search for entities in the knowledge graph

    Args:
        query: Search text
        entity_types: Optional comma-separated list of entity types to search
        limit: Maximum results
    """
    try:
        # Parse entity types
        types_list = None
        if entity_types:
            types_list = [t.strip() for t in entity_types.split(',')]

        results = await graph_store.search_entities(
            query=query,
            entity_types=types_list,
            limit=limit
        )

        return [EntitySearchResult(**result) for result in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@app.get("/graph/overview")
async def get_graph_overview():
    """
    Get comprehensive graph overview

    Returns statistics, recent investigations, and entity summaries
    """
    try:
        # Get statistics
        stats = await graph_store.get_graph_stats()

        # Mock recent investigations (in production, query from database)
        recent_investigations = await get_mock_investigations_data()
        recent_investigations = sorted(
            recent_investigations,
            key=lambda x: x.get('created_at', ''),
            reverse=True
        )[:5]

        return {
            "stats": stats,
            "recent_investigations": recent_investigations,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Overview retrieval failed: {str(e)}")


@app.post("/graph/initialize")
async def initialize_graph_schema():
    """Initialize Neo4j schema (constraints and indexes)"""
    try:
        await graph_store.initialize_schema()
        return {
            "status": "success",
            "message": "Graph schema initialized successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Schema initialization failed: {str(e)}")


# ========== Startup Event ==========

@app.on_event("startup")
async def startup_event():
    """Initialize connections on startup"""
    print("🚀 Starting OSINT Dashboard API...")

    # Test graph connection
    connected = await graph_store.verify_connection()
    if connected:
        print("✓ Neo4j connection verified")
        # Initialize schema
        try:
            await graph_store.initialize_schema()
            print("✓ Graph schema initialized")
        except Exception as e:
            print(f"⚠ Schema initialization warning: {e}")
    else:
        print("⚠ Neo4j connection failed - graph features will be limited")

    print("✓ Dashboard API ready")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("👋 Shutting down OSINT Dashboard API...")
    await graph_store.close()


# ========== Main ==========

if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("DASHBOARD_PORT", 8081))

    print(f"""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║              OSINT Agent Dashboard API                        ║
    ║                                                               ║
    ║  Running on: http://0.0.0.0:{port}                         ║
    ║  Docs: http://0.0.0.0:{port}/docs                          ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)

    uvicorn.run(app, host="0.0.0.0", port=port)
