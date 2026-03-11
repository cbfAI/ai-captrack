import axios from 'axios';
import type {
  AICapability,
  PaginatedResponse,
  UserFeedback,
  FeedbackType,
  CollectionResponse,
  CapabilitiesFilter,
} from '@/types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const capabilitiesApi = {
  getCapabilities: async (
    page: number = 1,
    pageSize: number = 20,
    filters?: CapabilitiesFilter
  ): Promise<PaginatedResponse> => {
    const params = new URLSearchParams();
    params.append('page', page.toString());
    params.append('page_size', pageSize.toString());
    
    if (filters?.capability_type) {
      params.append('capability_type', filters.capability_type);
    }
    if (filters?.source) {
      params.append('source', filters.source);
    }
    if (filters?.min_stars !== undefined) {
      params.append('min_stars', filters.min_stars.toString());
    }
    if (filters?.min_heat_score !== undefined) {
      params.append('min_heat_score', filters.min_heat_score.toString());
    }
    if (filters?.search) {
      params.append('search', filters.search);
    }
    if (filters?.sort_by) {
      params.append('sort_by', filters.sort_by);
    }
    if (filters?.sort_order) {
      params.append('sort_order', filters.sort_order);
    }

    const response = await api.get<PaginatedResponse>(`/capabilities?${params.toString()}`);
    return response.data;
  },

  getCapabilityById: async (id: string): Promise<AICapability> => {
    const response = await api.get<AICapability>(`/capabilities/${id}`);
    return response.data;
  },

  submitFeedback: async (
    capabilityId: string,
    feedbackType: FeedbackType
  ): Promise<UserFeedback> => {
    const response = await api.post<UserFeedback>(`/capabilities/${capabilityId}/feedback`, {
      capability_id: capabilityId,
      feedback_type: feedbackType,
    });
    return response.data;
  },
};

export const collectApi = {
  triggerCollection: async (): Promise<CollectionResponse> => {
    const response = await api.post<CollectionResponse>('/collect/trigger');
    return response.data;
  },
  getCollectionProgress: async (): Promise<any> => {
    const response = await api.get('/collect/progress');
    return response.data;
  },
};

export interface Favorite {
  id: string;
  capability_id: string;
  created_at: string;
}

export interface Statistics {
  total: number;
  by_type: Record<string, number>;
  by_source: Record<string, number>;
  avg_stars: number;
  avg_heat_score: number;
}

export const favoritesApi = {
  addFavorite: async (capabilityId: string): Promise<Favorite> => {
    const response = await api.post<Favorite>('/favorites', {
      capability_id: capabilityId,
    });
    return response.data;
  },
  removeFavorite: async (capabilityId: string): Promise<void> => {
    await api.delete(`/favorites/${capabilityId}`);
  },
  getFavorites: async (): Promise<Favorite[]> => {
    const response = await api.get<Favorite[]>('/favorites');
    return response.data;
  },
  getStatistics: async (): Promise<Statistics> => {
    const response = await api.get<Statistics>('/statistics');
    return response.data;
  },
};

export default api;
