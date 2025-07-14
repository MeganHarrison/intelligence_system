import { Database } from './supabase';

// Use the auto-generated Supabase types
export type DatabaseProject = Database['public']['Tables']['project']['Row'];
export type ProjectInsert = Database['public']['Tables']['project']['Insert'];
export type ProjectUpdate = Database['public']['Tables']['project']['Update'];

// Frontend display type (mapped from database for cleaner UI)
export interface Project {
  id: string; // mapped from project_number
  name: string;
  description?: string;
  project_type?: string;
  status: string;
  priority: string;
  start_date?: string;
  end_date?: string; // mapped from est_completion
  budget?: number; // mapped from est_revenue (represents estimated revenue)
  actual_cost?: number;
  progress_percentage: number;
  project_manager?: string;
  client_name?: string; // populated from join
  client_company?: string; // populated from join
  created_at: string;
  updated_at: string;
}

// Helper function to transform database project to frontend project
export function transformProjectForUI(dbProject: DatabaseProject): Project {
  return {
    id: dbProject.project_number,
    name: dbProject.name || '',
    description: dbProject.description || undefined,
    project_type: dbProject.project_type || undefined,
    status: dbProject.status || 'unknown',
    priority: dbProject.priority || 'medium',
    start_date: dbProject.start_date || undefined,
    end_date: dbProject.est_completion || undefined,
    budget: dbProject.est_revenue || undefined,
    actual_cost: dbProject.actual_cost || undefined,
    progress_percentage: dbProject.progress_percentage || 0,
    project_manager: dbProject.project_manager || undefined,
    client_name: undefined, // Will be populated from join
    client_company: undefined, // Will be populated from join
    created_at: dbProject.created_at,
    updated_at: dbProject.updated_at || dbProject.created_at,
  };
}

export interface ProjectsResponse {
  projects: Project[];
  total_count: number;
  status: string;
}