'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { 
  LayoutDashboard, 
  Users, 
  MessageSquare, 
  BarChart3,
  FileText,
  Settings,
  Brain,
  Activity
} from 'lucide-react'
import { useConnectionStatus } from '@/lib/providers/dashboard-provider'
import { useActiveWorkflows, useChatSessions } from '@/lib/hooks/use-ssr-safe-store'

const navigationItems = [
  {
    title: 'Overview',
    href: '/dashboard',
    icon: LayoutDashboard,
    description: 'Main dashboard and metrics'
  },
  {
    title: 'Agents',
    href: '/dashboard/agents',
    icon: Users,
    description: 'Strategic agent management'
  },
  {
    title: 'Chat',
    href: '/dashboard/chat',
    icon: MessageSquare,
    description: 'AI strategic assistant'
  },
  {
    title: 'Analytics',
    href: '/dashboard/analytics',
    icon: BarChart3,
    description: 'Performance insights'
  },
  {
    title: 'Documents',
    href: '/dashboard/documents',
    icon: FileText,
    description: 'Document management'
  }
]

interface DashboardNavProps {
  className?: string
  collapsed?: boolean
}

// Component for store-dependent badge counts
function NavBadge({ href }: { href: string }) {
  try {
    const activeWorkflows = useActiveWorkflows()
    const chatSessions = useChatSessions()

    const getBadgeCount = (href: string) => {
      switch (href) {
        case '/dashboard':
          return activeWorkflows?.length > 0 ? activeWorkflows.length : null
        case '/dashboard/chat':
          return chatSessions?.length > 0 ? chatSessions.length : null
        default:
          return null
      }
    }

    const badgeCount = getBadgeCount(href)
    
    if (!badgeCount) return null
    
    return (
      <Badge variant="default" className="ml-2 text-xs">
        {badgeCount}
      </Badge>
    )
  } catch (error) {
    console.warn('Error rendering NavBadge:', error)
    return null
  }
}

// Component for store-dependent status
function StatusSection({ collapsed }: { collapsed: boolean }) {
  try {
    const { isFullyConnected } = useConnectionStatus()
    const activeWorkflows = useActiveWorkflows()
    const chatSessions = useChatSessions()

    if (collapsed) return null

    return (
      <div className="pt-4 mt-4 border-t">
        <div className="px-3 py-2">
          <div className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground">System Status</span>
            <Badge variant={isFullyConnected ? 'default' : 'destructive'} className="text-xs">
              {isFullyConnected ? 'Online' : 'Offline'}
            </Badge>
          </div>
          <div className="mt-2 space-y-1 text-xs text-muted-foreground">
            <div className="flex items-center justify-between">
              <span>Active Workflows</span>
              <span>{activeWorkflows?.length || 0}</span>
            </div>
            <div className="flex items-center justify-between">
              <span>Chat Sessions</span>
              <span>{chatSessions?.length || 0}</span>
            </div>
          </div>
        </div>
      </div>
    )
  } catch (error) {
    console.warn('Error rendering StatusSection:', error)
    return null
  }
}

export function DashboardNav({ className, collapsed = false }: DashboardNavProps) {
  const pathname = usePathname()

  const isActive = (href: string) => {
    if (href === '/dashboard') {
      return pathname === href
    }
    return pathname.startsWith(href)
  }

  return (
    <nav className={cn('space-y-2', className)}>
      {navigationItems.map((item) => {
        const active = isActive(item.href)
        
        return (
          <Link key={item.href} href={item.href}>
            <Button
              variant={active ? 'default' : 'ghost'}
              className={cn(
                'w-full justify-start h-12',
                active && 'bg-primary text-primary-foreground',
                collapsed && 'px-2'
              )}
            >
              <item.icon className={cn('h-5 w-5', collapsed ? '' : 'mr-3')} />
              {!collapsed && (
                <>
                  <span className="flex-1 text-left">{item.title}</span>
                  <NavBadge href={item.href} />
                </>
              )}
            </Button>
          </Link>
        )
      })}

      {/* Connection Status */}
      <StatusSection collapsed={collapsed} />

      {/* Quick Actions */}
      {!collapsed && (
        <div className="pt-4 space-y-2">
          <p className="px-3 text-xs font-medium text-muted-foreground uppercase tracking-wider">
            Quick Actions
          </p>
          <Button variant="outline" size="sm" className="w-full justify-start h-9">
            <Brain className="h-4 w-4 mr-2" />
            Strategic Analysis
          </Button>
          <Button variant="outline" size="sm" className="w-full justify-start h-9">
            <Activity className="h-4 w-4 mr-2" />
            System Health
          </Button>
        </div>
      )}
    </nav>
  )
}

export default DashboardNav