"use client";

import { useEffect, useState } from 'react';
import axios from 'axios';

interface HealthData {
  status: string;
  timestamp: string;
  components: {
    doc_extractor: boolean;
    strategic_workflow: boolean;
    business_system: boolean;
    ai_chief: boolean;
  };
  active_connections: number;
  active_workflows: number;
}

export default function Dashboard() {
  const [healthData, setHealthData] = useState<HealthData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchHealth = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/health');
        setHealthData(response.data);
        setError(null);
      } catch (err) {
        setError('Failed to connect to backend');
        console.error('Backend connection error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchHealth();
    const interval = setInterval(fetchHealth, 5000); // Update every 5 seconds

    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-500 text-6xl mb-4">⚠️</div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Backend Connection Error</h1>
          <p className="text-gray-600 mb-4">{error}</p>
          <p className="text-sm text-gray-500">Make sure the backend server is running on port 8000</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Strategic Intelligence Dashboard</h1>
          <p className="mt-2 text-gray-600">Real-time system status and operations</p>
        </div>

        {/* System Status */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className={`h-3 w-3 rounded-full ${healthData?.status === 'healthy' ? 'bg-green-500' : 'bg-red-500'}`}></div>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">System Status</dt>
                    <dd className="text-lg font-medium text-gray-900 capitalize">{healthData?.status}</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="h-3 w-3 rounded-full bg-blue-500"></div>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">Active Connections</dt>
                    <dd className="text-lg font-medium text-gray-900">{healthData?.active_connections}</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="h-3 w-3 rounded-full bg-purple-500"></div>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">Active Workflows</dt>
                    <dd className="text-lg font-medium text-gray-900">{healthData?.active_workflows}</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Intelligence Components */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">Intelligence Components</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {healthData?.components && Object.entries(healthData.components).map(([component, status]) => (
                <div key={component} className="flex items-center justify-between p-3 border rounded-lg">
                  <div>
                    <p className="text-sm font-medium text-gray-900 capitalize">
                      {component.replace(/_/g, ' ')}
                    </p>
                    <p className={`text-xs ${status ? 'text-green-600' : 'text-red-600'}`}>
                      {status ? 'Active' : 'Inactive'}
                    </p>
                  </div>
                  <div className={`h-2 w-2 rounded-full ${status ? 'bg-green-500' : 'bg-red-500'}`}></div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Last Updated */}
        <div className="mt-8 text-center">
          <p className="text-sm text-gray-500">
            Last updated: {new Date(healthData?.timestamp || '').toLocaleString()}
          </p>
        </div>
      </div>
    </div>
  );
}