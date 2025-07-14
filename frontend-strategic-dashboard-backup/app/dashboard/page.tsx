'use client'

import { Suspense } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { 
  Brain, 
  MessageSquare, 
  FileSearch, 
  Users, 
  TrendingUp, 
  Activity,
  Clock,
  CheckCircle,
  AlertCircle,
  Settings,
  RefreshCw,
  Wifi,
  WifiOff
} from 'lucide-react'
import { 
  useDashboardMetrics, 
  useDashboardAgents, 
  useDashboardActivities,
  useDashboardUI,
  useActiveWorkflows
} from '@/lib/stores/dashboard'
import { useDashboard, useConnectionStatus } from '@/lib/providers/dashboard-provider'

function MetricsCard({ title, value, description, icon: Icon, trend }: {
  title: string
  value: string | number
  description: string
  icon: any
  trend?: 'up' | 'down' | 'stable'
}) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        <Icon className="h-4 w-4 text-muted-foreground" />
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        <p className="text-xs text-muted-foreground mt-1">{description}</p>
        {trend && (
          <div className="flex items-center mt-2">
            <TrendingUp className={`h-3 w-3 mr-1 ${
              trend === 'up' ? 'text-green-500' : 
              trend === 'down' ? 'text-red-500' : 'text-gray-500'
            }`} />
            <span className="text-xs text-muted-foreground">
              {trend === 'up' ? 'Improving' : trend === 'down' ? 'Declining' : 'Stable'}
            </span>
          </div>
        )}
      </CardContent>
    </Card>
  )
}

function AgentCard({ agent }: { agent: any }) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-500'
      case 'processing': return 'bg-yellow-500'
      case 'inactive': return 'bg-gray-500'
      default: return 'bg-gray-500'
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active': return <CheckCircle className="h-4 w-4" />
      case 'processing': return <Clock className="h-4 w-4" />
      case 'inactive': return <AlertCircle className="h-4 w-4" />
      default: return <AlertCircle className="h-4 w-4" />
    }
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg">{agent.name}</CardTitle>
          <Badge variant="outline" className="flex items-center gap-1">
            {getStatusIcon(agent.status)}
            {agent.status}
          </Badge>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          <div>
            <div className="flex justify-between text-sm mb-1">
              <span>Performance</span>
              <span>{agent.performance}%</span>
            </div>
            <Progress value={agent.performance} className="h-2" />
          </div>
          <div className="flex justify-between text-sm text-muted-foreground">
            <span>Tasks Completed</span>
            <span>{agent.tasksCompleted}</span>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

function QuickActions() {
  const { executeWorkflow } = useDashboard()
  const { isFullyConnected } = useConnectionStatus()

  const handleStrategicAnalysis = () => {
    executeWorkflow("What are our current strategic priorities and key execution gaps?")
  }

  const handleMarketAnalysis = () => {
    executeWorkflow("Provide a comprehensive market analysis based on our current documents")
  }

  const handleCompetitiveAnalysis = () => {
    executeWorkflow("Analyze our competitive position and recommend strategic improvements")
  }

  const handleRiskAssessment = () => {
    executeWorkflow("Conduct a strategic risk assessment of our current initiatives")
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Quick Actions</CardTitle>
        <CardDescription>
          Launch strategic workflows and analysis tools
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-3">
        <Button 
          className="w-full justify-start" 
          variant="outline"
          onClick={handleStrategicAnalysis}
          disabled={!isFullyConnected}
        >
          <Brain className="mr-2 h-4 w-4" />
          Strategic Analysis
        </Button>
        <Button 
          className="w-full justify-start" 
          variant="outline"
          onClick={handleMarketAnalysis}
          disabled={!isFullyConnected}
        >
          <TrendingUp className="mr-2 h-4 w-4" />
          Market Analysis
        </Button>
        <Button 
          className="w-full justify-start" 
          variant="outline"
          onClick={handleCompetitiveAnalysis}
          disabled={!isFullyConnected}
        >
          <Users className="mr-2 h-4 w-4" />
          Competitive Analysis
        </Button>
        <Button 
          className="w-full justify-start" 
          variant="outline"
          onClick={handleRiskAssessment}
          disabled={!isFullyConnected}
        >
          <AlertCircle className="mr-2 h-4 w-4" />
          Risk Assessment
        </Button>
        {!isFullyConnected && (
          <p className="text-xs text-muted-foreground mt-2">
            Connect to backend to enable workflows
          </p>
        )}
      </CardContent>
    </Card>
  )
}

