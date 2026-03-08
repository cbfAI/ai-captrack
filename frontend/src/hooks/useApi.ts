import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { capabilitiesApi, collectApi } from '@/services/api';
import type { CapabilitiesFilter, FeedbackType } from '@/types';

export const useCapabilities = (page: number, pageSize: number, filters?: CapabilitiesFilter) => {
  return useQuery({
    queryKey: ['capabilities', page, pageSize, filters],
    queryFn: () => capabilitiesApi.getCapabilities(page, pageSize, filters),
  });
};

export const useCapabilityById = (id: string) => {
  return useQuery({
    queryKey: ['capability', id],
    queryFn: () => capabilitiesApi.getCapabilityById(id),
    enabled: !!id,
  });
};

export const useSubmitFeedback = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ capabilityId, feedbackType }: { capabilityId: string; feedbackType: FeedbackType }) =>
      capabilitiesApi.submitFeedback(capabilityId, feedbackType),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['capabilities'] });
    },
  });
};

export const useTriggerCollection = () => {
  return useMutation({
    mutationFn: () => collectApi.triggerCollection(),
  });
};

export const useCollectionProgress = () => {
  return useQuery({
    queryKey: ['collection-progress'],
    queryFn: () => collectApi.getCollectionProgress(),
    refetchInterval: 2000, // 每2秒刷新一次
  });
};
