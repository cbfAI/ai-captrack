import { useState } from 'react';
import { useCapabilityById } from '@/hooks/useApi';
import type { CapabilityType } from '@/types';

interface DetailModalProps {
  capabilityId: string;
  onClose: () => void;
}

const typeColors: Record<CapabilityType, { bg: string; text: string; border: string; icon: string }> = {
  Agent: { bg: 'bg-purple-50', text: 'text-purple-700', border: 'border-purple-200', icon: '🤖' },
  Code: { bg: 'bg-green-50', text: 'text-green-700', border: 'border-green-200', icon: '💻' },
  Model: { bg: 'bg-blue-50', text: 'text-blue-700', border: 'border-blue-200', icon: '🧠' },
};

const sourceLabels: Record<string, { label: string; color: string }> = {
  huggingface: { label: 'HuggingFace', color: 'text-yellow-600' },
  github: { label: 'GitHub', color: 'text-gray-700' },
  futuretools: { label: 'FutureTools', color: 'text-orange-600' },
};

function formatNumber(num: number): string {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M';
  }
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K';
  }
  return num.toString();
}

export function DetailModal({ capabilityId, onClose }: DetailModalProps) {
  const { data: capability, isLoading, error } = useCapabilityById(capabilityId);
  const [imageError, setImageError] = useState(false);

  if (isLoading) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
        <div className="bg-white rounded-2xl p-8 max-w-2xl w-full mx-4">
          <div className="flex items-center justify-center">
            <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
          </div>
        </div>
      </div>
    );
  }

  if (error || !capability) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
        <div className="bg-white rounded-2xl p-8 max-w-2xl w-full mx-4 text-center">
          <div className="text-red-500 mb-4">
            <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <p className="text-gray-600">加载失败，请稍后重试</p>
          <button onClick={onClose} className="mt-4 btn-secondary">
            关闭
          </button>
        </div>
      </div>
    );
  }

  const typeStyle = typeColors[capability.capability_type] || typeColors.Model;
  const sourceStyle = sourceLabels[capability.source] || { label: capability.source, color: 'text-gray-600' };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4" onClick={onClose}>
      <div 
        className="bg-white rounded-2xl max-w-3xl w-full max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="sticky top-0 bg-white border-b border-gray-100 px-6 py-4 flex items-center justify-between rounded-t-2xl">
          <h2 className="text-xl font-bold text-gray-900">AI 能力详情</h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <svg className="w-6 h-6 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div className="p-6">
          <div className="flex items-start gap-4 mb-6">
            <div className={`w-16 h-16 rounded-2xl ${typeStyle.bg} flex items-center justify-center text-3xl`}>
              {typeStyle.icon}
            </div>
            <div className="flex-1">
              <h3 className="text-2xl font-bold text-gray-900 mb-2">{capability.name}</h3>
              <div className="flex items-center gap-2 flex-wrap">
                <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-semibold ${typeStyle.bg} ${typeStyle.text} border ${typeStyle.border}`}>
                  {capability.capability_type}
                </span>
                <span className={`text-sm font-medium ${sourceStyle.color}`}>
                  {sourceStyle.label}
                </span>
                {capability.is_open_source && (
                  <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-700">
                    <svg className="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                    开源
                  </span>
                )}
              </div>
            </div>
          </div>

          <div className="grid grid-cols-3 gap-4 mb-6">
            <div className="bg-gray-50 rounded-xl p-4 text-center">
              <div className="flex items-center justify-center gap-2 mb-1">
                <svg className="w-5 h-5 text-yellow-500" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
                <span className="text-lg font-bold text-gray-900">{formatNumber(capability.stars)}</span>
              </div>
              <p className="text-sm text-gray-500">Stars</p>
            </div>
            <div className="bg-gray-50 rounded-xl p-4 text-center">
              <div className="flex items-center justify-center gap-2 mb-1">
                <svg className="w-5 h-5 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z" />
                </svg>
                <span className="text-lg font-bold text-gray-900">{formatNumber(capability.heat_score)}</span>
              </div>
              <p className="text-sm text-gray-500">热度</p>
            </div>
            <div className="bg-gray-50 rounded-xl p-4 text-center">
              <div className="flex items-center justify-center gap-2 mb-1">
                <span className="text-lg font-bold text-gray-900">{capability.key_features?.length || 0}</span>
              </div>
              <p className="text-sm text-gray-500">特性数</p>
            </div>
          </div>

          <div className="mb-6">
            <h4 className="text-lg font-semibold text-gray-900 mb-3">描述</h4>
            <p className="text-gray-600 leading-relaxed">
              {capability.description || '暂无描述'}
            </p>
          </div>

          {capability.key_features && capability.key_features.length > 0 && (
            <div className="mb-6">
              <h4 className="text-lg font-semibold text-gray-900 mb-3">关键特性</h4>
              <div className="flex flex-wrap gap-2">
                {capability.key_features.map((feature, index) => (
                  <span key={index} className="inline-flex items-center px-3 py-1.5 rounded-lg bg-blue-50 text-blue-700 text-sm">
                    <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                    {feature}
                  </span>
                ))}
              </div>
            </div>
          )}

          {capability.pain_points && capability.pain_points.length > 0 && (
            <div className="mb-6">
              <h4 className="text-lg font-semibold text-gray-900 mb-3">解决的痛点</h4>
              <div className="flex flex-wrap gap-2">
                {capability.pain_points.map((point, index) => (
                  <span key={index} className="inline-flex items-center px-3 py-1.5 rounded-lg bg-red-50 text-red-700 text-sm">
                    <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                    {point}
                  </span>
                ))}
              </div>
            </div>
          )}

          {capability.differentiation && (
            <div className="mb-6">
              <h4 className="text-lg font-semibold text-gray-900 mb-3">与现有方案的区别</h4>
              <p className="text-gray-600 leading-relaxed bg-purple-50 p-4 rounded-xl border border-purple-100">
                {capability.differentiation}
              </p>
            </div>
          )}

          {capability.source_url && (
            <div className="flex gap-4 pt-4 border-t border-gray-100">
              <a
                href={capability.source_url}
                target="_blank"
                rel="noopener noreferrer"
                className="flex-1 btn-primary text-center py-3 inline-flex items-center justify-center gap-2"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                </svg>
                查看原文
              </a>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
