#!/usr/bin/env python3
"""
Example: AI-Powered Continuous Monitoring

Demonstrates automated, continuous OSINT monitoring with:
- Scheduled periodic investigations
- AI-driven change detection
- Automatic alert generation
- Adaptive monitoring strategies

This runs continuously and autonomously monitors targets
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents.llm_client import create_llm_client
from src.agents.osint_agent import OSINTAgent
from src.agents.workflow_orchestrator import WorkflowOrchestrator, WorkflowType
from src.memory.memory_store import MemoryStore
from src.tools.osint_tools import get_all_tools


async def main():
    """
    Run continuous AI-powered monitoring
    """
    print("=" * 80)
    print("AI-POWERED CONTINUOUS OSINT MONITORING")
    print("=" * 80)
    print("\n🤖 Autonomous monitoring system with AI-driven decision making\n")

    # Initialize
    llm_client = create_llm_client()
    memory = MemoryStore()
    tools = get_all_tools()

    agent = OSINTAgent(llm_client, tools, memory, config={'max_iterations': 10})
    orchestrator = WorkflowOrchestrator(agent, memory)

    # Define monitoring target
    target = "example.com"
    objective = f"Monitor {target} for any security, infrastructure, or operational changes"

    print(f"🎯 Monitoring Target: {target}")
    print(f"📋 Objective: {objective}")
    print(f"🔄 Mode: Continuous with AI-driven change detection\n")

    # Create continuous monitoring workflow
    print("⚙️  Setting up automated monitoring workflow...")

    workflow_id = await orchestrator.create_workflow(
        name=f"monitor_{target}",
        workflow_type=WorkflowType.CONTINUOUS,
        objective=objective,
        constraints={
            'focus_areas': ['dns', 'ssl', 'infrastructure', 'security'],
            'quick_scan': True
        },
        alert_conditions=[
            {
                'type': 'change_detected',
                'severity': 'medium',
                'description': 'AI detected changes in target'
            },
            {
                'type': 'risk_indicator',
                'severity': 'high',
                'description': 'Security risk indicators found'
            },
            {
                'type': 'new_entities',
                'threshold': 1,
                'severity': 'low',
                'description': 'New entities discovered'
            }
        ]
    )

    print(f"✓ Workflow created: {workflow_id}")
    print(f"✓ Alert conditions configured: 3 rules active\n")

    print("🚀 Starting continuous monitoring...")
    print("   The AI will:")
    print("   • Periodically investigate the target")
    print("   • Detect and analyze changes automatically")
    print("   • Generate alerts based on AI analysis")
    print("   • Adapt monitoring strategy based on findings")
    print("   • Log all activities to memory store\n")

    print("⏱️  Check interval: 60 seconds (for demo)")
    print("⚠️  Press Ctrl+C to stop monitoring\n")

    input("Press Enter to start monitoring...")

    # Start monitoring (runs indefinitely)
    try:
        await orchestrator.continuous_monitoring(
            workflow_id=workflow_id,
            check_interval=60  # Check every 60 seconds for demo
        )
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping monitoring...")

    # Show monitoring results
    print("\n" + "=" * 80)
    print("MONITORING SESSION SUMMARY")
    print("=" * 80)

    # Get workflow status
    status = orchestrator.get_workflow_status(workflow_id)
    print(f"\n📊 Workflow Status:")
    print(f"   • Name: {status['name']}")
    print(f"   • Executions: {status['executions']}")
    print(f"   • Last run: {status.get('last_execution', {}).get('end_time', 'N/A')}")

    # Get alerts
    alerts = orchestrator.get_alerts(status='active')
    print(f"\n🚨 Alerts Generated: {len(alerts)}")

    if alerts:
        print("\n   Recent Alerts:")
        for i, alert in enumerate(alerts[-5:], 1):
            severity = alert['severity'].upper()
            condition_type = alert['condition']['type']
            print(f"   {i}. [{severity}] {condition_type} - {alert['timestamp'][:19]}")

        print(f"\n💡 Acknowledge alerts using:")
        print(f"   orchestrator.acknowledge_alert(alert_id)")

    print(f"\n✅ Monitoring session complete")
    print(f"   All data saved to memory store for analysis\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Monitoring stopped by user")
