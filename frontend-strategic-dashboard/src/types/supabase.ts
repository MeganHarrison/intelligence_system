export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export type Database = {
  // Allows to automatically instanciate createClient with right options
  // instead of createClient<Database, { PostgrestVersion: 'XX' }>(URL, KEY)
  __InternalSupabase: {
    PostgrestVersion: "12.2.3 (519615d)"
  }
  public: {
    Tables: {
      alleato: {
        Row: {
          created_at: string | null
          data: string
          id: number
        }
        Insert: {
          created_at?: string | null
          data: string
          id?: never
        }
        Update: {
          created_at?: string | null
          data?: string
          id?: never
        }
        Relationships: []
      }
      categories: {
        Row: {
          id: number
          name: string | null
        }
        Insert: {
          id?: never
          name?: string | null
        }
        Update: {
          id?: never
          name?: string | null
        }
        Relationships: []
      }
      chat_sessions: {
        Row: {
          created_at: string | null
          id: string
        }
        Insert: {
          created_at?: string | null
          id?: string
        }
        Update: {
          created_at?: string | null
          id?: string
        }
        Relationships: []
      }
      chats: {
        Row: {
          created_at: string
          id: string
          title: string | null
          updated_at: string
          user_id: string
        }
        Insert: {
          created_at?: string
          id?: string
          title?: string | null
          updated_at?: string
          user_id: string
        }
        Update: {
          created_at?: string
          id?: string
          title?: string | null
          updated_at?: string
          user_id?: string
        }
        Relationships: [
          {
            foreignKeyName: "chats_user_id_fkey"
            columns: ["user_id"]
            isOneToOne: false
            referencedRelation: "users"
            referencedColumns: ["id"]
          },
        ]
      }
      clients: {
        Row: {
          address: string | null
          avatar: string | null
          company: string | null
          created_at: string | null
          email: string | null
          id: number
          industry: string | null
          metadata: Json | null
          name: string
          notes: string | null
          phone: string | null
          status: string | null
          tier: string | null
          updated_at: string | null
          website: string | null
        }
        Insert: {
          address?: string | null
          avatar?: string | null
          company?: string | null
          created_at?: string | null
          email?: string | null
          id?: never
          industry?: string | null
          metadata?: Json | null
          name: string
          notes?: string | null
          phone?: string | null
          status?: string | null
          tier?: string | null
          updated_at?: string | null
          website?: string | null
        }
        Update: {
          address?: string | null
          avatar?: string | null
          company?: string | null
          created_at?: string | null
          email?: string | null
          id?: never
          industry?: string | null
          metadata?: Json | null
          name?: string
          notes?: string | null
          phone?: string | null
          status?: string | null
          tier?: string | null
          updated_at?: string | null
          website?: string | null
        }
        Relationships: []
      }
      code_examples: {
        Row: {
          chunk_number: number
          content: string
          created_at: string
          embedding: string | null
          id: number
          metadata: Json
          source_id: string
          summary: string
          url: string
        }
        Insert: {
          chunk_number: number
          content: string
          created_at?: string
          embedding?: string | null
          id?: number
          metadata?: Json
          source_id: string
          summary: string
          url: string
        }
        Update: {
          chunk_number?: number
          content?: string
          created_at?: string
          embedding?: string | null
          id?: number
          metadata?: Json
          source_id?: string
          summary?: string
          url?: string
        }
        Relationships: [
          {
            foreignKeyName: "code_examples_source_id_fkey"
            columns: ["source_id"]
            isOneToOne: false
            referencedRelation: "sources"
            referencedColumns: ["source_id"]
          },
        ]
      }
      crawled_pages: {
        Row: {
          chunk_number: number
          content: string
          created_at: string
          embedding: string | null
          id: number
          metadata: Json
          source_id: string
          url: string
        }
        Insert: {
          chunk_number: number
          content: string
          created_at?: string
          embedding?: string | null
          id?: number
          metadata?: Json
          source_id: string
          url: string
        }
        Update: {
          chunk_number?: number
          content?: string
          created_at?: string
          embedding?: string | null
          id?: number
          metadata?: Json
          source_id?: string
          url?: string
        }
        Relationships: [
          {
            foreignKeyName: "crawled_pages_source_id_fkey"
            columns: ["source_id"]
            isOneToOne: false
            referencedRelation: "sources"
            referencedColumns: ["source_id"]
          },
        ]
      }
      credit_card_transactions: {
        Row: {
          account_remarks: string | null
          card_number: string | null
          category: string | null
          cost_code: string | null
          cost_type: string | null
          credit: number | null
          debit: number | null
          description: string | null
          employee: string | null
          id: number
          notes: string | null
          posted_date: string | null
          project_number: string | null
          projects: string | null
          status: string | null
          transaction_date: string | null
        }
        Insert: {
          account_remarks?: string | null
          card_number?: string | null
          category?: string | null
          cost_code?: string | null
          cost_type?: string | null
          credit?: number | null
          debit?: number | null
          description?: string | null
          employee?: string | null
          id: number
          notes?: string | null
          posted_date?: string | null
          project_number?: string | null
          projects?: string | null
          status?: string | null
          transaction_date?: string | null
        }
        Update: {
          account_remarks?: string | null
          card_number?: string | null
          category?: string | null
          cost_code?: string | null
          cost_type?: string | null
          credit?: number | null
          debit?: number | null
          description?: string | null
          employee?: string | null
          id?: number
          notes?: string | null
          posted_date?: string | null
          project_number?: string | null
          projects?: string | null
          status?: string | null
          transaction_date?: string | null
        }
        Relationships: []
      }
      document_metadata: {
        Row: {
          category: string | null
          created_at: string | null
          employee_id: number | null
          id: string
          project: string | null
          schema: string | null
          title: string | null
          url: string | null
        }
        Insert: {
          category?: string | null
          created_at?: string | null
          employee_id?: number | null
          id: string
          project?: string | null
          schema?: string | null
          title?: string | null
          url?: string | null
        }
        Update: {
          category?: string | null
          created_at?: string | null
          employee_id?: number | null
          id?: string
          project?: string | null
          schema?: string | null
          title?: string | null
          url?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "document_metadata_employee_id_fkey"
            columns: ["employee_id"]
            isOneToOne: false
            referencedRelation: "employees"
            referencedColumns: ["id"]
          },
        ]
      }
      document_rows: {
        Row: {
          dataset_id: string | null
          id: number
          row_data: Json | null
        }
        Insert: {
          dataset_id?: string | null
          id?: number
          row_data?: Json | null
        }
        Update: {
          dataset_id?: string | null
          id?: number
          row_data?: Json | null
        }
        Relationships: [
          {
            foreignKeyName: "document_rows_dataset_id_fkey"
            columns: ["dataset_id"]
            isOneToOne: false
            referencedRelation: "document_metadata"
            referencedColumns: ["id"]
          },
        ]
      }
      documents: {
        Row: {
          content: string | null
          created_at: string
          embedding: string | null
          id: number
          metadata: Json | null
          title: string | null
          user_id: string | null
        }
        Insert: {
          content?: string | null
          created_at?: string
          embedding?: string | null
          id?: number
          metadata?: Json | null
          title?: string | null
          user_id?: string | null
        }
        Update: {
          content?: string | null
          created_at?: string
          embedding?: string | null
          id?: number
          metadata?: Json | null
          title?: string | null
          user_id?: string | null
        }
        Relationships: []
      }
      embeddings: {
        Row: {
          content: string
          embedding: string | null
          id: number
        }
        Insert: {
          content: string
          embedding?: string | null
          id?: never
        }
        Update: {
          content?: string
          embedding?: string | null
          id?: never
        }
        Relationships: []
      }
      employees: {
        Row: {
          department: string | null
          email: string | null
          id: number
          name: string
          phone: string | null
          position: string | null
          salary: number | null
          start_date: string | null
          truck_allowance: number | null
        }
        Insert: {
          department?: string | null
          email?: string | null
          id?: never
          name: string
          phone?: string | null
          position?: string | null
          salary?: number | null
          start_date?: string | null
          truck_allowance?: number | null
        }
        Update: {
          department?: string | null
          email?: string | null
          id?: never
          name?: string
          phone?: string | null
          position?: string | null
          salary?: number | null
          start_date?: string | null
          truck_allowance?: number | null
        }
        Relationships: []
      }
      meetings: {
        Row: {
          action_items_count: number | null
          actual_date: string | null
          agenda: string | null
          attendees: string[] | null
          category: string | null
          client_id: number | null
          created_at: string | null
          description: string | null
          duration_minutes: number | null
          id: string
          link: string | null
          location: string | null
          meeting: string
          meeting_date: string
          meeting_type: string | null
          meeting_url: string | null
          metadata: Json | null
          notion_id: string
          page_content: string | null
          project_id: string | null
          projects: string | null
          scheduled_date: string | null
          sentiment: string | null
          source: string | null
          summary: string | null
          tag: string | null
          transcript_document_id: string | null
          updated_at: string | null
        }
        Insert: {
          action_items_count?: number | null
          actual_date?: string | null
          agenda?: string | null
          attendees?: string[] | null
          category?: string | null
          client_id?: number | null
          created_at?: string | null
          description?: string | null
          duration_minutes?: number | null
          id?: string
          link?: string | null
          location?: string | null
          meeting: string
          meeting_date: string
          meeting_type?: string | null
          meeting_url?: string | null
          metadata?: Json | null
          notion_id: string
          page_content?: string | null
          project_id?: string | null
          projects?: string | null
          scheduled_date?: string | null
          sentiment?: string | null
          source?: string | null
          summary?: string | null
          tag?: string | null
          transcript_document_id?: string | null
          updated_at?: string | null
        }
        Update: {
          action_items_count?: number | null
          actual_date?: string | null
          agenda?: string | null
          attendees?: string[] | null
          category?: string | null
          client_id?: number | null
          created_at?: string | null
          description?: string | null
          duration_minutes?: number | null
          id?: string
          link?: string | null
          location?: string | null
          meeting?: string
          meeting_date?: string
          meeting_type?: string | null
          meeting_url?: string | null
          metadata?: Json | null
          notion_id?: string
          page_content?: string | null
          project_id?: string | null
          projects?: string | null
          scheduled_date?: string | null
          sentiment?: string | null
          source?: string | null
          summary?: string | null
          tag?: string | null
          transcript_document_id?: string | null
          updated_at?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "meetings_client_id_fkey"
            columns: ["client_id"]
            isOneToOne: false
            referencedRelation: "clients"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "meetings_transcript_document_id_fkey"
            columns: ["transcript_document_id"]
            isOneToOne: false
            referencedRelation: "strategic_documents"
            referencedColumns: ["id"]
          },
        ]
      }
      messages: {
        Row: {
          chat_id: string | null
          content: string | null
          created_at: string | null
          id: string
          role: string
          updated_at: string | null
        }
        Insert: {
          chat_id?: string | null
          content?: string | null
          created_at?: string | null
          id?: string
          role: string
          updated_at?: string | null
        }
        Update: {
          chat_id?: string | null
          content?: string | null
          created_at?: string | null
          id?: string
          role?: string
          updated_at?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "messages_chat_id_fkey"
            columns: ["chat_id"]
            isOneToOne: false
            referencedRelation: "chat_sessions"
            referencedColumns: ["id"]
          },
        ]
      }
      n8n_chat_histories: {
        Row: {
          id: number
          message: Json
          session_id: string
        }
        Insert: {
          id?: number
          message: Json
          session_id: string
        }
        Update: {
          id?: number
          message?: Json
          session_id?: string
        }
        Relationships: []
      }
      nods_page: {
        Row: {
          checksum: string | null
          id: number
          meta: Json | null
          parent_page_id: number | null
          path: string
          source: string | null
          type: string | null
        }
        Insert: {
          checksum?: string | null
          id?: number
          meta?: Json | null
          parent_page_id?: number | null
          path: string
          source?: string | null
          type?: string | null
        }
        Update: {
          checksum?: string | null
          id?: number
          meta?: Json | null
          parent_page_id?: number | null
          path?: string
          source?: string | null
          type?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "nods_page_parent_page_id_fkey"
            columns: ["parent_page_id"]
            isOneToOne: false
            referencedRelation: "nods_page"
            referencedColumns: ["id"]
          },
        ]
      }
      nods_page_section: {
        Row: {
          content: string | null
          embedding: string | null
          heading: string | null
          id: number
          page_id: number
          slug: string | null
          token_count: number | null
        }
        Insert: {
          content?: string | null
          embedding?: string | null
          heading?: string | null
          id?: number
          page_id: number
          slug?: string | null
          token_count?: number | null
        }
        Update: {
          content?: string | null
          embedding?: string | null
          heading?: string | null
          id?: number
          page_id?: number
          slug?: string | null
          token_count?: number | null
        }
        Relationships: [
          {
            foreignKeyName: "nods_page_section_page_id_fkey"
            columns: ["page_id"]
            isOneToOne: false
            referencedRelation: "nods_page"
            referencedColumns: ["id"]
          },
        ]
      }
      profiles: {
        Row: {
          avatar_url: string | null
          full_name: string | null
          id: string
          updated_at: string | null
          username: string | null
          website: string | null
        }
        Insert: {
          avatar_url?: string | null
          full_name?: string | null
          id: string
          updated_at?: string | null
          username?: string | null
          website?: string | null
        }
        Update: {
          avatar_url?: string | null
          full_name?: string | null
          id?: string
          updated_at?: string | null
          username?: string | null
          website?: string | null
        }
        Relationships: []
      }
      project: {
        Row: {
          actual_cost: number | null
          budget: number | null
          client_id: number | null
          created_at: string
          description: string | null
          end_date: string | null
          est_completion: string | null
          est_profits: number | null
          est_revenue: number | null
          meetings: string | null
          metadata: Json | null
          name: string | null
          onedrive: string | null
          phase: string | null
          priority: string | null
          progress_percentage: number | null
          project_manager: string | null
          project_number: string
          project_type: string | null
          start_date: string | null
          state: string | null
          status: string | null
          updated_at: string | null
        }
        Insert: {
          actual_cost?: number | null
          budget?: number | null
          client_id?: number | null
          created_at?: string
          description?: string | null
          end_date?: string | null
          est_completion?: string | null
          est_profits?: number | null
          est_revenue?: number | null
          meetings?: string | null
          metadata?: Json | null
          name?: string | null
          onedrive?: string | null
          phase?: string | null
          priority?: string | null
          progress_percentage?: number | null
          project_manager?: string | null
          project_number: string
          project_type?: string | null
          start_date?: string | null
          state?: string | null
          status?: string | null
          updated_at?: string | null
        }
        Update: {
          actual_cost?: number | null
          budget?: number | null
          client_id?: number | null
          created_at?: string
          description?: string | null
          end_date?: string | null
          est_completion?: string | null
          est_profits?: number | null
          est_revenue?: number | null
          meetings?: string | null
          metadata?: Json | null
          name?: string | null
          onedrive?: string | null
          phase?: string | null
          priority?: string | null
          progress_percentage?: number | null
          project_manager?: string | null
          project_number?: string
          project_type?: string | null
          start_date?: string | null
          state?: string | null
          status?: string | null
          updated_at?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "project_client_id_fkey"
            columns: ["client_id"]
            isOneToOne: false
            referencedRelation: "clients"
            referencedColumns: ["id"]
          },
        ]
      }
      project_reports: {
        Row: {
          budget_status: Json | null
          created_at: string | null
          executive_summary: string | null
          generated_by: string | null
          id: string
          issues_resolved: string[] | null
          key_achievements: string[] | null
          metadata: Json | null
          next_milestones: string[] | null
          project_number: string | null
          report_data: Json | null
          report_period_end: string | null
          report_period_start: string | null
          report_type: string | null
          risks_identified: string[] | null
          schedule_status: Json | null
          updated_at: string | null
        }
        Insert: {
          budget_status?: Json | null
          created_at?: string | null
          executive_summary?: string | null
          generated_by?: string | null
          id?: string
          issues_resolved?: string[] | null
          key_achievements?: string[] | null
          metadata?: Json | null
          next_milestones?: string[] | null
          project_number?: string | null
          report_data?: Json | null
          report_period_end?: string | null
          report_period_start?: string | null
          report_type?: string | null
          risks_identified?: string[] | null
          schedule_status?: Json | null
          updated_at?: string | null
        }
        Update: {
          budget_status?: Json | null
          created_at?: string | null
          executive_summary?: string | null
          generated_by?: string | null
          id?: string
          issues_resolved?: string[] | null
          key_achievements?: string[] | null
          metadata?: Json | null
          next_milestones?: string[] | null
          project_number?: string | null
          report_data?: Json | null
          report_period_end?: string | null
          report_period_start?: string | null
          report_type?: string | null
          risks_identified?: string[] | null
          schedule_status?: Json | null
          updated_at?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "project_reports_project_number_fkey"
            columns: ["project_number"]
            isOneToOne: false
            referencedRelation: "enhanced_project_dashboard"
            referencedColumns: ["project_number"]
          },
          {
            foreignKeyName: "project_reports_project_number_fkey"
            columns: ["project_number"]
            isOneToOne: false
            referencedRelation: "project"
            referencedColumns: ["project_number"]
          },
        ]
      }
      site_pages: {
        Row: {
          chunk_number: number | null
          content: string | null
          embedding: string | null
          id: string
          metadata: Json | null
          summary: string | null
          title: string | null
          url: string | null
        }
        Insert: {
          chunk_number?: number | null
          content?: string | null
          embedding?: string | null
          id?: string
          metadata?: Json | null
          summary?: string | null
          title?: string | null
          url?: string | null
        }
        Update: {
          chunk_number?: number | null
          content?: string | null
          embedding?: string | null
          id?: string
          metadata?: Json | null
          summary?: string | null
          title?: string | null
          url?: string | null
        }
        Relationships: []
      }
      sources: {
        Row: {
          created_at: string
          source_id: string
          summary: string | null
          total_word_count: number | null
          updated_at: string
        }
        Insert: {
          created_at?: string
          source_id: string
          summary?: string | null
          total_word_count?: number | null
          updated_at?: string
        }
        Update: {
          created_at?: string
          source_id?: string
          summary?: string | null
          total_word_count?: number | null
          updated_at?: string
        }
        Relationships: []
      }
      strategic_documents: {
        Row: {
          client_id: number | null
          content: string
          created_at: string | null
          document_type: string | null
          embedding: string | null
          file_path: string | null
          file_size: number | null
          id: string
          metadata: Json | null
          mime_type: string | null
          project_id: string | null
          source_file: string | null
          source_meeting_id: string | null
          title: string
          updated_at: string | null
        }
        Insert: {
          client_id?: number | null
          content: string
          created_at?: string | null
          document_type?: string | null
          embedding?: string | null
          file_path?: string | null
          file_size?: number | null
          id?: string
          metadata?: Json | null
          mime_type?: string | null
          project_id?: string | null
          source_file?: string | null
          source_meeting_id?: string | null
          title: string
          updated_at?: string | null
        }
        Update: {
          client_id?: number | null
          content?: string
          created_at?: string | null
          document_type?: string | null
          embedding?: string | null
          file_path?: string | null
          file_size?: number | null
          id?: string
          metadata?: Json | null
          mime_type?: string | null
          project_id?: string | null
          source_file?: string | null
          source_meeting_id?: string | null
          title?: string
          updated_at?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "strategic_documents_client_id_fkey"
            columns: ["client_id"]
            isOneToOne: false
            referencedRelation: "clients"
            referencedColumns: ["id"]
          },
        ]
      }
      suggestions: {
        Row: {
          created_at: string
          description: string | null
          document_created_at: string
          document_id: number
          id: string
          is_resolved: boolean
          original_text: string
          suggested_text: string
          user_id: string
        }
        Insert: {
          created_at?: string
          description?: string | null
          document_created_at: string
          document_id: number
          id?: string
          is_resolved?: boolean
          original_text: string
          suggested_text: string
          user_id: string
        }
        Update: {
          created_at?: string
          description?: string | null
          document_created_at?: string
          document_id?: number
          id?: string
          is_resolved?: boolean
          original_text?: string
          suggested_text?: string
          user_id?: string
        }
        Relationships: [
          {
            foreignKeyName: "suggestions_document_id_fkey"
            columns: ["document_id"]
            isOneToOne: false
            referencedRelation: "documents"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "suggestions_user_id_fkey"
            columns: ["user_id"]
            isOneToOne: false
            referencedRelation: "users"
            referencedColumns: ["id"]
          },
        ]
      }
      tasks: {
        Row: {
          actual_hours: number | null
          assigned_by: string | null
          assigned_to: string | null
          completed_at: string | null
          created_at: string | null
          created_by: string | null
          description: string | null
          due_date: string | null
          estimated_hours: number | null
          id: string
          metadata: Json | null
          parent_task_id: string | null
          priority: string | null
          project: string | null
          project_id: string | null
          source_document: string | null
          source_document_id: string | null
          source_meeting_id: string | null
          status: string | null
          title: string
          updated_at: string | null
        }
        Insert: {
          actual_hours?: number | null
          assigned_by?: string | null
          assigned_to?: string | null
          completed_at?: string | null
          created_at?: string | null
          created_by?: string | null
          description?: string | null
          due_date?: string | null
          estimated_hours?: number | null
          id?: string
          metadata?: Json | null
          parent_task_id?: string | null
          priority?: string | null
          project?: string | null
          project_id?: string | null
          source_document?: string | null
          source_document_id?: string | null
          source_meeting_id?: string | null
          status?: string | null
          title: string
          updated_at?: string | null
        }
        Update: {
          actual_hours?: number | null
          assigned_by?: string | null
          assigned_to?: string | null
          completed_at?: string | null
          created_at?: string | null
          created_by?: string | null
          description?: string | null
          due_date?: string | null
          estimated_hours?: number | null
          id?: string
          metadata?: Json | null
          parent_task_id?: string | null
          priority?: string | null
          project?: string | null
          project_id?: string | null
          source_document?: string | null
          source_document_id?: string | null
          source_meeting_id?: string | null
          status?: string | null
          title?: string
          updated_at?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "tasks_parent_task_id_fkey"
            columns: ["parent_task_id"]
            isOneToOne: false
            referencedRelation: "tasks"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "tasks_source_document_id_fkey"
            columns: ["source_document_id"]
            isOneToOne: false
            referencedRelation: "strategic_documents"
            referencedColumns: ["id"]
          },
        ]
      }
      todos: {
        Row: {
          id: number
          inserted_at: string
          is_complete: boolean | null
          task: string | null
          user_id: string
        }
        Insert: {
          id?: number
          inserted_at?: string
          is_complete?: boolean | null
          task?: string | null
          user_id: string
        }
        Update: {
          id?: number
          inserted_at?: string
          is_complete?: boolean | null
          task?: string | null
          user_id?: string
        }
        Relationships: []
      }
      users: {
        Row: {
          created_at: string
          email: string
          id: string
          updated_at: string
        }
        Insert: {
          created_at?: string
          email: string
          id?: string
          updated_at?: string
        }
        Update: {
          created_at?: string
          email?: string
          id?: string
          updated_at?: string
        }
        Relationships: []
      }
      votes: {
        Row: {
          chat_id: string
          is_upvoted: boolean
          message_id: string
        }
        Insert: {
          chat_id: string
          is_upvoted: boolean
          message_id: string
        }
        Update: {
          chat_id?: string
          is_upvoted?: boolean
          message_id?: string
        }
        Relationships: [
          {
            foreignKeyName: "votes_chat_id_fkey"
            columns: ["chat_id"]
            isOneToOne: false
            referencedRelation: "chats"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "votes_message_id_fkey"
            columns: ["message_id"]
            isOneToOne: false
            referencedRelation: "messages"
            referencedColumns: ["id"]
          },
        ]
      }
    }
    Views: {
      enhanced_project_dashboard: {
        Row: {
          actual_cost: number | null
          blocked_tasks: number | null
          budget: number | null
          budget_utilization_percentage: number | null
          client_company: string | null
          client_name: string | null
          client_tier: string | null
          completed_tasks: number | null
          created_at: string | null
          end_date: string | null
          last_meeting_date: string | null
          last_report_date: string | null
          overdue_tasks: number | null
          priority: string | null
          progress_percentage: number | null
          project_manager: string | null
          project_name: string | null
          project_number: string | null
          start_date: string | null
          status: string | null
          total_documents: number | null
          total_meetings: number | null
          total_tasks: number | null
        }
        Relationships: []
      }
    }
    Functions: {
      assign_document_to_project: {
        Args: { doc_title: string; doc_content: string }
        Returns: {
          detected_project: string
          confidence: number
          method: string
          success: boolean
        }[]
      }
      binary_quantize: {
        Args: { "": string } | { "": unknown }
        Returns: unknown
      }
      extract_project_number_from_text: {
        Args: { input_text: string }
        Returns: string
      }
      get_page_parents: {
        Args: { page_id: number }
        Returns: {
          id: number
          parent_page_id: number
          path: string
          meta: Json
        }[]
      }
      get_project_context_enhanced: {
        Args: { entity_type: string; entity_value: string }
        Returns: {
          project_number: string
          project_name: string
          client_name: string
          project_status: string
          context_data: Json
        }[]
      }
      halfvec_avg: {
        Args: { "": number[] }
        Returns: unknown
      }
      halfvec_out: {
        Args: { "": unknown }
        Returns: unknown
      }
      halfvec_send: {
        Args: { "": unknown }
        Returns: string
      }
      halfvec_typmod_in: {
        Args: { "": unknown[] }
        Returns: number
      }
      hnsw_bit_support: {
        Args: { "": unknown }
        Returns: unknown
      }
      hnsw_halfvec_support: {
        Args: { "": unknown }
        Returns: unknown
      }
      hnsw_sparsevec_support: {
        Args: { "": unknown }
        Returns: unknown
      }
      hnswhandler: {
        Args: { "": unknown }
        Returns: unknown
      }
      ivfflat_bit_support: {
        Args: { "": unknown }
        Returns: unknown
      }
      ivfflat_halfvec_support: {
        Args: { "": unknown }
        Returns: unknown
      }
      ivfflathandler: {
        Args: { "": unknown }
        Returns: unknown
      }
      l2_norm: {
        Args: { "": unknown } | { "": unknown }
        Returns: number
      }
      l2_normalize: {
        Args: { "": string } | { "": unknown } | { "": unknown }
        Returns: unknown
      }
      match_code_examples: {
        Args: {
          query_embedding: string
          match_count?: number
          filter?: Json
          source_filter?: string
        }
        Returns: {
          id: number
          url: string
          chunk_number: number
          content: string
          summary: string
          metadata: Json
          source_id: string
          similarity: number
        }[]
      }
      match_crawled_pages: {
        Args: {
          query_embedding: string
          match_count?: number
          filter?: Json
          source_filter?: string
        }
        Returns: {
          id: number
          url: string
          chunk_number: number
          content: string
          metadata: Json
          source_id: string
          similarity: number
        }[]
      }
      match_documents: {
        Args:
          | { query_embedding: string; match_count?: number; filter?: Json }
          | { query_embedding: string; match_threshold: number }
          | {
              query_embedding: string
              match_threshold?: number
              match_count?: number
            }
        Returns: {
          content: string | null
          created_at: string
          embedding: string | null
          id: number
          metadata: Json | null
          title: string | null
          user_id: string | null
        }[]
      }
      match_page_sections: {
        Args: {
          embedding: string
          match_threshold: number
          match_count: number
          min_content_length: number
        }
        Returns: {
          id: number
          page_id: number
          slug: string
          heading: string
          content: string
          similarity: number
        }[]
      }
      search_documents_with_project_context: {
        Args: {
          query_embedding: string
          project_filter?: string
          document_type_filter?: string
          limit_count?: number
        }
        Returns: {
          id: string
          title: string
          content: string
          document_type: string
          project_name: string
          client_name: string
          project_number: string
          similarity: number
        }[]
      }
      sparsevec_out: {
        Args: { "": unknown }
        Returns: unknown
      }
      sparsevec_send: {
        Args: { "": unknown }
        Returns: string
      }
      sparsevec_typmod_in: {
        Args: { "": unknown[] }
        Returns: number
      }
      vector_avg: {
        Args: { "": number[] }
        Returns: string
      }
      vector_dims: {
        Args: { "": string } | { "": unknown }
        Returns: number
      }
      vector_norm: {
        Args: { "": string }
        Returns: number
      }
      vector_out: {
        Args: { "": string }
        Returns: unknown
      }
      vector_send: {
        Args: { "": string }
        Returns: string
      }
      vector_typmod_in: {
        Args: { "": unknown[] }
        Returns: number
      }
    }
    Enums: {
      color_source:
        | "99COLORS_NET"
        | "ART_PAINTS_YG07S"
        | "BYRNE"
        | "CRAYOLA"
        | "CMYK_COLOR_MODEL"
        | "COLORCODE_IS"
        | "COLORHEXA"
        | "COLORXS"
        | "CORNELL_UNIVERSITY"
        | "COLUMBIA_UNIVERSITY"
        | "DUKE_UNIVERSITY"
        | "ENCYCOLORPEDIA_COM"
        | "ETON_COLLEGE"
        | "FANTETTI_AND_PETRACCHI"
        | "FINDTHEDATA_COM"
        | "FERRARIO_1919"
        | "FEDERAL_STANDARD_595"
        | "FLAG_OF_INDIA"
        | "FLAG_OF_SOUTH_AFRICA"
        | "GLAZEBROOK_AND_BALDRY"
        | "GOOGLE"
        | "HEXCOLOR_CO"
        | "ISCC_NBS"
        | "KELLY_MOORE"
        | "MATTEL"
        | "MAERZ_AND_PAUL"
        | "MILK_PAINT"
        | "MUNSELL_COLOR_WHEEL"
        | "NATURAL_COLOR_SYSTEM"
        | "PANTONE"
        | "PLOCHERE"
        | "POURPRE_COM"
        | "RAL"
        | "RESENE"
        | "RGB_COLOR_MODEL"
        | "THOM_POOLE"
        | "UNIVERSITY_OF_ALABAMA"
        | "UNIVERSITY_OF_CALIFORNIA_DAVIS"
        | "UNIVERSITY_OF_CAMBRIDGE"
        | "UNIVERSITY_OF_NORTH_CAROLINA"
        | "UNIVERSITY_OF_TEXAS_AT_AUSTIN"
        | "X11_WEB"
        | "XONA_COM"
    }
    CompositeTypes: {
      [_ in never]: never
    }
  }
}

