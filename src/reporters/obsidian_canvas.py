"""
Obsidian Canvas Generator for OSINT Investigations

Creates visual mind maps and knowledge graphs from OSINT data
that can be opened directly in Obsidian.

Canvas Types:
- Entity Relationship Maps
- Investigation Timelines
- Network Graphs
- Finding Hierarchies
- Threat Landscapes
"""

import json
import hashlib
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import colorsys


class ObsidianCanvasGenerator:
    """
    Generate Obsidian Canvas files for visualizing OSINT investigations
    """

    # Canvas node types
    NODE_TYPE_TEXT = "text"
    NODE_TYPE_FILE = "file"
    NODE_TYPE_LINK = "link"
    NODE_TYPE_GROUP = "group"

    # Default dimensions
    DEFAULT_NODE_WIDTH = 250
    DEFAULT_NODE_HEIGHT = 150
    DEFAULT_GROUP_WIDTH = 400
    DEFAULT_GROUP_HEIGHT = 300

    # Colors for different entity types
    ENTITY_COLORS = {
        'domain': '#4CAF50',      # Green
        'ip': '#2196F3',          # Blue
        'person': '#FF9800',      # Orange
        'organization': '#9C27B0', # Purple
        'email': '#F44336',       # Red
        'url': '#00BCD4',         # Cyan
        'phone': '#FFEB3B',       # Yellow
        'location': '#795548',    # Brown
        'username': '#E91E63',    # Pink
        'finding': '#607D8B',     # Blue Grey
        'risk': '#D32F2F',        # Dark Red
        'event': '#1976D2',       # Dark Blue
        'tool': '#388E3C',        # Dark Green
        'default': '#757575'      # Grey
    }

    # Finding confidence colors
    CONFIDENCE_COLORS = {
        'very_high': '#1B5E20',   # Dark Green
        'high': '#43A047',        # Green
        'medium': '#FFA726',      # Orange
        'low': '#EF5350',         # Light Red
        'very_low': '#C62828',    # Dark Red
        'unknown': '#9E9E9E'      # Grey
    }

    def __init__(self, output_dir: str = "data/reports/obsidian"):
        """
        Initialize canvas generator

        Args:
            output_dir: Directory for canvas files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Canvas state
        self.nodes = []
        self.edges = []
        self.next_x = 0
        self.next_y = 0

    def generate_id(self, text: str) -> str:
        """Generate unique ID for canvas element"""
        return hashlib.md5(f"{text}{datetime.now().isoformat()}".encode()).hexdigest()[:16]

    def create_text_node(
        self,
        text: str,
        x: int,
        y: int,
        width: int = DEFAULT_NODE_WIDTH,
        height: int = DEFAULT_NODE_HEIGHT,
        color: Optional[str] = None
    ) -> Dict:
        """
        Create a text node

        Args:
            text: Node text content
            x, y: Position
            width, height: Dimensions
            color: Background color

        Returns:
            Node dictionary
        """
        node = {
            "id": self.generate_id(text),
            "type": self.NODE_TYPE_TEXT,
            "text": text,
            "x": x,
            "y": y,
            "width": width,
            "height": height
        }

        if color:
            node["color"] = color

        return node

    def create_group_node(
        self,
        label: str,
        x: int,
        y: int,
        width: int = DEFAULT_GROUP_WIDTH,
        height: int = DEFAULT_GROUP_HEIGHT,
        color: Optional[str] = None
    ) -> Dict:
        """Create a group node to contain other nodes"""
        node = {
            "id": self.generate_id(label),
            "type": self.NODE_TYPE_GROUP,
            "label": label,
            "x": x,
            "y": y,
            "width": width,
            "height": height
        }

        if color:
            node["color"] = color

        return node

    def create_edge(
        self,
        from_node_id: str,
        to_node_id: str,
        label: Optional[str] = None,
        color: Optional[str] = None
    ) -> Dict:
        """
        Create an edge between nodes

        Args:
            from_node_id: Source node ID
            to_node_id: Target node ID
            label: Optional edge label
            color: Optional edge color

        Returns:
            Edge dictionary
        """
        edge = {
            "id": self.generate_id(f"{from_node_id}-{to_node_id}"),
            "fromNode": from_node_id,
            "toNode": to_node_id
        }

        if label:
            edge["label"] = label

        if color:
            edge["color"] = color

        return edge

    def calculate_layout_grid(self, num_items: int, cols: int = 4) -> List[Tuple[int, int]]:
        """
        Calculate grid layout positions

        Args:
            num_items: Number of items to layout
            cols: Number of columns

        Returns:
            List of (x, y) positions
        """
        positions = []
        spacing_x = self.DEFAULT_NODE_WIDTH + 50
        spacing_y = self.DEFAULT_NODE_HEIGHT + 50

        for i in range(num_items):
            row = i // cols
            col = i % cols
            x = col * spacing_x
            y = row * spacing_y
            positions.append((x, y))

        return positions

    def calculate_radial_layout(
        self,
        num_items: int,
        center_x: int = 400,
        center_y: int = 300,
        radius: int = 300
    ) -> List[Tuple[int, int]]:
        """
        Calculate radial (circular) layout positions

        Args:
            num_items: Number of items to layout
            center_x, center_y: Center point
            radius: Radius of circle

        Returns:
            List of (x, y) positions
        """
        import math

        positions = []
        angle_step = (2 * math.pi) / max(num_items, 1)

        for i in range(num_items):
            angle = i * angle_step
            x = int(center_x + radius * math.cos(angle))
            y = int(center_y + radius * math.sin(angle))
            positions.append((x, y))

        return positions

    def generate_entity_map(
        self,
        investigation_data: Dict,
        layout: str = 'radial'
    ) -> str:
        """
        Generate entity relationship map

        Args:
            investigation_data: Investigation data
            layout: Layout type ('grid' or 'radial')

        Returns:
            Canvas JSON string
        """
        self.nodes = []
        self.edges = []

        # Extract entities and relationships
        processed_data = investigation_data.get('processed_data', {})
        entities = processed_data.get('entities', [])
        relationships = processed_data.get('relationships', [])

        if not entities:
            # Create a single node indicating no entities
            node = self.create_text_node(
                "No entities found in investigation",
                100, 100,
                color="#BDBDBD"
            )
            self.nodes.append(node)
        else:
            # Create central investigation node
            investigation_id = investigation_data.get('investigation_id', 'Investigation')
            objective = investigation_data.get('objective', '')[:100]

            central_node = self.create_text_node(
                f"**Investigation**\n\n{investigation_id}\n\n{objective}",
                0, 0,
                width=300,
                height=200,
                color="#1976D2"
            )
            self.nodes.append(central_node)

            # Layout entity nodes
            if layout == 'radial':
                positions = self.calculate_radial_layout(len(entities), center_x=0, center_y=0, radius=500)
            else:
                positions = self.calculate_layout_grid(len(entities))

            # Create entity nodes
            entity_id_map = {}

            for i, entity in enumerate(entities):
                if not isinstance(entity, dict):
                    continue

                entity_type = entity.get('type', 'unknown')
                entity_name = entity.get('name', 'Unknown')
                attributes = entity.get('attributes', {})

                # Build entity text
                entity_text = f"**{entity_type.upper()}**\n\n{entity_name}"
                if attributes:
                    entity_text += f"\n\n"
                    for key, value in list(attributes.items())[:3]:
                        entity_text += f"• {key}: {value}\n"

                # Get position
                x, y = positions[i]

                # Create node
                color = self.ENTITY_COLORS.get(entity_type, self.ENTITY_COLORS['default'])
                node = self.create_text_node(
                    entity_text,
                    x, y,
                    width=220,
                    height=180,
                    color=color
                )
                self.nodes.append(node)

                entity_id_map[entity_name] = node['id']

                # Connect to central node
                edge = self.create_edge(
                    central_node['id'],
                    node['id'],
                    label=entity_type
                )
                self.edges.append(edge)

            # Add relationship edges
            for relationship in relationships:
                if not isinstance(relationship, dict):
                    continue

                source = relationship.get('source', '')
                target = relationship.get('target', '')
                rel_type = relationship.get('type', 'related_to')

                if source in entity_id_map and target in entity_id_map:
                    edge = self.create_edge(
                        entity_id_map[source],
                        entity_id_map[target],
                        label=rel_type,
                        color="#FF6F00"
                    )
                    self.edges.append(edge)

        # Generate canvas JSON
        canvas = {
            "nodes": self.nodes,
            "edges": self.edges
        }

        return json.dumps(canvas, indent=2)

    def generate_timeline_canvas(self, investigation_data: Dict) -> str:
        """
        Generate investigation timeline visualization

        Args:
            investigation_data: Investigation data

        Returns:
            Canvas JSON string
        """
        self.nodes = []
        self.edges = []

        # Extract timeline events
        analysis = investigation_data.get('analysis', {})
        timeline = analysis.get('timeline', [])

        if not timeline:
            # No timeline data
            node = self.create_text_node(
                "No timeline data available",
                100, 100,
                color="#BDBDBD"
            )
            self.nodes.append(node)
        else:
            # Create timeline title
            title_node = self.create_text_node(
                f"**Investigation Timeline**\n\n{investigation_data.get('investigation_id', 'N/A')}",
                0, -200,
                width=400,
                height=100,
                color="#1976D2"
            )
            self.nodes.append(title_node)

            # Create timeline events (vertical layout)
            spacing_y = 200
            prev_node = None

            for i, event in enumerate(timeline):
                if isinstance(event, dict):
                    date = event.get('date', 'Unknown date')
                    description = event.get('description', 'No description')
                    event_type = event.get('type', 'event')
                else:
                    date = "Unknown"
                    description = str(event)
                    event_type = "event"

                # Create event node
                event_text = f"**{date}**\n\n{description}"
                y_pos = i * spacing_y

                node = self.create_text_node(
                    event_text,
                    0, y_pos,
                    width=350,
                    height=150,
                    color=self.ENTITY_COLORS.get(event_type, "#607D8B")
                )
                self.nodes.append(node)

                # Connect to previous event
                if prev_node:
                    edge = self.create_edge(
                        prev_node['id'],
                        node['id'],
                        color="#424242"
                    )
                    self.edges.append(edge)
                else:
                    # Connect first event to title
                    edge = self.create_edge(
                        title_node['id'],
                        node['id']
                    )
                    self.edges.append(edge)

                prev_node = node

        canvas = {
            "nodes": self.nodes,
            "edges": self.edges
        }

        return json.dumps(canvas, indent=2)

    def generate_findings_canvas(self, investigation_data: Dict) -> str:
        """
        Generate findings hierarchy visualization

        Args:
            investigation_data: Investigation data

        Returns:
            Canvas JSON string
        """
        self.nodes = []
        self.edges = []

        analysis = investigation_data.get('analysis', {})
        key_findings = analysis.get('key_findings', [])

        # Create investigation node
        inv_node = self.create_text_node(
            f"**Investigation Findings**\n\n{investigation_data.get('objective', '')}",
            0, -300,
            width=400,
            height=150,
            color="#1976D2"
        )
        self.nodes.append(inv_node)

        if not key_findings:
            no_findings_node = self.create_text_node(
                "No findings available",
                0, 0,
                color="#BDBDBD"
            )
            self.nodes.append(no_findings_node)

            edge = self.create_edge(inv_node['id'], no_findings_node['id'])
            self.edges.append(edge)
        else:
            # Group findings by confidence
            findings_by_confidence = {}
            for finding in key_findings:
                if isinstance(finding, dict):
                    confidence = finding.get('confidence', 'unknown')
                    if confidence not in findings_by_confidence:
                        findings_by_confidence[confidence] = []
                    findings_by_confidence[confidence].append(finding)

            # Create confidence groups
            group_spacing = 500
            group_x = -len(findings_by_confidence) * group_spacing // 2

            for confidence_level, findings in findings_by_confidence.items():
                # Create group node
                group_node = self.create_group_node(
                    f"{confidence_level.upper()} Confidence",
                    group_x, 0,
                    width=450,
                    height=200 + len(findings) * 100,
                    color=self.CONFIDENCE_COLORS.get(confidence_level, "#9E9E9E")
                )
                self.nodes.append(group_node)

                # Connect group to investigation
                edge = self.create_edge(
                    inv_node['id'],
                    group_node['id'],
                    label=f"{len(findings)} findings"
                )
                self.edges.append(edge)

                # Create finding nodes within group
                for i, finding in enumerate(findings):
                    description = finding.get('description', str(finding))[:200]
                    significance = finding.get('significance', 'unknown')

                    finding_text = f"**Finding**\n\n{description}\n\nSignificance: {significance}"

                    finding_node = self.create_text_node(
                        finding_text,
                        group_x + 20,
                        20 + i * 180,
                        width=400,
                        height=150,
                        color=self.CONFIDENCE_COLORS.get(confidence_level, "#9E9E9E")
                    )
                    self.nodes.append(finding_node)

                group_x += group_spacing

        canvas = {
            "nodes": self.nodes,
            "edges": self.edges
        }

        return json.dumps(canvas, indent=2)

    def generate_investigation_overview(self, investigation_data: Dict) -> str:
        """
        Generate complete investigation overview canvas

        Args:
            investigation_data: Investigation data

        Returns:
            Canvas JSON string
        """
        self.nodes = []
        self.edges = []

        # Central investigation node
        inv_id = investigation_data.get('investigation_id', 'Unknown')
        objective = investigation_data.get('objective', 'No objective')[:150]

        central_node = self.create_text_node(
            f"**OSINT Investigation**\n\n{inv_id}\n\n{objective}",
            0, 0,
            width=400,
            height=250,
            color="#0D47A1"
        )
        self.nodes.append(central_node)

        # Create category nodes in radial layout
        categories = []

        # Findings
        analysis = investigation_data.get('analysis', {})
        findings_count = len(analysis.get('key_findings', []))
        categories.append(('Findings', findings_count, '#4CAF50', -600, -300))

        # Entities
        processed_data = investigation_data.get('processed_data', {})
        entities_count = len(processed_data.get('entities', []))
        categories.append(('Entities', entities_count, '#2196F3', 600, -300))

        # Timeline
        timeline_count = len(analysis.get('timeline', []))
        categories.append(('Timeline Events', timeline_count, '#FF9800', -600, 300))

        # Risks
        risks_count = len(analysis.get('risk_indicators', []))
        categories.append(('Risk Indicators', risks_count, '#F44336', 600, 300))

        # Recommendations
        rec_count = len(analysis.get('recommendations', []))
        categories.append(('Recommendations', rec_count, '#9C27B0', 0, 500))

        # Collection results
        collection_count = len(investigation_data.get('collection_results', []))
        categories.append(('Data Sources', collection_count, '#00BCD4', 0, -500))

        # Create category nodes
        for label, count, color, x, y in categories:
            node = self.create_text_node(
                f"**{label}**\n\n{count} items",
                x, y,
                width=250,
                height=120,
                color=color
            )
            self.nodes.append(node)

            edge = self.create_edge(
                central_node['id'],
                node['id'],
                label=str(count)
            )
            self.edges.append(edge)

        # Add metadata
        metadata = investigation_data.get('metadata', {})
        meta_text = f"**Investigation Metadata**\n\n"
        meta_text += f"Duration: {metadata.get('duration_seconds', 0):.1f}s\n"
        meta_text += f"Iterations: {metadata.get('iterations', 0)}\n"
        meta_text += f"Tools Used: {metadata.get('tools_used', 0)}"

        meta_node = self.create_text_node(
            meta_text,
            -900, 0,
            width=250,
            height=150,
            color="#607D8B"
        )
        self.nodes.append(meta_node)

        edge = self.create_edge(central_node['id'], meta_node['id'])
        self.edges.append(edge)

        canvas = {
            "nodes": self.nodes,
            "edges": self.edges
        }

        return json.dumps(canvas, indent=2)

    def save_canvas(self, canvas_json: str, filename: str) -> Path:
        """
        Save canvas to .canvas file

        Args:
            canvas_json: Canvas JSON string
            filename: Filename (without extension)

        Returns:
            Path to saved file
        """
        filepath = self.output_dir / f"{filename}.canvas"

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(canvas_json)

        print(f"Canvas saved: {filepath}")
        return filepath

    def generate_all_canvases(self, investigation_data: Dict) -> Dict[str, Path]:
        """
        Generate all canvas types for an investigation

        Args:
            investigation_data: Investigation data

        Returns:
            Dictionary mapping canvas type to file path
        """
        inv_id = investigation_data.get('investigation_id', 'investigation')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        canvases = {}

        # Overview
        overview_json = self.generate_investigation_overview(investigation_data)
        canvases['overview'] = self.save_canvas(
            overview_json,
            f"{inv_id}_{timestamp}_overview"
        )

        # Entity map
        entity_json = self.generate_entity_map(investigation_data, layout='radial')
        canvases['entity_map'] = self.save_canvas(
            entity_json,
            f"{inv_id}_{timestamp}_entity_map"
        )

        # Timeline
        timeline_json = self.generate_timeline_canvas(investigation_data)
        canvases['timeline'] = self.save_canvas(
            timeline_json,
            f"{inv_id}_{timestamp}_timeline"
        )

        # Findings
        findings_json = self.generate_findings_canvas(investigation_data)
        canvases['findings'] = self.save_canvas(
            findings_json,
            f"{inv_id}_{timestamp}_findings"
        )

        return canvases


def create_obsidian_vault_structure(base_path: str = "data/obsidian_vault"):
    """
    Create Obsidian vault structure for OSINT investigations

    Args:
        base_path: Base path for vault
    """
    vault_path = Path(base_path)
    vault_path.mkdir(parents=True, exist_ok=True)

    # Create subdirectories
    (vault_path / "Investigations").mkdir(exist_ok=True)
    (vault_path / "Entities").mkdir(exist_ok=True)
    (vault_path / "Reports").mkdir(exist_ok=True)
    (vault_path / "Canvases").mkdir(exist_ok=True)

    # Create .obsidian folder (required for vault)
    obsidian_folder = vault_path / ".obsidian"
    obsidian_folder.mkdir(exist_ok=True)

    # Create basic workspace config
    workspace_config = {
        "main": {
            "id": "osint-vault",
            "type": "split",
            "children": []
        }
    }

    with open(obsidian_folder / "workspace.json", 'w') as f:
        json.dump(workspace_config, f, indent=2)

    print(f"Obsidian vault created at: {vault_path}")
    print(f"Open this folder in Obsidian to view your OSINT canvases!")

    return vault_path
