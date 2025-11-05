# 🗺️ Obsidian Canvas Integration Guide

## Overview

The OSINT Agent now includes **full integration with Obsidian Canvas** for creating interactive mind maps and knowledge graphs from your investigations!

### What is Obsidian Canvas?

Obsidian Canvas is an infinite canvas feature in Obsidian that lets you visually organize and connect your notes, creating mind maps and knowledge graphs. Perfect for visualizing complex OSINT investigations!

## 🎯 Features

### Automated Canvas Generation

The AI agent automatically generates **4 types of canvas visualizations**:

1. **Investigation Overview** - High-level summary with all key categories
2. **Entity Relationship Map** - Network graph of discovered entities
3. **Timeline** - Chronological event visualization
4. **Findings Hierarchy** - Findings organized by confidence level

### Visual Features

- **Color-Coded Nodes** - Different colors for different entity types and confidence levels
- **Automatic Layouts** - Radial, grid, and vertical layouts optimized for each canvas type
- **Interactive Connections** - Edges showing relationships between entities
- **Grouped Elements** - Visual grouping of related information
- **Rich Text** - Markdown formatting in nodes

## 🚀 Quick Start

### Method 1: Python API

```python
from src.agents.llm_client import create_llm_client
from src.agents.osint_agent import OSINTAgent
from src.memory.memory_store import MemoryStore
from src.tools.osint_tools import get_all_tools
from src.reporters.report_generator import ReportGenerator

# Run investigation
llm = create_llm_client()
agent = OSINTAgent(llm, get_all_tools(), MemoryStore())
result = await agent.investigate("Investigate example.com")

# Generate all canvas types
reporter = ReportGenerator()
investigation_data = {
    'investigation_id': result['investigation_id'],
    'objective': result['objective'],
    'analysis': result['analysis'],
    'processed_data': result['processed_data'],
    'collection_results': result['collection_results'],
    'metadata': result['metadata']
}

# Generate all canvases
reporter.generate_obsidian_canvas(investigation_data, canvas_type='all', save=True)
```

### Method 2: CLI

```bash
# Run investigation
python -m src.cli investigate "Investigate github.com"

# Generate canvas visualizations
python -m src.cli canvas <investigation_id> --type all

# Create Obsidian vault (first time only)
python -m src.cli create-vault
```

### Method 3: Example Script

```bash
# Run the comprehensive example
python examples/obsidian_canvas_generation.py
```

## 📊 Canvas Types Explained

### 1. Investigation Overview

**Purpose**: High-level summary of entire investigation

**Layout**: Radial layout with central investigation node

**Contains**:
- Central investigation node with ID and objective
- 6 category nodes:
  - Findings (count)
  - Entities (count)
  - Timeline Events (count)
  - Risk Indicators (count)
  - Recommendations (count)
  - Data Sources (count)
- Metadata node with investigation stats

**Best For**: Getting a quick overview of investigation scope

**Example**:
```
                    Findings (15)
                         |
    Data Sources (8) - INVESTIGATION - Entities (23)
                         |
                   Timeline (12)
```

### 2. Entity Relationship Map

**Purpose**: Visualize discovered entities and their connections

**Layout**: Radial layout around central investigation

**Contains**:
- Central investigation node
- Entity nodes (color-coded by type):
  - 🟢 Domains
  - 🔵 IP Addresses
  - 🟠 People
  - 🟣 Organizations
  - 🔴 Email Addresses
  - 🔷 URLs
  - 🟡 Phone Numbers
  - 🟤 Locations
  - 🩷 Usernames
- Relationship edges showing connections

**Best For**: Understanding entity networks and connections

**Example**:
```
     [Person] ----email_of----> [Email]
        |                          |
   works_at                   domain_of
        |                          |
        v                          v
 [Organization] <---owns--- [Domain]
```

### 3. Timeline Canvas

**Purpose**: Chronological visualization of events

**Layout**: Vertical timeline

**Contains**:
- Title node with investigation ID
- Event nodes in chronological order
- Sequential connections between events
- Date and description for each event

**Best For**: Understanding sequence and chronology

**Example**:
```
  [Investigation Timeline]
            |
    [2024-01-15: Event 1]
            |
    [2024-01-20: Event 2]
            |
    [2024-01-25: Event 3]
```

### 4. Findings Hierarchy

**Purpose**: Organize findings by confidence level

**Layout**: Grouped by confidence

**Contains**:
- Central investigation node
- Confidence level groups:
  - 🟢 Very High Confidence
  - 🟢 High Confidence
  - 🟠 Medium Confidence
  - 🔴 Low Confidence
  - 🔴 Very Low Confidence
