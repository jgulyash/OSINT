#!/usr/bin/env python3
"""
Example: Obsidian Canvas Mind Map Generation

Demonstrates how to generate interactive Obsidian Canvas mind maps
from OSINT investigation data.

Canvas Types:
1. Investigation Overview - High-level summary
2. Entity Relationship Map - Network of discovered entities
3. Timeline - Chronological event visualization
4. Findings Hierarchy - Organized by confidence level
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents.llm_client import create_llm_client
from src.agents.osint_agent import OSINTAgent
from src.memory.memory_store import MemoryStore
from src.reporters.report_generator import ReportGenerator
from src.reporters.obsidian_canvas import ObsidianCanvasGenerator, create_obsidian_vault_structure
from src.tools.osint_tools import get_all_tools


async def main():
    """
    Demonstrate Obsidian Canvas generation for OSINT investigations
    """
    print("=" * 80)
    print("OBSIDIAN CANVAS MIND MAP GENERATION FOR OSINT")
    print("=" * 80)
    print("\n🗺️  This example shows how to create visual mind maps from investigations\n")

    # Initialize AI-powered OSINT system
    print("⚙️  Initializing OSINT agent...")
    llm = create_llm_client()
    memory = MemoryStore()
    tools = get_all_tools()
    agent = OSINTAgent(llm, tools, memory, config={'max_iterations': 10})

    print(f"   ✓ AI Model: {llm.get_model_info()['model']}")
    print(f"   ✓ Tools: {len(tools)} available\n")

    # Run investigation
    objective = "Investigate github.com for infrastructure and security intelligence"

    print(f"🔍 Running investigation...")
    print(f"   Objective: {objective}\n")

    result = await agent.investigate(objective=objective, auto_report=False)

    investigation_id = result.get('investigation_id')
    print(f"\n✅ Investigation complete!")
    print(f"   ID: {investigation_id}")
    print(f"   Findings: {len(result.get('analysis', {}).get('key_findings', []))}")
    print(f"   Entities: {len(result.get('processed_data', {}).get('entities', []))}\n")

    # Prepare data for canvas generation
    investigation_data = {
        'investigation_id': investigation_id,
        'objective': objective,
        'analysis': result.get('analysis', {}),
        'processed_data': result.get('processed_data', {}),
        'collection_results': result.get('collection_results', []),
        'metadata': result.get('metadata', {})
    }

    # Create Obsidian vault structure
    print("=" * 80)
    print("CREATING OBSIDIAN VAULT")
    print("=" * 80)
    print()

    vault_path = create_obsidian_vault_structure("data/obsidian_vault")
    print(f"\n✅ Obsidian vault ready at: {vault_path}\n")

    # Generate canvases
    print("=" * 80)
    print("GENERATING OBSIDIAN CANVASES")
    print("=" * 80)
    print()

    canvas_gen = ObsidianCanvasGenerator(output_dir=str(vault_path / "Canvases"))

    # 1. Investigation Overview Canvas
    print("1️⃣  Generating Investigation Overview Canvas...")
    overview_json = canvas_gen.generate_investigation_overview(investigation_data)
    overview_path = canvas_gen.save_canvas(overview_json, f"{investigation_id}_overview")
    print(f"   ✓ Saved: {overview_path}\n")

    # 2. Entity Relationship Map Canvas
    print("2️⃣  Generating Entity Relationship Map Canvas...")
    entity_json = canvas_gen.generate_entity_map(investigation_data, layout='radial')
    entity_path = canvas_gen.save_canvas(entity_json, f"{investigation_id}_entity_map")
    print(f"   ✓ Saved: {entity_path}\n")

    # 3. Timeline Canvas
    print("3️⃣  Generating Timeline Canvas...")
    timeline_json = canvas_gen.generate_timeline_canvas(investigation_data)
    timeline_path = canvas_gen.save_canvas(timeline_json, f"{investigation_id}_timeline")
    print(f"   ✓ Saved: {timeline_path}\n")

    # 4. Findings Hierarchy Canvas
    print("4️⃣  Generating Findings Hierarchy Canvas...")
    findings_json = canvas_gen.generate_findings_canvas(investigation_data)
    findings_path = canvas_gen.save_canvas(findings_json, f"{investigation_id}_findings")
    print(f"   ✓ Saved: {findings_path}\n")

    # Summary
    print("=" * 80)
    print("CANVAS GENERATION COMPLETE")
    print("=" * 80)
    print()

    print(f"📊 Generated Canvases:")
    print(f"   1. Investigation Overview - {overview_path.name}")
    print(f"   2. Entity Relationship Map - {entity_path.name}")
    print(f"   3. Timeline - {timeline_path.name}")
    print(f"   4. Findings Hierarchy - {findings_path.name}")

    print(f"\n🗺️  All canvases saved to: {vault_path / 'Canvases'}")

    print(f"\n" + "=" * 80)
    print("HOW TO VIEW YOUR MIND MAPS")
    print("=" * 80)
    print()

    print("📓 Step-by-Step Instructions:")
    print()
    print("1. Download Obsidian (if not installed):")
    print("   https://obsidian.md/")
    print()
    print("2. Open Obsidian")
    print()
    print("3. Click 'Open folder as vault'")
    print()
    print(f"4. Navigate to and select: {vault_path}")
    print()
    print("5. In Obsidian's left sidebar, expand the 'Canvases' folder")
    print()
    print("6. Click on any .canvas file to open the interactive mind map!")
    print()
    print("7. You can:")
    print("   • Zoom in/out with mouse wheel")
    print("   • Pan by clicking and dragging")
    print("   • Rearrange nodes by dragging them")
    print("   • Double-click nodes to edit")
    print("   • Add notes and annotations")
    print("   • Create connections between nodes")
    print("   • Export as images")

    print(f"\n" + "=" * 80)
    print("CANVAS TYPES EXPLAINED")
    print("=" * 80)
    print()

    print("🔍 Investigation Overview:")
    print("   Central investigation node connected to all major categories")
    print("   (findings, entities, timeline, risks, recommendations, data sources)")
    print()

    print("🕸️  Entity Relationship Map:")
    print("   Radial layout showing all discovered entities and their relationships")
    print("   Color-coded by entity type (domains, IPs, people, organizations, etc.)")
    print()

    print("📅 Timeline:")
    print("   Vertical chronological visualization of investigation events")
    print("   Sequential connection from earliest to latest event")
    print()

    print("📋 Findings Hierarchy:")
    print("   Findings organized by confidence level (very high → very low)")
    print("   Grouped visually for easy pattern recognition")

    print(f"\n" + "=" * 80)
    print("INTEGRATION WITH REPORTS")
    print("=" * 80)
    print()

    print("💡 You can also generate canvases alongside regular reports:")
    print()
    print("Python:")
    print("```python")
    print("from src.reporters.report_generator import ReportGenerator")
    print()
    print("reporter = ReportGenerator()")
    print()
    print("# Generate all formats including canvas")
    print("reporter.generate_report(data, format='markdown', save=True)")
    print("reporter.generate_obsidian_canvas(data, canvas_type='all', save=True)")
    print("```")
    print()
    print("CLI:")
    print("```bash")
    print("# Generate investigation report")
    print("python -m src.cli investigate \"Investigate example.com\"")
    print()
    print("# Generate canvas visualizations")
    print(f"python -m src.cli canvas {investigation_id} --type all")
    print()
    print("# Create Obsidian vault")
    print("python -m src.cli create-vault")
    print("```")

    print(f"\n" + "=" * 80)
    print("✨ OSINT INVESTIGATION MIND MAPS READY!")
    print("=" * 80)
    print()

    print(f"🎯 Your interactive knowledge graphs are waiting in Obsidian!")
    print(f"📍 Vault location: {vault_path}")
    print(f"🗺️  Canvas location: {vault_path / 'Canvases'}")
    print()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Canvas generation interrupted")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
