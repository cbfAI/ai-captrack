import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { FilterBar } from '../FilterBar';
import type { CapabilitiesFilter } from '@/types';

describe('FilterBar', () => {
  const defaultProps = {
    filters: {} as CapabilitiesFilter,
    onFiltersChange: vi.fn(),
    totalCount: 100,
  };

  it('renders search input', () => {
    render(<FilterBar {...defaultProps} />);
    expect(screen.getByPlaceholderText('搜索 AI 能力...')).toBeDefined();
  });

  it('renders type select', () => {
    render(<FilterBar {...defaultProps} />);
    expect(screen.getByText('全部类型')).toBeDefined();
  });

  it('renders sort select', () => {
    render(<FilterBar {...defaultProps} />);
    expect(screen.getByText('默认排序（热度）')).toBeDefined();
  });

  it('renders min stars input', () => {
    render(<FilterBar {...defaultProps} />);
    expect(screen.getByLabelText('最低 Stars:')).toBeDefined();
  });

  it('renders total count', () => {
    render(<FilterBar {...defaultProps} />);
    expect(screen.getByText('共 100 个结果')).toBeDefined();
  });

  it('calls onFiltersChange when search is submitted', () => {
    const onFiltersChange = vi.fn();
    render(
      <FilterBar
        {...defaultProps}
        onFiltersChange={onFiltersChange}
      />
    );
    
    const input = screen.getByPlaceholderText('搜索 AI 能力...');
    fireEvent.change(input, { target: { value: 'test search' } });
    
    const searchButton = screen.getByText('搜索');
    fireEvent.click(searchButton);
    
    expect(onFiltersChange).toHaveBeenCalledWith(
      expect.objectContaining({ search: 'test search' })
    );
  });

  it('calls onFiltersChange when type is changed', () => {
    const onFiltersChange = vi.fn();
    render(
      <FilterBar
        {...defaultProps}
        onFiltersChange={onFiltersChange}
      />
    );
    
    const typeSelect = screen.getByDisplayValue('全部类型');
    fireEvent.change(typeSelect, { target: { value: 'Agent' } });
    
    expect(onFiltersChange).toHaveBeenCalledWith(
      expect.objectContaining({ capability_type: 'Agent' })
    );
  });

  it('calls onFiltersChange when sort is changed', () => {
    const onFiltersChange = vi.fn();
    render(
      <FilterBar
        {...defaultProps}
        onFiltersChange={onFiltersChange}
      />
    );
    
    const sortSelect = screen.getByDisplayValue('默认排序（热度）');
    fireEvent.change(sortSelect, { target: { value: 'stars_desc' } });
    
    expect(onFiltersChange).toHaveBeenCalledWith(
      expect.objectContaining({ sort_by: 'stars', sort_order: 'desc' })
    );
  });

  it('calls onFiltersChange when min stars is changed', () => {
    const onFiltersChange = vi.fn();
    render(
      <FilterBar
        {...defaultProps}
        onFiltersChange={onFiltersChange}
      />
    );
    
    const minStarsInput = screen.getByLabelText('最低 Stars:').nextElementSibling as HTMLInputElement;
    if (minStarsInput) {
      fireEvent.change(minStarsInput, { target: { value: '100' } });
      
      expect(onFiltersChange).toHaveBeenCalledWith(
        expect.objectContaining({ min_stars: 100 })
      );
    }
  });

  it('shows clear filters button when filters are active', () => {
    render(
      <FilterBar
        {...defaultProps}
        filters={{ capability_type: 'Agent' }}
      />
    );
    
    expect(screen.getByText('清除筛选')).toBeDefined();
  });

  it('does not show clear filters button when no filters are active', () => {
    render(<FilterBar {...defaultProps} />);
    
    expect(screen.queryByText('清除筛选')).toBeNull();
  });

  it('calls onFiltersChange with empty object when clear filters is clicked', () => {
    const onFiltersChange = vi.fn();
    render(
      <FilterBar
        {...defaultProps}
        onFiltersChange={onFiltersChange}
        filters={{ capability_type: 'Agent', min_stars: 100 }}
      />
    );
    
    const clearButton = screen.getByText('清除筛选');
    fireEvent.click(clearButton);
    
    expect(onFiltersChange).toHaveBeenCalledWith({});
  });

  it('displays current search value in input', () => {
    render(
      <FilterBar
        {...defaultProps}
        filters={{ search: 'existing search' }}
      />
    );
    
    const input = screen.getByDisplayValue('existing search');
    expect(input).toBeDefined();
  });

  it('displays current min stars value', () => {
    render(
      <FilterBar
        {...defaultProps}
        filters={{ min_stars: 500 }}
      />
    );
    
    const input = screen.getByDisplayValue('500');
    expect(input).toBeDefined();
  });
});
