// app/dashboard/layout.tsx
'use client'

import { ReactNode } from 'react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import DashboardNav from '@/components/navigation/dashboard-nav'
import { 
  Menu,
  Settings,
  User,
  Bell,
  Wifi,
  WifiOff
} from 'lucide-react'
import { useState } from 'react'
import { useConnectionStatus } from '@/lib/providers/dashboard-provider'

interface DashboardLayoutProps {
  children: ReactNode
}

export default function DashboardLayout({ children }: DashboardLayoutProps) {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)
  const { isFullyConnected } = useConnectionStatus()

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-14 items-center">
          {/* Logo and Navigation Toggle */}
          <div className="flex items-center space-x-4">
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
              className="md:hidden"
            >
              <Menu className="h-5 w-5" />
            </Button>
            
            <div className="font-bold text-xl">
              Strategic Intelligence
            </div>
          </div>

          {/* Center - Connection Status */}
          <div className="flex-1 flex justify-center">
            <Badge variant={isFullyConnected ? "default" : "destructive"} className="flex items-center gap-1">
              {isFullyConnected ? (
                <>
                  <Wifi className="h-3 w-3" />
                  Online
                </>
              ) : (
                <>
                  <WifiOff className="h-3 w-3" />
                  Offline
                </>
              )}
            </Badge>
          </div>

          {/* Right side actions */}
          <div className="flex items-center space-x-2">
            <Button variant="ghost" size="icon">
              <Bell className="h-4 w-4" />
            </Button>
            <Button variant="ghost" size="icon">
              <Settings className="h-4 w-4" />
            </Button>
            <Button variant="ghost" size="icon">
              <User className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <aside className={`fixed inset-y-0 left-0 z-40 w-64 transform bg-background border-r transition-transform duration-200 ease-in-out ${
          sidebarCollapsed ? '-translate-x-full md:translate-x-0 md:w-16' : 'translate-x-0'
        } md:relative md:inset-auto md:transform-none`}>
          <div className="flex h-full flex-col">
            <div className="flex-1 overflow-y-auto p-4 pt-8">
              <DashboardNav collapsed={sidebarCollapsed} />
            </div>
          </div>
        </aside>

        {/* Main content */}
        <main className="flex-1 overflow-x-hidden">
          <div className="p-6">
            {children}
          </div>
        </main>
      </div>

      {/* Sidebar backdrop for mobile */}
      {!sidebarCollapsed && (
        <div 
          className="fixed inset-0 z-30 bg-black/50 md:hidden"
          onClick={() => setSidebarCollapsed(true)}
        />
      )}
    </div>
  )
}