#!/usr/bin/env python3
"""
extract_key_metrics.py - Extract key financial metrics from target mutual fund URLs
Captures: expense ratio, exit load, minimum SIP, lock-in (ELSS), riskometer, benchmark, statement download
"""

import asyncio
import json
import os
import re
from datetime import datetime
from playwright.async_api import async_playwright
from typing import Dict, List, Optional

# Target URLs from architecture.md
TARGET_SCHEMES = {
    "Nippon India Large Cap Fund": "https://groww.in/mutual-funds/nippon-india-large-cap-fund-direct-growth",
    "Nippon India Taiwan Equity Fund": "https://groww.in/mutual-funds/nippon-india-taiwan-equity-fund-direct-growth", 
    "HDFC Mid-Cap Opportunities Fund": "https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth",
    "Quant Small Cap Fund": "https://groww.in/mutual-funds/quant-small-cap-fund-direct-plan-growth",
    "Nippon India Growth Fund": "https://groww.in/mutual-funds/nippon-india-growth-mid-cap-fund-direct-growth"
}

class MutualFundMetricsExtractor:
    def __init__(self):
        self.metrics_data = {}
        
    async def extract_fund_metrics(self, browser, fund_name: str, url: str) -> Dict:
        """Extract all key metrics for a single fund"""
        print(f"\n? Extracting metrics for: {fund_name}")
        print(f"   URL: {url}")
        
        try:
            page = await browser.new_page()
            await page.goto(url, wait_until="networkidle")
            
            # Wait for content to load
            await page.wait_for_timeout(3000)
            
            metrics = {
                "fund_name": fund_name,
                "url": url,
                "extracted_at": datetime.now().isoformat(),
                "expense_ratio": await self.extract_expense_ratio(page),
                "exit_load": await self.extract_exit_load(page),
                "minimum_sip": await self.extract_minimum_sip(page),
                "lock_in_period": await self.extract_lock_in_period(page),
                "riskometer": await self.extract_riskometer(page),
                "benchmark": await self.extract_benchmark(page),
                "statement_download": await self.extract_statement_download(page)
            }
            
            await page.close()
            return metrics
            
        except Exception as e:
            print(f"   ? Error extracting {fund_name}: {e}")
            return {
                "fund_name": fund_name,
                "url": url,
                "extracted_at": datetime.now().isoformat(),
                "error": str(e)
            }
    
    async def extract_expense_ratio(self, page) -> Optional[str]:
        """Extract expense ratio information"""
        try:
            # Look for expense ratio in various formats
            selectors = [
                "text=Expense Ratio",
                "[data-testid*='expense']",
                "text=Total Expense Ratio",
                "text=TER"
            ]
            
            for selector in selectors:
                try:
                    element = await page.locator(selector).first
                    if await element.count() > 0:
                        # Look for the value near this element
                        parent = await element.locator("xpath=../..")
                        text = await parent.text_content()
                        
                        # Extract percentage using regex
                        match = re.search(r'(\d+\.?\d*)\s*%?', text)
                        if match:
                            return f"{match.group(1)}%"
                except:
                    continue
            
            # Try general search for expense ratio patterns
            content = await page.content()
            matches = re.findall(r'expense ratio[:\s]*([0-9.]+)%?', content.lower())
            if matches:
                return f"{matches[0]}%"
                
        except Exception as e:
            print(f"     ? Expense ratio extraction error: {e}")
        
        return None
    
    async def extract_exit_load(self, page) -> Optional[str]:
        """Extract exit load information"""
        try:
            selectors = [
                "text=Exit Load",
                "[data-testid*='exit']",
                "text=Exit load"
            ]
            
            for selector in selectors:
                try:
                    element = await page.locator(selector).first
                    if await element.count() > 0:
                        parent = await element.locator("xpath=../..")
                        text = await parent.text_content()
                        
                        # Look for exit load patterns
                        if "nil" in text.lower() or "0%" in text:
                            return "0% (No exit load)"
                        elif "exit load" in text.lower():
                            # Extract the exit load description
                            lines = text.split('\n')
                            for line in lines:
                                if "exit load" in line.lower():
                                    return line.strip()
                except:
                    continue
            
            # General search
            content = await page.content()
            if "exit load" in content.lower():
                lines = content.split('\n')
                for line in lines:
                    if "exit load" in line.lower():
                        match = re.search(r'exit load[:\s]*([^.]+)', line.lower())
                        if match:
                            return match.group(1).strip()
                            
        except Exception as e:
            print(f"     ? Exit load extraction error: {e}")
        
        return None
    
    async def extract_minimum_sip(self, page) -> Optional[str]:
        """Extract minimum SIP amount"""
        try:
            selectors = [
                "text=Minimum SIP",
                "text=SIP Amount",
                "[data-testid*='sip']",
                "text=Minimum Investment"
            ]
            
            for selector in selectors:
                try:
                    element = await page.locator(selector).first
                    if await element.count() > 0:
                        parent = await element.locator("xpath=../..")
                        text = await parent.text_content()
                        
                        # Look for amount patterns (with currency symbols)
                        match = re.search(r'[\u20B9Rs]\s*([0-9,]+)', text)
                        if match:
                            return f"Rs {match.group(1)}"
                except:
                    continue
            
            # General search
            content = await page.content()
            matches = re.findall(r'minimum sip[:\s]*[\u20B9Rs]?\s*([0-9,]+)', content.lower())
            if matches:
                return f"Rs {matches[0]}"
                
        except Exception as e:
            print(f"     ? Minimum SIP extraction error: {e}")
        
        return None
    
    async def extract_lock_in_period(self, page) -> Optional[str]:
        """Extract lock-in period (especially for ELSS funds)"""
        try:
            selectors = [
                "text=Lock-in",
                "text=Lock In",
                "text=ELSS",
                "[data-testid*='lock']"
            ]
            
            for selector in selectors:
                try:
                    element = await page.locator(selector).first
                    if await element.count() > 0:
                        parent = await element.locator("xpath=../..")
                        text = await parent.text_content()
                        
                        # Look for lock-in period patterns
                        match = re.search(r'lock[-\s]?in[:\s]*([0-9]+)\s*(years?|months?)', text.lower())
                        if match:
                            return f"{match.group(1)} {match.group(2)}"
                        elif "elss" in text.lower():
                            return "3 years (ELSS tax benefit)"
                except:
                    continue
            
            # General search
            content = await page.content()
            if "elss" in content.lower():
                return "3 years (ELSS tax benefit)"
                
        except Exception as e:
            print(f"     ? Lock-in period extraction error: {e}")
        
        return None
    
    async def extract_riskometer(self, page) -> Optional[str]:
        """Extract riskometer classification"""
        try:
            selectors = [
                "text=Riskometer",
                "[data-testid*='risk']",
                "text=Risk Level"
            ]
            
            risk_levels = ["Very Low", "Low", "Moderately Low", "Moderate", "Moderately High", "High", "Very High"]
            
            for selector in selectors:
                try:
                    element = await page.locator(selector).first
                    if await element.count() > 0:
                        parent = await element.locator("xpath=../..")
                        text = await parent.text_content()
                        
                        for risk in risk_levels:
                            if risk.lower() in text.lower():
                                return risk
                except:
                    continue
            
            # General search
            content = await page.content()
            for risk in risk_levels:
                if risk.lower() in content.lower():
                    return risk
                    
        except Exception as e:
            print(f"     ? Riskometer extraction error: {e}")
        
        return None
    
    async def extract_benchmark(self, page) -> Optional[str]:
        """Extract benchmark index information"""
        try:
            selectors = [
                "text=Benchmark",
                "[data-testid*='benchmark']",
                "text=Index"
            ]
            
            for selector in selectors:
                try:
                    element = await page.locator(selector).first
                    if await element.count() > 0:
                        parent = await element.locator("xpath=../..")
                        text = await parent.text_content()
                        
                        # Look for common benchmark indices
                        benchmarks = [
                            "NIFTY 50", "NIFTY 100", "NIFTY 500", "NIFTY Midcap 150",
                            "NIFTY Smallcap 250", "BSE Sensex", "BSE 100", "BSE 200"
                        ]
                        
                        for benchmark in benchmarks:
                            if benchmark in text:
                                return benchmark
                except:
                    continue
            
            # General search
            content = await page.content()
            benchmarks = [
                "NIFTY 50", "NIFTY 100", "NIFTY 500", "NIFTY Midcap 150",
                "NIFTY Smallcap 250", "BSE Sensex", "BSE 100", "BSE 200"
            ]
            
            for benchmark in benchmarks:
                if benchmark in content:
                    return benchmark
                    
        except Exception as e:
            print(f"     ? Benchmark extraction error: {e}")
        
        return None
    
    async def extract_statement_download(self, page) -> Optional[str]:
        """Extract statement download instructions"""
        try:
            selectors = [
                "text=Statement",
                "text=Download",
                "[data-testid*='statement']",
                "text=Capital Gains"
            ]
            
            for selector in selectors:
                try:
                    element = await page.locator(selector).first
                    if await element.count() > 0:
                        parent = await element.locator("xpath=../..")
                        text = await parent.text_content()
                        
                        if "download" in text.lower() and ("statement" in text.lower() or "capital gain" in text.lower()):
                            # Extract download instructions
                            lines = text.split('\n')
                            for line in lines:
                                if any(word in line.lower() for word in ["download", "statement", "capital gain"]):
                                    return line.strip()
                except:
                    continue
            
            # General search
            content = await page.content()
            if "statement" in content.lower() and "download" in content.lower():
                return "Statement download available - Check fund portal"
                
        except Exception as e:
            print(f"     ? Statement download extraction error: {e}")
        
        return None
    
    async def run_extraction(self):
        """Run extraction for all target funds"""
        print("? Starting key metrics extraction...")
        print(f"   Target funds: {len(TARGET_SCHEMES)}")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            
            tasks = []
            for fund_name, url in TARGET_SCHEMES.items():
                task = self.extract_fund_metrics(browser, fund_name, url)
                tasks.append(task)
            
            # Extract all metrics concurrently
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            await browser.close()
        
        # Process results
        for result in results:
            if isinstance(result, Exception):
                print(f"   ? Extraction error: {result}")
            else:
                self.metrics_data[result['fund_name']] = result
        
        return self.metrics_data
    
    def save_results(self, filename: str = "key_fund_metrics.json"):
        """Save extracted metrics to JSON file"""
        os.makedirs("data/extracted", exist_ok=True)
        filepath = os.path.join("data/extracted", filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.metrics_data, f, indent=2, ensure_ascii=False)
        
        print(f"   ? Results saved to: {filepath}")
        return filepath
    
    def display_summary(self):
        """Display a user-friendly summary of extracted metrics"""
        print("\n" + "="*80)
        print("?? MUTUAL FUND KEY METRICS SUMMARY")
        print("="*80)
        
        for fund_name, metrics in self.metrics_data.items():
            print(f"\n? {fund_name}")
            print(f"   URL: {metrics.get('url', 'N/A')}")
            print(f"   Extracted: {metrics.get('extracted_at', 'N/A')}")
            
            if 'error' in metrics:
                print(f"   ? Error: {metrics['error']}")
                continue
            
            print(f"\n   ? Financial Metrics:")
            print(f"      Expense Ratio: {metrics.get('expense_ratio', 'Not found')}")
            print(f"      Exit Load: {metrics.get('exit_load', 'Not found')}")
            print(f"      Minimum SIP: {metrics.get('minimum_sip', 'Not found')}")
            print(f"      Lock-in Period: {metrics.get('lock_in_period', 'Not found')}")
            
            print(f"\n   ? Risk & Performance:")
            print(f"      Riskometer: {metrics.get('riskometer', 'Not found')}")
            print(f"      Benchmark: {metrics.get('benchmark', 'Not found')}")
            
            print(f"\n   ? User Services:")
            print(f"      Statement Download: {metrics.get('statement_download', 'Not found')}")
            
            print("-" * 60)

async def main():
    """Main execution function"""
    extractor = MutualFundMetricsExtractor()
    
    # Extract metrics from all target funds
    await extractor.run_extraction()
    
    # Save results
    extractor.save_results()
    
    # Display summary
    extractor.display_summary()
    
    print(f"\n? Extraction complete! Processed {len(extractor.metrics_data)} funds.")

if __name__ == "__main__":
    asyncio.run(main())
