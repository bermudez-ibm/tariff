import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatCurrency(amount: number, currency = 'USD'): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(amount);
}

export function formatDateTime(iso: string): string {
  return new Date(iso).toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

export function formatRelativeTime(iso: string): string {
  const diff = Date.now() - new Date(iso).getTime();
  const minutes = Math.floor(diff / 60000);
  if (minutes < 1) return 'just now';
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  if (days < 7) return `${days}d ago`;
  const weeks = Math.floor(days / 7);
  if (weeks < 4) return `${weeks}w ago`;
  const months = Math.floor(days / 30);
  return `${months}mo ago`;
}

export function getStatusBadgeColor(status: string): string {
  const statusLower = status.toLowerCase();
  if (statusLower === 'approved' || statusLower === 'resolved' || statusLower === 'qualified') {
    return 'green';
  }
  if (statusLower === 'blocked' || statusLower === 'critical') {
    return 'red';
  }
  if (statusLower === 'contingent' || statusLower === 'under_review') {
    return 'yellow';
  }
  if (statusLower === 'new' || statusLower === 'acknowledged') {
    return 'blue';
  }
  return 'gray';
}

export function getRiskBadgeColor(riskLevel: string): string {
  const riskLower = riskLevel.toLowerCase();
  if (riskLower === 'critical' || riskLower === 'high') {
    return 'red';
  }
  if (riskLower === 'medium' || riskLower === 'material') {
    return 'yellow';
  }
  if (riskLower === 'low' || riskLower === 'watchlist') {
    return 'green';
  }
  if (riskLower === 'non_material' || riskLower === 'informational') {
    return 'gray';
  }
  return 'gray';
}
