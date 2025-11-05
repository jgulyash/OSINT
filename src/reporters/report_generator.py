"""
Multi-Format Intelligence Report Generator

Supports:
- Markdown
- HTML
- JSON
- PDF (requires additional dependencies)
- CSV (for data exports)
- Obsidian Canvas (mind maps and knowledge graphs)
"""

import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

# Import Obsidian Canvas generator
try:
    from src.reporters.obsidian_canvas import ObsidianCanvasGenerator
    OBSIDIAN_AVAILABLE = True
except ImportError:
    OBSIDIAN_AVAILABLE = False


class ReportGenerator:
    """
    Generate intelligence reports in multiple formats
    """

    def __init__(self, output_dir: str = "data/reports"):
        """
        Initialize report generator

        Args:
            output_dir: Directory for saving reports
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_report(
        self,
        investigation_data: Dict,
        format: str = 'markdown',
        classification: str = 'UNCLASSIFIED',
        save: bool = True
    ) -> str:
        """
        Generate intelligence report

        Args:
            investigation_data: Complete investigation data
            format: Output format (markdown, html, json, pdf, csv)
            classification: Classification level
            save: Save report to file

        Returns:
            Report content as string
        """
        format = format.lower()

        if format == 'markdown':
            report = self._generate_markdown(investigation_data, classification)
        elif format == 'html':
            report = self._generate_html(investigation_data, classification)
        elif format == 'json':
            report = self._generate_json(investigation_data)
        elif format == 'csv':
            report = self._generate_csv(investigation_data)
        else:
            report = self._generate_markdown(investigation_data, classification)

        if save:
            self._save_report(report, investigation_data.get('investigation_id'), format)

        return report

    def _generate_markdown(self, data: Dict, classification: str) -> str:
        """Generate Markdown report"""
        investigation_id = data.get('investigation_id', 'UNKNOWN')
        objective = data.get('objective', 'Not specified')
        analysis = data.get('analysis', {})
        metadata = data.get('metadata', {})

        report = f"""# INTELLIGENCE REPORT
**Classification:** {classification}
**Investigation ID:** {investigation_id}
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

---

## EXECUTIVE SUMMARY

**Objective:** {objective}

**Investigation Status:** Completed
**Duration:** {metadata.get('duration_seconds', 'N/A')} seconds
**Iterations:** {metadata.get('iterations', 'N/A')}
**Tools Used:** {metadata.get('tools_used', 'N/A')}

