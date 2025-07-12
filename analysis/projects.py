import asyncio
import json
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging
from enum import Enum

logger = logging.getLogger(__name__)

class RiskCategory(Enum):
    RESOURCE = "resource"
    SCHEDULE = "schedule" 
    BUDGET = "budget"
    QUALITY = "quality"
    CLIENT = "client"
    TECHNICAL = "technical"

class PriorityLevel(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class ProjectContext:
    """Rich project context for intelligent briefings"""
    project_id: str
    project_name: str
    client_name: str
    status: str
    priority: str
    progress_percentage: int
    budget_utilization: float
    last_activity: datetime
    risk_indicators: List[str]
    recent_meetings: List[Dict]
    overdue_tasks: List[Dict]
    metadata: Dict[str, Any]

class ContextualProjectIntelligence:
    """
    Transforms generic data into specific, actionable project intelligence
    Think of this as your executive briefing specialist who knows every project intimately
    """
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.analysis_cache = {}
        
    async def generate_executive_briefing(self, days_lookback: int = 7) -> Dict[str, Any]:
        """
        Generate contextualized executive briefing with specific project intelligence
        """
        
        # Get all active projects with context
        project_contexts = await self._get_project_contexts()
        
        # Analyze each project for risks and opportunities
        project_analyses = []
        for context in project_contexts:
            analysis = await self._analyze_project_context(context)
            project_analyses.append(analysis)
        
        # Generate meeting intelligence with project context
        meeting_intelligence = await self._analyze_meeting_intelligence(days_lookback)
        
        # Risk analysis with specific project details
        risk_analysis = await self._analyze_risks_with_context(project_analyses)
        
        # Action items with project context
        action_items = await self._generate_contextual_action_items(project_analyses, meeting_intelligence)
        
        # Executive recommendations with specific details
        recommendations = await self._generate_executive_recommendations(project_analyses, risk_analysis)
        
        return {
            'briefing_date': datetime.now().isoformat(),
            'executive_summary': await self._create_executive_summary(project_analyses, risk_analysis),
            'project_intelligence': project_analyses,
            'meeting_intelligence': meeting_intelligence,
            'risk_analysis': risk_analysis,
            'action_items': action_items,
            'recommendations': recommendations,
            'performance_metrics': await self._calculate_portfolio_metrics(project_contexts)
        }
    
    async def _get_project_contexts(self) -> List[ProjectContext]:
        """Get rich context for all active projects"""
        
        sql = """
        SELECT 
            p.id, p.name, p.status, p.priority, p.progress_percentage,
            c.name as client_name, c.company as client_company,
            p.budget, p.actual_cost,
            COUNT(DISTINCT t.id) as total_tasks,
            COUNT(DISTINCT CASE WHEN t.status = 'completed' THEN t.id END) as completed_tasks,
            COUNT(DISTINCT CASE WHEN t.status = 'blocked' THEN t.id END) as blocked_tasks,
            COUNT(DISTINCT CASE WHEN t.due_date < NOW() AND t.status != 'completed' THEN t.id END) as overdue_tasks,
            MAX(m.actual_date) as last_meeting_date,
            COUNT(DISTINCT m.id) as meeting_count_7days
        FROM projects p
        LEFT JOIN clients c ON p.client_id = c.id
        LEFT JOIN tasks t ON p.id = t.project_id
        LEFT JOIN meetings m ON p.id = m.project_id AND m.actual_date >= NOW() - INTERVAL '7 days'
        WHERE p.status IN ('planning', 'active', 'on_hold')
        GROUP BY p.id, c.name, c.company, p.budget, p.actual_cost
        ORDER BY p.priority DESC, p.created_at DESC
        """
        
        results = await self.db.execute(sql)
        
        contexts = []
        for row in results:
            budget_utilization = (row['actual_cost'] / row['budget'] * 100) if row['budget'] > 0 else 0
            
            # Get recent meetings for this project
            recent_meetings = await self._get_recent_meetings(row['id'])
            
            # Get overdue tasks for this project
            overdue_tasks = await self._get_overdue_tasks(row['id'])
            
            # Calculate risk indicators
            risk_indicators = await self._calculate_risk_indicators(row)
            
            context = ProjectContext(
                project_id=row['id'],
                project_name=row['name'],
                client_name=row['client_name'] or row['client_company'],
                status=row['status'],
                priority=row['priority'],
                progress_percentage=row['progress_percentage'],
                budget_utilization=budget_utilization,
                last_activity=row['last_meeting_date'] or datetime.now() - timedelta(days=30),
                risk_indicators=risk_indicators,
                recent_meetings=recent_meetings,
                overdue_tasks=overdue_tasks,
                metadata={
                    'total_tasks': row['total_tasks'],
                    'completed_tasks': row['completed_tasks'],
                    'blocked_tasks': row['blocked_tasks'],
                    'meeting_count_7days': row['meeting_count_7days']
                }
            )
            contexts.append(context)
        
        return contexts
    
    async def _analyze_project_context(self, context: ProjectContext) -> Dict[str, Any]:
        """Analyze individual project for specific risks and opportunities"""
        
        analysis = {
            'project_id': context.project_id,
            'project_name': context.project_name,
            'client_name': context.client_name,
            'status_assessment': await self._assess_project_status(context),
            'risk_assessment': await self._assess_project_risks(context),
            'performance_indicators': await self._calculate_project_kpis(context),
            'recent_activity': await self._analyze_recent_activity(context),
            'action_required': await self._determine_actions_required(context),
            'priority_score': await self._calculate_priority_score(context)
        }
        
        return analysis
    
    async def _assess_project_status(self, context: ProjectContext) -> Dict[str, Any]:
        """Assess overall project health with specific indicators"""
        
        health_score = 100
        issues = []
        highlights = []
        
        # Budget assessment
        if context.budget_utilization > 90:
            health_score -= 25
            issues.append(f"Budget critical: {context.budget_utilization:.1f}% utilized")
        elif context.budget_utilization > 75:
            health_score -= 10
            issues.append(f"Budget concern: {context.budget_utilization:.1f}% utilized")
        else:
            highlights.append(f"Budget healthy: {context.budget_utilization:.1f}% utilized")
        
        # Progress assessment
        if context.progress_percentage < 10 and context.status == 'active':
            health_score -= 20
            issues.append("Project active but minimal progress recorded")
        elif context.progress_percentage > 80:
            highlights.append(f"Excellent progress: {context.progress_percentage}% complete")
        
        # Task assessment
        if context.metadata['blocked_tasks'] > 0:
            health_score -= 15
            issues.append(f"{context.metadata['blocked_tasks']} tasks currently blocked")
        
        if len(context.overdue_tasks) > 0:
            health_score -= 20
            issues.append(f"{len(context.overdue_tasks)} overdue tasks requiring attention")
        
        # Activity assessment
        days_since_meeting = (datetime.now() - context.last_activity).days
        if days_since_meeting > 14:
            health_score -= 15
            issues.append(f"No meetings in {days_since_meeting} days - potential communication gap")
        
        return {
            'health_score': max(0, health_score),
            'health_status': 'excellent' if health_score > 85 else 'good' if health_score > 70 else 'concerning' if health_score > 50 else 'critical',
            'issues': issues,
            'highlights': highlights
        }
    
    async def _assess_project_risks(self, context: ProjectContext) -> List[Dict[str, Any]]:
        """Assess specific project risks with detailed context"""
        
        risks = []
        
        # Budget risk
        if context.budget_utilization > 85:
            risks.append({
                'category': RiskCategory.BUDGET.value,
                'severity': 'high' if context.budget_utilization > 95 else 'medium',
                'description': f"Budget utilization at {context.budget_utilization:.1f}% for {context.project_name}",
                'impact': f"Potential cost overrun for {context.client_name} project",
                'recommended_action': "Schedule budget review meeting with stakeholders"
            })
        
        # Schedule risk from overdue tasks
        if len(context.overdue_tasks) > 0:
            risks.append({
                'category': RiskCategory.SCHEDULE.value,
                'severity': 'high' if len(context.overdue_tasks) > 3 else 'medium',
                'description': f"{len(context.overdue_tasks)} overdue tasks in {context.project_name}",
                'impact': f"Potential schedule delays affecting {context.client_name} delivery",
                'recommended_action': f"Review overdue tasks: {', '.join([task['title'] for task in context.overdue_tasks[:3]])}"
            })
        
        # Resource risk from blocked tasks
        if context.metadata['blocked_tasks'] > 0:
            risks.append({
                'category': RiskCategory.RESOURCE.value,
                'severity': 'medium',
                'description': f"{context.metadata['blocked_tasks']} blocked tasks in {context.project_name}",
                'impact': "Resource constraints affecting project velocity",
                'recommended_action': "Identify and resolve task blockers"
            })
        
        # Communication risk
        days_since_meeting = (datetime.now() - context.last_activity).days
        if days_since_meeting > 10:
            risks.append({
                'category': RiskCategory.CLIENT.value,
                'severity': 'medium' if days_since_meeting > 21 else 'low',
                'description': f"No client communication in {days_since_meeting} days for {context.project_name}",
                'impact': f"Potential alignment issues with {context.client_name}",
                'recommended_action': "Schedule status update meeting"
            })
        
        return risks
    
    async def _analyze_meeting_intelligence(self, days_lookback: int) -> Dict[str, Any]:
        """Analyze meeting patterns with project context"""
        
        sql = """
        SELECT 
            m.id, m.title, m.scheduled_date, m.actual_date, m.sentiment,
            m.summary, m.action_items_count,
            p.name as project_name, c.name as client_name,
            p.priority as project_priority
        FROM meetings m
        LEFT JOIN projects p ON m.project_id = p.id
        LEFT JOIN clients c ON p.client_id = c.id
        WHERE m.actual_date >= NOW() - INTERVAL '%s days'
        ORDER BY m.actual_date DESC
        """
        
        meetings = await self.db.execute(sql, (days_lookback,))
        
        # Analyze sentiment patterns by project
        sentiment_analysis = {}
        action_items_by_project = {}
        
        for meeting in meetings:
            project_key = f"{meeting['project_name']} ({meeting['client_name']})"
            
            if project_key not in sentiment_analysis:
                sentiment_analysis[project_key] = []
                action_items_by_project[project_key] = 0
            
            sentiment_analysis[project_key].append(meeting['sentiment'])
            action_items_by_project[project_key] += meeting['action_items_count'] or 0
        
        # Identify concerning patterns
        concerning_projects = []
        for project, sentiments in sentiment_analysis.items():
            negative_count = sentiments.count('negative')
            if negative_count > len(sentiments) / 2:  # More than half negative
                concerning_projects.append({
                    'project': project,
                    'issue': f'{negative_count}/{len(sentiments)} recent meetings negative sentiment',
                    'recommendation': 'Review project health and stakeholder satisfaction'
                })
        
        return {
            'total_meetings': len(meetings),
            'meetings_by_project': sentiment_analysis,
            'action_items_by_project': action_items_by_project,
            'concerning_projects': concerning_projects,
            'recent_meetings': [
                {
                    'title': m['title'],
                    'project': f"{m['project_name']} ({m['client_name']})",
                    'date': m['actual_date'],
                    'sentiment': m['sentiment'],
                    'summary': m['summary'][:200] + '...' if m['summary'] and len(m['summary']) > 200 else m['summary']
                } for m in meetings[:10]
            ]
        }
    
    async def _generate_contextual_action_items(self, project_analyses: List[Dict], meeting_intelligence: Dict) -> List[Dict[str, Any]]:
        """Generate specific action items with project context"""
        
        action_items = []
        
        # Critical project actions
        for analysis in project_analyses:
            if analysis['status_assessment']['health_score'] < 60:
                action_items.append({
                    'priority': PriorityLevel.CRITICAL.value,
                    'category': 'project_health',
                    'title': f"Review {analysis['project_name']} project health",
                    'description': f"Project health score: {analysis['status_assessment']['health_score']}/100",
                    'specific_issues': analysis['status_assessment']['issues'],
                    'client': analysis['client_name'],
                    'recommended_timeline': '24 hours'
                })
            
            # Budget-specific actions
            for risk in analysis['risk_assessment']:
                if risk['category'] == 'budget' and risk['severity'] == 'high':
                    action_items.append({
                        'priority': PriorityLevel.HIGH.value,
                        'category': 'budget_management',
                        'title': f"Address budget concerns - {analysis['project_name']}",
                        'description': risk['description'],
                        'client': analysis['client_name'],
                        'recommended_action': risk['recommended_action'],
                        'recommended_timeline': '48 hours'
                    })
        
        # Communication actions from meeting analysis
        for concern in meeting_intelligence['concerning_projects']:
            action_items.append({
                'priority': PriorityLevel.MEDIUM.value,
                'category': 'client_communication',
                'title': f"Address communication concerns - {concern['project']}",
                'description': concern['issue'],
                'recommended_action': concern['recommendation'],
                'recommended_timeline': '1 week'
            })
        
        return sorted(action_items, key=lambda x: ['critical', 'high', 'medium', 'low'].index(x['priority']))
    
    async def _generate_executive_recommendations(self, project_analyses: List[Dict], risk_analysis: Dict) -> List[Dict[str, Any]]:
        """Generate strategic recommendations with specific context"""
        
        recommendations = []
        
        # Portfolio-level insights
        high_risk_projects = [p for p in project_analyses if p['status_assessment']['health_score'] < 70]
        excellent_projects = [p for p in project_analyses if p['status_assessment']['health_score'] > 90]
        
        if len(high_risk_projects) > 0:
            project_names = [p['project_name'] for p in high_risk_projects]
            recommendations.append({
                'type': 'IMMEDIATE',
                'icon': '🚨',
                'title': 'High-risk projects require intervention',
                'description': f"Projects needing attention: {', '.join(project_names)}",
                'specific_actions': [
                    f"Schedule emergency review for {p['project_name']} (Client: {p['client_name']})"
                    for p in high_risk_projects[:3]
                ],
                'impact': 'Prevent project failures and client satisfaction issues'
            })
        
        if len(excellent_projects) > 0:
            recommendations.append({
                'type': 'STRATEGIC',
                'icon': '🎯',
                'title': 'Leverage successful project patterns',
                'description': f"High-performing projects: {', '.join([p['project_name'] for p in excellent_projects])}",
                'specific_actions': [
                    "Document best practices from high-performing projects",
                    "Apply successful patterns to struggling projects",
                    "Use as case studies for new client acquisitions"
                ],
                'impact': 'Scale successful approaches across portfolio'
            })
        
        # Resource optimization recommendations
        blocked_tasks_total = sum(p['status_assessment'].get('blocked_tasks', 0) for p in project_analyses)
        if blocked_tasks_total > 5:
            recommendations.append({
                'type': 'OPERATIONAL',
                'icon': '⚡',
                'title': 'Resolve resource bottlenecks',
                'description': f"{blocked_tasks_total} blocked tasks across {len(project_analyses)} projects",
                'specific_actions': [
                    "Identify common blockers across projects",
                    "Implement resource reallocation plan",
                    "Establish escalation process for blocked tasks"
                ],
                'impact': 'Improve project velocity and team productivity'
            })
        
        return recommendations
    
    async def _get_recent_meetings(self, project_id: str) -> List[Dict]:
        """Get recent meetings for a project"""
        sql = """
        SELECT title, scheduled_date, actual_date, sentiment, summary
        FROM meetings 
        WHERE project_id = %s AND actual_date >= NOW() - INTERVAL '30 days'
        ORDER BY actual_date DESC LIMIT 5
        """
        return await self.db.execute(sql, (project_id,))
    
    async def _get_overdue_tasks(self, project_id: str) -> List[Dict]:
        """Get overdue tasks for a project"""
        sql = """
        SELECT title, assigned_to, due_date, status
        FROM tasks 
        WHERE project_id = %s AND due_date < NOW() AND status != 'completed'
        ORDER BY due_date ASC LIMIT 10
        """
        return await self.db.execute(sql, (project_id,))
    
    async def _calculate_risk_indicators(self, project_data: Dict) -> List[str]:
        """Calculate risk indicators for a project"""
        indicators = []
        
        if project_data.get('overdue_tasks', 0) > 0:
            indicators.append('schedule_risk')
        
        budget_util = (project_data['actual_cost'] / project_data['budget'] * 100) if project_data['budget'] > 0 else 0
        if budget_util > 85:
            indicators.append('budget_risk')
        
        if project_data.get('blocked_tasks', 0) > 0:
            indicators.append('resource_risk')
        
        return indicators
    
    async def _create_executive_summary(self, project_analyses: List[Dict], risk_analysis: Dict) -> Dict[str, Any]:
        """Create executive summary with specific insights"""
        
        total_projects = len(project_analyses)
        critical_projects = [p for p in project_analyses if p['status_assessment']['health_score'] < 60]
        healthy_projects = [p for p in project_analyses if p['status_assessment']['health_score'] > 80]
        
        # Calculate portfolio health
        avg_health = sum(p['status_assessment']['health_score'] for p in project_analyses) / total_projects if total_projects > 0 else 0
        
        # Key metrics
        total_overdue_tasks = sum(len(p.get('overdue_tasks', [])) for p in project_analyses)
        total_action_items = sum(p.get('action_items_count', 0) for p in project_analyses)
        
        return {
            'portfolio_health': {
                'overall_score': round(avg_health, 1),
                'status': 'excellent' if avg_health > 85 else 'good' if avg_health > 70 else 'needs_attention',
                'total_projects': total_projects,
                'critical_projects': len(critical_projects),
                'healthy_projects': len(healthy_projects)
            },
            'key_insights': [
                f"📊 Portfolio Health: {avg_health:.1f}/100 across {total_projects} active projects",
                f"🚨 Critical Attention: {len(critical_projects)} projects need immediate intervention",
                f"✅ Strong Performance: {len(healthy_projects)} projects exceeding expectations",
                f"⏰ Action Required: {total_overdue_tasks} overdue tasks across portfolio"
            ],
            'executive_priorities': [
                f"Review {p['project_name']} (Client: {p['client_name']}) - Health: {p['status_assessment']['health_score']}/100"
                for p in critical_projects[:3]
            ] if critical_projects else ["All projects performing within acceptable parameters"]
        }
    
    async def _calculate_project_kpis(self, context: ProjectContext) -> Dict[str, Any]:
        """Calculate specific KPIs for a project"""
        
        task_completion_rate = (context.metadata['completed_tasks'] / context.metadata['total_tasks'] * 100) if context.metadata['total_tasks'] > 0 else 0
        
        return {
            'task_completion_rate': round(task_completion_rate, 1),
            'budget_efficiency': round(100 - context.budget_utilization, 1),
            'schedule_adherence': 100 - (len(context.overdue_tasks) / context.metadata['total_tasks'] * 100) if context.metadata['total_tasks'] > 0 else 100,
            'communication_frequency': context.metadata['meeting_count_7days'],
            'risk_score': len(context.risk_indicators) * 25  # Simple risk scoring
        }
    
    async def _analyze_recent_activity(self, context: ProjectContext) -> Dict[str, Any]:
        """Analyze recent project activity"""
        
        activity_summary = {
            'last_meeting': context.last_activity.strftime('%Y-%m-%d') if context.last_activity else 'No recent meetings',
            'recent_meeting_count': context.metadata['meeting_count_7days'],
            'task_velocity': context.metadata['completed_tasks'],  # Simplified velocity metric
            'communication_health': 'good' if context.metadata['meeting_count_7days'] > 0 else 'concerning'
        }
        
        return activity_summary
    
    async def _determine_actions_required(self, context: ProjectContext) -> List[str]:
        """Determine specific actions required for a project"""
        
        actions = []
        
        if len(context.overdue_tasks) > 0:
            actions.append(f"Review {len(context.overdue_tasks)} overdue tasks with team")
        
        if context.budget_utilization > 90:
            actions.append("Conduct emergency budget review")
        
        if context.metadata['blocked_tasks'] > 0:
            actions.append(f"Resolve {context.metadata['blocked_tasks']} blocked tasks")
        
        if (datetime.now() - context.last_activity).days > 14:
            actions.append("Schedule client check-in meeting")
        
        if context.progress_percentage < 20 and context.status == 'active':
            actions.append("Review project kickoff and initial deliverables")
        
        return actions
    
    async def _calculate_priority_score(self, context: ProjectContext) -> int:
        """Calculate priority score for project ranking"""
        
        score = 0
        
        # Health score impact (inverted - worse health = higher priority)
        health_score = await self._assess_project_status(context)
        score += (100 - health_score['health_score'])
        
        # Client priority
        if context.priority == 'high':
            score += 30
        elif context.priority == 'medium':
            score += 15
        
        # Overdue tasks impact
        score += len(context.overdue_tasks) * 10
        
        # Budget utilization impact
        if context.budget_utilization > 90:
            score += 25
        
        return min(score, 100)  # Cap at 100
    
    async def _calculate_portfolio_metrics(self, contexts: List[ProjectContext]) -> Dict[str, Any]:
        """Calculate portfolio-level performance metrics"""
        
        if not contexts:
            return {'message': 'No active projects found'}
        
        # Overall portfolio health
        total_projects = len(contexts)
        avg_progress = sum(c.progress_percentage for c in contexts) / total_projects
        avg_budget_util = sum(c.budget_utilization for c in contexts) / total_projects
        
        # Risk distribution
        high_risk_count = sum(1 for c in contexts if len(c.risk_indicators) > 2)
        medium_risk_count = sum(1 for c in contexts if len(c.risk_indicators) == 1 or len(c.risk_indicators) == 2)
        low_risk_count = total_projects - high_risk_count - medium_risk_count
        
        # Client distribution
        clients = list(set(c.client_name for c in contexts))
        
        return {
            'portfolio_size': total_projects,
            'avg_progress': round(avg_progress, 1),
            'avg_budget_utilization': round(avg_budget_util, 1),
            'risk_distribution': {
                'high_risk': high_risk_count,
                'medium_risk': medium_risk_count,
                'low_risk': low_risk_count
            },
            'client_count': len(clients),
            'performance_trend': 'improving' if avg_progress > 60 else 'concerning'
        }


# ============================================================================
# INTEGRATION WITH YOUR AI CHIEF OF STAFF
# ============================================================================

class EnhancedCEOBriefing:
    """
    Enhanced version of your AI Chief of Staff with contextual intelligence
    """
    
    def __init__(self, db_connection, doc_extractor):
        self.db = db_connection
        self.doc_extractor = doc_extractor
        self.project_intelligence = ContextualProjectIntelligence(db_connection)
    
    async def generate_enhanced_briefing(self) -> str:
        """Generate enhanced CEO briefing with specific project context"""
        
        # Get contextual project intelligence
        briefing_data = await self.project_intelligence.generate_executive_briefing()
        
        # Format the briefing
        briefing = self._format_enhanced_briefing(briefing_data)
        
        return briefing
    
    def _format_enhanced_briefing(self, data: Dict[str, Any]) -> str:
        """Format the enhanced briefing with specific project details"""
        
        briefing_date = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        briefing = f"""
# 📊 CEO STRATEGIC BRIEFING

📅 **DATE:** {briefing_date}

## 🎯 EXECUTIVE SUMMARY

**Portfolio Health:** {data['executive_summary']['portfolio_health']['overall_score']}/100 ({data['executive_summary']['portfolio_health']['status'].upper()})

**Key Metrics:**
• **{data['executive_summary']['portfolio_health']['total_projects']}** active projects across **{data['performance_metrics']['client_count']}** clients
• **{data['executive_summary']['portfolio_health']['critical_projects']}** projects requiring immediate attention
• **{data['executive_summary']['portfolio_health']['healthy_projects']}** projects exceeding expectations
• **{data['performance_metrics']['avg_progress']:.1f}%** average project progress

---

## 🚨 CRITICAL ATTENTION REQUIRED

"""
        
        # Add critical projects with specific details
        critical_actions = [action for action in data['action_items'] if action['priority'] == 'critical']
        if critical_actions:
            for action in critical_actions:
                briefing += f"""
**🔥 {action['title']}**
• **Client:** {action['client']}
• **Issue:** {action['description']}
• **Timeline:** {action['recommended_timeline']}
• **Actions:** {', '.join(action['specific_issues']) if 'specific_issues' in action else action.get('recommended_action', 'Review required')}

"""
        else:
            briefing += "✅ No critical issues requiring immediate attention\n\n"
        
        briefing += "---\n\n## 📈 PROJECT INTELLIGENCE\n\n"
        
        # Add project-specific intelligence
        for project in data['project_intelligence'][:5]:  # Top 5 projects by priority
            health = project['status_assessment']['health_score']
            status_emoji = "🟢" if health > 80 else "🟡" if health > 60 else "🔴"
            
            briefing += f"""
**{status_emoji} {project['project_name']} ({project['client_name']})**
• **Health Score:** {health}/100
• **Status:** {project['status_assessment']['health_status'].title()}
"""
            
            if project['status_assessment']['issues']:
                briefing += f"• **Issues:** {'; '.join(project['status_assessment']['issues'])}\n"
            
            if project['status_assessment']['highlights']:
                briefing += f"• **Highlights:** {'; '.join(project['status_assessment']['highlights'])}\n"
            
            if project['action_required']:
                briefing += f"• **Actions Required:** {'; '.join(project['action_required'][:2])}\n"
            
            briefing += "\n"
        
        briefing += "---\n\n## 🏢 MEETING INTELLIGENCE\n\n"
        
        # Add meeting intelligence with project context
        meeting_data = data['meeting_intelligence']
        briefing += f"**{meeting_data['total_meetings']}** meetings analyzed in last 7 days\n\n"
        
        if meeting_data['concerning_projects']:
            briefing += "**🚨 Communication Concerns:**\n"
            for concern in meeting_data['concerning_projects']:
                briefing += f"• **{concern['project']}:** {concern['issue']}\n"
            briefing += "\n"
        
        # Recent meetings with context
        briefing += "**Recent Key Meetings:**\n"
        for meeting in meeting_data['recent_meetings'][:5]:
            sentiment_emoji = "😊" if meeting['sentiment'] == 'positive' else "😐" if meeting['sentiment'] == 'neutral' else "😟"
            briefing += f"• {sentiment_emoji} **{meeting['title']}** ({meeting['project']}) - {meeting['date']}\n"
            if meeting['summary']:
                briefing += f"  {meeting['summary']}\n"
        
        briefing += "\n---\n\n## ⚠️ RISK ANALYSIS\n\n"
        
        # Add risk analysis with specific project context
        all_risks = []
        for project in data['project_intelligence']:
            all_risks.extend(project['risk_assessment'])
        
        risk_by_category = {}
        for risk in all_risks:
            category = risk['category']
            if category not in risk_by_category:
                risk_by_category[category] = []
            risk_by_category[category].append(risk)
        
        for category, risks in risk_by_category.items():
            high_severity = [r for r in risks if r['severity'] == 'high']
            if high_severity:
                briefing += f"**🚨 {category.upper()} RISK - HIGH**\n"
                for risk in high_severity:
                    briefing += f"• {risk['description']}\n"
                    briefing += f"  **Impact:** {risk['impact']}\n"
                    briefing += f"  **Action:** {risk['recommended_action']}\n\n"
        
        briefing += "---\n\n## 💡 CEO RECOMMENDATIONS\n\n"
        
        # Add specific recommendations
        for rec in data['recommendations']:
            briefing += f"**{rec['icon']} {rec['type']}: {rec['title']}**\n"
            briefing += f"• {rec['description']}\n"
            if 'specific_actions' in rec:
                for action in rec['specific_actions']:
                    briefing += f"  - {action}\n"
            briefing += f"• **Impact:** {rec['impact']}\n\n"
        
        briefing += "---\n\n## 📊 PORTFOLIO METRICS\n\n"
        
        metrics = data['performance_metrics']
        briefing += f"""
• **Portfolio Size:** {metrics['portfolio_size']} active projects
• **Average Progress:** {metrics['avg_progress']:.1f}%
• **Budget Utilization:** {metrics['avg_budget_utilization']:.1f}%
• **Risk Distribution:** {metrics['risk_distribution']['high_risk']} high, {metrics['risk_distribution']['medium_risk']} medium, {metrics['risk_distribution']['low_risk']} low
• **Performance Trend:** {metrics['performance_trend'].title()}

---

🎯 **BRIEFING COMPLETE!**
📊 **Total Projects Analyzed:** {metrics['portfolio_size']}
⚠️ **Critical Actions:** {len([a for a in data['action_items'] if a['priority'] == 'critical'])}
✅ **Recommendations Generated:** {len(data['recommendations'])}
"""
        
        return briefing


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

async def main():
    """Example of running the enhanced contextual briefing system"""
    
    print("🚀 CONTEXTUAL PROJECT INTELLIGENCE SYSTEM")
    print("=" * 60)
    
    # Mock database connection for demo
    class MockDB:
        async def execute(self, sql, params=None):
            # Return mock data that matches your real project structure
            return [
                {
                    'id': 'proj-001',
                    'name': 'Paradise Isle Resort Development',
                    'client_name': 'Paradise Isle Holdings',
                    'status': 'active',
                    'priority': 'high',
                    'progress_percentage': 45,
                    'budget': 2500000,
                    'actual_cost': 2100000,
                    'total_tasks': 24,
                    'completed_tasks': 18,
                    'blocked_tasks': 2,
                    'overdue_tasks': 3,
                    'last_meeting_date': datetime.now() - timedelta(days=2),
                    'meeting_count_7days': 2
                },
                {
                    'id': 'proj-002', 
                    'name': 'Goodwill Bloomington Store',
                    'client_name': 'Goodwill Industries',
                    'status': 'active',
                    'priority': 'medium',
                    'progress_percentage': 75,
                    'budget': 850000,
                    'actual_cost': 650000,
                    'total_tasks': 15,
                    'completed_tasks': 12,
                    'blocked_tasks': 0,
                    'overdue_tasks': 1,
                    'last_meeting_date': datetime.now() - timedelta(days=1),
                    'meeting_count_7days': 3
                }
            ]
    
    # Initialize the enhanced system
    db = MockDB()
    doc_extractor = None  # Your existing document extractor
    
    enhanced_briefing = EnhancedCEOBriefing(db, doc_extractor)
    
    # Generate the enhanced briefing
    briefing_output = await enhanced_briefing.generate_enhanced_briefing()
    
    print(briefing_output)

if __name__ == "__main__":
    asyncio.run(main())