type DatabaseWithoutInternals = Omit<Database, "__InternalSupabase">

type DefaultSchema = DatabaseWithoutInternals[Extract<keyof Database, "public">]

export type Tables<
  DefaultSchemaTableNameOrOptions extends
    | keyof (DefaultSchema["Tables"] & DefaultSchema["Views"])
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
        DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
      DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])[TableName] extends {
      Row: infer R
    }
    ? R
    : never
  : DefaultSchemaTableNameOrOptions extends keyof (DefaultSchema["Tables"] &
        DefaultSchema["Views"])
    ? (DefaultSchema["Tables"] &
        DefaultSchema["Views"])[DefaultSchemaTableNameOrOptions] extends {
        Row: infer R
      }
      ? R
      : never
    : never

export type TablesInsert<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Insert: infer I
    }
    ? I
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Insert: infer I
      }
      ? I
      : never
    : never

export type TablesUpdate<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Update: infer U
    }
    ? U
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Update: infer U
      }
      ? U
      : never
    : never

export type Enums<
  DefaultSchemaEnumNameOrOptions extends
    | keyof DefaultSchema["Enums"]
    | { schema: keyof DatabaseWithoutInternals },
  EnumName extends DefaultSchemaEnumNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"]
    : never = never,
> = DefaultSchemaEnumNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"][EnumName]
  : DefaultSchemaEnumNameOrOptions extends keyof DefaultSchema["Enums"]
    ? DefaultSchema["Enums"][DefaultSchemaEnumNameOrOptions]
    : never

