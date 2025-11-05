#!/usr/bin/env python3
"""
Example: AI-Powered Multi-Target Campaign

Demonstrates automated campaign across multiple targets with:
- Parallel or sequential AI-driven investigations
- Comparative analysis across targets
- Consolidated reporting
- Campaign-level insights

The AI autonomously investigates multiple targets and provides comparative intelligence
"""

import asyncio
import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents.llm_client import create_llm_client
from src.agents.osint_agent import OSINTAgent
from src.agents.workflow_orchestrator import WorkflowOrchestrator
from src.memory.memory_store import MemoryStore
from src.tools.osint_tools import get_all_tools


async def main():
    """
    Run AI-powered multi-target campaign
    """
    print("=" * 80)
    print("AI-POWERED MULTI-TARGET OSINT CAMPAIGN")
    print("=" * 80)
    print("\n🤖 Autonomous investigation of multiple targets with comparative analysis\n")

    # Define campaign targets
    targets = [
        {'name': 'github.com', 'category': 'tech'},
        {'name': 'gitlab.com', 'category': 'tech'},
        {'name': 'bitbucket.org', 'category': 'tech'}
    ]

    objective_template = """
    Investigate {target} and provide intelligence on:
    - Domain and infrastructure
    - Technologies and security posture
    - Notable characteristics
    """

    print(f"🎯 Campaign Targets: {len(targets)}")
    for i, target in enumerate(targets, 1):
        print(f"   {i}. {target['name']} ({target['category']})")

    print(f"\n📋 Investigation Template:")
    print(f"   {objective_template.strip()}")

    # Initialize AI system
    print(f"\n⚙️  Initializing AI-powered campaign system...")

    llm_client = create_llm_client()
    memory = MemoryStore()
    tools = get_all_tools()

    print(f"   ✓ AI Model: {llm_client.get_model_info()['model']}")
    print(f"   ✓ OSINT Tools: {len(tools)} available")

    agent = OSINTAgent(
        llm_client=llm_client,
        tools=tools,
        memory_store=memory,
        config={'max_iterations': 10}  # Faster per-target investigation
    )

    orchestrator = WorkflowOrchestrator(agent, memory)

    # Select campaign mode
    print(f"\n🔀 Campaign Execution Mode:")
    print(f"   1. Sequential (one after another, safer)")
    print(f"   2. Parallel (all at once, faster)")

    mode_choice = input("\n   Select mode (1 or 2): ").strip()
    parallel = (mode_choice == '2')

    mode_name = "PARALLEL" if parallel else "SEQUENTIAL"
    print(f"\n   ✓ Mode: {mode_name}")

    input(f"\nPress Enter to start {mode_name} campaign...")

    # Run campaign
    print(f"\n🚀 Starting AI-powered campaign...\n")

    result = await orchestrator.run_campaign(
        campaign_name="code_hosting_platforms_analysis",
        targets=targets,
        objective_template=objective_template,
        parallel=parallel
    )

    # Display results
    print("\n" + "=" * 80)
    print("CAMPAIGN COMPLETE")
    print("=" * 80)

    print(f"\n📊 Campaign Statistics:")
    print(f"   • Total targets: {len(targets)}")
    print(f"   • Successful investigations: {result['completed']}")
    print(f"   • Failed investigations: {result['failed']}")
    print(f"   • Start time: {result['start_time'][:19]}")
    print(f"   • End time: {result['end_time'][:19]}")

    from datetime import datetime
    duration = (
        datetime.fromisoformat(result['end_time']) -
        datetime.fromisoformat(result['start_time'])
    ).total_seconds()
    print(f"   • Total duration: {duration:.2f} seconds")
    print(f"   • Average per target: {duration/len(targets):.2f} seconds")

    # Analyze results per target
    print(f"\n🎯 Per-Target Results:")

    successful_results = [r for r in result['results'] if 'error' not in r]

    for i, (target, target_result) in enumerate(zip(targets, result['results']), 1):
        print(f"\n   {i}. {target['name']}")

        if 'error' in target_result:
            print(f"      ❌ Failed: {target_result['error']}")
        else:
            analysis = target_result.get('analysis', {})
            metadata = target_result.get('metadata', {})

            findings_count = len(analysis.get('key_findings', []))
            entities_count = len(target_result.get('processed_data', {}).get('entities', []))
            duration = metadata.get('duration_seconds', 0)

            print(f"      ✅ Success")
            print(f"         • Investigation ID: {target_result.get('investigation_id', 'N/A')[:12]}...")
            print(f"         • Findings: {findings_count}")
            print(f"         • Entities: {entities_count}")
            print(f"         • Duration: {duration:.2f}s")

            # Show top finding
            key_findings = analysis.get('key_findings', [])
            if key_findings:
                first_finding = key_findings[0]
                if isinstance(first_finding, dict):
                    desc = first_finding.get('description', str(first_finding))[:60]
                else:
                    desc = str(first_finding)[:60]
                print(f"         • Top finding: {desc}...")

    # AI-powered comparative analysis
    if len(successful_results) > 1:
        print(f"\n🧠 AI-Powered Comparative Analysis:")
        print(f"\n   Generating cross-target insights...")

        # Collect all analyses
        all_analyses = [r.get('analysis', {}) for r in successful_results]

        # Simple comparative metrics
        findings_per_target = [len(a.get('key_findings', [])) for a in all_analyses]
        entities_per_target = [len(r.get('processed_data', {}).get('entities', [])) for r in successful_results]

        avg_findings = sum(findings_per_target) / len(findings_per_target)
        avg_entities = sum(entities_per_target) / len(entities_per_target)

        print(f"\n   📈 Campaign-Wide Metrics:")
        print(f"      • Average findings per target: {avg_findings:.1f}")
        print(f"      • Average entities per target: {avg_entities:.1f}")
        print(f"      • Total intelligence gathered: {sum(findings_per_target)} findings")

        # Identify outliers
        max_findings_idx = findings_per_target.index(max(findings_per_target))
        print(f"\n   🏆 Most Intelligence Gathered: {targets[max_findings_idx]['name']}")
        print(f"      ({findings_per_target[max_findings_idx]} findings)")

    # Save campaign summary
    print(f"\n💾 Saving campaign results...")

    campaign_file = Path("data/investigations/campaign_results.json")
    campaign_file.parent.mkdir(parents=True, exist_ok=True)

    with open(campaign_file, 'w') as f:
        json.dump(result, f, indent=2, default=str)

    print(f"   ✓ Campaign results saved: {campaign_file}")

    print(f"\n" + "=" * 80)
    print("✅ AI-POWERED CAMPAIGN SUCCESSFULLY COMPLETED")
    print("=" * 80)
    print(f"\n💡 The AI autonomously:")
    print(f"   ✓ Investigated {len(targets)} targets")
    print(f"   ✓ Collected and analyzed intelligence for each")
    print(f"   ✓ Generated {sum(findings_per_target) if successful_results else 0} total findings")
    print(f"   ✓ Performed comparative analysis")
    print(f"   ✓ Created consolidated reports\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Campaign interrupted by user")
    except Exception as e:
        print(f"\n❌ Campaign failed: {e}")
        import traceback
        traceback.print_exc()
