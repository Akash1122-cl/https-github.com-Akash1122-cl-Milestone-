"use client";

/**
 * FundMetrics.js - Component for displaying fund metrics and comparisons
 */

import { useState, useEffect } from "react";
import { getAllFunds, getExpenseRatioComparison, getMetricsSummary } from "@/lib/metrics";

export default function FundMetrics() {
  const [funds, setFunds] = useState([]);
  const [comparison, setComparison] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState("overview");

  useEffect(() => {
    loadMetricsData();
  }, []);

  const loadMetricsData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const [fundsData, comparisonData, summaryData] = await Promise.all([
        getAllFunds(),
        getExpenseRatioComparison(),
        getMetricsSummary()
      ]);
      
      setFunds(fundsData);
      setComparison(comparisonData);
      setSummary(summaryData);
    } catch (err) {
      setError("Failed to load fund metrics. Please ensure the backend is running.");
      console.error("Metrics loading error:", err);
    } finally {
      setLoading(false);
    }
  };

  const formatExpenseRatio = (ratio) => {
    if (!ratio) return "N/A";
    return ratio;
  };

  const renderOverview = () => (
    <div className="metrics-overview">
      <h3>Portfolio Overview</h3>
      
      {summary && (
        <div className="summary-grid">
          <div className="summary-card">
            <h4>Total Funds</h4>
            <span className="summary-value">{summary.total_funds}</span>
          </div>
          
          <div className="summary-card">
            <h4>Avg Expense Ratio</h4>
            <span className="summary-value">
              {summary.expense_ratio_stats?.average ? 
                `${summary.expense_ratio_stats.average.toFixed(2)}%` : 
                "N/A"}
            </span>
          </div>
          
          <div className="summary-card">
            <h4>Risk Distribution</h4>
            <div className="risk-badges">
              {Object.entries(summary.risk_distribution || {}).map(([risk, count]) => (
                <span key={risk} className="risk-badge">
                  {risk}: {count}
                </span>
              ))}
            </div>
          </div>
          
          <div className="summary-card">
            <h4>Most Common Benchmark</h4>
            <span className="summary-value">
              {Object.keys(summary.benchmark_distribution || {})[0] || "N/A"}
            </span>
          </div>
        </div>
      )}
      
      <div className="funds-grid">
        {funds.map((fund) => (
          <div key={fund.fund_name} className="fund-card">
            <h4>{fund.fund_name}</h4>
            <div className="fund-metrics">
              <div className="metric">
                <span className="metric-label">Expense Ratio:</span>
                <span className="metric-value">{formatExpenseRatio(fund.expense_ratio)}</span>
              </div>
              <div className="metric">
                <span className="metric-label">Risk Level:</span>
                <span className="metric-value">{fund.riskometer || "N/A"}</span>
              </div>
              <div className="metric">
                <span className="metric-label">Benchmark:</span>
                <span className="metric-value">{fund.benchmark || "N/A"}</span>
              </div>
              <div className="metric">
                <span className="metric-label">Lock-in:</span>
                <span className="metric-value">{fund.lock_in_period || "N/A"}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderComparison = () => (
    <div className="metrics-comparison">
      <h3>Expense Ratio Comparison (Lowest First)</h3>
      
      <div className="comparison-table">
        <div className="table-header">
          <span>Fund Name</span>
          <span>Expense Ratio</span>
          <span>Risk Level</span>
          <span>Benchmark</span>
        </div>
        
        {comparison.map((fund, index) => (
          <div key={fund.fund_name} className={`table-row ${index < 2 ? "top-performer" : ""}`}>
            <span className="fund-name">{fund.fund_name}</span>
            <span className="expense-ratio">{formatExpenseRatio(fund.expense_ratio)}</span>
            <span className="risk-level">{fund.riskometer || "N/A"}</span>
            <span className="benchmark">{fund.benchmark || "N/A"}</span>
          </div>
        ))}
      </div>
      
      <div className="comparison-insights">
        <h4>Key Insights:</h4>
        <ul>
          <li>Most cost-effective: {comparison[0]?.fund_name} ({formatExpenseRatio(comparison[0]?.expense_ratio)})</li>
          <li>Least cost-effective: {comparison[comparison.length - 1]?.fund_name} ({formatExpenseRatio(comparison[comparison.length - 1]?.expense_ratio)})</li>
          <li>All funds have {summary?.risk_distribution?.Low || 0} low-risk rating</li>
          <li>Common benchmark: {summary?.benchmark_distribution && Object.keys(summary.benchmark_distribution)[0]}</li>
        </ul>
      </div>
    </div>
  );

  if (loading) {
    return (
      <div className="fund-metrics loading">
        <div className="loading-spinner">Loading fund metrics...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="fund-metrics error">
        <div className="error-message">{error}</div>
        <button onClick={loadMetricsData} className="retry-button">
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="fund-metrics">
      <div className="metrics-header">
        <h2>?? Fund Metrics Dashboard</h2>
        <div className="tab-navigation">
          <button
            className={`tab-button ${activeTab === "overview" ? "active" : ""}`}
            onClick={() => setActiveTab("overview")}
          >
            Overview
          </button>
          <button
            className={`tab-button ${activeTab === "comparison" ? "active" : ""}`}
            onClick={() => setActiveTab("comparison")}
          >
            Comparison
          </button>
        </div>
      </div>
      
      <div className="metrics-content">
        {activeTab === "overview" && renderOverview()}
        {activeTab === "comparison" && renderComparison()}
      </div>
    </div>
  );
}
