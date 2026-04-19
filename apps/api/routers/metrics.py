"""
metrics.py - API router for fund metrics endpoints
Provides RESTful access to fund metrics data and analysis
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from core.metrics_service import fund_metrics_service

router = APIRouter(prefix="/api/metrics", tags=["fund-metrics"])

class FundMetricsResponse(BaseModel):
    fund_name: str
    url: str
    extracted_at: str
    expense_ratio: Optional[str]
    exit_load: Optional[str]
    minimum_sip: Optional[str]
    lock_in_period: Optional[str]
    riskometer: Optional[str]
    benchmark: Optional[str]
    statement_download: Optional[str]

class MetricsSummaryResponse(BaseModel):
    total_funds: int
    expense_ratio_stats: Dict[str, Optional[float]]
    risk_distribution: Dict[str, int]
    benchmark_distribution: Dict[str, int]
    lock_in_distribution: Dict[str, int]
    last_updated: str

class ValidationResult(BaseModel):
    fund_name: str
    validation_status: str
    missing_fields: List[str]
    present_fields: List[str]
    data_quality_score: float

@router.get("/funds", response_model=List[FundMetricsResponse])
async def get_all_funds():
    """Get metrics for all available funds"""
    try:
        funds = fund_metrics_service.get_all_funds()
        return funds
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving funds: {str(e)}")

@router.get("/funds/{fund_name}", response_model=FundMetricsResponse)
async def get_fund_by_name(fund_name: str):
    """Get metrics for a specific fund by name"""
    try:
        fund = fund_metrics_service.get_fund_by_name(fund_name)
        if not fund:
            raise HTTPException(status_code=404, detail=f"Fund '{fund_name}' not found")
        return fund
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving fund: {str(e)}")

@router.get("/funds/category/{category}", response_model=List[FundMetricsResponse])
async def get_funds_by_category(category: str):
    """Get funds filtered by category (large-cap, mid-cap, small-cap, thematic)"""
    try:
        funds = fund_metrics_service.get_funds_by_category(category)
        if not funds:
            raise HTTPException(status_code=404, detail=f"No funds found for category '{category}'")
        return funds
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving funds by category: {str(e)}")

@router.get("/expense-ratio-comparison", response_model=List[FundMetricsResponse])
async def get_expense_ratio_comparison():
    """Get all funds sorted by expense ratio (lowest first)"""
    try:
        funds = fund_metrics_service.get_expense_ratio_comparison()
        return funds
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving expense ratio comparison: {str(e)}")

@router.get("/funds/lock-in", response_model=List[FundMetricsResponse])
async def get_funds_with_lock_in(lock_in_years: Optional[int] = Query(None, description="Filter by specific lock-in period in years")):
    """Get funds with lock-in period, optionally filtered by specific years"""
    try:
        funds = fund_metrics_service.get_funds_with_lock_in(lock_in_years)
        return funds
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving funds with lock-in: {str(e)}")

@router.get("/funds/risk/{risk_level}", response_model=List[FundMetricsResponse])
async def get_funds_by_risk_level(risk_level: str):
    """Get funds filtered by riskometer level"""
    try:
        funds = fund_metrics_service.get_funds_by_risk_level(risk_level)
        if not funds:
            raise HTTPException(status_code=404, detail=f"No funds found with risk level '{risk_level}'")
        return funds
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving funds by risk level: {str(e)}")

@router.get("/search", response_model=List[FundMetricsResponse])
async def search_funds(q: str = Query(..., description="Search query for fund names or attributes")):
    """Search funds by name or attributes"""
    try:
        if not q or len(q.strip()) < 2:
            raise HTTPException(status_code=400, detail="Search query must be at least 2 characters")
        
        funds = fund_metrics_service.search_funds(q.strip())
        return funds
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching funds: {str(e)}")

@router.get("/summary", response_model=MetricsSummaryResponse)
async def get_metrics_summary():
    """Get summary statistics of all fund metrics"""
    try:
        summary = fund_metrics_service.get_metric_summary()
        if "error" in summary:
            raise HTTPException(status_code=404, detail=summary["error"])
        return summary
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving metrics summary: {str(e)}")

@router.get("/validate/{fund_name}", response_model=ValidationResult)
async def validate_fund_data(fund_name: str):
    """Validate data completeness for a specific fund"""
    try:
        validation = fund_metrics_service.validate_fund_data(fund_name)
        if "error" in validation:
            raise HTTPException(status_code=404, detail=validation["error"])
        return validation
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error validating fund data: {str(e)}")

@router.get("/categories")
async def get_available_categories():
    """Get list of available fund categories"""
    try:
        categories = ["large-cap", "mid-cap", "small-cap", "thematic"]
        return {"categories": categories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving categories: {str(e)}")

@router.get("/risk-levels")
async def get_available_risk_levels():
    """Get list of available risk levels"""
    try:
        summary = fund_metrics_service.get_metric_summary()
        risk_levels = list(summary.get("risk_distribution", {}).keys())
        return {"risk_levels": risk_levels}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving risk levels: {str(e)}")

@router.get("/benchmarks")
async def get_available_benchmarks():
    """Get list of available benchmarks"""
    try:
        summary = fund_metrics_service.get_metric_summary()
        benchmarks = list(summary.get("benchmark_distribution", {}).keys())
        return {"benchmarks": benchmarks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving benchmarks: {str(e)}")
