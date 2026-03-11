import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { Pagination } from '../Pagination';

describe('Pagination', () => {
  it('renders current page and total pages', () => {
    render(
      <Pagination
        currentPage={2}
        totalPages={5}
        onPageChange={() => {}}
      />
    );
    expect(screen.getByText('第 2 / 5 页')).toBeDefined();
  });

  it('disables previous button on first page', () => {
    render(
      <Pagination
        currentPage={1}
        totalPages={5}
        onPageChange={() => {}}
      />
    );
    const prevButton = screen.getByLabelText('上一页');
    expect(prevButton.hasAttribute('disabled')).toBe(true);
  });

  it('disables next button on last page', () => {
    render(
      <Pagination
        currentPage={5}
        totalPages={5}
        onPageChange={() => {}}
      />
    );
    const nextButton = screen.getByLabelText('下一页');
    expect(nextButton.hasAttribute('disabled')).toBe(true);
  });

  it('enables both buttons on middle page', () => {
    render(
      <Pagination
        currentPage={3}
        totalPages={5}
        onPageChange={() => {}}
      />
    );
    const prevButton = screen.getByLabelText('上一页');
    const nextButton = screen.getByLabelText('下一页');
    expect(prevButton.hasAttribute('disabled')).toBe(false);
    expect(nextButton.hasAttribute('disabled')).toBe(false);
  });

  it('calls onPageChange with previous page when previous button is clicked', () => {
    const onPageChange = vi.fn();
    render(
      <Pagination
        currentPage={3}
        totalPages={5}
        onPageChange={onPageChange}
      />
    );
    
    const prevButton = screen.getByLabelText('上一页');
    fireEvent.click(prevButton);
    
    expect(onPageChange).toHaveBeenCalledWith(2);
  });

  it('calls onPageChange with next page when next button is clicked', () => {
    const onPageChange = vi.fn();
    render(
      <Pagination
        currentPage={3}
        totalPages={5}
        onPageChange={onPageChange}
      />
    );
    
    const nextButton = screen.getByLabelText('下一页');
    fireEvent.click(nextButton);
    
    expect(onPageChange).toHaveBeenCalledWith(4);
  });

  it('does not call onPageChange when disabled previous button is clicked', () => {
    const onPageChange = vi.fn();
    render(
      <Pagination
        currentPage={1}
        totalPages={5}
        onPageChange={onPageChange}
      />
    );
    
    const prevButton = screen.getByLabelText('上一页');
    fireEvent.click(prevButton);
    
    expect(onPageChange).not.toHaveBeenCalled();
  });

  it('does not call onPageChange when disabled next button is clicked', () => {
    const onPageChange = vi.fn();
    render(
      <Pagination
        currentPage={5}
        totalPages={5}
        onPageChange={onPageChange}
      />
    );
    
    const nextButton = screen.getByLabelText('下一页');
    fireEvent.click(nextButton);
    
    expect(onPageChange).not.toHaveBeenCalled();
  });

  it('renders page numbers when total pages is small', () => {
    render(
      <Pagination
        currentPage={2}
        totalPages={3}
        onPageChange={() => {}}
      />
    );
    expect(screen.getByText('1')).toBeDefined();
    expect(screen.getByText('2')).toBeDefined();
    expect(screen.getByText('3')).toBeDefined();
  });

  it('calls onPageChange with clicked page number', () => {
    const onPageChange = vi.fn();
    render(
      <Pagination
        currentPage={2}
        totalPages={5}
        onPageChange={onPageChange}
      />
    );
    
    const page4Button = screen.getByText('4');
    fireEvent.click(page4Button);
    
    expect(onPageChange).toHaveBeenCalledWith(4);
  });
});