- Finding nodes within each group

**Best For**: Prioritizing and validating findings

**Example**:
```
[INVESTIGATION]
      |
      +--- [VERY HIGH Confidence] ---+--- [Finding 1]
      |                               +--- [Finding 2]
      |
      +--- [HIGH Confidence] ---------+--- [Finding 3]
      |
      +--- [MEDIUM Confidence] -------+--- [Finding 4]
```

## 🎨 Color Coding

### Entity Types

| Entity Type   | Color      | Hex Code |
|---------------|------------|----------|
| Domain        | Green      | #4CAF50  |
| IP Address    | Blue       | #2196F3  |
| Person        | Orange     | #FF9800  |
| Organization  | Purple     | #9C27B0  |
| Email         | Red        | #F44336  |
| URL           | Cyan       | #00BCD4  |
| Phone         | Yellow     | #FFEB3B  |
| Location      | Brown      | #795548  |
| Username      | Pink       | #E91E63  |
| Finding       | Blue Grey  | #607D8B  |
| Risk          | Dark Red   | #D32F2F  |
| Event         | Dark Blue  | #1976D2  |
| Tool          | Dark Green | #388E3C  |

### Confidence Levels

| Confidence | Color      | Hex Code |
|------------|------------|----------|
| Very High  | Dark Green | #1B5E20  |
| High       | Green      | #43A047  |
| Medium     | Orange     | #FFA726  |
| Low        | Light Red  | #EF5350  |
| Very Low   | Dark Red   | #C62828  |
| Unknown    | Grey       | #9E9E9E  |

## 📂 File Structure

When you generate canvases, they're saved in this structure:

```
data/
└── obsidian_vault/           # Obsidian vault root
    ├── .obsidian/            # Obsidian configuration
    ├── Investigations/       # Investigation notes (future)
    ├── Entities/             # Entity notes (future)
    ├── Reports/              # Text reports (future)
    └── Canvases/             # Canvas files
        ├── <inv_id>_<timestamp>_overview.canvas
        ├── <inv_id>_<timestamp>_entity_map.canvas
        ├── <inv_id>_<timestamp>_timeline.canvas
        └── <inv_id>_<timestamp>_findings.canvas
```

## 🔧 Advanced Usage

### Generate Specific Canvas Types

```python
from src.reporters.report_generator import ReportGenerator

reporter = ReportGenerator()

# Generate only overview
reporter.generate_obsidian_canvas(data, canvas_type='overview')

# Generate only entity map
reporter.generate_obsidian_canvas(data, canvas_type='entity_map')

# Generate only timeline
reporter.generate_obsidian_canvas(data, canvas_type='timeline')

# Generate only findings
reporter.generate_obsidian_canvas(data, canvas_type='findings')

# Generate all types
reporter.generate_obsidian_canvas(data, canvas_type='all')
```

### Custom Canvas Generator

```python
from src.reporters.obsidian_canvas import ObsidianCanvasGenerator

# Create custom generator with custom output directory
canvas_gen = ObsidianCanvasGenerator(output_dir='./my_canvases')

# Generate with custom layout
entity_json = canvas_gen.generate_entity_map(data, layout='radial')  # or 'grid'

# Save canvas
canvas_gen.save_canvas(entity_json, 'my_custom_canvas')
```

### Create Obsidian Vault

```python
from src.reporters.obsidian_canvas import create_obsidian_vault_structure

# Create vault at custom location
vault_path = create_obsidian_vault_structure('./my_osint_vault')
```

## 📖 How to View Canvases

### Step 1: Install Obsidian

1. Download from https://obsidian.md/
2. Install for your platform (Windows, Mac, Linux)
3. Launch Obsidian

### Step 2: Open Vault

1. In Obsidian, click "Open folder as vault"
2. Navigate to `data/obsidian_vault/`
3. Select the folder and click "Open"

### Step 3: View Canvases

1. In left sidebar, expand "Canvases" folder
2. Click on any `.canvas` file
3. The interactive mind map opens in the main view

### Step 4: Interact with Canvas

**Navigation:**
- **Zoom**: Mouse wheel or trackpad pinch
- **Pan**: Click and drag on empty space
- **Select**: Click on nodes or edges

**Editing:**
- **Move nodes**: Drag nodes to rearrange
- **Edit text**: Double-click on text nodes
- **Add notes**: Right-click → Add note
- **Create connections**: Drag from node edge to another node
- **Change colors**: Right-click node → Change color

**Viewing:**
- **Zoom to fit**: Click zoom-to-fit button in toolbar
- **Fullscreen**: Click fullscreen button
- **Export**: File → Export as PNG/SVG

## 🎯 Use Cases

