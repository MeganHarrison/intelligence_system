'use client'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { 
  Brain, 
  Activity,
  Clock,
  CheckCircle,
  AlertCircle,
  Play,
  Pause,
  RefreshCw,
  Settings,
  TrendingUp,
  Users,
  Zap
} from 'lucide-react'
import { 
  useDashboardAgents,
  useDashboardUI,
  useActiveWorkflows
} from '@/lib/stores/dashboard'
import { useDashboard, useConnectionStatus } from '@/lib/providers/dashboard-provider'

function AgentDetailCard({ agent }: { agent: any }) {
  const { executeWorkflow } = useDashboard()
  const { isFullyConnected } = useConnectionStatus()

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'text-green-600 bg-green-50 border-green-200'
      case 'processing': return 'text-yellow-600 bg-yellow-50 border-yellow-200'
      case 'inactive': return 'text-gray-600 bg-gray-50 border-gray-200'
      case 'error': return 'text-red-600 bg-red-50 border-red-200'
      default: return 'text-gray-600 bg-gray-50 border-gray-200'
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active': return <CheckCircle className="h-4 w-4" />
      case 'processing': return <Clock className="h-4 w-4 animate-pulse" />
      case 'inactive': return <Pause className="h-4 w-4" />
      case 'error': return <AlertCircle className="h-4 w-4" />
      default: return <AlertCircle className="h-4 w-4" />
    }
  }

  const getAgentWorkflow = (agentId: string) => {
    switch (agentId) {
      case 'intelligence_officer':
        return "Conduct comprehensive intelligence analysis of current market conditions"
      case 'strategic_advisor':
        return "Provide strategic recommendations based on available intelligence"
      case 'execution_coordinator':
        return "Analyze execution capabilities and recommend optimization strategies"
      case 'ai_chief_of_staff':
        return "Generate executive briefing and strategic summary"
      default:
        return "Execute specialized analysis workflow"
    }
  }

  const handleRunWorkflow = () => {
    const workflow = getAgentWorkflow(agent.id)
    executeWorkflow(workflow)
  }

  return (
    <Card className="h-full">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2 rounded-lg bg-primary/10">
              <Brain className="h-5 w-5 text-primary" />
            </div>
            <div>
              <CardTitle className="text-lg">{agent.name}</CardTitle>
              <CardDescription>{agent.id}</CardDescription>
            </div>
          </div>
          <div className={`flex items-center gap-2 px-3 py-1 rounded-full border ${getStatusColor(agent.status)}`}>
            {getStatusIcon(agent.status)}
            <span className="text-sm font-medium capitalize">{agent.status}</span>
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Performance Metrics */}
        <div className="space-y-4">
          <div>
            <div className="flex justify-between text-sm mb-2">
              <span className="font-medium">Performance Score</span>
              <span className="text-muted-foreground">{agent.performanceScore || 0}%</span>
            </div>
            <Progress value={agent.performanceScore || 0} className="h-2" />
          </div>

          <div className="grid grid-cols-2 gap-4 text-sm">
            <div className="space-y-1">
              <span className="text-muted-foreground">Tasks Completed</span>
              <div className="flex items-center space-x-1">
                <CheckCircle className="h-3 w-3 text-green-500" />
                <span className="font-medium">{agent.tasksCompleted || 0}</span>
              </div>
            </div>
            <div className="space-y-1">
              <span className="text-muted-foreground">Last Activity</span>
              <div className="flex items-center space-x-1">
                <Clock className="h-3 w-3 text-blue-500" />
                <span className="font-medium">{agent.lastActivity || 'Never'}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="space-y-3">
          <h4 className="text-sm font-medium text-muted-foreground">Quick Actions</h4>
          <div className="flex flex-col space-y-2">
            <Button 
              variant="outline" 
              size="sm" 
              className="justify-start"
              onClick={handleRunWorkflow}
              disabled={!isFullyConnected || agent.status === 'processing'}
            >
              <Play className="mr-2 h-3 w-3" />
              Run Analysis
            </Button>
            <Button 
              variant="outline" 
              size="sm" 
              className="justify-start"
              disabled={!isFullyConnected}
            >
              <Settings className="mr-2 h-3 w-3" />
              Configure
            </Button>
          </div>
        </div>

        {/* Agent Status Details */}
        <div className="pt-4 border-t space-y-2">
          <div className="flex justify-between text-xs">
            <span className="text-muted-foreground">Uptime</span>
            <span>99.9%</span>
          </div>
          <div className="flex justify-between text-xs">
            <span className="text-muted-foreground">Response Time</span>
            <span>0.8s avg</span>
          </div>
          <div className="flex justify-between text-xs">
            <span className="text-muted-foreground">Success Rate</span>
            <span>{agent.performanceScore || 0}%</span>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

