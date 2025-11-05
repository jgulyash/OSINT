"""
Command Line Interface for AI-Powered OSINT Agent

Provides interactive and automated investigation capabilities
"""

import asyncio
import click
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown
from rich import print as rprint

# Import OSINT components
from src.agents.llm_client import create_llm_client
from src.agents.osint_agent import OSINTAgent
from src.agents.workflow_orchestrator import WorkflowOrchestrator, WorkflowType
from src.memory.memory_store import MemoryStore
from src.reporters.report_generator import ReportGenerator
from src.tools.osint_tools import get_all_tools

console = Console()


def load_env():
    """Load environment variables from .env file"""
    try:
        from dotenv import load_dotenv
        env_path = Path(__file__).parent.parent / '.env'
        if env_path.exists():
            load_dotenv(env_path)
            console.print("[green]✓[/green] Loaded environment configuration")
        else:
            console.print("[yellow]![/yellow] No .env file found. Using defaults or environment variables.")
    except ImportError:
        console.print("[yellow]![/yellow] python-dotenv not installed. Set environment variables manually.")


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """
    🔍 AI-Powered OSINT Intelligence Agent

    Autonomous open source intelligence gathering and analysis using AI.
    """
    load_env()


@cli.command()
@click.argument('objective')
@click.option('--format', '-f', default='markdown', type=click.Choice(['markdown', 'html', 'json', 'csv']),
              help='Report output format')
@click.option('--max-iterations', '-i', default=15, type=int, help='Maximum investigation iterations')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--classification', '-c', default='UNCLASSIFIED', help='Classification level')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def investigate(objective: str, format: str, max_iterations: int, output: Optional[str],
                classification: str, verbose: bool):
    """
    🔍 Run an AI-powered OSINT investigation

    OBJECTIVE: Investigation question or target

    Example:
        osint investigate "Investigate the domain example.com for security intelligence"
    """
    console.print(Panel.fit(
        f"[bold cyan]AI-Powered OSINT Investigation[/bold cyan]\n\n"
        f"[yellow]Objective:[/yellow] {objective}\n"
        f"[yellow]Max Iterations:[/yellow] {max_iterations}\n"
        f"[yellow]Report Format:[/yellow] {format}",
        title="🔍 Investigation Starting",
        border_style="cyan"
    ))

    async def run_investigation():
        # Initialize components
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Initializing AI-powered agent...", total=None)

            # Create LLM client
            llm_client = create_llm_client()

            # Create memory store
            memory = MemoryStore()

            # Get OSINT tools
            tools = get_all_tools()

            # Create agent
            config = {'max_iterations': max_iterations}
            agent = OSINTAgent(llm_client, tools, memory, config)

            # Create investigation
            await memory.create_investigation(
                agent.generate_investigation_id(objective),
                objective
            )

            progress.update(task, description="[green]✓ Agent initialized")

        console.print("\n[bold green]Starting autonomous investigation...[/bold green]\n")

        try:
            # Run investigation
            result = await agent.investigate(objective=objective, auto_report=True)

            console.print("\n[bold green]✓ Investigation completed![/bold green]\n")

            # Display summary
            display_investigation_summary(result)

            # Generate and save report
            if result.get('report'):
                save_report(result, format, output, classification)

            return result

        except Exception as e:
            console.print(f"\n[bold red]✗ Investigation failed:[/bold red] {e}")
            if verbose:
                console.print_exception()
            sys.exit(1)

    asyncio.run(run_investigation())


@cli.command()
@click.argument('name')
@click.argument('objective')
@click.option('--type', '-t', type=click.Choice(['one_time', 'scheduled', 'continuous']),
              default='one_time', help='Workflow type')
@click.option('--interval', '-i', type=int, help='Check interval in seconds (for continuous monitoring)')
@click.option('--schedule', '-s', help='Schedule configuration (e.g., "daily at 09:00")')
def workflow(name: str, objective: str, type: str, interval: Optional[int], schedule: Optional[str]):
    """
    🔄 Create and run automated OSINT workflows

    NAME: Workflow name
    OBJECTIVE: Investigation objective

    Example:
        osint workflow "daily-threat-check" "Monitor example.com for threats" --type continuous --interval 3600
    """
    async def run_workflow():
        # Initialize components
        llm_client = create_llm_client()
        memory = MemoryStore()
        tools = get_all_tools()
        agent = OSINTAgent(llm_client, tools, memory)

        # Create orchestrator
        orchestrator = WorkflowOrchestrator(agent, memory)

        # Create workflow
        workflow_type = WorkflowType(type)
        schedule_config = {'interval': schedule} if schedule else {}

        workflow_id = await orchestrator.create_workflow(
            name=name,
            workflow_type=workflow_type,
            objective=objective,
            schedule_config=schedule_config
        )

        console.print(f"[green]✓[/green] Workflow created: {workflow_id}")

        # Execute based on type
        if type == 'one_time':
            console.print("\n[cyan]Executing one-time workflow...[/cyan]")
            result = await orchestrator.execute_workflow(workflow_id)
            console.print("[green]✓[/green] Workflow completed!")

        elif type == 'continuous':
            console.print(f"\n[cyan]Starting continuous monitoring (interval: {interval}s)...[/cyan]")
            console.print("[yellow]Press Ctrl+C to stop[/yellow]\n")
            await orchestrator.continuous_monitoring(workflow_id, check_interval=interval or 300)

        elif type == 'scheduled':
            console.print(f"\n[cyan]Scheduling workflow: {schedule}[/cyan]")
            await orchestrator.schedule_workflow(workflow_id)
            console.print("[green]✓[/green] Workflow scheduled!")

    try:
        asyncio.run(run_workflow())
    except KeyboardInterrupt:
        console.print("\n[yellow]Workflow stopped by user[/yellow]")