### 1. Threat Intelligence Analysis

Generate entity maps to visualize:
- Attack infrastructure (domains, IPs)
- Threat actor connections
- Malware distribution networks
- Command and control infrastructure

### 2. Corporate Investigation

Use timelines and entity maps for:
- Corporate structure analysis
- M&A intelligence
- Competitive analysis
- Due diligence visualization

### 3. Person of Interest

Create comprehensive profiles with:
- Social media connections
- Employment history timeline
- Associated entities (people, orgs, locations)
- Digital footprint mapping

### 4. Domain/Infrastructure Analysis

Visualize:
- DNS relationships
- Subdomain structure
- Associated IPs and services
- Certificate chains
- Hosting relationships

### 5. Incident Investigation

Track incidents with:
- Chronological timeline of events
- Entity involvement
- Risk assessment
- Evidence correlation

## 💡 Tips & Best Practices

### Canvas Organization

1. **Start with Overview** - Get the big picture first
2. **Drill into Entity Map** - Understand connections
3. **Review Timeline** - Understand chronology
4. **Validate with Findings** - Check confidence levels

### Customization

1. **Rearrange Nodes** - Organize visually for your workflow
2. **Add Annotations** - Double-click nodes to add notes
3. **Color-Code** - Use colors to highlight important items
4. **Create Groups** - Manually group related nodes
5. **Add Links** - Connect to other Obsidian notes

### Integration

1. **Link to Reports** - Create links from canvas to full reports
2. **Cross-Reference** - Link canvases from different investigations
3. **Tag Entities** - Use Obsidian tags for easy searching
4. **Create Indexes** - Build master canvases linking to others

### Performance

1. **Large Investigations** - Consider generating specific canvas types
2. **Many Entities** - Use grid layout instead of radial
3. **Export Static** - Export as PNG for sharing
4. **Version Control** - Canvas files are JSON, can be Git-tracked

## 🔌 Integration Workflow

### Automated Investigation with Canvas

```python
async def investigate_with_canvas(objective):
    # 1. Run AI investigation
    agent = OSINTAgent(llm, tools, memory)
    result = await agent.investigate(objective)

    # 2. Generate standard reports
    reporter = ReportGenerator()
    reporter.generate_report(data, format='markdown')
    reporter.generate_report(data, format='html')
    reporter.generate_report(data, format='json')

    # 3. Generate Obsidian canvases
    reporter.generate_obsidian_canvas(data, canvas_type='all')

    # 4. Open in Obsidian (manual)
    print("View canvases in Obsidian at: data/obsidian_vault/Canvases/")
```

### Continuous Monitoring with Canvas Updates

```python
async def monitor_with_canvas(target, interval=3600):
    orchestrator = WorkflowOrchestrator(agent, memory)

    # Create monitoring workflow
    workflow_id = await orchestrator.create_workflow(
        name=f"monitor_{target}",
        workflow_type=WorkflowType.CONTINUOUS,
        objective=f"Monitor {target} for changes"
    )

    # Custom callback to generate canvas on each check
    async def on_investigation_complete(result):
        reporter = ReportGenerator()
        reporter.generate_obsidian_canvas(result, canvas_type='all')
        print("Canvas updated in Obsidian!")

    # Run monitoring
    await orchestrator.continuous_monitoring(workflow_id, check_interval=interval)
```

## 📚 References

- **Obsidian**: https://obsidian.md/
- **Canvas Documentation**: https://help.obsidian.md/Plugins/Canvas
- **Canvas File Format**: https://jsoncanvas.org/

## 🆘 Troubleshooting

### Canvases not appearing in Obsidian

1. Check vault path is correct: `data/obsidian_vault/`
2. Ensure Canvases folder exists
3. Refresh Obsidian file explorer (Ctrl/Cmd + R)
4. Check .canvas files were created in filesystem

### Nodes overlapping

- Use zoom controls to zoom out
- Switch to grid layout: `layout='grid'`
- Manually rearrange nodes in Obsidian

### Colors not showing

- Colors are set in canvas JSON
- Some Obsidian themes may override colors
- Check Obsidian appearance settings

### Canvas file won't open

- Ensure Obsidian is updated to latest version
- Check .canvas file is valid JSON
- Try opening in text editor to verify format

## 🎉 Examples

See the comprehensive example:
```bash
python examples/obsidian_canvas_generation.py
```

This will:
1. Run an AI-powered investigation
2. Generate all 4 canvas types
3. Create Obsidian vault structure
4. Save canvases ready for viewing
5. Show you how to open in Obsidian

---

**Now your OSINT investigations come with beautiful, interactive mind maps!** 🗺️✨
