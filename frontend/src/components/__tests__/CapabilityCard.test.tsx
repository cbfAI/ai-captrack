import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { CapabilityCard } from '../CapabilityCard';
import type { AICapability } from '@/types';

const mockCapability: AICapability = {
  id: '1',
  name: 'Test AI Model',
  description: 'A test AI model description',
  translated_description: '测试AI模型描述',
  capability_type: 'Model',
  source: 'github',
  source_url: 'https://github.com/test/model',
  is_open_source: true,
  key_features: ['feature1', 'feature2'],
  pain_points: ['pain1'],
  differentiation: 'Different from others',
  stars: 1000,
  heat_score: 950.5,
  heat_trend: 'rising',
  thumbs_up: 50,
  thumbs_down: 5,
  metadata_: { language: 'Python' },
  created_at: '2024-01-01T00:00:00Z',
  updated_at: '2024-01-01T00:00:00Z',
};

describe('CapabilityCard', () => {
  it('renders capability name', () => {
    render(
      <CapabilityCard
        capability={mockCapability}
        onClick={() => {}}
        onShare={() => {}}
      />
    );
    expect(screen.getByText('Test AI Model')).toBeDefined();
  });

  it('renders translated description when available', () => {
    render(
      <CapabilityCard
        capability={mockCapability}
        onClick={() => {}}
        onShare={() => {}}
      />
    );
    expect(screen.getByText('测试AI模型描述')).toBeDefined();
  });

  it('renders original description when translated is not available', () => {
    const capabilityWithoutTranslation = {
      ...mockCapability,
      translated_description: null,
    };
    render(
      <CapabilityCard
        capability={capabilityWithoutTranslation}
        onClick={() => {}}
        onShare={() => {}}
      />
    );
    expect(screen.getByText('A test AI model description')).toBeDefined();
  });

  it('renders stars count', () => {
    render(
      <CapabilityCard
        capability={mockCapability}
        onClick={() => {}}
        onShare={() => {}}
      />
    );
    expect(screen.getByText('1,000')).toBeDefined();
  });

  it('renders heat score', () => {
    render(
      <CapabilityCard
        capability={mockCapability}
        onClick={() => {}}
        onShare={() => {}}
      />
    );
    expect(screen.getByText('950.5')).toBeDefined();
  });

  it('renders heat trend indicator for rising', () => {
    render(
      <CapabilityCard
        capability={mockCapability}
        onClick={() => {}}
        onShare={() => {}}
      />
    );
    // 上升趋势应该显示向上箭头
    expect(screen.getByText('↗')).toBeDefined();
  });

  it('calls onClick when card is clicked', () => {
    const handleClick = vi.fn();
    render(
      <CapabilityCard
        capability={mockCapability}
        onClick={handleClick}
        onShare={() => {}}
      />
    );
    
    const card = screen.getByText('Test AI Model').closest('.capability-card');
    if (card) {
      fireEvent.click(card);
      expect(handleClick).toHaveBeenCalledTimes(1);
    }
  });

  it('calls onShare when share button is clicked', () => {
    const handleShare = vi.fn();
    render(
      <CapabilityCard
        capability={mockCapability}
        onClick={() => {}}
        onShare={handleShare}
      />
    );
    
    const shareButton = screen.getByLabelText('分享');
    if (shareButton) {
      fireEvent.click(shareButton);
      expect(handleShare).toHaveBeenCalledTimes(1);
    }
  });

  it('renders capability type badge', () => {
    render(
      <CapabilityCard
        capability={mockCapability}
        onClick={() => {}}
        onShare={() => {}}
      />
    );
    expect(screen.getByText('Model')).toBeDefined();
  });

  it('renders source badge', () => {
    render(
      <CapabilityCard
        capability={mockCapability}
        onClick={() => {}}
        onShare={() => {}}
      />
    );
    expect(screen.getByText('github')).toBeDefined();
  });

  it('renders open source badge when is_open_source is true', () => {
    render(
      <CapabilityCard
        capability={mockCapability}
        onClick={() => {}}
        onShare={() => {}}
      />
    );
    expect(screen.getByText('开源')).toBeDefined();
  });

  it('does not render open source badge when is_open_source is false', () => {
    const closedSourceCapability = { ...mockCapability, is_open_source: false };
    render(
      <CapabilityCard
        capability={closedSourceCapability}
        onClick={() => {}}
        onShare={() => {}}
      />
    );
    expect(screen.queryByText('开源')).toBeNull();
  });

  it('renders thumbs up and thumbs down counts', () => {
    render(
      <CapabilityCard
        capability={mockCapability}
        onClick={() => {}}
        onShare={() => {}}
      />
    );
    expect(screen.getByText('50')).toBeDefined();
    expect(screen.getByText('5')).toBeDefined();
  });
});
