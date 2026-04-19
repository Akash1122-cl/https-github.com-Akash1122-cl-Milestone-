import os
import sys

# Append the API directory so imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../apps/api")))

from fastapi.testclient import TestClient
from main import app

def run_live_tests():
    print("==================================================================")
    print("🚀 LIVE API ENDPOINT TESTING (FastAPI TestClient)")
    print("==================================================================\n")
    
    # Needs to be initialized with the app
    client = TestClient(app)

    # ---------------------------------------------------------
    print("▶️  [TEST 1] Testing Guardrail Engine (Advisory Query)")
    print("Query: 'Should I invest my money in HDFC or Nippon?'")
    try:
        response = client.post(
            "/api/chat/query", 
            json={
                "thread_id": "run-1",
                "query": "Should I invest my money in HDFC or Nippon?",
                "scheme_name": None
            }
        )
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Answer: {data.get('answer', '')}")
        print(f"Blocked (is_advisory): {data.get('is_advisory')}")
    except Exception as e:
        print(f"❌ Error: {e}")
    print("-" * 65)

    # ---------------------------------------------------------
    print("\n▶️  [TEST 2] Testing Semantic Retrieval & AI Generation (Factual Query)")
    print("Query: 'What is the exact expense ratio?'")
    print("Target Schema: 'Nippon India Target URL' equivalent...")
    
    # We will search for Nippon India Growth Fund
    try:
        response = client.post(
            "/api/chat/query", 
            json={
                "thread_id": "run-2",
                "query": "What is the expense ratio?",
                "scheme_name": "Nippon India Growth Mid Cap Fund Direct Growth"
            }
        )
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Bot Output: {data.get('answer', '')}")
        print(f"Citation Attached: {data.get('citation', 'None')}")
        print(f"Last Updated Meta: {data.get('last_updated', 'None')}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n==================================================================")
    print("🏁 LIVE TESTING COMPLETE")
    print("==================================================================")

if __name__ == "__main__":
    run_live_tests()
