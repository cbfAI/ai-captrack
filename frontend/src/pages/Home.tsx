import { useState, lazy, Suspense } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useCapabilities } from '@/hooks/useApi';
import { Header } from '@/components/Header';
import { FilterBar } from '@/components/FilterBar';
import { CapabilityCard } from '@/components/CapabilityCard';
import { Pagination } from '@/components/Pagination';
import { CardSkeleton, FilterBarSkeleton } from '@/components/Skeleton';
import { StatsCard } from '@/components/StatsCard';
import { favoritesApi, Statistics } from '@/services/api';
import type { CapabilitiesFilter } from '@/types';

// Lazy load DetailModal - only loads when user clicks a card
const DetailModal = lazy(() => import('@/components/DetailModal').then(module => ({ default: module.DetailModal })));

export function Home() {
  const [page, setPage] = useState(1);
  const [filters, setFilters] = useState<CapabilitiesFilter>({});
  const [selectedCapabilityId, setSelectedCapabilityId] = useState<string | null>(null);
  const [showStats, setShowStats] = useState(true);
  const pageSize = 20;

  const { data, isLoading, error } = useCapabilities(page, pageSize, filters);
  const { data: statistics, isLoading: statsLoading } = useQuery<Statistics>({
    queryKey: ['statistics'],
    queryFn: () => favoritesApi.getStatistics(),
    refetchInterval: 30000,
  });

  const handleFiltersChange = (newFilters: CapabilitiesFilter) => {
    setFilters(newFilters);
    setPage(1);
  };

  const handleCardClick = (capabilityId: string) => {
    setSelectedCapabilityId(capabilityId);
  };

  const handleCloseDetail = () => {
    setSelectedCapabilityId(null);
  };

const handleExport = () => {
    if (!data?.items) return;

    const csvContent = [
      ['名称', '描述', '类型', '来源', 'Stars', '热度', '开源', 'URL'].join(','),
      ...data.items.map(item => [
        `"${item.name}"`,
        `"${item.description || ''}"`,
        item.capability_type,
        item.source,
        item.stars,
        item.heat_score,
        item.is_open_source ? '是' : '否',
        item.source_url || ''
      ].join(','))
    ].join('\n');

    const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `ai_capabilities_${new Date().toISOString().split('T')[0]}.csv`;
    link.click();
  };

  const totalPages = data ? Math.ceil(data.total / pageSize) : 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-purple-50">
      <Header onExport={handleExport} onToggleStats={() => setShowStats(!showStats)} showStats={showStats} />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {isLoading ? <FilterBarSkeleton /> : (
          <FilterBar
            filters={filters}
            onFiltersChange={handleFiltersChange}
            totalCount={data?.total || 0}
          />
        )}

        {showStats && <StatsCard statistics={statistics} isLoading={statsLoading} />}

        {isLoading && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {Array.from({ length: 6 }).map((_, index) => (
              <CardSkeleton key={index} />
            ))}
          </div>
        )}

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-xl p-8 text-center">
            <div className="text-red-500 mb-4">
              <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
            <p className="text-red-600 text-lg mb-2">加载失败</p>
            <p className="text-red-400 text-sm">请稍后重试</p>
          </div>
        )}

        {!isLoading && !error && data && (
          <>
            {data.items.length === 0 ? (
              <div className="text-center py-20">
                <div className="text-8xl mb-6">🔍</div>
                <p className="text-gray-600 text-xl font-medium mb-2">暂无 AI 能力数据</p>
                <p className="text-gray-400 text-sm">点击右上角"刷新数据"开始采集</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {data.items.map((capability) => (
<CapabilityCard
                  key={capability.id}
                  capability={capability}
                  onClick={() => handleCardClick(capability.id)}
                />
                ))}
              </div>
            )}

            <Pagination
              currentPage={page}
              totalPages={totalPages}
              onPageChange={setPage}
            />
          </>
        )}
      </main>

      {selectedCapabilityId && (
        <Suspense fallback={
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
            <div className="bg-white rounded-2xl p-8 max-w-2xl w-full mx-4">
              <div className="flex items-center justify-center">
                <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
              </div>
            </div>
          </div>
        }>
          <DetailModal
            capabilityId={selectedCapabilityId}
            onClose={handleCloseDetail}
          />
        </Suspense>
      )}

      <footer className="border-t border-gray-200/50 mt-16 py-8 bg-white/50 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-gray-500 text-sm">
          <p>AI CapTrack © 2024 - 发现最新 AI 能力</p>
        </div>
      </footer>
    </div>
  );
}

export default Home;
