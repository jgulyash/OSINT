"""
OSINT Agent - Autonomous Intelligence Collection and Analysis

This agent implements the complete intelligence lifecycle:
1. Planning & Direction
2. Collection
3. Processing
4. Analysis
5. Dissemination
6. Feedback
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional, Callable
from enum import Enum
import hashlib


class IntelligencePhase(Enum):
    """Intelligence lifecycle phases"""
    PLANNING = "planning"
    COLLECTION = "collection"
    PROCESSING = "processing"
    ANALYSIS = "analysis"
    DISSEMINATION = "dissemination"
    FEEDBACK = "feedback"


class ConfidenceLevel(Enum):
    """Confidence levels for intelligence findings"""
    VERY_HIGH = "very_high"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    VERY_LOW = "very_low"


class OSINTAgent:
    """
    Autonomous OSINT Investigation Agent implementing the intelligence lifecycle
    """

    def __init__(
        self,
        llm_client,
        tools: List[Callable],
        memory_store,
        config: Optional[Dict] = None
    ):
        """
        Initialize the OSINT agent

        Args:
            llm_client: LLM API client (OpenAI/Anthropic/etc)
            tools: List of callable OSINT tools
            memory_store: Memory/database instance for persistence
            config: Optional configuration dictionary
        """
        self.llm = llm_client
        self.tools = {tool.__name__: tool for tool in tools}
        self.memory = memory_store
        self.config = config or {}

        # Investigation state
        self.objective = None
        self.current_phase = None
        self.investigation_id = None
        self.max_iterations = self.config.get('max_iterations', 15)
        self.min_confidence = self.config.get('min_confidence', 0.6)

        # Logging
        self.logger = logging.getLogger('OSINTAgent')
        self.setup_logging()

    def setup_logging(self):
        """Configure logging for the agent"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def generate_investigation_id(self, objective: str) -> str:
        """Generate unique investigation ID"""
        timestamp = datetime.now().isoformat()
        hash_input = f"{objective}{timestamp}".encode()
        return hashlib.md5(hash_input).hexdigest()[:12]

    async def log_action(self, action: str, data: Any, phase: IntelligencePhase):
        """
        Log action to memory store

        Args:
            action: Action name/type
            data: Action data
            phase: Current intelligence phase
        """
        entry = {
            'investigation_id': self.investigation_id,
            'timestamp': datetime.now().isoformat(),
            'phase': phase.value,
            'action': action,
            'data': data
        }

        await self.memory.store(entry)
        self.logger.info(f"[{phase.value}] {action}")

    # ==================== PHASE 1: PLANNING & DIRECTION ====================

    async def plan_investigation(self, objective: str, constraints: Optional[Dict] = None) -> Dict:
        """
        Phase 1: Planning & Direction

        Create comprehensive investigation plan based on objective

        Args:
            objective: Investigation objective/question
            constraints: Optional constraints (time, scope, sources, etc.)

        Returns:
            Investigation plan with strategy and actions
        """
        self.current_phase = IntelligencePhase.PLANNING
        self.objective = objective
        self.investigation_id = self.generate_investigation_id(objective)

        self.logger.info(f"Investigation ID: {self.investigation_id}")
        self.logger.info(f"Objective: {objective}")

        constraints_text = ""
        if constraints:
            constraints_text = f"\n\nCONSTRAINTS:\n{json.dumps(constraints, indent=2)}"

        planning_prompt = f"""You are an expert OSINT analyst creating an investigation plan.

OBJECTIVE: {objective}{constraints_text}

AVAILABLE TOOLS:
{self._format_tools_description()}

Create a comprehensive investigation plan that follows the intelligence lifecycle:

1. **Information Requirements**: What specific information do we need?
2. **Collection Strategy**: Which sources and tools to use, in what order?
3. **Priority Actions**: 8-12 specific actions with:
   - Tool to use
   - Specific query/parameters
   - Expected intelligence value
   - Dependencies (if any)
4. **Success Criteria**: How will we know we have sufficient intelligence?
5. **Risk Assessment**: What are the potential challenges or limitations?

Output as structured JSON with keys: information_requirements, collection_strategy, actions, success_criteria, risk_assessment
"""

        try:
            response = await self.llm.complete(planning_prompt)
            plan = json.loads(response)

            # Add metadata
            plan['investigation_id'] = self.investigation_id
            plan['objective'] = objective
            plan['created_at'] = datetime.now().isoformat()

            await self.log_action("investigation_planned", plan, IntelligencePhase.PLANNING)

            return plan

        except Exception as e:
            self.logger.error(f"Planning failed: {e}")
            # Fallback to basic plan
            return self._create_fallback_plan(objective)

    def _format_tools_description(self) -> str:
        """Format available tools for LLM context"""
        descriptions = []
        for name, tool in self.tools.items():
            doc = tool.__doc__ or "No description"
            descriptions.append(f"- {name}: {doc.strip()}")
        return "\n".join(descriptions)

    def _create_fallback_plan(self, objective: str) -> Dict:
        """Create basic fallback plan if LLM planning fails"""
        return {
            'investigation_id': self.investigation_id,
            'objective': objective,
            'information_requirements': ["General information about the target"],
            'collection_strategy': "Sequential execution of available tools",
            'actions': [
                {
                    'tool': list(self.tools.keys())[0] if self.tools else 'none',
                    'parameters': {'query': objective},
                    'priority': 1
                }
            ],
            'success_criteria': ["Gather basic information"],
            'risk_assessment': "Limited plan due to planning error",
            'created_at': datetime.now().isoformat()
        }

    # ==================== PHASE 2: COLLECTION ====================

    async def execute_action(self, action: Dict) -> Dict:
        """
        Execute a single collection action using appropriate tool

        Args:
            action: Action dict with tool, parameters, etc.

        Returns:
            Result from tool execution with metadata
        """
        self.current_phase = IntelligencePhase.COLLECTION

        tool_name = action.get('tool')
        parameters = action.get('parameters', {})

        if tool_name not in self.tools:
            error_result = {
                "success": False,
                "error": f"Tool '{tool_name}' not available",
                "tool": tool_name
            }
            await self.log_action(f"collection_error_{tool_name}", error_result, IntelligencePhase.COLLECTION)
            return error_result

        try:
            self.logger.info(f"Executing: {tool_name} with {parameters}")

            tool = self.tools[tool_name]
            result = await tool(**parameters)

            execution_result = {
                "success": True,
                "tool": tool_name,
                "parameters": parameters,
                "data": result,
                "timestamp": datetime.now().isoformat()
            }

            await self.log_action(f"collection_{tool_name}", execution_result, IntelligencePhase.COLLECTION)

            return execution_result

        except Exception as e:
            self.logger.error(f"Tool execution error ({tool_name}): {e}")
            error_result = {
                "success": False,
                "tool": tool_name,
                "parameters": parameters,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            await self.log_action(f"collection_error_{tool_name}", error_result, IntelligencePhase.COLLECTION)
            return error_result

    async def collect_intelligence(self, actions: List[Dict]) -> List[Dict]:
        """
        Execute multiple collection actions

        Args:
            actions: List of actions to execute

        Returns:
            List of results from all actions
        """
        self.current_phase = IntelligencePhase.COLLECTION
        results = []

        for i, action in enumerate(actions):
            self.logger.info(f"Collection action {i+1}/{len(actions)}")
            result = await self.execute_action(action)
            results.append(result)

            # Small delay to be respectful to APIs
            await asyncio.sleep(0.5)

        return results

    # ==================== PHASE 3: PROCESSING ====================

    async def process_raw_data(self, raw_results: List[Dict]) -> Dict:
        """
        Phase 3: Processing

        Clean, normalize, and structure raw collection results

        Args:
            raw_results: Raw results from collection phase

        Returns:
            Processed and structured data
        """
        self.current_phase = IntelligencePhase.PROCESSING

        processing_prompt = f"""You are processing raw OSINT collection data.

OBJECTIVE: {self.objective}

RAW COLLECTION RESULTS:
{json.dumps(raw_results, indent=2, default=str)}

Process this data by:
1. **Extracting** key information relevant to the objective
2. **Normalizing** data formats (dates, locations, names, etc.)
3. **Deduplicating** redundant information
4. **Categorizing** findings by type (entities, events, relationships, etc.)
5. **Cross-referencing** information from multiple sources
6. **Identifying** data quality issues or gaps

Output as structured JSON with keys: entities, events, relationships, metadata, data_quality_notes
"""

        try:
            response = await self.llm.complete(processing_prompt)
            processed = json.loads(response)

            processed['processing_timestamp'] = datetime.now().isoformat()
            processed['sources_processed'] = len(raw_results)

            await self.log_action("data_processed", processed, IntelligencePhase.PROCESSING)

            return processed

        except Exception as e:
            self.logger.error(f"Processing failed: {e}")
            # Return raw data if processing fails
            return {
                "entities": [],
                "events": [],
                "relationships": [],
                "metadata": {"error": str(e), "raw_count": len(raw_results)},
                "data_quality_notes": ["Processing failed, raw data preserved"]
            }

    # ==================== PHASE 4: ANALYSIS ====================

    async def analyze_intelligence(self, processed_data: Dict, context: Optional[Dict] = None) -> Dict:
        """
        Phase 4: Analysis

        Synthesize processed data into actionable intelligence

        Args:
            processed_data: Processed data from previous phase
            context: Optional additional context

        Returns:
            Intelligence analysis with findings, insights, and assessments
        """
        self.current_phase = IntelligencePhase.ANALYSIS

        # Retrieve investigation history for context
        history = await self.memory.get_by_investigation(self.investigation_id)

        context_text = ""
        if context:
            context_text = f"\n\nADDITIONAL CONTEXT:\n{json.dumps(context, indent=2)}"

        analysis_prompt = f"""You are an expert intelligence analyst. Analyze the processed OSINT data.

OBJECTIVE: {self.objective}

PROCESSED DATA:
{json.dumps(processed_data, indent=2, default=str)}

INVESTIGATION HISTORY:
{json.dumps(history[-10:], indent=2, default=str) if history else "None"}{context_text}

Provide comprehensive analysis:

1. **Key Findings**: Most important discoveries (ranked by significance)
2. **Insights**: What does this tell us? What patterns emerge?
3. **Confidence Assessment**: How reliable is each finding? (very_high, high, medium, low, very_low)
4. **Gaps & Limitations**: What don't we know? What couldn't be verified?
5. **Contradictions**: Any conflicting information?
6. **Risk Indicators**: Red flags, warnings, or concerns
7. **Network Analysis**: Relationships and connections found
8. **Timeline**: Chronological sequence of relevant events
9. **Attribution**: Source reliability and credibility assessment
10. **Recommendations**: What actions or further investigation needed?

For each finding, provide:
- Description
- Evidence (source references)
- Confidence level
- Significance (high/medium/low)

Output as structured JSON.
"""

        try:
            response = await self.llm.complete(analysis_prompt)
            analysis = json.loads(response)

            # Add metadata
            analysis['analysis_timestamp'] = datetime.now().isoformat()
            analysis['investigation_id'] = self.investigation_id
            analysis['analyst'] = 'OSINTAgent'

            await self.log_action("intelligence_analyzed", analysis, IntelligencePhase.ANALYSIS)

            return analysis

        except Exception as e:
            self.logger.error(f"Analysis failed: {e}")
            return self._create_fallback_analysis(processed_data)

    def _create_fallback_analysis(self, processed_data: Dict) -> Dict:
        """Create basic analysis if LLM analysis fails"""
        return {
            'key_findings': ["Analysis limited due to processing error"],
            'insights': [],
            'confidence_assessment': {"overall": "low"},
            'gaps': ["Full analysis unavailable"],
            'recommendations': ["Manual review recommended"],
            'analysis_timestamp': datetime.now().isoformat()
        }

    # ==================== PHASE 5: DISSEMINATION ====================

    async def generate_report(
        self,
        analysis: Dict,
        format: str = 'markdown',
        classification: str = 'UNCLASSIFIED'
    ) -> str:
        """
        Phase 5: Dissemination

        Generate intelligence report for stakeholders

        Args:
            analysis: Analysis results
            format: Output format (markdown, json, html)
            classification: Classification level

        Returns:
            Formatted intelligence report
        """
        self.current_phase = IntelligencePhase.DISSEMINATION

        if format == 'json':
            report = json.dumps(analysis, indent=2, default=str)
        else:
            report_prompt = f"""Generate a professional intelligence report.

CLASSIFICATION: {classification}
OBJECTIVE: {self.objective}
INVESTIGATION ID: {self.investigation_id}

ANALYSIS:
{json.dumps(analysis, indent=2, default=str)}

Create a comprehensive report in {format} format with:

1. **Header**: Classification, date, investigation ID
2. **Executive Summary**: 2-3 paragraphs for decision-makers
3. **Objective**: What was investigated and why
4. **Methodology**: Sources and techniques used
5. **Key Findings**: Most important discoveries (bullet points)
6. **Detailed Analysis**: In-depth examination of findings
7. **Evidence**: Supporting data and sources
8. **Confidence Assessment**: Reliability of intelligence
9. **Gaps & Limitations**: What's unknown or uncertain
10. **Recommendations**: Suggested actions or further investigation
11. **Timeline**: If relevant events occurred over time
12. **Appendices**: Additional data, sources, methodology notes

Use clear, professional intelligence report style.
Format for readability with proper headings and structure.
"""

            try:
                report = await self.llm.complete(report_prompt)
            except Exception as e:
                self.logger.error(f"Report generation failed: {e}")
                report = self._create_fallback_report(analysis, format)

        # Save report
        report_data = {
            'report': report,
            'format': format,
            'classification': classification,
            'generated_at': datetime.now().isoformat()
        }

        await self.log_action("report_generated", report_data, IntelligencePhase.DISSEMINATION)

        return report

    def _create_fallback_report(self, analysis: Dict, format: str) -> str:
        """Create basic report if generation fails"""
        if format == 'json':
            return json.dumps(analysis, indent=2, default=str)
        else:
            return f"""# OSINT Investigation Report

**Investigation ID**: {self.investigation_id}
**Objective**: {self.objective}
**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary

Investigation completed with limited analysis due to processing constraints.

## Raw Analysis Data

```json
{json.dumps(analysis, indent=2, default=str)}
```

## Note

Full report generation encountered an error. Please review the raw analysis data above.
"""

    # ==================== PHASE 6: FEEDBACK ====================

    async def evaluate_investigation(self) -> Dict:
        """
        Phase 6: Feedback

        Evaluate investigation effectiveness and quality

        Returns:
            Evaluation metrics and improvement suggestions
        """
        self.current_phase = IntelligencePhase.FEEDBACK

        # Retrieve complete investigation history
        history = await self.memory.get_by_investigation(self.investigation_id)

        evaluation_prompt = f"""Evaluate this OSINT investigation for quality and effectiveness.

OBJECTIVE: {self.objective}
INVESTIGATION ID: {self.investigation_id}

COMPLETE INVESTIGATION HISTORY:
{json.dumps(history, indent=2, default=str)}

Evaluate:

1. **Objective Achievement**: Did we answer the original question? (%)
2. **Coverage**: How comprehensive was the investigation? (%)
3. **Source Quality**: Reliability of sources used (score 1-10)
4. **Efficiency**: Were resources used effectively? (score 1-10)
5. **Timeliness**: Completed in reasonable time? (score 1-10)
6. **Gaps**: What was missed or could be improved?
7. **Lessons Learned**: What worked well? What didn't?
8. **Recommendations**: How to improve future investigations?

Provide scores and detailed feedback. Output as JSON.
"""

        try:
            response = await self.llm.complete(evaluation_prompt)
            evaluation = json.loads(response)

            evaluation['evaluation_timestamp'] = datetime.now().isoformat()

            await self.log_action("investigation_evaluated", evaluation, IntelligencePhase.FEEDBACK)

            return evaluation

        except Exception as e:
            self.logger.error(f"Evaluation failed: {e}")
            return {
                'objective_achievement': 0,
                'notes': f"Evaluation failed: {e}",
                'evaluation_timestamp': datetime.now().isoformat()
            }

    # ==================== ADAPTIVE DECISION LOGIC ====================

    async def should_continue_investigation(self, iteration: int, current_findings: List[Dict]) -> Dict:
        """
        Determine if investigation should continue or conclude

        Args:
            iteration: Current iteration number
            current_findings: Current investigation findings

        Returns:
            Decision dict with continue flag and reasoning
        """
        if iteration >= self.max_iterations:
            return {
                'continue': False,
                'reason': 'Maximum iterations reached',
                'recommendation': 'Conclude investigation'
            }

        decision_prompt = f"""Evaluate if this OSINT investigation should continue.

OBJECTIVE: {self.objective}
CURRENT ITERATION: {iteration}/{self.max_iterations}

CURRENT FINDINGS:
{json.dumps(current_findings[-5:], indent=2, default=str)}

Decide: Should we continue investigating?

Consider:
- Have we answered the objective sufficiently?
- Are recent findings adding new value?
- Are we seeing diminishing returns?
- Are there unexplored leads worth pursuing?

Output JSON with:
- continue: true/false
- confidence: how confident are you? (0-1)
- reason: explanation
- recommendation: continue/conclude/pivot
"""

        try:
            response = await self.llm.complete(decision_prompt)
            decision = json.loads(response)
            return decision
        except Exception as e:
            self.logger.error(f"Decision logic failed: {e}")
            # Default to continue if uncertain
            return {
                'continue': iteration < self.max_iterations - 2,
                'reason': 'Default behavior due to decision error',
                'recommendation': 'continue'
            }

    async def adapt_strategy(self, current_state: Dict) -> List[Dict]:
        """
        Dynamically adapt investigation strategy based on current state

        Args:
            current_state: Current investigation state and findings

        Returns:
            New actions to take
        """
        adaptation_prompt = f"""You are adapting an OSINT investigation strategy.

OBJECTIVE: {self.objective}

CURRENT STATE:
{json.dumps(current_state, indent=2, default=str)}

AVAILABLE TOOLS:
{self._format_tools_description()}

Based on what we've learned, suggest 3-5 new actions to take.

Focus on:
- Following up on interesting leads
- Filling identified gaps
- Resolving contradictions
- Exploring new angles discovered
- Cross-verifying important findings

Output as JSON array of actions with: tool, parameters, rationale
"""

        try:
            response = await self.llm.complete(adaptation_prompt)
            new_actions = json.loads(response)

            await self.log_action("strategy_adapted", new_actions, self.current_phase)

            return new_actions if isinstance(new_actions, list) else []
        except Exception as e:
            self.logger.error(f"Strategy adaptation failed: {e}")
            return []

    # ==================== MAIN INVESTIGATION ORCHESTRATION ====================

    async def investigate(
        self,
        objective: str,
        constraints: Optional[Dict] = None,
        auto_report: bool = True
    ) -> Dict:
        """
        Run complete autonomous investigation through all intelligence lifecycle phases

        Args:
            objective: Investigation objective/question
            constraints: Optional constraints
            auto_report: Generate report automatically

        Returns:
            Complete investigation results with report
        """
        start_time = datetime.now()
        self.logger.info("=" * 60)
        self.logger.info("OSINT INVESTIGATION STARTING")
        self.logger.info("=" * 60)

        try:
            # PHASE 1: PLANNING & DIRECTION
            self.logger.info("\n[PHASE 1/6] PLANNING & DIRECTION")
            plan = await self.plan_investigation(objective, constraints)

            # PHASE 2: COLLECTION
            self.logger.info("\n[PHASE 2/6] COLLECTION")
            actions_queue = plan.get('actions', [])
            all_results = []
            iteration = 0

            while actions_queue and iteration < self.max_iterations:
                self.logger.info(f"\nIteration {iteration + 1}/{self.max_iterations}")

                # Execute next batch of actions
                batch_size = min(3, len(actions_queue))
                current_batch = actions_queue[:batch_size]
                actions_queue = actions_queue[batch_size:]

                results = await self.collect_intelligence(current_batch)
                all_results.extend(results)

                # Check if should continue
                decision = await self.should_continue_investigation(iteration, all_results)

                if not decision.get('continue', True):
                    self.logger.info(f"Concluding: {decision.get('reason')}")
                    break

                # Adapt strategy if needed
                if not actions_queue and decision.get('recommendation') == 'pivot':
                    self.logger.info("Adapting investigation strategy...")
                    new_actions = await self.adapt_strategy({
                        'plan': plan,
                        'results': all_results[-5:],
                        'iteration': iteration
                    })
                    actions_queue.extend(new_actions)

                iteration += 1

            # PHASE 3: PROCESSING
            self.logger.info("\n[PHASE 3/6] PROCESSING")
            processed_data = await self.process_raw_data(all_results)

            # PHASE 4: ANALYSIS
            self.logger.info("\n[PHASE 4/6] ANALYSIS")
            analysis = await self.analyze_intelligence(processed_data)

            # PHASE 5: DISSEMINATION
            report = None
            if auto_report:
                self.logger.info("\n[PHASE 5/6] DISSEMINATION")
                report = await self.generate_report(analysis)

            # PHASE 6: FEEDBACK
            self.logger.info("\n[PHASE 6/6] FEEDBACK")
            evaluation = await self.evaluate_investigation()

            # Compile complete results
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            complete_results = {
                'investigation_id': self.investigation_id,
                'objective': objective,
                'plan': plan,
                'collection_results': all_results,
                'processed_data': processed_data,
                'analysis': analysis,
                'report': report,
                'evaluation': evaluation,
                'metadata': {
                    'start_time': start_time.isoformat(),
                    'end_time': end_time.isoformat(),
                    'duration_seconds': duration,
                    'iterations': iteration,
                    'tools_used': len(set([r.get('tool') for r in all_results if r.get('tool')]))
                }
            }

            self.logger.info("\n" + "=" * 60)
            self.logger.info("INVESTIGATION COMPLETE")
            self.logger.info(f"Duration: {duration:.2f} seconds")
            self.logger.info(f"Iterations: {iteration}")
            self.logger.info("=" * 60)

            return complete_results

        except Exception as e:
            self.logger.error(f"Investigation failed: {e}")
            raise
