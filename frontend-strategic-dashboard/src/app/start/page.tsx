import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 sm:text-6xl">
            Strategic Intelligence
            <span className="text-blue-600"> Dashboard</span>
          </h1>
          <p className="mt-6 text-lg text-gray-600 max-w-3xl mx-auto">
            Your AI-powered command center for business intelligence, strategic analysis, 
            and operational insights. Connect with your AI Chief of Staff and monitor 
            your strategic operations in real-time.
          </p>
        </div>

        <div className="mt-12 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Dashboard Card */}
          <Link
            href="/dashboard"
            className="group relative bg-white p-6 rounded-xl shadow-sm border border-gray-200 hover:shadow-lg transition-shadow"
          >
            <div className="text-3xl mb-4">📊</div>
            <h3 className="text-xl font-semibold text-gray-900 group-hover:text-blue-600">
              System Dashboard
            </h3>
            <p className="mt-2 text-gray-600">
              Monitor system health, intelligence components, and real-time operational metrics.
            </p>
            <div className="mt-4 text-blue-600 text-sm font-medium">
              View Dashboard →
            </div>
          </Link>

          {/* Projects Card */}
          <Link
            href="/projects"
            className="group relative bg-white p-6 rounded-xl shadow-sm border border-gray-200 hover:shadow-lg transition-shadow"
          >
            <div className="text-3xl mb-4">🚀</div>
            <h3 className="text-xl font-semibold text-gray-900 group-hover:text-blue-600">
              Projects Portfolio
            </h3>
            <p className="mt-2 text-gray-600">
              Manage and monitor your project portfolio with real-time insights and analytics.
            </p>
            <div className="mt-4 text-blue-600 text-sm font-medium">
              View Projects →
            </div>
          </Link>

          {/* Chat Card */}
          <Link
            href="/chat"
            className="group relative bg-white p-6 rounded-xl shadow-sm border border-gray-200 hover:shadow-lg transition-shadow"
          >
            <div className="text-3xl mb-4">🤖</div>
            <h3 className="text-xl font-semibold text-gray-900 group-hover:text-blue-600">
              AI Strategic Chat
            </h3>
            <p className="mt-2 text-gray-600">
              Chat with your AI Chief of Staff for strategic insights and business intelligence.
            </p>
            <div className="mt-4 text-blue-600 text-sm font-medium">
              Start Chat →
            </div>
          </Link>

          {/* Analytics Card */}
          <div className="group relative bg-white p-6 rounded-xl shadow-sm border border-gray-200 opacity-75">
            <div className="text-3xl mb-4">📈</div>
            <h3 className="text-xl font-semibold text-gray-500">
              Analytics & Reports
            </h3>
            <p className="mt-2 text-gray-500">
              Advanced analytics, trend analysis, and strategic reporting capabilities.
            </p>
            <div className="mt-4 text-gray-400 text-sm font-medium">
              Coming Soon
            </div>
          </div>
        </div>

        <div className="mt-16 bg-blue-50 rounded-xl p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Quick Start</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm">
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">1. Check System Status</h3>
              <p className="text-gray-600">
                Visit the dashboard to ensure all intelligence components are running properly.
              </p>
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">2. Review Projects</h3>
              <p className="text-gray-600">
                Monitor your project portfolio and track progress across all active initiatives.
              </p>
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">3. Start Strategic Chat</h3>
              <p className="text-gray-600">
                Chat with your AI Chief of Staff to get business insights and strategic analysis.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}