"""

        # Key Findings
        key_findings = analysis.get('key_findings', [])
        if key_findings:
            report += "## KEY FINDINGS\n\n"
            for i, finding in enumerate(key_findings, 1):
                if isinstance(finding, dict):
                    description = finding.get('description', str(finding))
                    confidence = finding.get('confidence', 'unknown')
                    significance = finding.get('significance', 'unknown')
                    report += f"{i}. **{description}**\n"
                    report += f"   - Confidence: {confidence}\n"
                    report += f"   - Significance: {significance}\n\n"
                else:
                    report += f"{i}. {finding}\n\n"

        # Insights
        insights = analysis.get('insights', [])
        if insights:
            report += "## ANALYSIS & INSIGHTS\n\n"
            for insight in insights:
                if isinstance(insight, dict):
                    report += f"- **{insight.get('title', 'Insight')}:** {insight.get('description', '')}\n"
                else:
                    report += f"- {insight}\n"
            report += "\n"

        # Network Analysis
        network = analysis.get('network_analysis', {})
        if network:
            report += "## NETWORK ANALYSIS\n\n"
            report += f"{network}\n\n"

        # Timeline
        timeline = analysis.get('timeline', [])
        if timeline:
            report += "## TIMELINE\n\n"
            for event in timeline:
                if isinstance(event, dict):
                    date = event.get('date', 'Unknown')
                    description = event.get('description', 'No description')
                    report += f"- **{date}:** {description}\n"
                else:
                    report += f"- {event}\n"
            report += "\n"

        # Entities
        processed_data = data.get('processed_data', {})
        entities = processed_data.get('entities', [])
        if entities:
            report += "## IDENTIFIED ENTITIES\n\n"

            # Group by type
            entities_by_type = {}
            for entity in entities:
                if isinstance(entity, dict):
                    entity_type = entity.get('type', 'unknown')
                    if entity_type not in entities_by_type:
                        entities_by_type[entity_type] = []
                    entities_by_type[entity_type].append(entity)

            for entity_type, entity_list in entities_by_type.items():
                report += f"### {entity_type.title()}\n\n"
                for entity in entity_list:
                    name = entity.get('name', 'Unknown')
                    attributes = entity.get('attributes', {})
                    report += f"- **{name}**"
                    if attributes:
                        report += f": {json.dumps(attributes)}"
                    report += "\n"
                report += "\n"

        # Relationships
        relationships = processed_data.get('relationships', [])
        if relationships:
            report += "## RELATIONSHIPS\n\n"
            for rel in relationships:
                if isinstance(rel, dict):
                    source = rel.get('source', 'Unknown')
                    target = rel.get('target', 'Unknown')
                    rel_type = rel.get('type', 'related to')
                    report += f"- {source} **{rel_type}** {target}\n"
            report += "\n"

        # Confidence Assessment
        confidence = analysis.get('confidence_assessment', {})
        if confidence:
            report += "## CONFIDENCE ASSESSMENT\n\n"
            if isinstance(confidence, dict):
                for key, value in confidence.items():
                    report += f"- **{key}:** {value}\n"
            else:
                report += f"{confidence}\n"
            report += "\n"

        # Gaps & Limitations
        gaps = analysis.get('gaps', [])
        limitations = analysis.get('limitations', [])
        if gaps or limitations:
            report += "## GAPS & LIMITATIONS\n\n"
            if gaps:
                report += "**Gaps in Intelligence:**\n"
                for gap in gaps:
                    report += f"- {gap}\n"
                report += "\n"
            if limitations:
                report += "**Limitations:**\n"
                for limitation in limitations:
                    report += f"- {limitation}\n"
                report += "\n"

        # Risk Indicators
        risks = analysis.get('risk_indicators', [])
        if risks:
            report += "## RISK INDICATORS\n\n"
            for risk in risks:
                if isinstance(risk, dict):
                    severity = risk.get('severity', 'unknown')
                    description = risk.get('description', str(risk))
                    report += f"- **[{severity.upper()}]** {description}\n"
                else:
                    report += f"- {risk}\n"
            report += "\n"

        # Recommendations
        recommendations = analysis.get('recommendations', [])
        if recommendations:
            report += "## RECOMMENDATIONS\n\n"
            for i, rec in enumerate(recommendations, 1):
                report += f"{i}. {rec}\n"
            report += "\n"

        # Attribution & Sources
        attribution = analysis.get('attribution', {})
        if attribution:
            report += "## SOURCE ATTRIBUTION\n\n"
            if isinstance(attribution, dict):
                for source, details in attribution.items():
                    report += f"**{source}:** {details}\n"
            else:
                report += f"{attribution}\n"
            report += "\n"

        # Data Quality Notes
        data_quality = processed_data.get('data_quality_notes', [])
        if data_quality:
            report += "## DATA QUALITY NOTES\n\n"
            for note in data_quality:
                report += f"- {note}\n"
            report += "\n"

        # Methodology
        report += "## METHODOLOGY\n\n"
        report += f"This investigation utilized automated OSINT collection and analysis across multiple sources.\n\n"
        report += f"**Collection Methods:**\n"
        collection_results = data.get('collection_results', [])
        tools_used = set()
        for result in collection_results:
            if isinstance(result, dict) and result.get('tool'):
                tools_used.add(result['tool'])

        for tool in sorted(tools_used):
            report += f"- {tool}\n"

        report += "\n**Analysis Framework:** Intelligence Lifecycle (Planning, Collection, Processing, Analysis, Dissemination, Feedback)\n\n"

        # Footer
        report += "---\n\n"
        report += f"**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
        report += f"**Generated By:** OSINT Agent v1.0\n"
        report += f"**Classification:** {classification}\n"

        return report

    def _generate_html(self, data: Dict, classification: str) -> str:
        """Generate HTML report"""
        # Convert markdown to HTML (simplified)
        markdown_report = self._generate_markdown(data, classification)

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Intelligence Report - {data.get('investigation_id', 'UNKNOWN')}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 8px;
        }}
        h3 {{
            color: #7f8c8d;
        }}
        .classification {{
            background-color: #27ae60;
            color: white;
            padding: 10px 20px;
            border-radius: 4px;
            display: inline-block;
            font-weight: bold;
            margin-bottom: 20px;
        }}
        .metadata {{
            background-color: #ecf0f1;
            padding: 15px;
            border-radius: 4px;
            margin: 20px 0;
        }}
        .finding {{
            border-left: 4px solid #3498db;
            padding-left: 15px;
            margin: 15px 0;
        }}
        .risk {{
            border-left: 4px solid #e74c3c;
            padding-left: 15px;
            margin: 10px 0;
        }}
        .confidence {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 3px;
            font-size: 12px;
            font-weight: bold;
        }}
        .confidence-high {{
            background-color: #27ae60;
            color: white;
        }}
        .confidence-medium {{
            background-color: #f39c12;
            color: white;
        }}
        .confidence-low {{
            background-color: #e74c3c;
            color: white;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #34495e;
            color: white;
        }}
        pre {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
            overflow-x: auto;
        }}
        code {{
            background-color: #f8f9fa;
            padding: 2px 6px;
            border-radius: 3px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="classification">{classification}</div>
        <h1>INTELLIGENCE REPORT</h1>

        <div class="metadata">
            <strong>Investigation ID:</strong> {data.get('investigation_id', 'UNKNOWN')}<br>
            <strong>Objective:</strong> {data.get('objective', 'Not specified')}<br>
            <strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}<br>
            <strong>Duration:</strong> {data.get('metadata', {}).get('duration_seconds', 'N/A')} seconds
        </div>

        <pre>{self._escape_html(markdown_report)}</pre>
    </div>
</body>
</html>"""

        return html

    def _generate_json(self, data: Dict) -> str:
        """Generate JSON report"""
        return json.dumps(data, indent=2, default=str)

    def _generate_csv(self, data: Dict) -> str:
        """Generate CSV export of findings"""
        csv_lines = ["Type,Content,Confidence,Timestamp,Source\n"]

        # Extract findings
        analysis = data.get('analysis', {})
        findings = analysis.get('key_findings', [])

        for finding in findings:
            if isinstance(finding, dict):
                finding_type = finding.get('type', 'finding')
                content = str(finding.get('description', finding)).replace('"', '""')
                confidence = finding.get('confidence', 'unknown')
                timestamp = finding.get('timestamp', datetime.now().isoformat())
                source = finding.get('source', 'unknown')

                csv_lines.append(f'"{finding_type}","{content}","{confidence}","{timestamp}","{source}"\n')

        return "".join(csv_lines)

    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters"""
        return (text
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&#39;'))

    def _save_report(self, content: str, investigation_id: str, format: str):
        """Save report to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{investigation_id}_{timestamp}.{format}"
        filepath = self.output_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"Report saved: {filepath}")

    def generate_executive_brief(self, data: Dict) -> str:
        """
        Generate concise executive brief (1-2 pages)

        Args:
            data: Investigation data

        Returns:
            Executive brief as markdown
        """
        analysis = data.get('analysis', {})
        key_findings = analysis.get('key_findings', [])[:5]  # Top 5 findings

        brief = f"""# EXECUTIVE BRIEF
**Investigation ID:** {data.get('investigation_id')}
**Date:** {datetime.now().strftime('%Y-%m-%d')}

## SUMMARY
**Objective:** {data.get('objective')}

## TOP FINDINGS
"""

        for i, finding in enumerate(key_findings, 1):
            if isinstance(finding, dict):
                brief += f"{i}. {finding.get('description', str(finding))}\n"
            else:
                brief += f"{i}. {finding}\n"

        brief += f"\n## RECOMMENDATION\n"
        recommendations = analysis.get('recommendations', [])
        if recommendations:
            brief += f"{recommendations[0]}\n"

        return brief

    def generate_technical_appendix(self, data: Dict) -> str:
        """
        Generate detailed technical appendix

        Args:
            data: Investigation data

        Returns:
            Technical appendix as markdown
        """
        appendix = "# TECHNICAL APPENDIX\n\n"

        # Collection details
        appendix += "## COLLECTION DETAILS\n\n"
        collection_results = data.get('collection_results', [])

        for i, result in enumerate(collection_results, 1):
            if isinstance(result, dict):
                tool = result.get('tool', 'unknown')
                success = result.get('success', False)
                appendix += f"### Collection {i}: {tool}\n"
                appendix += f"- Success: {success}\n"
                appendix += f"- Timestamp: {result.get('timestamp', 'N/A')}\n"
                if result.get('parameters'):
                    appendix += f"- Parameters: {json.dumps(result['parameters'])}\n"
                appendix += "\n"

        # Raw data summary
        appendix += "## RAW DATA SUMMARY\n\n"
        processed_data = data.get('processed_data', {})
        appendix += f"- Entities: {len(processed_data.get('entities', []))}\n"
        appendix += f"- Events: {len(processed_data.get('events', []))}\n"
        appendix += f"- Relationships: {len(processed_data.get('relationships', []))}\n"

        return appendix

    def create_dashboard_data(self, data: Dict) -> Dict:
        """
        Create data structure for dashboard visualization

        Args:
            data: Investigation data

        Returns:
            Dashboard data structure
        """
        analysis = data.get('analysis', {})

        dashboard = {
            'investigation_id': data.get('investigation_id'),
            'objective': data.get('objective'),
            'status': 'completed',
            'metrics': {
                'findings_count': len(analysis.get('key_findings', [])),
                'entities_count': len(data.get('processed_data', {}).get('entities', [])),
                'relationships_count': len(data.get('processed_data', {}).get('relationships', [])),
                'duration': data.get('metadata', {}).get('duration_seconds', 0),
                'tools_used': data.get('metadata', {}).get('tools_used', 0)
            },
            'confidence_distribution': self._calculate_confidence_distribution(analysis),
            'entity_types': self._count_entity_types(data.get('processed_data', {})),
            'timeline_data': analysis.get('timeline', []),
            'risk_level': self._calculate_risk_level(analysis)
        }

        return dashboard

    def _calculate_confidence_distribution(self, analysis: Dict) -> Dict:
        """Calculate confidence level distribution"""
        distribution = {
            'very_high': 0,
            'high': 0,
            'medium': 0,
            'low': 0,
            'very_low': 0
        }

        findings = analysis.get('key_findings', [])
        for finding in findings:
            if isinstance(finding, dict):
                confidence = finding.get('confidence', 'unknown')
                if confidence in distribution:
                    distribution[confidence] += 1

        return distribution

    def _count_entity_types(self, processed_data: Dict) -> Dict:
        """Count entities by type"""
        entity_counts = {}

        entities = processed_data.get('entities', [])
        for entity in entities:
            if isinstance(entity, dict):
                entity_type = entity.get('type', 'unknown')
                entity_counts[entity_type] = entity_counts.get(entity_type, 0) + 1

        return entity_counts

    def _calculate_risk_level(self, analysis: Dict) -> str:
        """Calculate overall risk level"""
        risk_indicators = analysis.get('risk_indicators', [])

        if not risk_indicators:
            return 'low'

        # Simple heuristic based on number of risk indicators
        if len(risk_indicators) >= 5:
            return 'high'
        elif len(risk_indicators) >= 2:
            return 'medium'
        else:
            return 'low'

    def generate_obsidian_canvas(
        self,
        data: Dict,
        canvas_type: str = 'overview',
        save: bool = True
    ) -> Optional[str]:
        """
        Generate Obsidian Canvas mind map

        Args:
            data: Investigation data
            canvas_type: Type of canvas (overview, entity_map, timeline, findings, all)
            save: Save canvas to file

        Returns:
            Canvas JSON string or None if Obsidian not available
        """
        if not OBSIDIAN_AVAILABLE:
            print("Warning: Obsidian Canvas generator not available")
            return None

        canvas_gen = ObsidianCanvasGenerator()

        if canvas_type == 'overview':
            canvas_json = canvas_gen.generate_investigation_overview(data)
            if save:
                inv_id = data.get('investigation_id', 'investigation')
                canvas_gen.save_canvas(canvas_json, f"{inv_id}_overview")
            return canvas_json

        elif canvas_type == 'entity_map':
            canvas_json = canvas_gen.generate_entity_map(data, layout='radial')
            if save:
                inv_id = data.get('investigation_id', 'investigation')
                canvas_gen.save_canvas(canvas_json, f"{inv_id}_entity_map")
            return canvas_json

        elif canvas_type == 'timeline':
            canvas_json = canvas_gen.generate_timeline_canvas(data)
            if save:
                inv_id = data.get('investigation_id', 'investigation')
                canvas_gen.save_canvas(canvas_json, f"{inv_id}_timeline")
            return canvas_json

        elif canvas_type == 'findings':
            canvas_json = canvas_gen.generate_findings_canvas(data)
            if save:
                inv_id = data.get('investigation_id', 'investigation')
                canvas_gen.save_canvas(canvas_json, f"{inv_id}_findings")
            return canvas_json

        elif canvas_type == 'all':
            canvases = canvas_gen.generate_all_canvases(data)
            print(f"Generated {len(canvases)} canvas files:")
            for canvas_type, filepath in canvases.items():
                print(f"  - {canvas_type}: {filepath}")
            return json.dumps({'canvases': [str(p) for p in canvases.values()]})

        else:
            print(f"Unknown canvas type: {canvas_type}")
            return None