function RecentActivity() {
  const activities = useDashboardActivities()

  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'workflow': return 'bg-blue-500'
      case 'document': return 'bg-green-500'
      case 'chat': return 'bg-purple-500'
      case 'analysis': return 'bg-yellow-500'
      default: return 'bg-gray-500'
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Recent Activity</CardTitle>
        <CardDescription>
          Latest updates from your strategic intelligence system
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {activities.length > 0 ? (
            activities.slice(0, 5).map((activity) => (
              <div key={activity.id} className="flex items-start space-x-3">
                <div className={`w-2 h-2 ${getActivityIcon(activity.type)} rounded-full mt-2 flex-shrink-0`} />
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900 dark:text-gray-100">
                    {activity.description}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    {activity.timestamp}
                  </p>
                </div>
                <Badge variant="outline" className="text-xs">
                  {activity.status}
                </Badge>
              </div>
            ))
          ) : (
            <div className="text-center py-8 text-muted-foreground">
              <Activity className="mx-auto h-8 w-8 mb-2 opacity-50" />
              <p className="text-sm">No recent activity</p>
              <p className="text-xs">Start a workflow to see activity here</p>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  )
}

function DashboardSkeleton() {
  return (
    <div className="space-y-6">
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {[1, 2, 3, 4].map((i) => (
          <Card key={i}>
            <CardHeader className="animate-pulse">
              <div className="h-4 bg-gray-200 rounded w-1/2"></div>
            </CardHeader>
            <CardContent className="animate-pulse">
              <div className="h-8 bg-gray-200 rounded w-1/3 mb-2"></div>
              <div className="h-3 bg-gray-200 rounded w-full"></div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}

export default function DashboardPage() {
  const metrics = useDashboardMetrics()
  const agents = useDashboardAgents()
  const activeWorkflows = useActiveWorkflows()
  const { isLoading, error } = useDashboardUI()
  const { refreshData } = useDashboard()
  const { isFullyConnected, isApiConnected, isWebSocketConnected } = useConnectionStatus()

  return (
    <div className="bg-background">
      {/* Main Content */}
      <div className="container py-6">
        <div className="space-y-6">
          {/* Welcome Section */}
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold tracking-tight">Welcome back!</h1>
              <p className="text-muted-foreground">
                Your strategic intelligence system is running smoothly. Here's what's happening:
              </p>
            </div>
            <Button 
              variant="outline"
              onClick={refreshData}
              disabled={isLoading || !isApiConnected}
            >
              <RefreshCw className={`h-4 w-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
              Refresh Data
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

          {/* Metrics Cards */}
          <Suspense fallback={<DashboardSkeleton />}>
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
              <MetricsCard
                title="Total Documents"
                value={metrics.totalDocuments || 0}
                description="Processed and indexed"
                icon={FileSearch}
                trend="up"
              />
              <MetricsCard
                title="Recent Activity"
                value={metrics.recentActivity || 0}
                description="Actions in the last 24h"
                icon={Activity}
                trend="up"
              />
              <MetricsCard
                title="Confidence Score"
                value={`${metrics.confidenceScore || 0}%`}
                description="AI analysis accuracy"
                icon={TrendingUp}
                trend="stable"
              />
              <MetricsCard
                title="Active Workflows"
                value={activeWorkflows.length}
                description="Currently processing"
                icon={Brain}
                trend="stable"
              />
            </div>
          </Suspense>

          {/* Main Dashboard Tabs */}
          <Tabs defaultValue="overview" className="space-y-4">
            <TabsList className="grid w-full grid-cols-4">
              <TabsTrigger value="overview">Overview</TabsTrigger>
              <TabsTrigger value="agents">Agents</TabsTrigger>
              <TabsTrigger value="workflows">Workflows</TabsTrigger>
              <TabsTrigger value="analytics">Analytics</TabsTrigger>
            </TabsList>

            <TabsContent value="overview" className="space-y-4">
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                <div className="lg:col-span-2 space-y-4">
                  <RecentActivity />
                </div>
                <div className="space-y-4">
                  <QuickActions />
                </div>
              </div>
            </TabsContent>

            <TabsContent value="agents" className="space-y-4">
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-2">
                {agents.length > 0 ? (
                  agents.map((agent) => (
                    <AgentCard key={agent.id} agent={agent} />
                  ))
                ) : (
                  <Card className="col-span-2">
                    <CardContent className="pt-6">
                      <div className="text-center py-8 text-muted-foreground">
                        <Users className="mx-auto h-12 w-12 mb-4 opacity-50" />
                        <p>No agents available</p>
                        <p className="text-sm">Check backend connection</p>
                      </div>
                    </CardContent>
                  </Card>
                )}
              </div>
            </TabsContent>

            <TabsContent value="workflows" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle>Active Workflows</CardTitle>
                  <CardDescription>
                    Monitor and manage running strategic analysis workflows
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  {activeWorkflows.length > 0 ? (
                    <div className="space-y-4">
                      {activeWorkflows.map((workflow) => (
                        <Card key={workflow.id}>
                          <CardContent className="pt-6">
                            <div className="space-y-3">
                              <div className="flex justify-between items-start">
                                <div className="flex-1">
                                  <h4 className="font-medium text-sm">{workflow.query}</h4>
                                  <p className="text-xs text-muted-foreground">{workflow.currentStep}</p>
                                </div>
                                <Badge variant="outline">
                                  {workflow.status}
                                </Badge>
                              </div>
                              <div>
                                <div className="flex justify-between text-xs mb-1">
                                  <span>Progress</span>
                                  <span>{workflow.progress}%</span>
                                </div>
                                <Progress value={workflow.progress} className="h-2" />
                              </div>
                              <div className="text-xs text-muted-foreground">
                                Started: {new Date(workflow.startTime).toLocaleTimeString()}
                              </div>
                            </div>
                          </CardContent>
                        </Card>
                      ))}
                    </div>
                  ) : (
                    <div className="text-center py-8 text-muted-foreground">
                      <Brain className="mx-auto h-12 w-12 mb-4 opacity-50" />
                      <p>No active workflows</p>
                      <p className="text-sm">Start a new strategic analysis to see workflows here</p>
                    </div>
                  )}
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="analytics" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle>Analytics & Insights</CardTitle>
                  <CardDescription>
                    Strategic performance metrics and business intelligence
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="text-center py-8 text-muted-foreground">
                    <TrendingUp className="mx-auto h-12 w-12 mb-4 opacity-50" />
                    <p>Analytics dashboard coming soon</p>
                    <p className="text-sm">Advanced charts and insights will be available here</p>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  )
}