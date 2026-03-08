import { useState } from 'react';
import type { CapabilityType, CapabilitiesFilter } from '@/types';

interface FilterBarProps {
  filters: CapabilitiesFilter;
  onFiltersChange: (filters: CapabilitiesFilter) => void;
  totalCount: number;
}

const capabilityTypes: { value: CapabilityType | ''; label: string }[] = [
  { value: '', label: '全部类型' },
  { value: 'Agent', label: 'Agent' },
  { value: 'Code', label: 'Code' },
  { value: 'Model', label: 'Model' },
];

type SortOption = 'stars_desc' | 'stars_asc' | 'heat_desc' | 'heat_asc' | 'name_asc' | 'name_desc';

const sortOptions: { value: SortOption; label: string }[] = [
  { value: 'stars_desc', label: '⭐ Stars 从高到低' },
  { value: 'stars_asc', label: '⭐ Stars 从低到高' },
  { value: 'heat_desc', label: '🔥 热度从高到低' },
  { value: 'heat_asc', label: '🔥 热度从低到高' },
  { value: 'name_asc', label: '📝 名称 A-Z' },
  { value: 'name_desc', label: '📝 名称 Z-A' },
];

export function FilterBar({ filters, onFiltersChange, totalCount }: FilterBarProps) {
  const [searchInput, setSearchInput] = useState(filters.search || '');

  const handleTypeChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value as CapabilityType | '';
    onFiltersChange({
      ...filters,
      capability_type: value || undefined,
    });
  };

  const handleSortChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value as SortOption;
    onFiltersChange({
      ...filters,
      sort: value,
    });
  };

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onFiltersChange({
      ...filters,
      search: searchInput || undefined,
    });
  };

  const handleMinStarsChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value ? parseInt(e.target.value) : undefined;
    onFiltersChange({
      ...filters,
      min_stars: value,
    });
  };

  const handleClearFilters = () => {
    setSearchInput('');
    onFiltersChange({});
  };

  const hasActiveFilters = filters.capability_type || filters.min_stars || filters.search || filters.sort;

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4 mb-6">
      <div className="flex flex-wrap items-center gap-4">
        <div className="flex-1 min-w-[200px]">
          <form onSubmit={handleSearchSubmit} className="flex gap-2">
            <input
              type="text"
              value={searchInput}
              onChange={(e) => setSearchInput(e.target.value)}
              placeholder="搜索 AI 能力..."
              className="flex-1 px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
            />
            <button type="submit" className="btn-primary">
              搜索
            </button>
          </form>
        </div>

        <select
          value={filters.capability_type || ''}
          onChange={handleTypeChange}
          className="px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white"
        >
          {capabilityTypes.map((type) => (
            <option key={type.value} value={type.value}>
              {type.label}
            </option>
          ))}
        </select>

        <select
          value={filters.sort || ''}
          onChange={handleSortChange}
          className="px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white"
        >
          <option value="">排序方式</option>
          {sortOptions.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>

        <div className="flex items-center gap-2">
          <label className="text-sm text-gray-600">最低 Stars:</label>
          <input
            type="number"
            value={filters.min_stars || ''}
            onChange={handleMinStarsChange}
            placeholder="0"
            className="w-24 px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        {hasActiveFilters && (
          <button
            onClick={handleClearFilters}
            className="text-sm text-gray-500 hover:text-gray-700 px-3 py-2 rounded-lg hover:bg-gray-100 transition-colors"
          >
            清除筛选
          </button>
        )}

        <div className="ml-auto text-sm text-gray-500 font-medium">
          共 {totalCount} 个结果
        </div>
      </div>
    </div>
  );
}
