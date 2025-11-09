"""
Neo4j Knowledge Graph Store for OSINT Agent

Stores entities, relationships, and investigation graphs
"""

import os
from typing import Dict, List, Optional, Any
from datetime import datetime
import asyncio
from neo4j import AsyncGraphDatabase, AsyncDriver


class GraphStore:
    """Knowledge graph storage using Neo4j"""

    def __init__(self, uri: str = None, user: str = None, password: str = None):
        """
        Initialize Neo4j connection

        Args:
            uri: Neo4j URI (default: from env or bolt://localhost:7687)
            user: Neo4j user (default: from env or neo4j)
            password: Neo4j password (default: from env or password)
        """
        self.uri = uri or os.getenv('NEO4J_URI', 'bolt://localhost:7687')
        self.user = user or os.getenv('NEO4J_USER', 'neo4j')
        self.password = password or os.getenv('NEO4J_PASSWORD', 'password')
        self.driver: Optional[AsyncDriver] = None

    async def connect(self):
        """Establish connection to Neo4j"""
        if not self.driver:
            self.driver = AsyncGraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password)
            )

    async def close(self):
        """Close Neo4j connection"""
        if self.driver:
            await self.driver.close()
            self.driver = None

    async def verify_connection(self) -> bool:
        """Verify Neo4j connection is working"""
        try:
            await self.connect()
            async with self.driver.session() as session:
                result = await session.run("RETURN 1 as num")
                record = await result.single()
                return record['num'] == 1
        except Exception as e:
            print(f"Neo4j connection failed: {e}")
            return False

    async def initialize_schema(self):
        """Create constraints and indexes for better performance"""
        await self.connect()

        constraints = [
            "CREATE CONSTRAINT IF NOT EXISTS FOR (i:Investigation) REQUIRE i.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (d:Domain) REQUIRE d.name IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (ip:IPAddress) REQUIRE ip.address IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (o:Organization) REQUIRE o.name IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (t:ThreatActor) REQUIRE t.name IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (ind:Indicator) REQUIRE ind.value IS UNIQUE"
        ]

        indexes = [
            "CREATE INDEX IF NOT EXISTS FOR (i:Investigation) ON (i.created_at)",
            "CREATE INDEX IF NOT EXISTS FOR (i:Investigation) ON (i.status)",
            "CREATE INDEX IF NOT EXISTS FOR (d:Domain) ON (d.created_at)",
            "CREATE INDEX IF NOT EXISTS FOR (ip:IPAddress) ON (ip.created_at)"
        ]

        async with self.driver.session() as session:
            for constraint in constraints:
                try:
                    await session.run(constraint)
                except Exception as e:
                    print(f"Constraint creation warning: {e}")

            for index in indexes:
                try:
                    await session.run(index)
                except Exception as e:
                    print(f"Index creation warning: {e}")

    # ========== Investigation Nodes ==========

    async def create_investigation_node(
        self,
        investigation_id: str,
        objective: str,
        status: str = "in_progress",
        metadata: Dict = None
    ) -> Dict:
        """Create Investigation node"""
        await self.connect()

        async with self.driver.session() as session:
            result = await session.run(
                """
                CREATE (i:Investigation {
                    id: $id,
                    objective: $objective,
                    status: $status,
                    created_at: datetime(),
                    metadata: $metadata
                })
                RETURN i
                """,
                id=investigation_id,
                objective=objective,
                status=status,
                metadata=metadata or {}
            )
            record = await result.single()
            return dict(record['i']) if record else {}

    async def update_investigation_node(
        self,
        investigation_id: str,
        status: str = None,
        findings_count: int = None,
        confidence: float = None
    ) -> Dict:
        """Update Investigation node"""
        await self.connect()

        updates = []
        params = {'id': investigation_id}

        if status:
            updates.append("i.status = $status")
            params['status'] = status
        if findings_count is not None:
            updates.append("i.findings_count = $findings_count")
            params['findings_count'] = findings_count
        if confidence is not None:
            updates.append("i.confidence = $confidence")
            params['confidence'] = confidence

        if not updates:
            return {}

        updates.append("i.updated_at = datetime()")

        async with self.driver.session() as session:
            result = await session.run(
                f"""
                MATCH (i:Investigation {{id: $id}})
                SET {', '.join(updates)}
                RETURN i
                """,
                **params
            )
            record = await result.single()
            return dict(record['i']) if record else {}

    # ========== Entity Nodes ==========

    async def create_domain_node(
        self,
        domain: str,
        properties: Dict = None
    ) -> Dict:
        """Create or merge Domain node"""
        await self.connect()

        props = properties or {}

        async with self.driver.session() as session:
            result = await session.run(
                """
                MERGE (d:Domain {name: $name})
                ON CREATE SET
                    d.created_at = datetime(),
                    d.first_seen = $first_seen,
                    d.registrar = $registrar,
                    d.country = $country,
                    d.confidence = $confidence
                ON MATCH SET
                    d.last_seen = datetime(),
                    d.confidence = CASE
                        WHEN $confidence > COALESCE(d.confidence, 0)
                        THEN $confidence
                        ELSE d.confidence
                    END
                RETURN d
                """,
                name=domain,
                first_seen=props.get('first_seen'),
                registrar=props.get('registrar'),
                country=props.get('country'),
                confidence=props.get('confidence', 0.8)
            )
            record = await result.single()
            return dict(record['d']) if record else {}

    async def create_ip_node(
        self,
        ip_address: str,
        properties: Dict = None
    ) -> Dict:
        """Create or merge IP Address node"""
        await self.connect()

        props = properties or {}

        async with self.driver.session() as session:
            result = await session.run(
                """
                MERGE (ip:IPAddress {address: $address})
                ON CREATE SET
                    ip.created_at = datetime(),
                    ip.country = $country,
                    ip.asn = $asn,
                    ip.org = $org,
                    ip.confidence = $confidence
                ON MATCH SET
                    ip.last_seen = datetime()
                RETURN ip
                """,
                address=ip_address,
                country=props.get('country'),
                asn=props.get('asn'),
                org=props.get('org'),
                confidence=props.get('confidence', 0.8)
            )
            record = await result.single()
            return dict(record['ip']) if record else {}

    async def create_organization_node(
        self,
        org_name: str,
        properties: Dict = None
    ) -> Dict:
        """Create or merge Organization node"""
        await self.connect()

        props = properties or {}

        async with self.driver.session() as session:
            result = await session.run(
                """
                MERGE (o:Organization {name: $name})
                ON CREATE SET
                    o.created_at = datetime(),
                    o.industry = $industry,
                    o.country = $country,
                    o.confidence = $confidence
                ON MATCH SET
                    o.last_seen = datetime()
                RETURN o
                """,
                name=org_name,
                industry=props.get('industry'),
                country=props.get('country'),
                confidence=props.get('confidence', 0.8)
            )
            record = await result.single()
            return dict(record['o']) if record else {}

    async def create_threat_actor_node(
        self,
        actor_name: str,
        properties: Dict = None
    ) -> Dict:
        """Create or merge ThreatActor node"""
        await self.connect()

        props = properties or {}

        async with self.driver.session() as session:
            result = await session.run(
                """
                MERGE (t:ThreatActor {name: $name})
                ON CREATE SET
                    t.created_at = datetime(),
                    t.attribution = $attribution,
                    t.ttps = $ttps,
                    t.confidence = $confidence
                ON MATCH SET
                    t.last_seen = datetime()
                RETURN t
                """,
                name=actor_name,
                attribution=props.get('attribution'),
                ttps=props.get('ttps', []),
                confidence=props.get('confidence', 0.8)
            )
            record = await result.single()
            return dict(record['t']) if record else {}

    async def create_indicator_node(
        self,
        indicator_value: str,
        indicator_type: str,
        properties: Dict = None
    ) -> Dict:
        """Create or merge Indicator node (IoC)"""
        await self.connect()

        props = properties or {}

        async with self.driver.session() as session:
            result = await session.run(
                """
                MERGE (ind:Indicator {value: $value})
                ON CREATE SET
                    ind.type = $type,
                    ind.created_at = datetime(),
                    ind.severity = $severity,
                    ind.confidence = $confidence
                ON MATCH SET
                    ind.last_seen = datetime()
                RETURN ind
                """,
                value=indicator_value,
                type=indicator_type,
                severity=props.get('severity', 'medium'),
                confidence=props.get('confidence', 0.8)
            )
            record = await result.single()
            return dict(record['ind']) if record else {}

    # ========== Relationships ==========

    async def create_relationship(
        self,
        from_type: str,
        from_id: str,
        rel_type: str,
        to_type: str,
        to_id: str,
        properties: Dict = None
    ) -> Dict:
        """
        Create relationship between two nodes

        Args:
            from_type: Source node label (Investigation, Domain, etc.)
            from_id: Source node identifier (id or name/address)
            rel_type: Relationship type (INVESTIGATES, RESOLVES_TO, etc.)
            to_type: Target node label
            to_id: Target node identifier
            properties: Optional relationship properties
        """
        await self.connect()

        props = properties or {}

        # Determine the property name for matching
        id_prop = 'id' if from_type == 'Investigation' else self._get_id_property(from_type)
        to_id_prop = 'id' if to_type == 'Investigation' else self._get_id_property(to_type)

        async with self.driver.session() as session:
            result = await session.run(
                f"""
                MATCH (from:{from_type} {{{id_prop}: $from_id}})
                MATCH (to:{to_type} {{{to_id_prop}: $to_id}})
                MERGE (from)-[r:{rel_type}]->(to)
                ON CREATE SET
                    r.created_at = datetime(),
                    r.confidence = $confidence,
                    r.context = $context
                RETURN r
                """,
                from_id=from_id,
                to_id=to_id,
                confidence=props.get('confidence', 0.8),
                context=props.get('context', '')
            )
            record = await result.single()
            return dict(record['r']) if record else {}

    def _get_id_property(self, node_type: str) -> str:
        """Get the ID property name for a node type"""
        if node_type == 'Domain':
            return 'name'
        elif node_type == 'IPAddress':
            return 'address'
        elif node_type in ['Organization', 'ThreatActor']:
            return 'name'
        elif node_type == 'Indicator':
            return 'value'
        return 'id'

    # ========== Query Methods ==========

    async def get_investigation_graph(
        self,
        investigation_id: str,
        depth: int = 2
    ) -> Dict:
        """
        Get complete graph for an investigation

        Returns nodes and edges for visualization
        """
        await self.connect()

        async with self.driver.session() as session:
            result = await session.run(
                """
                MATCH path = (i:Investigation {id: $id})-[*1..2]-(n)
                WITH i, collect(DISTINCT n) as nodes, collect(DISTINCT relationships(path)) as rels
                RETURN i, nodes, rels
                """,
                id=investigation_id
            )

            record = await result.single()
            if not record:
                return {'nodes': [], 'edges': []}

            # Format for visualization
            nodes = []
            edges = []

            # Add investigation node
            inv_node = dict(record['i'])
            nodes.append({
                'id': inv_node['id'],
                'label': inv_node.get('objective', 'Investigation')[:50],
                'type': 'Investigation',
                'properties': inv_node
            })

            # Add related nodes
            for node in record['nodes']:
                node_dict = dict(node)
                labels = list(node.labels)
                node_type = labels[0] if labels else 'Unknown'

                # Get appropriate ID and label
                if node_type == 'Domain':
                    node_id = node_dict.get('name')
                    node_label = node_id
                elif node_type == 'IPAddress':
                    node_id = node_dict.get('address')
                    node_label = node_id
                elif node_type in ['Organization', 'ThreatActor']:
                    node_id = node_dict.get('name')
                    node_label = node_id
                elif node_type == 'Indicator':
                    node_id = node_dict.get('value')
                    node_label = f"{node_dict.get('type', 'IOC')}: {node_id[:30]}"
                else:
                    node_id = node_dict.get('id', str(node.id))
                    node_label = str(node_id)[:50]

                nodes.append({
                    'id': node_id,
                    'label': node_label,
                    'type': node_type,
                    'properties': node_dict
                })

            # Add relationships
            for rel_list in record['rels']:
                for rel in rel_list:
                    rel_dict = dict(rel)
                    edges.append({
                        'source': rel.start_node.element_id,
                        'target': rel.end_node.element_id,
                        'type': rel.type,
                        'properties': rel_dict
                    })

            return {
                'nodes': nodes,
                'edges': edges,
                'investigation_id': investigation_id
            }

    async def find_related_investigations(
        self,
        entity_type: str,
        entity_id: str
    ) -> List[Dict]:
        """Find all investigations that involve a specific entity"""
        await self.connect()

        id_prop = self._get_id_property(entity_type)

        async with self.driver.session() as session:
            result = await session.run(
                f"""
                MATCH (e:{entity_type} {{{id_prop}: $entity_id}})--(i:Investigation)
                RETURN DISTINCT i
                ORDER BY i.created_at DESC
                """,
                entity_id=entity_id
            )

            investigations = []
            async for record in result:
                inv = dict(record['i'])
                investigations.append(inv)

            return investigations

    async def find_entity_connections(
        self,
        entity_type: str,
        entity_id: str,
        max_depth: int = 3
    ) -> Dict:
        """Find entities connected to a given entity"""
        await self.connect()

        id_prop = self._get_id_property(entity_type)

        async with self.driver.session() as session:
            result = await session.run(
                f"""
                MATCH path = (start:{entity_type} {{{id_prop}: $entity_id}})-[*1..{max_depth}]-(connected)
                WHERE NOT connected:Investigation
                RETURN DISTINCT connected, length(path) as distance
                ORDER BY distance
                LIMIT 50
                """,
                entity_id=entity_id
            )

            connections = []
            async for record in result:
                node = record['connected']
                labels = list(node.labels)
                node_type = labels[0] if labels else 'Unknown'
                node_dict = dict(node)

                connections.append({
                    'type': node_type,
                    'data': node_dict,
                    'distance': record['distance']
                })

            return {
                'entity': {'type': entity_type, 'id': entity_id},
                'connections': connections
            }

    async def get_graph_stats(self) -> Dict:
        """Get overall graph statistics"""
        await self.connect()

        async with self.driver.session() as session:
            # Count nodes by label
            result = await session.run(
                """
                MATCH (n)
                RETURN labels(n)[0] as label, count(n) as count
                """
            )

            node_counts = {}
            async for record in result:
                node_counts[record['label']] = record['count']

            # Count relationships
            result = await session.run(
                """
                MATCH ()-[r]->()
                RETURN count(r) as total_relationships
                """
            )
            record = await result.single()
            total_rels = record['total_relationships'] if record else 0

            return {
                'nodes': node_counts,
                'total_nodes': sum(node_counts.values()),
                'total_relationships': total_rels
            }

    async def search_entities(
        self,
        query: str,
        entity_types: List[str] = None,
        limit: int = 20
    ) -> List[Dict]:
        """
        Search for entities by text query

        Args:
            query: Search text
            entity_types: Optional list of entity types to search
            limit: Maximum results to return
        """
        await self.connect()

        if not entity_types:
            entity_types = ['Domain', 'IPAddress', 'Organization', 'ThreatActor', 'Indicator']

        results = []

        async with self.driver.session() as session:
            for entity_type in entity_types:
                # Determine search property
                if entity_type in ['Domain', 'Organization', 'ThreatActor']:
                    search_prop = 'name'
                elif entity_type == 'IPAddress':
                    search_prop = 'address'
                elif entity_type == 'Indicator':
                    search_prop = 'value'
                else:
                    continue

                result = await session.run(
                    f"""
                    MATCH (n:{entity_type})
                    WHERE toLower(n.{search_prop}) CONTAINS toLower($query)
                    RETURN n, '{entity_type}' as type
                    LIMIT $limit
                    """,
                    query=query,
                    limit=limit
                )

                async for record in result:
                    node_dict = dict(record['n'])
                    results.append({
                        'type': record['type'],
                        'data': node_dict
                    })

        return results[:limit]
