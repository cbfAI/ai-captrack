export type CapabilityType = 'Agent' | 'Code' | 'Model';

export type CapabilitySource = 'huggingface' | 'github' | 'futuretools' | 'openrouter';

export type FeedbackType = 'thumbs_up' | 'thumbs_down';

export interface AICapability {
  id: string;
  name: string;
  description: string | null;
  translated_description: string | null;
  capability_type: CapabilityType;
  source: CapabilitySource;
  source_url: string | null;
  is_open_source: boolean | null;
  key_features: string[];
  pain_points: string[];
  differentiation: string | null;
  stars: number;
  heat_score: number;
  heat_trend: string | null;
  thumbs_up: number;
  thumbs_down: number;
  metadata_: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export interface UserFeedback {
  id: string;
  capability_id: string;
  feedback_type: FeedbackType;
  created_at: string;
}

export type SortBy = 'stars' | 'heat' | 'name' | 'created_at' | 'updated_at';
export type SortOrder = 'asc' | 'desc';

export interface CapabilitiesFilter {
  capability_type?: CapabilityType;
  source?: CapabilitySource;
  min_stars?: number;
  min_heat_score?: number;
  search?: string;
  sort_by?: SortBy;
  sort_order?: SortOrder;
}

export interface PaginatedResponse {
  items: AICapability[];
  total: number;
  page: number;
  page_size: number;
  filters?: CapabilitiesFilter;
}

export interface CollectionResult {
  source: string;
  collected: number;
  after_dedup: number;
  status: 'success' | 'error';
  error?: string;
}

export interface CollectionResponse {
  total_collected: number;
  results: CollectionResult[];
}