@cli.command()
@click.argument('targets', nargs=-1, required=True)
@click.option('--objective-template', '-t', required=True,
              help='Objective template with {target} placeholder')
@click.option('--parallel', '-p', is_flag=True, help='Run investigations in parallel')
@click.option('--output-dir', '-o', type=click.Path(), help='Output directory for reports')
def campaign(targets, objective_template: str, parallel: bool, output_dir: Optional[str]):
    """
    🎯 Run multi-target investigation campaign

    TARGETS: Space-separated list of targets

    Example:
        osint campaign example.com target.org --objective-template "Investigate {target} for security issues"
    """
    async def run_campaign():
        console.print(Panel.fit(
            f"[bold cyan]Multi-Target Campaign[/bold cyan]\n\n"
            f"[yellow]Targets:[/yellow] {len(targets)}\n"
            f"[yellow]Mode:[/yellow] {'Parallel' if parallel else 'Sequential'}\n"
            f"[yellow]Template:[/yellow] {objective_template}",
            title="🎯 Campaign Starting",
            border_style="cyan"
        ))

        # Initialize
        llm_client = create_llm_client()
        memory = MemoryStore()
        tools = get_all_tools()
        agent = OSINTAgent(llm_client, tools, memory)
        orchestrator = WorkflowOrchestrator(agent, memory)

        # Prepare targets
        target_list = [{'name': t} for t in targets]

        # Run campaign
        result = await orchestrator.run_campaign(
            campaign_name=f"campaign_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            targets=target_list,
            objective_template=objective_template,
            parallel=parallel
        )

        # Display results
        console.print(f"\n[bold green]✓ Campaign completed![/bold green]")
        console.print(f"Successful: {result['completed']}/{len(targets)}")
        console.print(f"Failed: {result['failed']}/{len(targets)}")

        # Save campaign results
        if output_dir:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)

            campaign_file = output_path / f"campaign_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(campaign_file, 'w') as f:
                json.dump(result, f, indent=2, default=str)

            console.print(f"\n[green]Campaign results saved to:[/green] {campaign_file}")

    asyncio.run(run_campaign())


@cli.command()
@click.option('--limit', '-l', default=20, type=int, help='Number of investigations to show')
def history(limit: int):
    """
    📜 View investigation history
    """
    async def show_history():
        memory = MemoryStore()
        investigations = await memory.list_investigations(limit=limit)

        if not investigations:
            console.print("[yellow]No investigations found[/yellow]")
            return

        table = Table(title="Investigation History")
        table.add_column("ID", style="cyan")
        table.add_column("Objective", style="white")
        table.add_column("Status", style="green")
        table.add_column("Created", style="yellow")

        for inv in investigations:
            table.add_row(
                inv['id'][:12],
                inv['objective'][:50] + ('...' if len(inv['objective']) > 50 else ''),
                inv['status'],
                inv['created_at'][:19]
            )

        console.print(table)

    asyncio.run(show_history())


@cli.command()
@click.argument('investigation_id')
def report(investigation_id: str):
    """
    📄 Generate report for an investigation

    INVESTIGATION_ID: Investigation ID to report on
    """
    async def generate_report():
        memory = MemoryStore()

        # Get investigation data
        summary = await memory.get_investigation_summary(investigation_id)

        if not summary:
            console.print(f"[red]Investigation {investigation_id} not found[/red]")
            return

        # Export investigation
        data_str = await memory.export_investigation(investigation_id, format='json')
        data = json.loads(data_str)

        # Generate report
        reporter = ReportGenerator()
        report_content = reporter.generate_report(data, format='markdown', save=True)

        # Display report
        console.print(Panel(
            Markdown(report_content),
            title=f"Investigation Report: {investigation_id[:12]}",
            border_style="green"
        ))

    asyncio.run(generate_report())


