#!/usr/bin/env python3
"""
Example: Fully Automated AI-Powered OSINT Investigation

This example demonstrates how the AI agent autonomously:
1. Plans the investigation strategy
2. Collects intelligence from multiple sources
3. Processes and normalizes data
4. Analyzes findings with AI
5. Generates comprehensive reports
6. Evaluates investigation quality

NO MANUAL INTERVENTION REQUIRED - The AI makes all decisions
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents.llm_client import create_llm_client
from src.agents.osint_agent import OSINTAgent
from src.memory.memory_store import MemoryStore
from src.reporters.report_generator import ReportGenerator
from src.tools.osint_tools import get_all_tools


async def main():
    """
    Run fully automated investigation
    """
    print("=" * 80)
    print("FULLY AUTOMATED AI-POWERED OSINT INVESTIGATION")
    print("=" * 80)
    print("\n🤖 The AI agent will autonomously handle the entire investigation")
    print("   No manual steps required!\n")

    # Define investigation objective
    objective = """
    Investigate the domain 'github.com' and provide comprehensive intelligence including:
    - Domain registration and ownership information
    - DNS and infrastructure details
    - SSL/TLS certificate information
    - Web presence and technologies
    - Any security-relevant findings
    """

    print(f"📋 Objective: {objective.strip()}\n")

    # Initialize AI-powered components
    print("⚙️  Initializing AI-powered OSINT system...")

    # Create LLM client (AI brain)
    llm_client = create_llm_client()
    print(f"   ✓ AI Model: {llm_client.get_model_info()['model']}")

    # Create memory store
    memory = MemoryStore()
    print(f"   ✓ Memory Store: Initialized")

    # Load OSINT tools
    tools = get_all_tools()
    print(f"   ✓ OSINT Tools: {len(tools)} tools loaded")

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
    print(f"   ✓ Autonomous Agent: Ready\n")

    # ==================== AUTONOMOUS INVESTIGATION ====================

    print("🚀 Starting autonomous investigation...\n")
    print("The AI will now:")
    print("   1. 🧠 Create an investigation plan using AI reasoning")
    print("   2. 🔍 Execute intelligence collection autonomously")
    print("   3. 🔄 Process and normalize collected data")
    print("   4. 🎯 Analyze findings with AI")
    print("   5. 📊 Make adaptive decisions to continue or pivot")
    print("   6. 📝 Generate intelligence reports")
    print("   7. ✅ Evaluate investigation quality\n")

    input("Press Enter to start the AI-powered investigation...")

    # Run completely autonomous investigation
    result = await agent.investigate(
        objective=objective,
        constraints={
            'time_limit': 600,  # 10 minutes max
            'focus_areas': ['infrastructure', 'security', 'technology']
        },
        auto_report=True
    )

    # ==================== RESULTS ====================

    print("\n" + "=" * 80)
    print("AUTONOMOUS INVESTIGATION COMPLETE")
    print("=" * 80)

    metadata = result.get('metadata', {})
    analysis = result.get('analysis', {})
    processed_data = result.get('processed_data', {})

    print(f"\n📊 Investigation Metrics:")
    print(f"   • Investigation ID: {result.get('investigation_id')}")
    print(f"   • Duration: {metadata.get('duration_seconds', 0):.2f} seconds")
    print(f"   • AI Iterations: {metadata.get('iterations', 0)}")
    print(f"   • Tools Used: {metadata.get('tools_used', 0)}")

    print(f"\n🎯 Intelligence Gathered:")
    print(f"   • Key Findings: {len(analysis.get('key_findings', []))}")
    print(f"   • Entities Identified: {len(processed_data.get('entities', []))}")
    print(f"   • Relationships Mapped: {len(processed_data.get('relationships', []))}")
    print(f"   • Events Timeline: {len(analysis.get('timeline', []))}")

    # Show AI-generated findings
    print(f"\n🧠 AI-Generated Key Findings:")
    key_findings = analysis.get('key_findings', [])[:5]
    for i, finding in enumerate(key_findings, 1):
        if isinstance(finding, dict):
            desc = finding.get('description', str(finding))
            conf = finding.get('confidence', 'unknown')
            print(f"   {i}. [{conf.upper()}] {desc}")
        else:
            print(f"   {i}. {finding}")

    # Show AI confidence assessment
    confidence = analysis.get('confidence_assessment', {})
    if confidence:
        print(f"\n🎖️  AI Confidence Assessment:")
        if isinstance(confidence, dict):
            for key, value in list(confidence.items())[:3]:
                print(f"   • {key}: {value}")

    # Show AI recommendations
    recommendations = analysis.get('recommendations', [])
    if recommendations:
        print(f"\n💡 AI Recommendations:")
        for i, rec in enumerate(recommendations[:3], 1):
            print(f"   {i}. {rec}")

    # Generate reports
    print(f"\n📄 Generating AI-powered intelligence reports...")

    reporter = ReportGenerator()
    investigation_data = {
        'investigation_id': result.get('investigation_id'),
        'objective': objective,
        'analysis': analysis,
        'processed_data': processed_data,
        'collection_results': result.get('collection_results'),
        'metadata': metadata
    }

    # Generate multiple format reports
    formats_generated = []
    for fmt in ['markdown', 'html', 'json']:
        try:
            reporter.generate_report(
                investigation_data,
                format=fmt,
                classification='UNCLASSIFIED',
                save=True
            )
            formats_generated.append(fmt.upper())
        except Exception as e:
            print(f"   ⚠️  Failed to generate {fmt} report: {e}")

    print(f"   ✓ Reports generated: {', '.join(formats_generated)}")
    print(f"   ✓ Saved to: data/reports/\n")

    # Show evaluation
    evaluation = result.get('evaluation', {})
    if evaluation:
        print(f"📈 AI Self-Evaluation:")
        print(f"   • Objective Achievement: {evaluation.get('objective_achievement', 'N/A')}%")
        print(f"   • Coverage: {evaluation.get('coverage', 'N/A')}%")
        print(f"   • Source Quality: {evaluation.get('source_quality', 'N/A')}/10")

    print(f"\n" + "=" * 80)
    print("✅ AUTONOMOUS AI INVESTIGATION SUCCESSFULLY COMPLETED")
    print("=" * 80)
    print(f"\nThe AI agent autonomously:")
    print(f"   ✓ Planned the investigation strategy")
    print(f"   ✓ Collected intelligence from {metadata.get('tools_used', 0)} sources")
    print(f"   ✓ Processed and analyzed {len(result.get('collection_results', []))} data points")
    print(f"   ✓ Generated {len(analysis.get('key_findings', []))} intelligence findings")
    print(f"   ✓ Created comprehensive reports in {len(formats_generated)} formats")
    print(f"   ✓ Evaluated its own performance")
    print(f"\n💡 All decisions were made autonomously by AI - zero manual intervention!\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Investigation interrupted by user")
    except Exception as e:
        print(f"\n❌ Investigation failed: {e}")
        import traceback
        traceback.print_exc()
