import sys
import os
from pathlib import Path

# Add apps/api to path so we can import core modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../apps/api")))

from core.retriever import retrieve_context
from core.generator import generate_answer, is_advisory_query, REFUSAL_PROMPT

def test_phase_15():
    print("="*60)
    print("🚦  PHASE 15 INTEGRATION TEST — CHROMA CLOUD + GEMINI AI")
    print("="*60)

    # --- Test Case 1: Refusal Engine (Advisory Check) ---
    print("\n[TEST 1] Testing Investment Advice Refusal...")
    q1 = "Which mutual fund is the best to invest in right now?"
    if is_advisory_query(q1):
        print("  ✅ PASS: Advisory query correctly intercepted.")
    else:
        print("  ❌ FAIL: Advisory query was not intercepted.")

    # --- Test Case 2: Retriever Engine (Cloud Connectivity) ---
    print("\n[TEST 2] Testing Chroma Cloud Retrieval (Quant Fund)...")
    q2 = "What is the exit load?"
    scheme = "Quant Small Cap Fund Direct Plan Growth"
    
    try:
        context, citation, updated_date = retrieve_context(q2, scheme, top_k=3)
        if context and "exit load" in context.lower():
            print(f"  ✅ PASS: Context retrieved from Cloud. (Citation: {citation})")
            print(f"  🔍 Snippet: {context[:100]}...")
        else:
            print(f"  ❌ FAIL: Context retrieval failed or returned empty. (Context: {context})")
    except Exception as e:
        print(f"  ❌ FAIL: Error during cloud retrieval: {e}")

    # --- Test Case 3: Generator Engine (Gemini Synthesis) ---
    print("\n[TEST 3] Testing Gemini AI Generation...")
    if not os.getenv("GEMINI_API_KEY"):
        print("  ⚠️  SKIP: Gemini API Key not found in environment.")
    else:
        try:
            test_context = "The exit load for Quant Small Cap Fund is 1% if redeemed within 1 year."
            test_query = "What is the exit load?"
            answer = generate_answer(test_query, test_context)
            if "1%" in answer:
                print(f"  ✅ PASS: Gemini correctly synthesized the answer.")
                print(f"  💬 Answer: {answer}")
            else:
                print(f"  ❌ FAIL: Gemini returned unexpected answer: {answer}")
        except Exception as e:
            print(f"  ❌ FAIL: Error during Gemini generation: {e}")

    print("\n" + "="*60)
    print("🏁  TESTING COMPLETE")
    print("="*60)

if __name__ == "__main__":
    test_phase_15()
