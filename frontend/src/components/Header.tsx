import { useTriggerCollection, useCollectionProgress } from '@/hooks/useApi';

interface HeaderProps {
  onExport?: () => void;
  onToggleStats?: () => void;
  showStats?: boolean;
}

export function Header({ onExport, onToggleStats, showStats }: HeaderProps) {
  const triggerCollection = useTriggerCollection();
  const { data: progress } = useCollectionProgress();

  const handleRefresh = () => {
    triggerCollection.mutate();
  };

  const isCollecting = progress?.status === 'running';
  const isCompleted = progress?.status === 'completed';

  return (
    <header className="bg-white border-b border-gray-100 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">AI CapTrack</h1>
              <p className="text-xs text-gray-500">AI 能力追踪平台</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            {onToggleStats && (
              <button
                onClick={onToggleStats}
                className={`flex items-center gap-2 px-3 py-2 rounded-lg transition-colors ${
                  showStats 
                    ? 'bg-blue-100 text-blue-700 hover:bg-blue-200' 
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
                title={showStats ? '隐藏统计' : '显示统计'}
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                <span className="text-sm font-medium hidden sm:inline">统计</span>
              </button>
            )}

            {onExport && (
              <button
                onClick={onExport}
                className="flex items-center gap-2 px-3 py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg transition-colors"
                title="导出 CSV"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
                <span className="text-sm font-medium hidden sm:inline">导出</span>
              </button>
            )}

            <button
              onClick={handleRefresh}
              disabled={isCollecting}
              className="flex items-center gap-2 px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors disabled:opacity-50"
            >
              <svg
                className={`w-4 h-4 ${isCollecting ? 'animate-spin' : ''}`}
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              {isCollecting ? '采集中...' : '刷新数据'}
            </button>

            {isCollecting && (
              <div className="flex flex-col items-end gap-1">
                <div className="text-xs text-gray-600">
                  {progress?.current_source || '准备中'}
                </div>
                <div className="w-32 bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-blue-500 h-2 rounded-full" 
                    style={{ width: `${progress?.progress || 0}%` }}
                  ></div>
                </div>
                <div className="text-xs text-gray-500">
                  {progress?.progress || 0}%
                </div>
              </div>
            )}

            {isCompleted && (
              <div className="text-xs text-green-600 flex items-center gap-1">
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                采集完成
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}
