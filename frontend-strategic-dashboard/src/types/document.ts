import { Database } from './supabase';

// Use the auto-generated Supabase types for strategic documents
export type DatabaseStrategicDocument = Database['public']['Tables']['strategic_documents']['Row'];
export type StrategicDocumentInsert = Database['public']['Tables']['strategic_documents']['Insert'];
export type StrategicDocumentUpdate = Database['public']['Tables']['strategic_documents']['Update'];

// Frontend display type for strategic documents
export interface StrategicDocument {
  id: string;
  title: string;
  content?: string;
  document_type?: string;
  file_path?: string;
  file_size?: number;
  mime_type?: string;
  source_file?: string;
  source_meeting_id?: string;
  project_id?: string;
  client_id?: number;
  client_name?: string; // populated from join
  project_name?: string; // populated from join
  file_url?: string; // URL to access the file
  created_at: string;
  updated_at?: string;
}

export interface StrategicDocumentsResponse {
  documents: StrategicDocument[];
  total_count: number;
  status: string;
}

// Helper function to transform database document to frontend document
export function transformDocumentForUI(dbDocument: DatabaseStrategicDocument): StrategicDocument {
  return {
    id: dbDocument.id,
    title: dbDocument.title,
    content: dbDocument.content || undefined,
    document_type: dbDocument.document_type || undefined,
    file_path: dbDocument.file_path || undefined,
    file_size: dbDocument.file_size || undefined,
    mime_type: dbDocument.mime_type || undefined,
    source_file: dbDocument.source_file || undefined,
    source_meeting_id: dbDocument.source_meeting_id || undefined,
    project_id: dbDocument.project_id || undefined,
    client_id: dbDocument.client_id || undefined,
    client_name: undefined, // Will be populated from join
    project_name: undefined, // Will be populated from join
    created_at: dbDocument.created_at || new Date().toISOString(),
    updated_at: dbDocument.updated_at || undefined,
  };
}