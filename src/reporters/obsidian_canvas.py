"""
Obsidian Canvas Generator for OSINT Investigations
Updated to match TRM Labs Assignment template format

Creates visual mind maps using hub-and-spoke pattern with:
- Central subject node
- Radial category groups
- Directional labeled edges
- Consistent color scheme
"""

import json
import hashlib
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path


class ObsidianCanvasGenerator:
    """
    Generate Obsidian Canvas files matching TRM Labs investigation format
    """

    # Node types
    NODE_TYPE_TEXT = "text"
    NODE_TYPE_GROUP = "group"

    # Standard dimensions (matching template)
    SUBJECT_WIDTH = 250
    SUBJECT_HEIGHT = 60
    GROUP_WIDTH = 300
    GROUP_MIN_HEIGHT = 300
    ITEM_WIDTH = 250
    ITEM_HEIGHT = 60
    ITEM_SPACING = 12

    # Color scheme (matching template)
    COLORS = {
        'subject': "1",
        'emails': "2",
        'social_media': "3",
        'phone_numbers': "4",
        'bio_data': "5",
        'usernames': "6",
        'contacts': "#f60465",
        'leads': "#9a4c88",
        'breach_data': "#6e1111",
        'relatives': "#d905f5",
        'profession': "#887e11",
        'vehicles': "2",
        'accomplices': "#b57878",
        'digital_footprint': "#558212",
        'locations': "#090fc3",
        'images': "#77500e",
        'timeline': "#1976D2",
        'findings': "#607D8B",
        'entities': "#4CAF50",
        'risks': "#F44336",
        'tools': "#388E3C"
    }

    # Phone number emoji icons (matching template)
    PHONE_ICONS = {
        'mobile': '📱',
        'landline': '☎️',
        'office': '📞',
        'satellite': '🛰️',
        'business': '💼',
        'messaging': '💬',
        'burner': '🔥',
        'encrypted': '📱🔒'
    }

    def __init__(self, output_dir: str = "data/reports/obsidian"):
        """Initialize canvas generator"""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.nodes = []
        self.edges = []
        self.node_id_counter = 0

    def generate_id(self, prefix: str = "") -> str:
        """Generate unique ID for canvas element"""
        self.node_id_counter += 1
        base = f"{prefix}{datetime.now().timestamp()}{self.node_id_counter}"
        return hashlib.md5(base.encode()).hexdigest()[:16]

    def create_text_node(
        self,
        text: str,
        x: int,
        y: int,
        width: int = ITEM_WIDTH,
        height: int = ITEM_HEIGHT,
        color: Optional[str] = None
    ) -> Dict:
        """Create a text node"""
        node = {
            "id": self.generate_id("text"),
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
        width: int = GROUP_WIDTH,
        height: int = GROUP_MIN_HEIGHT,
        color: Optional[str] = None
    ) -> Dict:
        """Create a group node"""
        node = {
            "id": self.generate_id("group"),
            "type": self.NODE_TYPE_GROUP,
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "label": label
        }

        if color:
            node["color"] = color

        return node

    def create_edge(
        self,
        from_node_id: str,
        to_node_id: str,
        from_side: str = "right",
        to_side: str = "left",
        label: Optional[str] = None,
        color: Optional[str] = None
    ) -> Dict:
        """
        Create a directional edge between nodes

        Args:
            from_node_id: Source node ID
            to_node_id: Target node ID
            from_side: Side to connect from (left, right, top, bottom)
            to_side: Side to connect to (left, right, top, bottom)
            label: Optional edge label
            color: Optional edge color
        """
        edge = {
            "id": self.generate_id("edge"),
            "fromNode": from_node_id,
            "fromSide": from_side,
            "toNode": to_node_id,
            "toSide": to_side
        }

        if label:
            edge["label"] = label

        if color:
            edge["color"] = color

        return edge

    def calculate_group_positions_radial(
        self,
        num_groups: int,
        center_x: int = 0,
        center_y: int = 0,
        radius: int = 600
    ) -> List[Tuple[int, int, str, str]]:
        """
        Calculate radial positions for groups around center

        Returns:
            List of (x, y, from_side, to_side) tuples
        """
        import math

        positions = []
        angle_step = (2 * math.pi) / num_groups

        for i in range(num_groups):
            angle = i * angle_step - (math.pi / 2)  # Start from top
            x = int(center_x + radius * math.cos(angle))
            y = int(center_y + radius * math.sin(angle))

            # Determine edge sides based on position relative to center
            if x < center_x - 100:
                from_side = "left"
                to_side = "right"
            elif x > center_x + 100:
                from_side = "right"
                to_side = "left"
            elif y < center_y:
                from_side = "top"
                to_side = "bottom"
            else:
                from_side = "bottom"
                to_side = "top"

            positions.append((x, y, from_side, to_side))

        return positions

    def generate_person_investigation_canvas(
        self,
        investigation_data: Dict,
        subject_name: str = "Subject"
    ) -> str:
        """
        Generate person-of-interest investigation canvas
        Matches TRM Labs template format

        Args:
            investigation_data: Investigation data
            subject_name: Name of subject being investigated

        Returns:
            Canvas JSON string
        """
        self.nodes = []
        self.edges = []

        # Extract data
        processed_data = investigation_data.get('processed_data', {})
        analysis = investigation_data.get('analysis', {})
        entities = processed_data.get('entities', [])

        # Create central subject node
        subject_x, subject_y = -85, 126
        subject_node = self.create_text_node(
            subject_name or "Seed Data",
            subject_x,
            subject_y,
            width=self.SUBJECT_WIDTH,
            height=self.SUBJECT_HEIGHT,
            color=self.COLORS['subject']
        )
        self.nodes.append(subject_node)

        # Create subject group
        subject_group = self.create_group_node(
            "Subject",
            subject_x - 15,
            subject_y - 21,
            width=self.SUBJECT_WIDTH + 30,
            height=self.SUBJECT_HEIGHT + 47,
            color=self.COLORS['subject']
        )
        self.nodes.append(subject_group)

        # Organize entities by type
        entities_by_type = {}
        for entity in entities:
            if isinstance(entity, dict):
                entity_type = entity.get('type', 'unknown')
                if entity_type not in entities_by_type:
                    entities_by_type[entity_type] = []
                entities_by_type[entity_type].append(entity)

        # Define category configurations with positions (matching template layout)
        categories = [
            # Left side
            ('social_media', 'Social Media', -640, -1240, 'left', 'right'),
            ('usernames', 'Usernames', -1060, -600, 'left', 'right'),
            ('phone_numbers', 'Phone Numbers', -1160, -213, 'left', 'right'),
            ('emails', 'Emails', -660, 540, 'left', 'right'),
            ('leads', 'Leads to Pursue', -1089, 600, 'left', 'top'),

            # Top
            ('bio_data', 'Bio Data', -220, -1180, 'top', 'bottom'),
            ('breach_data', 'Breach Data', 249, -929, 'top', 'left'),
            ('profession', 'Profession', 640, -1037, 'top', 'bottom'),

            # Right side
            ('vehicles', 'Vehicles', 778, -540, 'top', 'left'),
            ('images', 'Images', 405, -144, 'right', 'left'),
            ('accomplices', 'Accomplices', 477, 387, 'right', 'left'),
            ('digital_footprint', 'Digital Footprint', 1140, 281, 'right', 'left'),
            ('locations', 'Locations', 820, -27, 'right', 'left'),
            ('contacts', 'Contacts', 260, 800, 'bottom', 'top'),

            # Bottom
            ('relatives', 'Relatives', -220, 711, 'bottom', 'top'),
        ]

        # Create category groups
        for cat_key, cat_label, x, y, from_side, to_side in categories:
            # Get items for this category
            items = self._get_category_items(cat_key, entities_by_type, analysis, investigation_data)

            if items:
                # Calculate group height based on items
                group_height = max(
                    self.GROUP_MIN_HEIGHT,
                    20 + (len(items) * (self.ITEM_HEIGHT + self.ITEM_SPACING)) + 20
                )

                # Create group
                group_node = self.create_group_node(
                    cat_label,
                    x,
                    y,
                    width=self.GROUP_WIDTH,
                    height=group_height,
                    color=self.COLORS.get(cat_key, "2")
                )
                self.nodes.append(group_node)

                # Create items within group
                item_x = x + 15
                item_y = y + 20

                for i, item in enumerate(items[:10]):  # Limit to 10 items per category
                    item_node = self.create_text_node(
                        item,
                        item_x,
                        item_y,
                        width=self.ITEM_WIDTH,
                        height=self.ITEM_HEIGHT if '\n' not in item else self.ITEM_HEIGHT + 20,
                        color=self.COLORS.get(cat_key, "2")
                    )
                    self.nodes.append(item_node)

                    item_y += self.ITEM_HEIGHT + self.ITEM_SPACING

                # Create edge from subject to group
                edge = self.create_edge(
                    subject_group['id'],
                    group_node['id'],
                    from_side=from_side,
                    to_side=to_side,
                    label=cat_label,
                    color=self.COLORS.get(cat_key, "2")
                )
                self.edges.append(edge)

        canvas = {
            "nodes": self.nodes,
            "edges": self.edges
        }

        return json.dumps(canvas, indent=2)

    def _get_category_items(
        self,
        category: str,
        entities_by_type: Dict,
        analysis: Dict,
        investigation_data: Dict
    ) -> List[str]:
        """Get items for a specific category"""
        items = []

        if category == 'social_media':
            platforms = ['Twitter', 'Instagram', 'LinkedIn', 'Google', 'Facebook',
                        'YouTube', 'TikTok', 'Snapchat', 'Telegram', 'Reddit',
                        'Discord', 'Paste Sites']
            # Check if we have usernames for these platforms
            usernames = entities_by_type.get('username', [])
            for platform in platforms:
                for username in usernames:
                    if isinstance(username, dict):
                        name = username.get('name', '')
                        if platform.lower() in name.lower():
                            items.append(platform)
                            break
                if not items or platform not in items:
                    items.append(platform)

        elif category == 'emails':
            emails = entities_by_type.get('email', [])
            for email in emails[:8]:
                if isinstance(email, dict):
                    items.append(email.get('name', 'email@domain.com'))
                else:
                    items.append(str(email))

        elif category == 'phone_numbers':
            phones = entities_by_type.get('phone', [])
            icons = list(self.PHONE_ICONS.values())
            for i, phone in enumerate(phones[:8]):
                icon = icons[i % len(icons)]
                if isinstance(phone, dict):
                    number = phone.get('name', '(303) 456-7890')
                else:
                    number = str(phone)
                items.append(f"{icon} {number}")

        elif category == 'usernames':
            items = ['Usernames', 'Handles', 'Forum Aliases', 'Account Identifiers']

        elif category == 'bio_data':
            items = ['Full Name', 'Alias', 'DPOB', 'Passport', 'National ID',
                    'Marital Status', 'Languages', 'Biometric (fingerprint, DNA)',
                    'Military Service']

        elif category == 'profession':
            items = ['Businesses', 'Employment', 'Education', 'Skills']

        elif category == 'breach_data':
            items = ['Passwords', 'Usernames', 'IPs', 'Forums', 'Breach Event']

        elif category == 'vehicles':
            items = ['Personal', 'Stolen', 'Borrowed', 'Multiple Drivers']

        elif category == 'accomplices':
            items = ['Accomplice1', 'Accomplice2', 'Accomplice3', 'Accomplice4']

        elif category == 'contacts':
            items = ['Name/Identifier1', 'Name/Identifier2', 'Name/Identifier3',
                    'Name/Identifier4', 'Name/Identifier5', 'Name/Identifier6',
                    'Name/Identifier7', 'Name/Identifier8']

        elif category == 'leads':
            items = ['Lead1', 'Lead2', 'Lead3', 'Lead4', 'Lead5', 'Lead6']

        elif category == 'relatives':
            items = ['Spouse/Significant Other', 'Children', 'Parents', 'Siblings',
                    'Key Extended Family']

        elif category == 'locations':
            locations = entities_by_type.get('location', [])
            items = ['City, Country', 'Neighborhood', 'Address', 'Obscure Reference']
            for loc in locations[:4]:
                if isinstance(loc, dict):
                    name = loc.get('name', '')
                    if name and name not in items:
                        items.append(name)

        elif category == 'images':
            items = ['Passport', 'Social Media', 'Surface or Dark Web']

        elif category == 'digital_footprint':
            items = ['IPs', 'Geo Metadata', 'Device/Network Identifiers',
                    'Online Behavior Patterns']

        return items

    def generate_investigation_overview(self, investigation_data: Dict) -> str:
        """
        Generate investigation overview in hub-and-spoke format

        Args:
            investigation_data: Investigation data

        Returns:
            Canvas JSON string
        """
        # Use the person investigation format as default overview
        subject_name = investigation_data.get('objective', 'Investigation')[:50]
        return self.generate_person_investigation_canvas(investigation_data, subject_name)

    def generate_entity_map(self, investigation_data: Dict, layout: str = 'radial') -> str:
        """Generate entity relationship map (keeping existing implementation for compatibility)"""
        # For now, use the new person investigation format
        return self.generate_person_investigation_canvas(investigation_data, "Entity Network")

    def generate_timeline_canvas(self, investigation_data: Dict) -> str:
        """Generate timeline (keep existing vertical implementation)"""
        self.nodes = []
        self.edges = []

        analysis = investigation_data.get('analysis', {})
        timeline = analysis.get('timeline', [])

        # Create title
        title_node = self.create_text_node(
            f"**Investigation Timeline**",
            -175, -200,
            width=350, height=80,
            color=self.COLORS['timeline']
        )
        self.nodes.append(title_node)

        if timeline:
            prev_node = None
            for i, event in enumerate(timeline[:15]):
                if isinstance(event, dict):
                    date = event.get('date', 'Unknown date')
                    description = event.get('description', '')
                else:
                    date = "Event"
                    description = str(event)

                event_text = f"**{date}**\n\n{description[:100]}"
                y_pos = i * 180

                node = self.create_text_node(
                    event_text,
                    -175, y_pos,
                    width=350, height=150,
                    color=self.COLORS['timeline']
                )
                self.nodes.append(node)

                if prev_node:
                    edge = self.create_edge(
                        prev_node['id'],
                        node['id'],
                        from_side="bottom",
                        to_side="top",
                        color=self.COLORS['timeline']
                    )
                    self.edges.append(edge)
                else:
                    edge = self.create_edge(
                        title_node['id'],
                        node['id'],
                        from_side="bottom",
                        to_side="top"
                    )
                    self.edges.append(edge)

                prev_node = node

        canvas = {"nodes": self.nodes, "edges": self.edges}
        return json.dumps(canvas, indent=2)

    def generate_findings_canvas(self, investigation_data: Dict) -> str:
        """Generate findings hierarchy (keep existing grouped implementation)"""
        self.nodes = []
        self.edges = []

        analysis = investigation_data.get('analysis', {})
        key_findings = analysis.get('key_findings', [])

        # Create investigation node
        inv_node = self.create_text_node(
            f"**Investigation Findings**",
            -175, -300,
            width=350, height=100,
            color=self.COLORS['findings']
        )
        self.nodes.append(inv_node)

        if key_findings:
            # Group by confidence
            findings_by_confidence = {}
            for finding in key_findings:
                if isinstance(finding, dict):
                    confidence = finding.get('confidence', 'unknown')
                    if confidence not in findings_by_confidence:
                        findings_by_confidence[confidence] = []
                    findings_by_confidence[confidence].append(finding)

            # Create groups
            group_x = -len(findings_by_confidence) * 250
            for conf_level, findings in findings_by_confidence.items():
                group_height = 100 + len(findings) * 130

                group_node = self.create_group_node(
                    f"{conf_level.upper()} Confidence",
                    group_x, 0,
                    width=450, height=group_height,
                    color=self.COLORS.get(conf_level, "#9E9E9E")
                )
                self.nodes.append(group_node)

                edge = self.create_edge(
                    inv_node['id'],
                    group_node['id'],
                    from_side="bottom",
                    to_side="top",
                    label=f"{len(findings)} findings"
                )
                self.edges.append(edge)

                # Add findings
                for i, finding in enumerate(findings[:8]):
                    desc = finding.get('description', str(finding))[:150]
                    finding_node = self.create_text_node(
                        f"**Finding**\n\n{desc}",
                        group_x + 20,
                        20 + i * 130,
                        width=400, height=110
                    )
                    self.nodes.append(finding_node)

                group_x += 500

        canvas = {"nodes": self.nodes, "edges": self.edges}
        return json.dumps(canvas, indent=2)

    def save_canvas(self, canvas_json: str, filename: str) -> Path:
        """Save canvas to .canvas file"""
        filepath = self.output_dir / f"{filename}.canvas"

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(canvas_json)

        print(f"Canvas saved: {filepath}")
        return filepath

    def generate_all_canvases(self, investigation_data: Dict) -> Dict[str, Path]:
        """Generate all canvas types"""
        inv_id = investigation_data.get('investigation_id', 'investigation')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        canvases = {}

        # Person investigation format (new)
        person_json = self.generate_person_investigation_canvas(investigation_data)
        canvases['person_investigation'] = self.save_canvas(
            person_json,
            f"{inv_id}_{timestamp}_person_investigation"
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
    """Create Obsidian vault structure"""
    vault_path = Path(base_path)
    vault_path.mkdir(parents=True, exist_ok=True)

    # Create subdirectories
    (vault_path / "Investigations").mkdir(exist_ok=True)
    (vault_path / "Entities").mkdir(exist_ok=True)
    (vault_path / "Reports").mkdir(exist_ok=True)
    (vault_path / "Canvases").mkdir(exist_ok=True)

    # Create .obsidian folder
    obsidian_folder = vault_path / ".obsidian"
    obsidian_folder.mkdir(exist_ok=True)

    # Create workspace config
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
    return vault_path
