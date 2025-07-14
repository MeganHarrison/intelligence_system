'use client'

import { useState, useMemo } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { 
  BarChart3, 
  TrendingUp, 
  TrendingDown,
  Activity,
  Brain,
  Users,
  Clock,
  Target,
  Zap,
  RefreshCw,
  Download,
  Filter
} from 'lucide-react'
import { 
  LineChart, 
  Line, 
  AreaChart, 
  Area,
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts'
import { 
  useDashboardMetrics,
  useDashboardAgents,
  useDashboardActivities,
  useActiveWorkflows
} from '@/lib/stores/dashboard'
import { useChatSessions } from '@/lib/stores/chat'
import { useConnectionStatus } from '@/lib/providers/dashboard-provider'

// Mock data for demonstration - in a real app this would come from the backend
const generateMockData = () => {
  const dates = Array.from({ length: 30 }, (_, i) => {
    const date = new Date()
    date.setDate(date.getDate() - (29 - i))
    return date.toISOString().split('T')[0]
  })

  return {
    workflowActivity: dates.map((date, i) => ({
      date,
      workflows: Math.floor(Math.random() * 20) + 5,
      success: Math.floor(Math.random() * 18) + 4,
      avgDuration: Math.floor(Math.random() * 60) + 30
    })),
    agentPerformance: [
      { name: 'Intelligence Officer', performance: 94, tasks: 156, uptime: 99.9 },
      { name: 'Strategic Advisor', performance: 91, tasks: 89, uptime: 99.7 },
      { name: 'Execution Coordinator', performance: 88, tasks: 67, uptime: 99.5 },
      { name: 'AI Chief of Staff', performance: 96, tasks: 234, uptime: 99.8 }
    ],
    documentTypes: [
      { name: 'Strategic Plans', value: 45, color: '#3b82f6' },
      { name: 'Meeting Notes', value: 32, color: '#10b981' },
      { name: 'Reports', value: 28, color: '#f59e0b' },
      { name: 'Presentations', value: 23, color: '#ef4444' }
    ],
    chatMetrics: dates.slice(-7).map((date, i) => ({
      date: date.split('-').slice(1).join('/'),
      messages: Math.floor(Math.random() * 50) + 20,
      sessions: Math.floor(Math.random() * 10) + 5,
      avgResponseTime: Math.floor(Math.random() * 2000) + 500
    }))
  }
}

function MetricCard({ title, value, change, icon: Icon, trend }: {
  title: string
  value: string | number
  change?: string
  icon: any
  trend?: 'up' | 'down' | 'stable'
}) {
  const getTrendColor = () => {
    switch (trend) {
      case 'up': return 'text-green-600'
      case 'down': return 'text-red-600'
      case 'stable': return 'text-blue-600'
      default: return 'text-gray-600'
    }
  }

  const getTrendIcon = () => {
    switch (trend) {
      case 'up': return <TrendingUp className="h-3 w-3" />
      case 'down': return <TrendingDown className="h-3 w-3" />
      default: return null
    }
  }

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        <Icon className="h-4 w-4 text-muted-foreground" />
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        {change && (
          <div className={`flex items-center space-x-1 text-xs ${getTrendColor()}`}>
            {getTrendIcon()}
            <span>{change}</span>
          </div>
        )}
      </CardContent>
    </Card>
  )
}

function WorkflowAnalytics({ data }: { data: any[] }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Workflow Activity (30 Days)</CardTitle>
        <CardDescription>
          Daily workflow execution and success rates
        </CardDescription>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <AreaChart data={data}>
            <defs>
              <linearGradient id="colorWorkflows" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8}/>
                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0.1}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="date" 
              tick={{ fontSize: 12 }}
              tickFormatter={(value) => new Date(value).getMonth() + 1 + '/' + new Date(value).getDate()}
            />
            <YAxis tick={{ fontSize: 12 }} />
            <Tooltip 
              labelFormatter={(value) => `Date: ${value}`}
              formatter={(value, name) => [value, name === 'workflows' ? 'Total Workflows' : 'Successful']}
            />
            <Area 
              type="monotone" 
              dataKey="workflows" 
              stroke="#3b82f6" 
              fillOpacity={1}
              fill="url(#colorWorkflows)" 
            />
            <Area 
              type="monotone" 
              dataKey="success" 
              stroke="#10b981" 
              fillOpacity={0.6}
              fill="#10b981" 
            />
          </AreaChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}

function AgentPerformanceChart({ data }: { data: any[] }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Agent Performance</CardTitle>
        <CardDescription>
          Performance scores and task completion by agent
        </CardDescription>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="name" 
              tick={{ fontSize: 12 }}
              angle={-45}
              textAnchor="end"
              height={80}
            />
            <YAxis tick={{ fontSize: 12 }} />
            <Tooltip />
            <Bar dataKey="performance" fill="#3b82f6" name="Performance %" />
            <Bar dataKey="tasks" fill="#10b981" name="Tasks Completed" />
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}

