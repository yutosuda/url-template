/**
 * Type definitions for URL shortener frontend.
 */

// API Response Types
export interface URLResponse {
  id: number;
  short_code: string;
  original_url: string;
  click_count: number;
  created_at: string;
  updated_at: string;
}

export interface ClickResponse {
  id: number;
  url_id: number;
  client_ip: string;
  user_agent: string;
  referer: string;
  timestamp: string;
}

export interface StatsResponse {
  total_urls: number;
  total_clicks: number;
  top_urls?: URLResponse[];
}

// API Request Types
export interface URLCreateRequest {
  original_url: string;
}

// Component Props Types
export interface URLCardProps {
  url: URLResponse;
  onRefresh?: () => void;
}

export interface URLFormProps {
  onSubmit: (data: URLCreateRequest) => void;
  isLoading?: boolean;
}

export interface StatsCardProps {
  stats: StatsResponse;
}

export interface ClickHistoryProps {
  shortCode: string;
  clicks: ClickResponse[];
}

// Form Types
export interface URLFormData {
  original_url: string;
}

// API Error Types
export interface APIError {
  detail: string;
  status_code?: number;
}

// Utility Types
export type LoadingState = 'idle' | 'loading' | 'success' | 'error';

export interface AsyncState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
} 