import { Project } from '@/types/project';

interface ProjectCardProps {
  project: Project;
}

const statusColors = {
  'planning': 'bg-blue-100 text-blue-800',
  'active': 'bg-green-100 text-green-800',
  'on_hold': 'bg-yellow-100 text-yellow-800',
  'completed': 'bg-gray-100 text-gray-800',
  'cancelled': 'bg-red-100 text-red-800'
};

const priorityColors = {
  'high': 'bg-red-100 text-red-800',
  'medium': 'bg-yellow-100 text-yellow-800',
  'low': 'bg-green-100 text-green-800'
};

export function ProjectCard({ project }: ProjectCardProps) {
  const costToRevenueRatio = project.budget && project.budget > 0 
    ? (project.actual_cost || 0) / project.budget * 100 
    : 0;

  const formatCurrency = (amount?: number) => {
    if (!amount) return '$0';
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  };

  const formatDate = (dateString?: string) => {
    if (!dateString) return 'Not set';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const getProgressColor = (percentage: number) => {
    if (percentage >= 80) return 'bg-green-500';
    if (percentage >= 50) return 'bg-blue-500';
    if (percentage >= 25) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  const getCostHealthColor = (ratio: number) => {
    if (ratio <= 50) return 'text-green-600';  // Low cost compared to revenue
    if (ratio <= 75) return 'text-yellow-600'; // Moderate cost ratio
    return 'text-red-600'; // High cost ratio
  };

  return (
    <div className="bg-white rounded-lg border border-gray-200 shadow-sm hover:shadow-md transition-shadow duration-200">
      {/* Header */}
      <div className="p-6 border-b border-gray-100">
        <div className="flex items-start justify-between">
          <div className="flex-1 min-w-0">
            <h3 className="text-lg font-semibold text-gray-900 truncate">
              {project.name}
            </h3>
            {project.client_name && (
              <p className="text-sm text-gray-600 mt-1">
                {project.client_name}
                {project.client_company && ` (${project.client_company})`}
              </p>
            )}
            {project.description && (
              <p className="text-sm text-gray-500 mt-2 line-clamp-2">
                {project.description}
              </p>
            )}
          </div>
          <div className="flex flex-col items-end space-y-2 ml-4">
            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
              statusColors[project.status as keyof typeof statusColors] || 'bg-gray-100 text-gray-800'
            }`}>
              {project.status.replace('_', ' ')}
            </span>
            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
              priorityColors[project.priority as keyof typeof priorityColors] || 'bg-gray-100 text-gray-800'
            }`}>
              {project.priority} priority
            </span>
          </div>
        </div>
      </div>

      {/* Progress and Metrics */}
      <div className="p-6 space-y-4">
        {/* Progress Bar */}
        <div>
          <div className="flex items-center justify-between text-sm mb-2">
            <span className="text-gray-600">Progress</span>
            <span className="font-medium text-gray-900">{project.progress_percentage}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className={`h-2 rounded-full transition-all duration-300 ${getProgressColor(project.progress_percentage)}`}
              style={{ width: `${project.progress_percentage}%` }}
            ></div>
          </div>
        </div>

        {/* Revenue Information */}
        {project.budget && (
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span className="text-gray-600">Est. Revenue</span>
              <p className="font-medium text-gray-900">{formatCurrency(project.budget)}</p>
            </div>
            <div>
              <span className="text-gray-600">Actual Cost</span>
              <p className={`font-medium ${getCostHealthColor(costToRevenueRatio)}`}>
                {formatCurrency(project.actual_cost)}
              </p>
            </div>
          </div>
        )}

        {/* Project Details */}
        <div className="grid grid-cols-1 gap-3 text-sm border-t border-gray-100 pt-4">
          {project.project_type && (
            <div className="flex justify-between">
              <span className="text-gray-600">Type</span>
              <span className="font-medium text-gray-900 capitalize">
                {project.project_type.replace('_', ' ')}
              </span>
            </div>
          )}
          
          {project.project_manager && (
            <div className="flex justify-between">
              <span className="text-gray-600">Manager</span>
              <span className="font-medium text-gray-900">{project.project_manager}</span>
            </div>
          )}

          <div className="flex justify-between">
            <span className="text-gray-600">Start Date</span>
            <span className="font-medium text-gray-900">{formatDate(project.start_date)}</span>
          </div>

          <div className="flex justify-between">
            <span className="text-gray-600">End Date</span>
            <span className="font-medium text-gray-900">{formatDate(project.end_date)}</span>
          </div>

          {costToRevenueRatio > 0 && (
            <div className="flex justify-between">
              <span className="text-gray-600">Cost Ratio</span>
              <span className={`font-medium ${getCostHealthColor(costToRevenueRatio)}`}>
                {costToRevenueRatio.toFixed(1)}%
              </span>
            </div>
          )}
        </div>
      </div>

      {/* Footer */}
      <div className="px-6 py-3 bg-gray-50 rounded-b-lg">
        <div className="flex items-center justify-between text-xs text-gray-500">
          <span>Created: {formatDate(project.created_at)}</span>
          <span>Updated: {formatDate(project.updated_at)}</span>
        </div>
      </div>
    </div>
  );
}