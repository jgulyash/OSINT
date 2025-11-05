#!/usr/bin/env python3
"""
AI-Powered OSINT Agent - Main Entry Point

Complete autonomous intelligence gathering and analysis workflow
"""

import asyncio
import sys
import os
import logging
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.agents.llm_client import create_llm_client
from src.agents.osint_agent import OSINTAgent
from src.agents.workflow_orchestrator import WorkflowOrchestrator, WorkflowType
from src.memory.memory_store import MemoryStore
from src.reporters.report_generator import ReportGenerator
from src.tools.osint_tools import get_all_tools

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def setup_logging():
    """Configure logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('data/osint_agent.log')
        ]
    )


async def run_simple_investigation(objective: str):
    """
    Run a simple AI-powered investigation

    Args:
        objective: Investigation objective
    """
    print("=" * 80)
    print("AI-POWERED OSINT INVESTIGATION")
    print("=" * 80)
    print(f"\nObjective: {objective}\n")

    # Initialize AI-powered components
    print("🤖 Initializing AI-powered OSINT agent...")
    llm_client = create_llm_client()
    memory = MemoryStore()
    tools = get_all_tools()

    print(f"✓ LLM Client: {llm_client.get_model_info()['model']}")
    print(f"✓ Available Tools: {len(tools)}")
    print(f"✓ Memory Store: Connected")

    # Create autonomous agent
    agent = OSINTAgent(
        llm_client=llm_client,
        tools=tools,
        memory_store=memory,
        config={
            'max_iterations': 15,
            'min_confidence': 0.6
        }
    )

    print("\n🔍 Starting autonomous investigation...")
    print("   The AI agent will:")
    print("   1. Create investigation plan")
    print("   2. Collect intelligence from multiple sources")
    print("   3. Process and normalize data")
    print("   4. Analyze findings with AI")
    print("   5. Generate intelligence report")
    print("   6. Evaluate investigation quality\n")

    # Run complete autonomous investigation
    result = await agent.investigate(objective=objective, auto_report=True)

    # Display results
    print("\n" + "=" * 80)
    print("INVESTIGATION COMPLETE")
    print("=" * 80)

    metadata = result.get('metadata', {})
    analysis = result.get('analysis', {})

    print(f"\n📊 Investigation Metrics:")
    print(f"   • Duration: {metadata.get('duration_seconds', 0):.2f} seconds")
    print(f"   • Iterations: {metadata.get('iterations', 0)}")
    print(f"   • Tools Used: {metadata.get('tools_used', 0)}")
    print(f"   • Findings: {len(analysis.get('key_findings', []))}")
    print(f"   • Entities: {len(result.get('processed_data', {}).get('entities', []))}")

    # Save report
    print(f"\n📄 Generating intelligence report...")
    reporter = ReportGenerator()

    investigation_data = {
        'investigation_id': result.get('investigation_id'),
        'objective': objective,
        'analysis': analysis,
        'processed_data': result.get('processed_data'),
        'collection_results': result.get('collection_results'),
        'metadata': metadata
    }

    # Generate in multiple formats
    formats = ['markdown', 'html', 'json']
    for fmt in formats:
        report = reporter.generate_report(
            investigation_data,
            format=fmt,
            classification='UNCLASSIFIED',
            save=True
        )
        print(f"   ✓ {fmt.upper()} report generated")

    print(f"\n✅ Reports saved to: data/reports/")
    print(f"\n🎯 Investigation ID: {result.get('investigation_id')}")

    return result


async def run_automated_workflow():
    """
    Demonstrate automated workflow with AI orchestration
    """
    print("\n" + "=" * 80)
    print("AUTOMATED AI-POWERED WORKFLOW DEMO")
    print("=" * 80)

    # Initialize
    llm_client = create_llm_client()
    memory = MemoryStore()
    tools = get_all_tools()
    agent = OSINTAgent(llm_client, tools, memory)

    # Create workflow orchestrator
    orchestrator = WorkflowOrchestrator(agent, memory)

    print("\n🔄 Creating automated workflows...\n")

    # Workflow 1: One-time investigation
    print("1️⃣  Creating one-time investigation workflow...")
    workflow1_id = await orchestrator.create_workflow(
        name="security_assessment",
        workflow_type=WorkflowType.ONE_TIME,
        objective="Perform security assessment of github.com domain",
        constraints={'time_limit': 300, 'sources': ['web', 'dns', 'ssl']},
        alert_conditions=[
            {'type': 'risk_indicator', 'severity': 'high'},
            {'type': 'finding_count', 'threshold': 3}
        ]
    )
    print(f"   ✓ Workflow created: {workflow1_id}")

    # Execute workflow
    print(f"\n🚀 Executing automated workflow...")
    result1 = await orchestrator.execute_workflow(workflow1_id)

    if 'error' not in result1:
        print(f"   ✓ Workflow completed successfully")
        print(f"   • Investigation ID: {result1.get('investigation_id')}")
        print(f"   • Findings: {len(result1.get('analysis', {}).get('key_findings', []))}")
    else:
        print(f"   ✗ Workflow failed: {result1.get('error')}")

    # Check for alerts
    alerts = orchestrator.get_alerts(status='active')
    if alerts:
        print(f"\n🚨 {len(alerts)} alerts triggered:")
        for alert in alerts:
            print(f"   • [{alert['severity'].upper()}] {alert['condition']['type']}")

    print(f"\n✅ Automated workflow demonstration complete!")


async def run_multi_target_campaign():
    """
    Demonstrate multi-target automated campaign
    """
    print("\n" + "=" * 80)
    print("MULTI-TARGET AI CAMPAIGN")
    print("=" * 80)

    targets = [
        {'name': 'github.com', 'type': 'domain'},
        {'name': 'google.com', 'type': 'domain'},
        {'name': 'cloudflare.com', 'type': 'domain'}
    ]

    print(f"\n🎯 Campaign targets: {len(targets)}")
    for t in targets:
        print(f"   • {t['name']} ({t['type']})")

    # Initialize
    llm_client = create_llm_client()
    memory = MemoryStore()
    tools = get_all_tools()
    agent = OSINTAgent(llm_client, tools, memory, config={'max_iterations': 10})

    orchestrator = WorkflowOrchestrator(agent, memory)

    print(f"\n🚀 Starting AI-powered campaign (sequential)...")

    # Run campaign
    result = await orchestrator.run_campaign(
        campaign_name="domain_security_scan",
        targets=targets,
        objective_template="Investigate {target} for security and infrastructure information",
        parallel=False  # Sequential for demo
    )

    print(f"\n📊 Campaign Results:")
    print(f"   • Total targets: {len(targets)}")
    print(f"   • Successful: {result['completed']}")
    print(f"   • Failed: {result['failed']}")
    print(f"   • Duration: {(datetime.fromisoformat(result['end_time']) - datetime.fromisoformat(result['start_time'])).total_seconds():.2f}s")

    print(f"\n✅ Campaign complete!")


async def interactive_demo():
    """
    Interactive demonstration of AI-powered OSINT capabilities
    """
    print("\n" + "=" * 80)
    print("🤖 AI-POWERED OSINT AGENT - INTERACTIVE DEMO")
    print("=" * 80)

    print("\nThis demonstration showcases the autonomous AI-powered capabilities:")
    print("")
    print("1. 🔍 Single Investigation - AI-driven intelligence gathering")
    print("2. 🔄 Automated Workflow - Scheduled and triggered investigations")
    print("3. 🎯 Multi-Target Campaign - Parallel target analysis")
    print("4. 📊 Full Demo - All capabilities")
    print("5. ❌ Exit")

    choice = input("\nSelect demo (1-5): ").strip()

    if choice == '1':
        objective = input("\nEnter investigation objective: ").strip()
        if not objective:
            objective = "Investigate github.com for security and infrastructure information"
            print(f"Using default: {objective}")

        await run_simple_investigation(objective)

    elif choice == '2':
        await run_automated_workflow()

    elif choice == '3':
        await run_multi_target_campaign()

    elif choice == '4':
        print("\n🚀 Running full demonstration...\n")
        await run_simple_investigation("Investigate example.com for OSINT intelligence")
        await run_automated_workflow()
        await run_multi_target_campaign()

    elif choice == '5':
        print("\n👋 Exiting...")
        return

    else:
        print("\n❌ Invalid choice")


def main():
    """Main entry point"""
    setup_logging()

    # Ensure data directories exist
    Path("data/reports").mkdir(parents=True, exist_ok=True)
    Path("data/investigations").mkdir(parents=True, exist_ok=True)
    Path("data/cache").mkdir(parents=True, exist_ok=True)

    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║        🤖 AI-POWERED OSINT INTELLIGENCE AGENT 🤖              ║
    ║                                                               ║
    ║     Autonomous Intelligence Gathering & Analysis System      ║
    ║                         Version 1.0                           ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)

    # Check if objective provided as argument
    if len(sys.argv) > 1:
        objective = " ".join(sys.argv[1:])
        print(f"\n🎯 Running investigation from command line argument...")
        asyncio.run(run_simple_investigation(objective))
    else:
        # Interactive mode
        asyncio.run(interactive_demo())

    print("\n" + "=" * 80)
    print("Thank you for using AI-Powered OSINT Agent!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        logging.exception("Fatal error in main")
        sys.exit(1)