function SystemOverview() {
  const agents = useDashboardAgents()
  const activeWorkflows = useActiveWorkflows()
  const { isFullyConnected } = useConnectionStatus()

  const activeAgents = agents.filter(a => a.status === 'active').length
  const avgPerformance = agents.length > 0 
    ? Math.round(agents.reduce((sum, agent) => sum + (agent.performanceScore || 0), 0) / agents.length)
    : 0

  return (
    <div className="grid gap-4 md:grid-cols-4">
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Total Agents</CardTitle>
          <Users className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{agents.length}</div>
          <p className="text-xs text-muted-foreground">
            {activeAgents} active
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Active Workflows</CardTitle>
          <Activity className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{activeWorkflows.length}</div>
          <p className="text-xs text-muted-foreground">
            Currently processing
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Avg Performance</CardTitle>
          <TrendingUp className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{avgPerformance}%</div>
          <p className="text-xs text-muted-foreground">
            System efficiency
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">System Status</CardTitle>
          <Zap className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">
            {isFullyConnected ? 
              <span className="text-green-600">Online</span> : 
              <span className="text-red-600">Offline</span>
            }
          </div>
          <p className="text-xs text-muted-foreground">
            Connection status
          </p>
        </CardContent>
      </Card>
    </div>
  )
}

export default function AgentsPage() {
  const agents = useDashboardAgents()
  const { isLoading, error } = useDashboardUI()
  const { refreshData } = useDashboard()
  const { isApiConnected } = useConnectionStatus()

  return (
    <div className="bg-background">
      {/* Main Content */}
      <div className="container py-6">
        <div className="space-y-6">
          {/* Page Header */}
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold tracking-tight">Strategic Agents</h1>
              <p className="text-muted-foreground">
                Monitor and manage your AI strategic intelligence agents
              </p>
            </div>
            <Button 
              variant="outline"
              onClick={refreshData}
              disabled={isLoading || !isApiConnected}
            >
              <RefreshCw className={`h-4 w-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
              Refresh
            </Button>
          </div>

          {/* Error Display */}
          {error && (
            <Card className="border-destructive">
              <CardContent className="pt-6">
                <div className="flex items-center space-x-2 text-destructive">
                  <AlertCircle className="h-4 w-4" />
                  <span className="text-sm font-medium">{error}</span>
                </div>
              </CardContent>
            </Card>
          )}

          {/* System Overview */}
          <SystemOverview />

          {/* Agents Grid */}
          <div className="space-y-4">
            <h2 className="text-xl font-semibold">Agent Details</h2>
            {agents.length > 0 ? (
              <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-2">
                {agents.map((agent) => (
                  <AgentDetailCard key={agent.id} agent={agent} />
                ))}
              </div>
            ) : (
              <Card>
                <CardContent className="pt-6">
                  <div className="text-center py-8 text-muted-foreground">
                    <Users className="mx-auto h-12 w-12 mb-4 opacity-50" />
                    <p className="text-lg font-medium mb-2">No agents available</p>
                    <p className="text-sm">
                      {!isApiConnected 
                        ? 'Connect to the backend API to see your strategic agents'
                        : 'Check your backend configuration and try refreshing'
                      }
                    </p>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}