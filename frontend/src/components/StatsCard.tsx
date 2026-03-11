import type { Statistics } from '@/services/api';

interface StatsCardProps {
  statistics: Statistics | undefined;
  isLoading: boolean;
}

function formatNumber(num: number): string {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M';
  }
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K';
  }
  return num.toFixed(0);
}

export function StatsCard({ statistics, isLoading }: StatsCardProps) {
  if (isLoading || !statistics) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 mb-6 animate-pulse">
        <div className="h-6 bg-gray-200 rounded w-32 mb-4"></div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="h-20 bg-gray-200 rounded-xl"></div>
          <div className="h-20 bg-gray-200 rounded-xl"></div>
          <div className="h-20 bg-gray-200 rounded-xl"></div>
          <div className="h-20 bg-gray-200 rounded-xl"></div>
        </div>
      </div>
    );
  }

  const typeColors: Record<string, string> = {
    'Agent': 'from-purple-500 to-purple-600',
    'Code': 'from-green-500 to-green-600',
    'Model': 'from-blue-500 to-blue-600',
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 mb-6">
      <h3 className="text-lg font-bold text-gray-900 mb-4">数据统计</h3>
      
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-4 text-white">
          <div className="text-3xl font-bold">{formatNumber(statistics.total)}</div>
          <div className="text-sm opacity-90">AI 能力总数</div>
        </div>
        
        <div className="bg-gradient-to-br from-yellow-500 to-orange-500 rounded-xl p-4 text-white">
          <div className="text-3xl font-bold">{formatNumber(statistics.avg_stars)}</div>
          <div className="text-sm opacity-90">平均 Stars</div>
        </div>
        
        <div className="bg-gradient-to-br from-red-500 to-pink-500 rounded-xl p-4 text-white">
          <div className="text-3xl font-bold">{formatNumber(statistics.avg_heat_score)}</div>
          <div className="text-sm opacity-90">平均热度</div>
        </div>
        
        <div className="bg-gradient-to-br from-purple-500 to-indigo-500 rounded-xl p-4 text-white">
          <div className="text-3xl font-bold">{Object.keys(statistics.by_source).length}</div>
          <div className="text-sm opacity-90">数据来源</div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <h4 className="text-sm font-medium text-gray-500 mb-2">按类型分布</h4>
          <div className="flex flex-wrap gap-2">
            {Object.entries(statistics.by_type).map(([type, count]) => (
              <div
                key={type}
                className={`inline-flex items-center px-3 py-1.5 rounded-lg bg-gradient-to-r ${typeColors[type] || 'from-gray-500 to-gray-600'} text-white text-sm font-medium`}
              >
                <span className="mr-2">
                  {type === 'Agent' ? '🤖' : type === 'Code' ? '💻' : '🧠'}
                </span>
                {type}: {count}
              </div>
            ))}
          </div>
        </div>
        
        <div>
          <h4 className="text-sm font-medium text-gray-500 mb-2">按来源分布</h4>
          <div className="flex flex-wrap gap-2">
            {Object.entries(statistics.by_source).map(([source, count]) => (
              <span
                key={source}
                className="inline-flex items-center px-3 py-1.5 rounded-lg bg-gray-100 text-gray-700 text-sm font-medium"
              >
                {source}: {count}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
