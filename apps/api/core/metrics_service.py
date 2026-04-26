"""
metrics_service.py - Backend service for fund metrics data
Provides structured access to extracted key financial metrics
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

class FundMetricsService:
    """Service for accessing and managing fund metrics data"""
    
    def __init__(self):
        self.metrics_file = os.path.join(os.path.dirname(__file__), "../../../data/extracted/key_fund_metrics.json")
        self._metrics_cache = None
        self._last_loaded = None
    
    def _load_metrics(self) -> Dict[str, Any]:
        """Load metrics from file with caching"""
        try:
            # Check if cache needs refresh
            if (self._metrics_cache is None or 
                self._last_loaded is None or 
                (datetime.now() - self._last_loaded).seconds > 300):  # 5 minute cache
                
                with open(self.metrics_file, 'r', encoding='utf-8') as f:
                    self._metrics_cache = json.load(f)
                    self._last_loaded = datetime.now()
            
            return self._metrics_cache
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}
    
    def get_all_funds(self) -> List[Dict[str, Any]]:
        """Get metrics for all funds"""
        metrics = self._load_metrics()
        return list(metrics.values())
    
    def get_fund_by_name(self, fund_name: str) -> Optional[Dict[str, Any]]:
        """Get metrics for a specific fund by name"""
        metrics = self._load_metrics()
        return metrics.get(fund_name)
    
    def get_funds_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get funds filtered by category (large-cap, mid-cap, small-cap, thematic)"""
        all_funds = self.get_all_funds()
        
        category_keywords = {
            "large-cap": ["large cap", "large-cap"],
            "mid-cap": ["mid cap", "mid-cap"],
            "small-cap": ["small cap", "small-cap"],
            "thematic": ["taiwan", "sector", "thematic"]
        }
        
        keywords = category_keywords.get(category.lower(), [])
        filtered_funds = []
        
        for fund in all_funds:
            fund_name = fund.get('fund_name', '').lower()
            if any(keyword in fund_name for keyword in keywords):
                filtered_funds.append(fund)
        
        return filtered_funds
    
    def get_expense_ratio_comparison(self) -> List[Dict[str, Any]]:
        """Get all funds sorted by expense ratio (lowest first)"""
        all_funds = self.get_all_funds()
        
        # Filter funds with valid expense ratios
        funds_with_ratio = []
        for fund in all_funds:
            expense_ratio = fund.get('expense_ratio')
            if expense_ratio and isinstance(expense_ratio, str):
                # Extract numeric value
                try:
                    ratio_value = float(expense_ratio.replace('%', '').strip())
                    fund['ratio_numeric'] = ratio_value
                    funds_with_ratio.append(fund)
                except ValueError:
                    continue
        
        # Sort by expense ratio
        funds_with_ratio.sort(key=lambda x: x['ratio_numeric'])
        return funds_with_ratio
    
    def get_funds_with_lock_in(self, lock_in_years: int = None) -> List[Dict[str, Any]]:
        """Get funds with specific lock-in period"""
        all_funds = self.get_all_funds()
        filtered_funds = []
        
        for fund in all_funds:
            lock_in = fund.get('lock_in_period', '')
            if lock_in_years is None:
                # Return all funds with any lock-in period
                if lock_in and 'year' in lock_in.lower():
                    filtered_funds.append(fund)
            else:
                # Return funds with specific lock-in period
                if str(lock_in_years) in lock_in:
                    filtered_funds.append(fund)
        
        return filtered_funds
    
    def get_funds_by_risk_level(self, risk_level: str) -> List[Dict[str, Any]]:
        """Get funds filtered by riskometer level"""
        all_funds = self.get_all_funds()
        
        filtered_funds = []
        for fund in all_funds:
            fund_risk = fund.get('riskometer', '').lower()
            if risk_level.lower() in fund_risk:
                filtered_funds.append(fund)
        
        return filtered_funds
    
    def search_funds(self, query: str) -> List[Dict[str, Any]]:
        """Search funds by name or attributes.
        
        Normalizes hyphens/spaces so 'hdfc mid cap' matches 'HDFC Mid-Cap Opportunities Fund'.
        Also matches on individual keywords (words ≥4 chars) for partial queries.
        """
        all_funds = self.get_all_funds()
        # Normalize: lowercase + replace hyphens with spaces
        query_normalized = query.lower().replace('-', ' ')
        query_words = [w for w in query_normalized.split() if len(w) >= 4]
        
        matching_funds = []
        seen = set()
        for fund in all_funds:
            fund_name = fund.get('fund_name', '')
            # Normalize fund name the same way
            fund_name_normalized = fund_name.lower().replace('-', ' ')
            benchmark_normalized = fund.get('benchmark', '').lower().replace('-', ' ')
            
            matched = False
            # Full phrase match (normalized)
            if query_normalized in fund_name_normalized or query_normalized in benchmark_normalized:
                matched = True
            # Keyword match: all significant words must appear in fund name
            elif query_words and all(word in fund_name_normalized for word in query_words):
                matched = True
            # Any keyword match (looser fallback)
            elif query_words and any(word in fund_name_normalized for word in query_words):
                matched = True
            elif query_normalized in fund.get('riskometer', '').lower():
                matched = True
            
            if matched and fund_name not in seen:
                matching_funds.append(fund)
                seen.add(fund_name)
        
        return matching_funds
    
    def get_metric_summary(self) -> Dict[str, Any]:
        """Get summary statistics of all metrics"""
        all_funds = self.get_all_funds()
        
        if not all_funds:
            return {"error": "No fund data available"}
        
        # Calculate statistics
        expense_ratios = []
        risk_levels = {}
        benchmarks = {}
        lock_in_periods = {}
        
        for fund in all_funds:
            # Expense ratio statistics
            ratio = fund.get('expense_ratio')
            if ratio and isinstance(ratio, str):
                try:
                    ratio_value = float(ratio.replace('%', '').strip())
                    expense_ratios.append(ratio_value)
                except ValueError:
                    pass
            
            # Risk level counts
            risk = fund.get('riskometer', 'Unknown')
            risk_levels[risk] = risk_levels.get(risk, 0) + 1
            
            # Benchmark counts
            benchmark = fund.get('benchmark', 'Unknown')
            benchmarks[benchmark] = benchmarks.get(benchmark, 0) + 1
            
            # Lock-in period counts
            lock_in = fund.get('lock_in_period', 'Unknown')
            lock_in_periods[lock_in] = lock_in_periods.get(lock_in, 0) + 1
        
        summary = {
            "total_funds": len(all_funds),
            "expense_ratio_stats": {
                "min": min(expense_ratios) if expense_ratios else None,
                "max": max(expense_ratios) if expense_ratios else None,
                "average": sum(expense_ratios) / len(expense_ratios) if expense_ratios else None
            },
            "risk_distribution": risk_levels,
            "benchmark_distribution": benchmarks,
            "lock_in_distribution": lock_in_periods,
            "last_updated": datetime.now().isoformat()
        }
        
        return summary
    
    def validate_fund_data(self, fund_name: str) -> Dict[str, Any]:
        """Validate data completeness for a specific fund"""
        fund = self.get_fund_by_name(fund_name)
        
        if not fund:
            return {"error": f"Fund '{fund_name}' not found"}
        
        required_fields = [
            'expense_ratio', 'exit_load', 'minimum_sip', 
            'lock_in_period', 'riskometer', 'benchmark'
        ]
        
        validation_result = {
            "fund_name": fund_name,
            "validation_status": "complete",
            "missing_fields": [],
            "present_fields": [],
            "data_quality_score": 0
        }
        
        present_count = 0
        for field in required_fields:
            value = fund.get(field)
            if value and value not in [None, '', 'Not found']:
                validation_result["present_fields"].append(field)
                present_count += 1
            else:
                validation_result["missing_fields"].append(field)
        
        validation_result["data_quality_score"] = (present_count / len(required_fields)) * 100
        
        if validation_result["missing_fields"]:
            validation_result["validation_status"] = "incomplete"
        
        return validation_result

# Global instance for use across the application
fund_metrics_service = FundMetricsService()