@cli.command()
def tools():
    """
    🛠️  List available OSINT tools
    """
    from src.tools.osint_tools import get_tool_descriptions

    tool_descriptions = get_tool_descriptions()

    table = Table(title="Available OSINT Tools", show_lines=True)
    table.add_column("Tool", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")

    for tool_name, description in sorted(tool_descriptions.items()):
        table.add_row(tool_name, description)

    console.print(table)
    console.print(f"\n[green]Total tools available:[/green] {len(tool_descriptions)}")


@cli.command()
def config():
    """
    ⚙️  Show current configuration
    """
    console.print(Panel.fit(
        "[bold cyan]OSINT Agent Configuration[/bold cyan]",
        border_style="cyan"
    ))

    # Check environment
    config_items = [
        ("LLM Provider", os.getenv('DEFAULT_LLM_PROVIDER', 'openai')),
        ("OpenAI API Key", "✓ Set" if os.getenv('OPENAI_API_KEY') else "✗ Not set"),
        ("Anthropic API Key", "✓ Set" if os.getenv('ANTHROPIC_API_KEY') else "✗ Not set"),
        ("Database Path", os.getenv('DATABASE_PATH', 'data/osint_memory.db')),
        ("Reports Directory", os.getenv('REPORTS_DIR', 'data/reports')),
    ]

    table = Table(show_header=False)
    table.add_column("Setting", style="yellow")
    table.add_column("Value", style="white")

    for key, value in config_items:
        table.add_row(key, value)

    console.print(table)


@cli.command()
@click.option('--check-all', '-a', is_flag=True, help='Check all components')
def health(check_all: bool):
    """
    🏥 Health check for OSINT agent
    """
    console.print("[bold cyan]Running health check...[/bold cyan]\n")

    checks = []

    # Check LLM client
    try:
        llm_client = create_llm_client()
        checks.append(("LLM Client", True, llm_client.get_model_info()['model']))
    except Exception as e:
        checks.append(("LLM Client", False, str(e)))

    # Check memory store
    try:
        memory = MemoryStore()
        checks.append(("Memory Store", True, "Connected"))
    except Exception as e:
        checks.append(("Memory Store", False, str(e)))

    # Check tools
    try:
        tools = get_all_tools()
        checks.append(("OSINT Tools", True, f"{len(tools)} tools available"))
    except Exception as e:
        checks.append(("OSINT Tools", False, str(e)))

    # Display results
    table = Table(title="Health Check Results")
    table.add_column("Component", style="cyan")
    table.add_column("Status", style="white")
    table.add_column("Details", style="yellow")

    for component, status, details in checks:
        status_icon = "[green]✓[/green]" if status else "[red]✗[/red]"
        table.add_row(component, status_icon, details)

    console.print(table)

    # Overall status
    all_passed = all(check[1] for check in checks)
    if all_passed:
        console.print("\n[bold green]All systems operational![/bold green]")
    else:
        console.print("\n[bold red]Some components need attention![/bold red]")
        sys.exit(1)


def display_investigation_summary(result: dict):
    """Display investigation summary"""
    metadata = result.get('metadata', {})
    analysis = result.get('analysis', {})

    summary_text = f"""
[bold]Investigation Summary[/bold]

[cyan]Investigation ID:[/cyan] {result.get('investigation_id', 'N/A')}
[cyan]Duration:[/cyan] {metadata.get('duration_seconds', 0):.2f} seconds
[cyan]Iterations:[/cyan] {metadata.get('iterations', 0)}
[cyan]Tools Used:[/cyan] {metadata.get('tools_used', 0)}

[bold yellow]Key Findings:[/bold yellow] {len(analysis.get('key_findings', []))}
[bold yellow]Entities Identified:[/bold yellow] {len(result.get('processed_data', {}).get('entities', []))}
[bold yellow]Relationships:[/bold yellow] {len(result.get('processed_data', {}).get('relationships', []))}
"""

    console.print(Panel(summary_text, title="Investigation Complete", border_style="green"))


def save_report(result: dict, format: str, output: Optional[str], classification: str):
    """Save investigation report"""
    reporter = ReportGenerator()

    investigation_data = {
        'investigation_id': result.get('investigation_id'),
        'objective': result.get('objective'),
        'analysis': result.get('analysis'),
        'processed_data': result.get('processed_data'),
        'collection_results': result.get('collection_results'),
        'metadata': result.get('metadata')
    }

    report = reporter.generate_report(
        investigation_data,
        format=format,
        classification=classification,
        save=output is None
    )

    if output:
        with open(output, 'w') as f:
            f.write(report)
        console.print(f"\n[green]Report saved to:[/green] {output}")
    else:
        console.print(f"\n[green]Report saved to:[/green] data/reports/")


if __name__ == '__main__':
    cli()
