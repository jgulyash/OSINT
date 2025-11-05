"""
Memory and Data Persistence System for OSINT Agent

Provides short-term and long-term memory storage for investigations
"""

import json
import sqlite3
import asyncio
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
import hashlib


class MemoryStore:
    """
    Persistent memory storage for OSINT investigations
    Uses SQLite for structured storage and JSON for flexible data
    """

    def __init__(self, db_path: str = "data/osint_memory.db"):
        """
        Initialize memory store

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._ensure_db_directory()
        self.conn = None
        self._init_database()

    def _ensure_db_directory(self):
        """Ensure database directory exists"""
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)

    def _init_database(self):
        """Initialize database schema"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

        cursor = self.conn.cursor()

        # Investigations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS investigations (
                id TEXT PRIMARY KEY,
                objective TEXT NOT NULL,
                status TEXT DEFAULT 'active',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                metadata TEXT
            )
        ''')

        # Actions/Events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                investigation_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                phase TEXT NOT NULL,
                action TEXT NOT NULL,
                data TEXT,
                FOREIGN KEY (investigation_id) REFERENCES investigations(id)
            )
        ''')

        # Findings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS findings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                investigation_id TEXT NOT NULL,
                finding_type TEXT NOT NULL,
                content TEXT NOT NULL,
                confidence REAL,
                source TEXT,
                timestamp TEXT NOT NULL,
                metadata TEXT,
                FOREIGN KEY (investigation_id) REFERENCES investigations(id)
            )
        ''')

        # Entities table (people, orgs, domains, IPs, etc.)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS entities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                investigation_id TEXT NOT NULL,
                entity_type TEXT NOT NULL,
                name TEXT NOT NULL,
                attributes TEXT,
                first_seen TEXT NOT NULL,
                last_seen TEXT NOT NULL,
                FOREIGN KEY (investigation_id) REFERENCES investigations(id)
            )
        ''')

        # Relationships table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS relationships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                investigation_id TEXT NOT NULL,
                entity1_id INTEGER NOT NULL,
                entity2_id INTEGER NOT NULL,
                relationship_type TEXT NOT NULL,
                confidence REAL,
                metadata TEXT,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (investigation_id) REFERENCES investigations(id),
                FOREIGN KEY (entity1_id) REFERENCES entities(id),
                FOREIGN KEY (entity2_id) REFERENCES entities(id)
            )
        ''')

        # Create indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_actions_investigation ON actions(investigation_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_actions_timestamp ON actions(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_findings_investigation ON findings(investigation_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_entities_investigation ON entities(investigation_id)')

        self.conn.commit()

    async def store(self, entry: Dict[str, Any]) -> bool:
        """
        Store an entry in memory

        Args:
            entry: Entry data with investigation_id, phase, action, data

        Returns:
            Success status
        """
        try:
            cursor = self.conn.cursor()

            investigation_id = entry.get('investigation_id')
            timestamp = entry.get('timestamp', datetime.now().isoformat())
            phase = entry.get('phase', 'unknown')
            action = entry.get('action', 'unknown')
            data = json.dumps(entry.get('data', {}))

            cursor.execute('''
                INSERT INTO actions (investigation_id, timestamp, phase, action, data)
                VALUES (?, ?, ?, ?, ?)
            ''', (investigation_id, timestamp, phase, action, data))

            self.conn.commit()
            return True

        except Exception as e:
            print(f"Error storing entry: {e}")
            return False

    async def create_investigation(self, investigation_id: str, objective: str, metadata: Optional[Dict] = None) -> bool:
        """
        Create new investigation record

        Args:
            investigation_id: Unique investigation ID
            objective: Investigation objective
            metadata: Optional metadata

        Returns:
            Success status
        """
        try:
            cursor = self.conn.cursor()

            timestamp = datetime.now().isoformat()

            cursor.execute('''
                INSERT INTO investigations (id, objective, status, created_at, updated_at, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (investigation_id, objective, 'active', timestamp, timestamp, json.dumps(metadata or {})))

            self.conn.commit()
            return True

        except Exception as e:
            print(f"Error creating investigation: {e}")
            return False

    async def update_investigation_status(self, investigation_id: str, status: str) -> bool:
        """
        Update investigation status

        Args:
            investigation_id: Investigation ID
            status: New status (active, completed, failed)

        Returns:
            Success status
        """
        try:
            cursor = self.conn.cursor()

            cursor.execute('''
                UPDATE investigations
                SET status = ?, updated_at = ?
                WHERE id = ?
            ''', (status, datetime.now().isoformat(), investigation_id))

            self.conn.commit()
            return True

        except Exception as e:
            print(f"Error updating investigation: {e}")
            return False

    async def get_by_investigation(self, investigation_id: str, limit: Optional[int] = None) -> List[Dict]:
        """
        Get all actions for an investigation

        Args:
            investigation_id: Investigation ID
            limit: Optional limit on number of results

        Returns:
            List of action entries
        """
        try:
            cursor = self.conn.cursor()

            query = 'SELECT * FROM actions WHERE investigation_id = ? ORDER BY timestamp DESC'
            if limit:
                query += f' LIMIT {limit}'

            cursor.execute(query, (investigation_id,))

            rows = cursor.fetchall()
            return [dict(row) for row in rows]

        except Exception as e:
            print(f"Error retrieving actions: {e}")
            return []

    async def store_finding(
        self,
        investigation_id: str,
        finding_type: str,
        content: str,
        confidence: float = 0.5,
        source: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> bool:
        """
        Store an intelligence finding

        Args:
            investigation_id: Investigation ID
            finding_type: Type of finding
            content: Finding content
            confidence: Confidence level (0-1)
            source: Data source
            metadata: Additional metadata

        Returns:
            Success status
        """
        try:
            cursor = self.conn.cursor()

            cursor.execute('''
                INSERT INTO findings (investigation_id, finding_type, content, confidence, source, timestamp, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                investigation_id,
                finding_type,
                content,
                confidence,
                source or 'unknown',
                datetime.now().isoformat(),
                json.dumps(metadata or {})
            ))

            self.conn.commit()
            return True

        except Exception as e:
            print(f"Error storing finding: {e}")
            return False

    async def get_findings(self, investigation_id: str, min_confidence: float = 0.0) -> List[Dict]:
        """
        Get findings for an investigation

        Args:
            investigation_id: Investigation ID
            min_confidence: Minimum confidence threshold

        Returns:
            List of findings
        """
        try:
            cursor = self.conn.cursor()

            cursor.execute('''
                SELECT * FROM findings
                WHERE investigation_id = ? AND confidence >= ?
                ORDER BY confidence DESC, timestamp DESC
            ''', (investigation_id, min_confidence))

            rows = cursor.fetchall()
            return [dict(row) for row in rows]

        except Exception as e:
            print(f"Error retrieving findings: {e}")
            return []

    async def store_entity(
        self,
        investigation_id: str,
        entity_type: str,
        name: str,
        attributes: Optional[Dict] = None
    ) -> int:
        """
        Store an entity (person, organization, domain, etc.)

        Args:
            investigation_id: Investigation ID
            entity_type: Type of entity
            name: Entity name/identifier
            attributes: Additional attributes

        Returns:
            Entity ID
        """
        try:
            cursor = self.conn.cursor()

            timestamp = datetime.now().isoformat()

            # Check if entity already exists
            cursor.execute('''
                SELECT id FROM entities
                WHERE investigation_id = ? AND entity_type = ? AND name = ?
            ''', (investigation_id, entity_type, name))

            existing = cursor.fetchone()

            if existing:
                # Update last_seen
                entity_id = existing[0]
                cursor.execute('''
                    UPDATE entities SET last_seen = ?, attributes = ?
                    WHERE id = ?
                ''', (timestamp, json.dumps(attributes or {}), entity_id))
            else:
                # Insert new entity
                cursor.execute('''
                    INSERT INTO entities (investigation_id, entity_type, name, attributes, first_seen, last_seen)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (investigation_id, entity_type, name, json.dumps(attributes or {}), timestamp, timestamp))

                entity_id = cursor.lastrowid

            self.conn.commit()
            return entity_id

        except Exception as e:
            print(f"Error storing entity: {e}")
            return -1

    async def store_relationship(
        self,
        investigation_id: str,
        entity1_id: int,
        entity2_id: int,
        relationship_type: str,
        confidence: float = 0.5,
        metadata: Optional[Dict] = None
    ) -> bool:
        """
        Store relationship between entities

        Args:
            investigation_id: Investigation ID
            entity1_id: First entity ID
            entity2_id: Second entity ID
            relationship_type: Type of relationship
            confidence: Confidence level
            metadata: Additional metadata

        Returns:
            Success status
        """
        try:
            cursor = self.conn.cursor()

            cursor.execute('''
                INSERT INTO relationships (investigation_id, entity1_id, entity2_id, relationship_type, confidence, metadata, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                investigation_id,
                entity1_id,
                entity2_id,
                relationship_type,
                confidence,
                json.dumps(metadata or {}),
                datetime.now().isoformat()
            ))

            self.conn.commit()
            return True

        except Exception as e:
            print(f"Error storing relationship: {e}")
            return False

    async def get_entities(self, investigation_id: str, entity_type: Optional[str] = None) -> List[Dict]:
        """
        Get entities for an investigation

        Args:
            investigation_id: Investigation ID
            entity_type: Optional filter by entity type

        Returns:
            List of entities
        """
        try:
            cursor = self.conn.cursor()

            if entity_type:
                cursor.execute('''
                    SELECT * FROM entities
                    WHERE investigation_id = ? AND entity_type = ?
                    ORDER BY last_seen DESC
                ''', (investigation_id, entity_type))
            else:
                cursor.execute('''
                    SELECT * FROM entities
                    WHERE investigation_id = ?
                    ORDER BY last_seen DESC
                ''', (investigation_id,))

            rows = cursor.fetchall()
            return [dict(row) for row in rows]

        except Exception as e:
            print(f"Error retrieving entities: {e}")
            return []

    async def get_relationships(self, investigation_id: str) -> List[Dict]:
        """
        Get relationships for an investigation

        Args:
            investigation_id: Investigation ID

        Returns:
            List of relationships with entity details
        """
        try:
            cursor = self.conn.cursor()

            cursor.execute('''
                SELECT r.*, e1.name as entity1_name, e1.entity_type as entity1_type,
                       e2.name as entity2_name, e2.entity_type as entity2_type
                FROM relationships r
                JOIN entities e1 ON r.entity1_id = e1.id
                JOIN entities e2 ON r.entity2_id = e2.id
                WHERE r.investigation_id = ?
                ORDER BY r.timestamp DESC
            ''', (investigation_id,))

            rows = cursor.fetchall()
            return [dict(row) for row in rows]

        except Exception as e:
            print(f"Error retrieving relationships: {e}")
            return []

    async def get_investigation_summary(self, investigation_id: str) -> Dict:
        """
        Get comprehensive summary of an investigation

        Args:
            investigation_id: Investigation ID

        Returns:
            Investigation summary
        """
        try:
            cursor = self.conn.cursor()

            # Get investigation details
            cursor.execute('SELECT * FROM investigations WHERE id = ?', (investigation_id,))
            investigation = cursor.fetchone()

            if not investigation:
                return {}

            # Get counts
            cursor.execute('SELECT COUNT(*) FROM actions WHERE investigation_id = ?', (investigation_id,))
            action_count = cursor.fetchone()[0]

            cursor.execute('SELECT COUNT(*) FROM findings WHERE investigation_id = ?', (investigation_id,))
            finding_count = cursor.fetchone()[0]

            cursor.execute('SELECT COUNT(*) FROM entities WHERE investigation_id = ?', (investigation_id,))
            entity_count = cursor.fetchone()[0]

            cursor.execute('SELECT COUNT(*) FROM relationships WHERE investigation_id = ?', (investigation_id,))
            relationship_count = cursor.fetchone()[0]

            return {
                'investigation': dict(investigation),
                'counts': {
                    'actions': action_count,
                    'findings': finding_count,
                    'entities': entity_count,
                    'relationships': relationship_count
                }
            }

        except Exception as e:
            print(f"Error getting investigation summary: {e}")
            return {}

    async def list_investigations(self, status: Optional[str] = None, limit: int = 50) -> List[Dict]:
        """
        List all investigations

        Args:
            status: Optional filter by status
            limit: Maximum number of results

        Returns:
            List of investigations
        """
        try:
            cursor = self.conn.cursor()

            if status:
                cursor.execute('''
                    SELECT * FROM investigations
                    WHERE status = ?
                    ORDER BY created_at DESC
                    LIMIT ?
                ''', (status, limit))
            else:
                cursor.execute('''
                    SELECT * FROM investigations
                    ORDER BY created_at DESC
                    LIMIT ?
                ''', (limit,))

            rows = cursor.fetchall()
            return [dict(row) for row in rows]

        except Exception as e:
            print(f"Error listing investigations: {e}")
            return []

    async def export_investigation(self, investigation_id: str, format: str = 'json') -> str:
        """
        Export complete investigation data

        Args:
            investigation_id: Investigation ID
            format: Export format (json, csv)

        Returns:
            Exported data as string
        """
        summary = await self.get_investigation_summary(investigation_id)
        actions = await self.get_by_investigation(investigation_id)
        findings = await self.get_findings(investigation_id)
        entities = await self.get_entities(investigation_id)
        relationships = await self.get_relationships(investigation_id)

        data = {
            'summary': summary,
            'actions': actions,
            'findings': findings,
            'entities': entities,
            'relationships': relationships
        }

        if format == 'json':
            return json.dumps(data, indent=2, default=str)
        else:
            # For CSV, would need to flatten the data structure
            return json.dumps(data, indent=2, default=str)

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

    def __del__(self):
        """Cleanup on deletion"""
        self.close()


class InMemoryStore(MemoryStore):
    """
    In-memory variant for testing or temporary operations
    """

    def __init__(self):
        """Initialize in-memory store"""
        self.db_path = ":memory:"
        self.conn = None
        self._init_database()
