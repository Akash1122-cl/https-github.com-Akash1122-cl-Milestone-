#!/usr/bin/env python3
"""
demo_script.py - Automated demo script for Mutual Fund FAQ Assistant
Creates a 3-minute video demonstration of key features
"""

import asyncio
import time
from playwright.async_api import async_playwright
import json
import os

async def create_demo_video():
    """Create a 3-minute demo video of the Mutual Fund FAQ Assistant"""
    
    print("?? Starting demo video recording...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(record_video_dir="demo_videos")
        page = await context.new_page()
        
        # Navigate to the application
        await page.goto("http://localhost:3000")
        await page.wait_for_load_state("networkidle")
        
        print("?? Recording demo video...")
        
        # Demo sequence (3 minutes total)
        demo_steps = [
            # 0:00 - 0:30: Introduction
            {
                "action": "type_welcome",
                "description": "Show welcome message and disclaimer",
                "duration": 30
            },
            
            # 0:30 - 1:00: Basic factual queries
            {
                "action": "ask_expense_ratio",
                "description": "Ask about expense ratio for Nippon India Large Cap Fund",
                "duration": 30
            },
            {
                "action": "ask_risk_level", 
                "description": "Ask about riskometer for Quant Small Cap Fund",
                "duration": 30
            },
            
            # 1:00 - 1:30: Advisory query test
            {
                "action": "ask_advisory",
                "description": "Ask 'Should I invest in HDFC or Nippon?' to test refusal",
                "duration": 30
            },
            
            # 1:30 - 2:00: Multi-session features
            {
                "action": "create_session",
                "description": "Create new chat session",
                "duration": 15
            },
            {
                "action": "switch_session",
                "description": "Switch between sessions",
                "duration": 15
            },
            
            # 2:00 - 2:30: Metrics dashboard
            {
                "action": "switch_to_metrics",
                "description": "Switch to metrics dashboard view",
                "duration": 15
            },
            {
                "action": "show_overview",
                "description": "Show portfolio overview with statistics",
                "duration": 15
            },
            {
                "action": "show_comparison",
                "description": "Show expense ratio comparison table",
                "duration": 15
            },
            
            # 2:30 - 3:00: Advanced features
            {
                "action": "mobile_view",
                "description": "Show mobile responsiveness",
                "duration": 15
            },
            {
                "action": "final_summary",
                "description": "Show system capabilities summary",
                "duration": 15
            }
        ]
        
        # Execute demo steps
        for i, step in enumerate(demo_steps):
            print(f"?? Step {i+1}/{len(demo_steps)}: {step['description']}")
            
            if step["action"] == "type_welcome":
                await page.locator('.input-field').fill("Welcome to Mutual Fund FAQ Assistant!")
                await page.wait_for_timeout(2000)
                
            elif step["action"] == "ask_expense_ratio":
                await page.locator('.input-field').fill("What is the expense ratio for Nippon India Large Cap Fund?")
                await page.locator('.send-btn').click()
                await page.wait_for_timeout(3000)
                
            elif step["action"] == "ask_risk_level":
                await page.locator('.input-field').fill("What is the riskometer rating for Quant Small Cap Fund?")
                await page.locator('.send-btn').click()
                await page.wait_for_timeout(3000)
                
            elif step["action"] == "ask_advisory":
                await page.locator('.input-field').fill("Should I invest in HDFC or Nippon?")
                await page.locator('.send-btn').click()
                await page.wait_for_timeout(3000)
                
            elif step["action"] == "create_session":
                await page.locator('text="New Session"').click()
                await page.wait_for_timeout(2000)
                
            elif step["action"] == "switch_session":
                await page.locator('.session-item').first.click()
                await page.wait_for_timeout(2000)
                
            elif step["action"] == "switch_to_metrics":
                await page.locator('text="?? Metrics"').click()
                await page.wait_for_timeout(2000)
                
            elif step["action"] == "show_overview":
                await page.locator('text="Overview"').click()
                await page.wait_for_timeout(2000)
                
            elif step["action"] == "show_comparison":
                await page.locator('text="Comparison"').click()
                await page.wait_for_timeout(2000)
                
            elif step["action"] == "mobile_view":
                # Simulate mobile view
                await page.set_viewport_size({"width": 375, "height": 667})
                await page.wait_for_timeout(2000)
                # Reset to desktop
                await page.set_viewport_size({"width": 1280, "height": 720})
                
            elif step["action"] == "final_summary":
                await page.locator('text="?? Chat"').click()
                await page.wait_for_timeout(2000)
            
            # Wait for step duration
            await page.wait_for_timeout(step["duration"] * 1000)
        
        await browser.close()
        
        print("?? Demo video completed!")
        print("?? Video saved to: demo_videos/")
        
        # Create demo summary
        demo_summary = {
            "video_path": "demo/videos/mutual_fund_demo.mp4",
            "duration": "3 minutes",
            "features_demonstrated": [
                "Multi-session chat with isolation",
                "Facts-only responses with citations", 
                "Advisory query refusal",
                "Real-time metrics dashboard",
                "Expense ratio comparison",
                "Mobile responsiveness",
                "SEBI compliance"
            ],
            "access_instructions": "Run 'python demo_script.py' to regenerate demo"
        }
        
        with open("demo_summary.json", "w") as f:
            json.dump(demo_summary, f, indent=2)
        
        print("?? Demo summary saved to: demo_summary.json")
        print(f"?? Access demo at: http://localhost:3000")

def create_jupyter_notebook():
    """Create a Jupyter notebook for interactive demo"""
    
    notebook_content = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# Mutual Fund FAQ Assistant - Interactive Demo\n",
                    "\n",
                    "## ? Working Prototype\n",
                    "**Live Demo**: http://localhost:3000\n",
                    "\n",
                    "This notebook provides an interactive demonstration of the Mutual Fund FAQ Assistant system.\n",
                    "\n",
                    "## ? Features to Test\n",
                    "1. **Multi-Session Chat**: Create and manage multiple conversation threads\n",
                    "2. **Facts-Only Responses**: Source-backed answers with citations\n", 
                    "3. **Advisory Guardrails**: Automatic refusal of investment advice\n",
                    "4. **Real-Time Metrics**: Live fund data and comparison tools\n",
                    "5. **SEBI Compliance**: Educational responses with regulatory compliance\n"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Test the live demo\n",
                    "import requests\n",
                    "import json\n",
                    "\n",
                    "# Test basic factual query\n",
                    "response = requests.post(\n",
                    "    'http://127.0.0.1:8000/api/chat/query',\n",
                    "    json={\n",
                    "        'thread_id': 'test-session',\n",
                    "        'query': 'What is the expense ratio for Nippon India Large Cap Fund?',\n",
                    "        'scheme_name': None\n",
                    "    }\n",
                    ")\n",
                    "\n",
                    "if response.status_code == 200:\n",
                    "    data = response.json()\n",
                    "    print(f'Answer: {data[\"answer\"]}')\n",
                    "    print(f'Citation: {data[\"citation\"]}')\n",
                    "    print(f'Is Advisory: {data[\"is_advisory\"]}')\n",
                    "else:\n",
                    "    print('Error:', response.status_code)\n",
                    "\n",
                    "# Test metrics API\n",
                    "metrics_response = requests.get('http://127.0.0.1:8000/api/metrics/funds')\n",
                    "if metrics_response.status_code == 200:\n",
                    "    funds = metrics_response.json()\n",
                    "    print(f'Total funds: {len(funds)}')\n",
                    "    for fund in funds:\n",
                    "        print(f'{fund[\"fund_name\"]}: {fund[\"expense_ratio\"]}')\n"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.9.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }
    
    with open("demo_notebook.ipynb", "w") as f:
        json.dump(notebook_content, f, indent=2)
    
    print("?? Jupyter notebook created: demo_notebook.ipynb")

if __name__ == "__main__":
    print("?? Mutual Fund FAQ Assistant Demo Generator")
    print("Choose demo option:")
    print("1. Create 3-minute demo video")
    print("2. Create interactive Jupyter notebook")
    print("3. Both")
    
    choice = input("Enter your choice (1-3): ").strip()
    
    if choice == "1":
        asyncio.run(create_demo_video())
    elif choice == "2":
        create_jupyter_notebook()
    elif choice == "3":
        asyncio.run(create_demo_video())
        create_jupyter_notebook()
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")