export type CompositeTypes<
  PublicCompositeTypeNameOrOptions extends
    | keyof DefaultSchema["CompositeTypes"]
    | { schema: keyof DatabaseWithoutInternals },
  CompositeTypeName extends PublicCompositeTypeNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"]
    : never = never,
> = PublicCompositeTypeNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"][CompositeTypeName]
  : PublicCompositeTypeNameOrOptions extends keyof DefaultSchema["CompositeTypes"]
    ? DefaultSchema["CompositeTypes"][PublicCompositeTypeNameOrOptions]
    : never

export const Constants = {
  public: {
    Enums: {
      color_source: [
        "99COLORS_NET",
        "ART_PAINTS_YG07S",
        "BYRNE",
        "CRAYOLA",
        "CMYK_COLOR_MODEL",
        "COLORCODE_IS",
        "COLORHEXA",
        "COLORXS",
        "CORNELL_UNIVERSITY",
        "COLUMBIA_UNIVERSITY",
        "DUKE_UNIVERSITY",
        "ENCYCOLORPEDIA_COM",
        "ETON_COLLEGE",
        "FANTETTI_AND_PETRACCHI",
        "FINDTHEDATA_COM",
        "FERRARIO_1919",
        "FEDERAL_STANDARD_595",
        "FLAG_OF_INDIA",
        "FLAG_OF_SOUTH_AFRICA",
        "GLAZEBROOK_AND_BALDRY",
        "GOOGLE",
        "HEXCOLOR_CO",
        "ISCC_NBS",
        "KELLY_MOORE",
        "MATTEL",
        "MAERZ_AND_PAUL",
        "MILK_PAINT",
        "MUNSELL_COLOR_WHEEL",
        "NATURAL_COLOR_SYSTEM",
        "PANTONE",
        "PLOCHERE",
        "POURPRE_COM",
        "RAL",
        "RESENE",
        "RGB_COLOR_MODEL",
        "THOM_POOLE",
        "UNIVERSITY_OF_ALABAMA",
        "UNIVERSITY_OF_CALIFORNIA_DAVIS",
        "UNIVERSITY_OF_CAMBRIDGE",
        "UNIVERSITY_OF_NORTH_CAROLINA",
        "UNIVERSITY_OF_TEXAS_AT_AUSTIN",
        "X11_WEB",
        "XONA_COM",
      ],
    },
  },
} as const
