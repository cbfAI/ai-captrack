import { useState } from 'react';
import type { AICapability, CapabilityType } from '@/types';
import { useSubmitFeedback } from '@/hooks/useApi';

interface CapabilityCardProps {
  capability: AICapability;
  onClick?: () => void;
  onShare?: () => void;
}

const typeColors: Record<CapabilityType, { bg: string; text: string; border: string }> = {
  Agent: { bg: 'bg-purple-50', text: 'text-purple-700', border: 'border-purple-200' },
  Code: { bg: 'bg-green-50', text: 'text-green-700', border: 'border-green-200' },
  Model: { bg: 'bg-blue-50', text: 'text-blue-700', border: 'border-blue-200' },
};

const sourceLabels: Record<string, { label: string; color: string }> = {
  huggingface: { label: 'HuggingFace', color: 'text-yellow-600' },
  github: { label: 'GitHub', color: 'text-gray-700' },
  futuretools: { label: 'FutureTools', color: 'text-orange-600' },
  openrouter: { label: 'OpenRouter', color: 'text-indigo-600' },
};

export function CapabilityCard({ capability, onClick }: CapabilityCardProps) {
  const [feedbackGiven, setFeedbackGiven] = useState<'up' | 'down' | null>(null);
  const [isHovered, setIsHovered] = useState(false);
  const submitFeedback = useSubmitFeedback();

  const typeStyle = typeColors[capability.capability_type] || typeColors.Model;
  const sourceStyle = sourceLabels[capability.source] || { label: capFirstLetter(capability.source), color: 'text-gray-600' };

  function capFirstLetter(str: string) {
    return str.charAt(0).toUpperCase() + str.slice(1);
  }

  const handleFeedback = (type: 'up' | 'down', e: React.MouseEvent) => {
    e.stopPropagation();
    if (feedbackGiven) return;
    
    submitFeedback.mutate({
      capabilityId: capability.id,
      feedbackType: type === 'up' ? 'thumbs_up' : 'thumbs_down',
    });
    setFeedbackGiven(type);
  };

  return (
    <div 
      className={`group relative bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden cursor-pointer transition-all duration-300 hover:shadow-xl hover:-translate-y-1 hover:border-blue-200 ${isHovered ? 'ring-2 ring-blue-100' : ''}`}
      onClick={onClick}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className={`absolute top-0 left-0 w-1 h-full ${typeStyle.bg.replace('bg-', 'bg-')}`}></div>
      
      <div className="p-5 ml-2">
        <div className="flex items-start justify-between mb-3">
          <div className="flex-1 min-w-0">
            <h3 className="font-bold text-lg text-gray-900 truncate pr-4 group-hover:text-blue-600 transition-colors" title={capability.name}>
              {capability.name}
            </h3>
            <div className="flex items-center gap-2 mt-2">
              <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold ${typeStyle.bg} ${typeStyle.text} border ${typeStyle.border}`}>
                {capability.capability_type}
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

        <p className="text-gray-600 text-sm mb-4 line-clamp-3 leading-relaxed">
          {capability.description || '暂无描述'}
        </p>

        <div className="flex items-center justify-between pt-3 border-t border-gray-100">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-1.5 text-sm">
              <svg className="w-4 h-4 text-yellow-500" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
              <span className="font-medium text-gray-700">{formatNumber(capability.stars)}</span>
            </div>
            <div className="flex items-center gap-1.5 text-sm">
              <svg className="w-4 h-4 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z" />
              </svg>
              <span className="font-medium text-gray-700">{formatNumber(capability.heat_score)}</span>
              {capability.heat_trend && (
                <span className={`text-xs px-1.5 py-0.5 rounded ${
                  capability.heat_trend === 'rising' ? 'bg-green-100 text-green-600' :
                  capability.heat_trend === 'declining' ? 'bg-red-100 text-red-600' :
                  'bg-gray-100 text-gray-600'
                }`}>
                  {capability.heat_trend === 'rising' ? '↑' : 
                   capability.heat_trend === 'declining' ? '↓' : '→'}
                </span>
              )}
            </div>
          </div>

          <div className="flex items-center gap-1" onClick={(e) => e.stopPropagation()}>
            <button
              onClick={(e) => handleFeedback('up', e)}
              disabled={submitFeedback.isPending || feedbackGiven !== null}
              className={`p-2 rounded-lg transition-all duration-200 ${
                feedbackGiven === 'up'
                  ? 'bg-green-100 text-green-600 scale-110'
                  : 'hover:bg-green-50 text-gray-400 hover:text-green-500 hover:scale-110'
              }`}
              title="推荐"
            >
              <svg className="w-5 h-5" fill={feedbackGiven === 'up' ? 'currentColor' : 'none'} stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" />
              </svg>
            </button>
            <button
              onClick={(e) => handleFeedback('down', e)}
              disabled={submitFeedback.isPending || feedbackGiven !== null}
              className={`p-2 rounded-lg transition-all duration-200 ${
                feedbackGiven === 'down'
                  ? 'bg-red-100 text-red-600 scale-110'
                  : 'hover:bg-red-50 text-gray-400 hover:text-red-500 hover:scale-110'
              }`}
              title="不推荐"
            >
              <svg className="w-5 h-5" fill={feedbackGiven === 'down' ? 'currentColor' : 'none'} stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 14H5.236a2 2 0 01-1.789-2.894l3.5-7A2 2 0 018.736 3h4.018a2 2 0 01.485.06l3.76.94m-7 10v5a2 2 0 002 2h.096c.5 0 .905-.405.905-.904 0-.715.211-1.413.608-2.008L17 13V4m-7 10h2m5-10h2a2 2 0 012 2v6a2 2 0 01-2 2h-2.5" />
              </svg>
            </button>
          </div>
        </div>

        <div className="flex items-center justify-between mt-3">
          <span className={`text-xs font-medium ${sourceStyle.color}`}>
            {sourceStyle.label}
          </span>
          {capability.source_url && (
            <a
              href={capability.source_url}
              target="_blank"
              rel="noopener noreferrer"
              onClick={(e) => e.stopPropagation()}
              className="text-sm text-blue-500 hover:text-blue-600 font-medium inline-flex items-center gap-1 transition-colors"
            >
              查看详情
              <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </a>
          )}
        </div>
      </div>
    </div>
  );
}

function formatNumber(num: number): string {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M';
  }
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K';
  }
  return num.toString();
}
