"""
Workflow Orchestrator for Automated OSINT Operations

Handles:
- Scheduled investigations
- Continuous monitoring
- Alert generation
- Multi-target campaigns
- Automated reporting
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Callable
from enum import Enum
import schedule
from pathlib import Path


class WorkflowType(Enum):
    """Types of automated workflows"""
    ONE_TIME = "one_time"
    SCHEDULED = "scheduled"
    CONTINUOUS = "continuous"
    TRIGGERED = "triggered"


class WorkflowStatus(Enum):
    """Workflow execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


class WorkflowOrchestrator:
    """
    Orchestrates automated OSINT workflows and campaigns
    """

    def __init__(self, agent, memory_store, config: Optional[Dict] = None):
        """
        Initialize workflow orchestrator

        Args:
            agent: OSINT agent instance
            memory_store: Memory store instance
            config: Optional configuration
        """
        self.agent = agent
        self.memory = memory_store
        self.config = config or {}

        self.workflows = {}
        self.running_tasks = {}
        self.alerts = []

        self.logger = logging.getLogger('WorkflowOrchestrator')
        logging.basicConfig(level=logging.INFO)

    async def create_workflow(
        self,
        name: str,
        workflow_type: WorkflowType,
        objective: str,
        schedule_config: Optional[Dict] = None,
        constraints: Optional[Dict] = None,
        alert_conditions: Optional[List[Dict]] = None
    ) -> str:
        """
        Create a new workflow

        Args:
            name: Workflow name
            workflow_type: Type of workflow
            objective: Investigation objective
            schedule_config: Scheduling configuration (for scheduled workflows)
            constraints: Investigation constraints
            alert_conditions: Conditions that trigger alerts

        Returns:
            Workflow ID
        """
        workflow_id = f"wf_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{name}"

        workflow = {
            'id': workflow_id,
            'name': name,
            'type': workflow_type.value,
            'objective': objective,
            'schedule_config': schedule_config or {},
            'constraints': constraints or {},
            'alert_conditions': alert_conditions or [],
            'status': WorkflowStatus.PENDING.value,
            'created_at': datetime.now().isoformat(),
            'executions': [],
            'results': []
        }

        self.workflows[workflow_id] = workflow

        self.logger.info(f"Created workflow: {workflow_id} ({workflow_type.value})")

        return workflow_id

    async def execute_workflow(self, workflow_id: str) -> Dict:
        """
        Execute a workflow

        Args:
            workflow_id: Workflow ID

        Returns:
            Execution results
        """
        if workflow_id not in self.workflows:
            return {"error": f"Workflow {workflow_id} not found"}

        workflow = self.workflows[workflow_id]

        # Update status
        workflow['status'] = WorkflowStatus.RUNNING.value
        execution_start = datetime.now()

        self.logger.info(f"Executing workflow: {workflow_id}")

        try:
            # Run investigation
            result = await self.agent.investigate(
                objective=workflow['objective'],
                constraints=workflow['constraints'],
                auto_report=True
            )

            # Record execution
            execution = {
                'start_time': execution_start.isoformat(),
                'end_time': datetime.now().isoformat(),
                'status': 'completed',
                'investigation_id': result.get('investigation_id'),
                'summary': {
                    'findings': len(result.get('analysis', {}).get('key_findings', [])),
                    'entities': len(result.get('processed_data', {}).get('entities', [])),
                    'duration': (datetime.now() - execution_start).total_seconds()
                }
            }

            workflow['executions'].append(execution)
            workflow['results'].append(result)
            workflow['status'] = WorkflowStatus.COMPLETED.value

            # Check alert conditions
            await self._check_alert_conditions(workflow, result)

            self.logger.info(f"Workflow completed: {workflow_id}")

            return result

        except Exception as e:
            self.logger.error(f"Workflow execution failed: {e}")

            execution = {
                'start_time': execution_start.isoformat(),
                'end_time': datetime.now().isoformat(),
                'status': 'failed',
                'error': str(e)
            }

            workflow['executions'].append(execution)
            workflow['status'] = WorkflowStatus.FAILED.value

            return {"error": str(e)}

    async def _check_alert_conditions(self, workflow: Dict, result: Dict):
        """
        Check if alert conditions are met

        Args:
            workflow: Workflow configuration
            result: Investigation results
        """
        alert_conditions = workflow.get('alert_conditions', [])

        for condition in alert_conditions:
            condition_type = condition.get('type')
            threshold = condition.get('threshold')

            triggered = False
            alert_data = {}

            if condition_type == 'finding_count':
                finding_count = len(result.get('analysis', {}).get('key_findings', []))
                if finding_count >= threshold:
                    triggered = True
                    alert_data = {'finding_count': finding_count, 'threshold': threshold}

            elif condition_type == 'high_confidence_finding':
                findings = result.get('analysis', {}).get('key_findings', [])
                high_conf_findings = [f for f in findings if f.get('confidence') == 'very_high' or f.get('confidence') == 'high']
                if len(high_conf_findings) > 0:
                    triggered = True
                    alert_data = {'high_confidence_findings': high_conf_findings}

            elif condition_type == 'keyword_match':
                keywords = condition.get('keywords', [])
                report = result.get('report', '')
                matched_keywords = [kw for kw in keywords if kw.lower() in report.lower()]
                if len(matched_keywords) > 0:
                    triggered = True
                    alert_data = {'matched_keywords': matched_keywords}

            elif condition_type == 'risk_indicator':
                risk_indicators = result.get('analysis', {}).get('risk_indicators', [])
                if len(risk_indicators) > 0:
                    triggered = True
                    alert_data = {'risk_indicators': risk_indicators}

            if triggered:
                await self._create_alert(workflow, condition, alert_data, result)

    async def _create_alert(self, workflow: Dict, condition: Dict, alert_data: Dict, result: Dict):
        """
        Create an alert

        Args:
            workflow: Workflow configuration
            condition: Alert condition that was triggered
            alert_data: Data that triggered the alert
            result: Full investigation results
        """
        alert = {
            'id': f"alert_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'workflow_id': workflow['id'],
            'workflow_name': workflow['name'],
            'condition': condition,
            'alert_data': alert_data,
            'investigation_id': result.get('investigation_id'),
            'timestamp': datetime.now().isoformat(),
            'severity': condition.get('severity', 'medium'),
            'status': 'active'
        }

        self.alerts.append(alert)

        self.logger.warning(f"ALERT TRIGGERED: {alert['id']} - {condition.get('type')}")

        # In production: Send notifications (email, Slack, webhook, etc.)

    async def schedule_workflow(self, workflow_id: str):
        """
        Schedule a workflow for periodic execution

        Args:
            workflow_id: Workflow ID
        """
        if workflow_id not in self.workflows:
            self.logger.error(f"Workflow {workflow_id} not found")
            return

        workflow = self.workflows[workflow_id]
        schedule_config = workflow.get('schedule_config', {})

        interval = schedule_config.get('interval')  # 'daily', 'hourly', 'weekly'
        time_of_day = schedule_config.get('time')  # e.g., '09:00'

        self.logger.info(f"Scheduling workflow {workflow_id}: {interval} at {time_of_day}")

        # This is a simplified scheduling - in production use APScheduler or Celery
        async def scheduled_execution():
            while workflow['status'] != WorkflowStatus.PAUSED.value:
                await self.execute_workflow(workflow_id)

                # Wait for next execution
                if interval == 'hourly':
                    await asyncio.sleep(3600)
                elif interval == 'daily':
                    await asyncio.sleep(86400)
                elif interval == 'weekly':
                    await asyncio.sleep(604800)
                else:
                    break

        # Start scheduled task
        task = asyncio.create_task(scheduled_execution())
        self.running_tasks[workflow_id] = task

    async def continuous_monitoring(
        self,
        workflow_id: str,
        check_interval: int = 300
    ):
        """
        Run continuous monitoring workflow

        Args:
            workflow_id: Workflow ID
            check_interval: Interval between checks in seconds
        """
        if workflow_id not in self.workflows:
            self.logger.error(f"Workflow {workflow_id} not found")
            return

        workflow = self.workflows[workflow_id]

        self.logger.info(f"Starting continuous monitoring: {workflow_id}")

        async def monitor():
            previous_result = None

            while workflow['status'] != WorkflowStatus.PAUSED.value:
                result = await self.execute_workflow(workflow_id)

                # Compare with previous result to detect changes
                if previous_result:
                    changes = self._detect_changes(previous_result, result)
                    if changes:
                        self.logger.info(f"Changes detected in {workflow_id}: {len(changes)} changes")
                        await self._create_alert(
                            workflow,
                            {'type': 'change_detected', 'severity': 'medium'},
                            {'changes': changes},
                            result
                        )

                previous_result = result

                await asyncio.sleep(check_interval)

        task = asyncio.create_task(monitor())
        self.running_tasks[workflow_id] = task

    def _detect_changes(self, previous: Dict, current: Dict) -> List[Dict]:
        """
        Detect changes between two investigation results

        Args:
            previous: Previous results
            current: Current results

        Returns:
            List of detected changes
        """
        changes = []

        # Compare entities
        prev_entities = set(e.get('name') for e in previous.get('processed_data', {}).get('entities', []))
        curr_entities = set(e.get('name') for e in current.get('processed_data', {}).get('entities', []))

        new_entities = curr_entities - prev_entities
        removed_entities = prev_entities - curr_entities

        if new_entities:
            changes.append({
                'type': 'new_entities',
                'count': len(new_entities),
                'entities': list(new_entities)
            })

        if removed_entities:
            changes.append({
                'type': 'removed_entities',
                'count': len(removed_entities),
                'entities': list(removed_entities)
            })

        # Compare findings
        prev_findings_count = len(previous.get('analysis', {}).get('key_findings', []))
        curr_findings_count = len(current.get('analysis', {}).get('key_findings', []))

        if curr_findings_count > prev_findings_count:
            changes.append({
                'type': 'new_findings',
                'previous_count': prev_findings_count,
                'current_count': curr_findings_count,
                'delta': curr_findings_count - prev_findings_count
            })

        return changes

    async def run_campaign(
        self,
        campaign_name: str,
        targets: List[Dict],
        objective_template: str,
        parallel: bool = False
    ) -> Dict:
        """
        Run multi-target investigation campaign

        Args:
            campaign_name: Campaign name
            targets: List of targets to investigate
            objective_template: Objective template with {target} placeholder
            parallel: Run investigations in parallel

        Returns:
            Campaign results
        """
        self.logger.info(f"Starting campaign: {campaign_name} with {len(targets)} targets")

        campaign_results = {
            'campaign_name': campaign_name,
            'start_time': datetime.now().isoformat(),
            'targets': targets,
            'results': []
        }

        if parallel:
            # Run investigations in parallel
            tasks = []
            for target in targets:
                objective = objective_template.format(target=target.get('name', target))
                task = self.agent.investigate(objective=objective)
                tasks.append(task)

            results = await asyncio.gather(*tasks, return_exceptions=True)
            campaign_results['results'] = results

        else:
            # Run investigations sequentially
            for target in targets:
                objective = objective_template.format(target=target.get('name', target))
                self.logger.info(f"Investigating target: {target}")

                try:
                    result = await self.agent.investigate(objective=objective)
                    campaign_results['results'].append(result)
                except Exception as e:
                    self.logger.error(f"Target investigation failed: {e}")
                    campaign_results['results'].append({'error': str(e), 'target': target})

                # Small delay between targets
                await asyncio.sleep(2)

        campaign_results['end_time'] = datetime.now().isoformat()
        campaign_results['completed'] = len([r for r in campaign_results['results'] if 'error' not in r])
        campaign_results['failed'] = len([r for r in campaign_results['results'] if 'error' in r])

        self.logger.info(f"Campaign complete: {campaign_results['completed']}/{len(targets)} successful")

        return campaign_results

    async def pause_workflow(self, workflow_id: str) -> bool:
        """
        Pause a running workflow

        Args:
            workflow_id: Workflow ID

        Returns:
            Success status
        """
        if workflow_id in self.workflows:
            self.workflows[workflow_id]['status'] = WorkflowStatus.PAUSED.value

            if workflow_id in self.running_tasks:
                self.running_tasks[workflow_id].cancel()

            self.logger.info(f"Workflow paused: {workflow_id}")
            return True

        return False

    async def resume_workflow(self, workflow_id: str) -> bool:
        """
        Resume a paused workflow

        Args:
            workflow_id: Workflow ID

        Returns:
            Success status
        """
        if workflow_id in self.workflows:
            workflow = self.workflows[workflow_id]
            workflow['status'] = WorkflowStatus.RUNNING.value

            # Restart based on workflow type
            if workflow['type'] == WorkflowType.SCHEDULED.value:
                await self.schedule_workflow(workflow_id)
            elif workflow['type'] == WorkflowType.CONTINUOUS.value:
                await self.continuous_monitoring(workflow_id)

            self.logger.info(f"Workflow resumed: {workflow_id}")
            return True

        return False

    def get_workflow_status(self, workflow_id: str) -> Dict:
        """
        Get workflow status and statistics

        Args:
            workflow_id: Workflow ID

        Returns:
            Workflow status information
        """
        if workflow_id not in self.workflows:
            return {"error": "Workflow not found"}

        workflow = self.workflows[workflow_id]

        return {
            'id': workflow_id,
            'name': workflow['name'],
            'status': workflow['status'],
            'type': workflow['type'],
            'executions': len(workflow['executions']),
            'last_execution': workflow['executions'][-1] if workflow['executions'] else None,
            'created_at': workflow['created_at']
        }

    def get_all_workflows(self) -> List[Dict]:
        """
        Get all workflows

        Returns:
            List of workflow summaries
        """
        return [
            {
                'id': wf_id,
                'name': wf['name'],
                'type': wf['type'],
                'status': wf['status'],
                'executions': len(wf['executions'])
            }
            for wf_id, wf in self.workflows.items()
        ]

    def get_alerts(self, severity: Optional[str] = None, status: str = 'active') -> List[Dict]:
        """
        Get alerts

        Args:
            severity: Filter by severity
            status: Filter by status

        Returns:
            List of alerts
        """
        filtered_alerts = [a for a in self.alerts if a['status'] == status]

        if severity:
            filtered_alerts = [a for a in filtered_alerts if a['severity'] == severity]

        return filtered_alerts

    async def acknowledge_alert(self, alert_id: str) -> bool:
        """
        Acknowledge an alert

        Args:
            alert_id: Alert ID

        Returns:
            Success status
        """
        for alert in self.alerts:
            if alert['id'] == alert_id:
                alert['status'] = 'acknowledged'
                alert['acknowledged_at'] = datetime.now().isoformat()
                return True

        return False

    async def export_workflows(self, filepath: str):
        """
        Export all workflows to file

        Args:
            filepath: File path for export
        """
        export_data = {
            'workflows': self.workflows,
            'alerts': self.alerts,
            'exported_at': datetime.now().isoformat()
        }

        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)

        self.logger.info(f"Workflows exported to {filepath}")

    async def import_workflows(self, filepath: str):
        """
        Import workflows from file

        Args:
            filepath: File path to import from
        """
        with open(filepath, 'r') as f:
            import_data = json.load(f)

        self.workflows.update(import_data.get('workflows', {}))
        self.alerts.extend(import_data.get('alerts', []))

        self.logger.info(f"Workflows imported from {filepath}")
