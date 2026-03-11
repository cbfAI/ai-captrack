import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { Header } from '../Header';

describe('Header', () => {
  const defaultProps = {
    onExport: vi.fn(),
    onToggleStats: vi.fn(),
    showStats: true,
  };

  it('renders app title', () => {
    render(<Header {...defaultProps} />);
    expect(screen.getByText('AI CapTrack')).toBeDefined();
  });

  it('renders subtitle', () => {
    render(<Header {...defaultProps} />);
    expect(screen.getByText('发现最新 AI 能力')).toBeDefined();
  });

  it('calls onExport when export button is clicked', () => {
    const onExport = vi.fn();
    render(<Header {...defaultProps} onExport={onExport} />);
    
    const exportButton = screen.getByLabelText('导出数据');
    fireEvent.click(exportButton);
    
    expect(onExport).toHaveBeenCalledTimes(1);
  });

  it('calls onToggleStats when stats toggle is clicked', () => {
    const onToggleStats = vi.fn();
    render(<Header {...defaultProps} onToggleStats={onToggleStats} />);
    
    const statsButton = screen.getByLabelText('隐藏统计');
    fireEvent.click(statsButton);
    
    expect(onToggleStats).toHaveBeenCalledTimes(1);
  });

  it('shows "隐藏统计" label when showStats is true', () => {
    render(<Header {...defaultProps} showStats={true} />);
    expect(screen.getByLabelText('隐藏统计')).toBeDefined();
  });

  it('shows "显示统计" label when showStats is false', () => {
    render(<Header {...defaultProps} showStats={false} />);
    expect(screen.getByLabelText('显示统计')).toBeDefined();
  });

  it('renders GitHub link', () => {
    render(<Header {...defaultProps} />);
    const githubLink = screen.getByLabelText('GitHub');
    expect(githubLink).toBeDefined();
    expect(githubLink.getAttribute('href')).toContain('github.com');
  });
});
