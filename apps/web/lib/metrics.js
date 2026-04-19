/**
 * metrics.js - API client for fund metrics endpoints
 * Provides access to structured fund data and analysis tools
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

/**
 * Get all funds with their metrics
 */
export async function getAllFunds() {
  const response = await fetch(`${API_BASE}/api/metrics/funds`);
  if (!response.ok) throw new Error(`API Error: ${response.status}`);
  return response.json();
}

/**
 * Get a specific fund by name
 */
export async function getFundByName(fundName) {
  const response = await fetch(`${API_BASE}/api/metrics/funds/${encodeURIComponent(fundName)}`);
  if (!response.ok) throw new Error(`API Error: ${response.status}`);
  return response.json();
}

/**
 * Get funds filtered by category
 */
export async function getFundsByCategory(category) {
  const response = await fetch(`${API_BASE}/api/metrics/funds/category/${category}`);
  if (!response.ok) throw new Error(`API Error: ${response.status}`);
  return response.json();
}

/**
 * Get expense ratio comparison (sorted by lowest first)
 */
export async function getExpenseRatioComparison() {
  const response = await fetch(`${API_BASE}/api/metrics/expense-ratio-comparison`);
  if (!response.ok) throw new Error(`API Error: ${response.status}`);
  return response.json();
}

/**
 * Get funds with lock-in period
 */
export async function getFundsWithLockIn(lockInYears = null) {
  const url = lockInYears 
    ? `${API_BASE}/api/metrics/funds/lock-in?lock_in_years=${lockInYears}`
    : `${API_BASE}/api/metrics/funds/lock-in`;
  
  const response = await fetch(url);
  if (!response.ok) throw new Error(`API Error: ${response.status}`);
  return response.json();
}

/**
 * Get funds filtered by risk level
 */
export async function getFundsByRiskLevel(riskLevel) {
  const response = await fetch(`${API_BASE}/api/metrics/funds/risk/${riskLevel}`);
  if (!response.ok) throw new Error(`API Error: ${response.status}`);
  return response.json();
}

/**
 * Search funds by name or attributes
 */
export async function searchFunds(query) {
  const response = await fetch(`${API_BASE}/api/metrics/search?q=${encodeURIComponent(query)}`);
  if (!response.ok) throw new Error(`API Error: ${response.status}`);
  return response.json();
}

/**
 * Get metrics summary statistics
 */
export async function getMetricsSummary() {
  const response = await fetch(`${API_BASE}/api/metrics/summary`);
  if (!response.ok) throw new Error(`API Error: ${response.status}`);
  return response.json();
}

/**
 * Get available categories
 */
export async function getAvailableCategories() {
  const response = await fetch(`${API_BASE}/api/metrics/categories`);
  if (!response.ok) throw new Error(`API Error: ${response.status}`);
  return response.json();
}

/**
 * Get available risk levels
 */
export async function getAvailableRiskLevels() {
  const response = await fetch(`${API_BASE}/api/metrics/risk-levels`);
  if (!response.ok) throw new Error(`API Error: ${response.status}`);
  return response.json();
}

/**
 * Get available benchmarks
 */
export async function getAvailableBenchmarks() {
  const response = await fetch(`${API_BASE}/api/metrics/benchmarks`);
  if (!response.ok) throw new Error(`API Error: ${response.status}`);
  return response.json();
}

/**
 * Validate fund data completeness
 */
export async function validateFundData(fundName) {
  const response = await fetch(`${API_BASE}/api/metrics/validate/${encodeURIComponent(fundName)}`);
  if (!response.ok) throw new Error(`API Error: ${response.status}`);
  return response.json();
}