function DocumentDistribution({ data }: { data: any[] }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Document Distribution</CardTitle>
        <CardDescription>
          Types of documents in the knowledge base
        </CardDescription>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={60}
              outerRadius={100}
              dataKey="value"
              nameKey="name"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
        <div className="mt-4 grid grid-cols-2 gap-2">
          {data.map((item) => (
            <div key={item.name} className="flex items-center space-x-2">
              <div 
                className="w-3 h-3 rounded-full" 
                style={{ backgroundColor: item.color }}
              />
              <span className="text-sm text-muted-foreground">
                {item.name}: {item.value}
              </span>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}

function ChatAnalytics({ data }: { data: any[] }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Chat Activity (7 Days)</CardTitle>
        <CardDescription>
          AI chat sessions and response times
        </CardDescription>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" tick={{ fontSize: 12 }} />
            <YAxis yAxisId="left" tick={{ fontSize: 12 }} />
            <YAxis yAxisId="right" orientation="right" tick={{ fontSize: 12 }} />
            <Tooltip />
            <Line 
              yAxisId="left"
              type="monotone" 
              dataKey="messages" 
              stroke="#3b82f6" 
              strokeWidth={2}
              name="Messages"
            />
            <Line 
              yAxisId="left"
              type="monotone" 
              dataKey="sessions" 
              stroke="#10b981" 
              strokeWidth={2}
              name="Sessions"
            />
            <Line 
              yAxisId="right"
              type="monotone" 
              dataKey="avgResponseTime" 
              stroke="#f59e0b" 
              strokeWidth={2}
              name="Avg Response Time (ms)"
            />
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}

export default function AnalyticsPage() {
  const metrics = useDashboardMetrics()
  const agents = useDashboardAgents()
  const activities = useDashboardActivities()
  const activeWorkflows = useActiveWorkflows()
  const chatSessions = useChatSessions()
  const { isApiConnected } = useConnectionStatus()

  const [refreshing, setRefreshing] = useState(false)

  const mockData = useMemo(() => generateMockData(), [])

  const handleRefresh = async () => {
    setRefreshing(true)
    // Simulate refresh delay
    await new Promise(resolve => setTimeout(resolve, 1000))
    setRefreshing(false)
  }

  const handleExport = () => {
    // Simulate export functionality
    console.log('Exporting analytics data...')
  }

  // Calculate real metrics
  const totalChatMessages = chatSessions.reduce((sum, session) => sum + session.messages.length, 0)
  const avgAgentPerformance = agents.length > 0 
    ? Math.round(agents.reduce((sum, agent) => sum + (agent.performanceScore || 0), 0) / agents.length)
    : 0

  return (
    <div className="bg-background">
      {/* Main Content */}
      <div className="container py-6">
        <div className="space-y-6">
          {/* Page Header */}
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold tracking-tight">Strategic Analytics</h1>
              <p className="text-muted-foreground">
                Performance metrics, insights, and business intelligence analytics
              </p>
            </div>
            <div className="flex items-center space-x-2">
              <Button 
                variant="outline" 
                size="sm"
                onClick={handleRefresh}
                disabled={refreshing}
              >
                <RefreshCw className={`h-4 w-4 mr-2 ${refreshing ? 'animate-spin' : ''}`} />
                Refresh
              </Button>
              <Button 
                variant="outline" 
                size="sm"
                onClick={handleExport}
              >
                <Download className="h-4 w-4 mr-2" />
                Export
              </Button>
            </div>
          </div>

          {/* Key Metrics */}
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <MetricCard
              title="Total Workflows"
              value={mockData.workflowActivity.reduce((sum, day) => sum + day.workflows, 0)}
              change="+12% from last month"
              icon={Brain}
              trend="up"
            />
            <MetricCard
              title="Agent Performance"
              value={`${avgAgentPerformance}%`}
              change="+3% from last week"
              icon={Users}
              trend="up"
            />
            <MetricCard
              title="Chat Messages"
              value={totalChatMessages}
              change="+8% from yesterday"
              icon={Activity}
              trend="up"
            />
            <MetricCard
              title="Success Rate"
              value="94.2%"
              change="+1.2% from last week"
              icon={Target}
              trend="up"
            />
          </div>

          {/* Analytics Tabs */}
          <Tabs defaultValue="workflows" className="space-y-4">
            <TabsList className="grid w-full grid-cols-4">
              <TabsTrigger value="workflows">Workflows</TabsTrigger>
              <TabsTrigger value="agents">Agents</TabsTrigger>
              <TabsTrigger value="chat">Chat</TabsTrigger>
              <TabsTrigger value="documents">Documents</TabsTrigger>
            </TabsList>

            <TabsContent value="workflows" className="space-y-4">
              <div className="grid gap-4 lg:grid-cols-1">
                <WorkflowAnalytics data={mockData.workflowActivity} />
              </div>
            </TabsContent>

            <TabsContent value="agents" className="space-y-4">
              <div className="grid gap-4 lg:grid-cols-1">
                <AgentPerformanceChart data={mockData.agentPerformance} />
              </div>
            </TabsContent>

            <TabsContent value="chat" className="space-y-4">
              <div className="grid gap-4 lg:grid-cols-1">
                <ChatAnalytics data={mockData.chatMetrics} />
              </div>
            </TabsContent>

            <TabsContent value="documents" className="space-y-4">
              <div className="grid gap-4 md:grid-cols-2">
                <DocumentDistribution data={mockData.documentTypes} />
                <Card>
                  <CardHeader>
                    <CardTitle>Document Insights</CardTitle>
                    <CardDescription>
                      Key statistics about your document library
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <div className="text-2xl font-bold">{metrics.totalDocuments || 128}</div>
                        <p className="text-xs text-muted-foreground">Total Documents</p>
                      </div>
                      <div>
                        <div className="text-2xl font-bold">245.7 MB</div>
                        <p className="text-xs text-muted-foreground">Total Size</p>
                      </div>
                      <div>
                        <div className="text-2xl font-bold">7</div>
                        <p className="text-xs text-muted-foreground">Recent Uploads</p>
                      </div>
                      <div>
                        <div className="text-2xl font-bold">2</div>
                        <p className="text-xs text-muted-foreground">Processing Queue</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  )
}