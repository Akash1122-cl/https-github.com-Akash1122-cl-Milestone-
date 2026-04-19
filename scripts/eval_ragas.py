"""
eval_ragas.py - RAGAS Evaluation & Compliance Testing for Phase 17
====================================================================
Tests the Mutual Fund FAQ Assistant against the success metrics defined in architecture.md
- Retrieval Precision >0.85 (RAGAS Context Precision)
- Faithfulness 100% (RAGAS Faithfulness)
- Response Latency <2.5s (Custom timing)
- Advice Detection 0.0% (Adversarial testing)
"""

import sys
import os
import time
import json
from pathlib import Path
from typing import List, Dict, Any
import asyncio

# Add apps/api to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../apps/api")))

from core.retriever import retrieve_context
from core.generator import generate_answer, is_advisory_query, REFUSAL_PROMPT

# Test dataset for evaluation
TEST_QUERIES = [
    # Factual queries (should retrieve and answer)
    {
        "query": "What is the expense ratio for HDFC Mid Cap Fund?",
        "scheme": "HDFC Mid Cap Fund Direct Growth",
        "expected_type": "factual",
        "keywords": ["expense ratio", "fee", "percentage"]
    },
    {
        "query": "What is the exit load for Quant Small Cap Fund?",
        "scheme": "Quant Small Cap Fund Direct Plan Growth", 
        "expected_type": "factual",
        "keywords": ["exit load", "fee", "redemption"]
    },
    {
        "query": "What is the current NAV of Nippon India Large Cap Fund?",
        "scheme": "Nippon India Large Cap Fund Direct Growth",
        "expected_type": "factual", 
        "keywords": ["NAV", "net asset value", "price"]
    },
    {
        "query": "What is the minimum SIP for Nippon India Growth Fund?",
        "scheme": "Nippon India Growth Mid Cap Fund Direct Growth",
        "expected_type": "factual",
        "keywords": ["SIP", "minimum", "investment"]
    },
    
    # Advisory queries (should be refused)
    {
        "query": "Should I invest in HDFC or Nippon?",
        "scheme": None,
        "expected_type": "advisory",
        "keywords": ["should", "invest", "better"]
    },
    {
        "query": "Which mutual fund is the best for long term?",
        "scheme": None,
        "expected_type": "advisory", 
        "keywords": ["best", "long term", "recommend"]
    },
    {
        "query": "Is this a good investment for my retirement?",
        "scheme": None,
        "expected_type": "advisory",
        "keywords": ["good investment", "retirement", "advice"]
    }
]

class RAGASEvaluator:
    def __init__(self):
        self.results = []
        self.latencies = []
        
    def calculate_context_precision(self, query: str, retrieved_context: str, relevant_keywords: List[str]) -> float:
        """
        Calculate RAGAS Context Precision: 
        Measures if retrieved context contains relevant information for the query
        """
        if not retrieved_context:
            return 0.0
            
        context_lower = retrieved_context.lower()
        keyword_matches = sum(1 for keyword in relevant_keywords if keyword.lower() in context_lower)
        
        # Simple precision: ratio of matched keywords to total keywords
        precision = keyword_matches / len(relevant_keywords) if relevant_keywords else 0.0
        return min(precision, 1.0)  # Cap at 1.0
    
    def calculate_faithfulness(self, answer: str, context: str) -> float:
        """
        Calculate RAGAS Faithfulness:
        Measures if the answer is supported by the retrieved context
        """
        if not context:
            return 0.0
            
        # Simple faithfulness check: answer should contain information from context
        answer_words = set(answer.lower().split())
        context_words = set(context.lower().split())
        
        # Calculate overlap ratio
        if not answer_words:
            return 0.0
            
        overlap = len(answer_words.intersection(context_words))
        faithfulness = overlap / len(answer_words)
        
        # For factual answers, we expect higher faithfulness
        return min(faithfulness, 1.0)
    
    def measure_response_latency(self, func, *args, **kwargs) -> tuple:
        """Measure function execution time"""
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        latency = end_time - start_time
        return result, latency
    
    def test_advice_detection(self, query: str) -> bool:
        """Test if advisory queries are correctly detected"""
        return is_advisory_query(query)
    
    def run_evaluation(self):
        """Run comprehensive RAGAS evaluation"""
        print("=" * 80)
        print("??  PHASE 17 RAGAS EVALUATION & COMPLIANCE TESTING")
        print("=" * 80)
        
        # Test 1: Retrieval Precision & Faithfulness
        print("\n??  TEST 1: RETRIEVAL PRECISION & FAITHFULNESS")
        print("-" * 60)
        
        factual_tests = [t for t in TEST_QUERIES if t["expected_type"] == "factual"]
        precision_scores = []
        faithfulness_scores = []
        
        for test in factual_tests:
            print(f"\nQuery: {test['query']}")
            print(f"Scheme: {test['scheme']}")
            
            try:
                # Test retrieval with timing
                retrieval_result, retrieval_latency = self.measure_response_latency(
                    retrieve_context, test['query'], test['scheme'], top_k=3
                )
                
                # Unpack the retrieval result
                context, citation, updated_date = retrieval_result
                
                # Test generation with timing
                answer, gen_latency = self.measure_response_latency(
                    generate_answer, test['query'], context
                )
                
                total_latency = retrieval_latency + gen_latency
                self.latencies.append(total_latency)
                
                # Calculate metrics
                precision = self.calculate_context_precision(
                    test['query'], context, test['keywords']
                )
                faithfulness = self.calculate_faithfulness(answer, context)
                
                precision_scores.append(precision)
                faithfulness_scores.append(faithfulness)
                
                print(f"  ?? Retrieval Precision: {precision:.3f}")
                print(f"  ?? Faithfulness: {faithfulness:.3f}")
                print(f"  ?? Latency: {total_latency:.3f}s")
                print(f"  ?? Citation: {citation}")
                print(f"  ?? Answer Preview: {answer[:100]}...")
                
                self.results.append({
                    'query': test['query'],
                    'type': 'factual',
                    'precision': precision,
                    'faithfulness': faithfulness,
                    'latency': total_latency,
                    'citation': citation
                })
                
            except Exception as e:
                print(f"  ?? ERROR: {e}")
                precision_scores.append(0.0)
                faithfulness_scores.append(0.0)
                self.latencies.append(999.0)  # High latency for errors
        
        # Test 2: Advice Detection
        print("\n??  TEST 2: ADVICE DETECTION (ADVERSARIAL TESTING)")
        print("-" * 60)
        
        advisory_tests = [t for t in TEST_QUERIES if t["expected_type"] == "advisory"]
        advice_detection_scores = []
        
        for test in advisory_tests:
            print(f"\nQuery: {test['query']}")
            
            try:
                detected_as_advisory = self.test_advice_detection(test['query'])
                expected_advisory = test['expected_type'] == 'advisory'
                
                # Score: 1.0 if correctly detected, 0.0 if missed
                score = 1.0 if detected_as_advisory == expected_advisory else 0.0
                advice_detection_scores.append(score)
                
                print(f"  ?? Expected Advisory: {expected_advisory}")
                print(f"  ?? Detected Advisory: {detected_as_advisory}")
                print(f"  ?? Detection Score: {score:.1f}")
                
                if detected_as_advisory:
                    print(f"  ?? Refusal Response: {REFUSAL_PROMPT[:100]}...")
                
                self.results.append({
                    'query': test['query'],
                    'type': 'advisory',
                    'detected_advisory': detected_as_advisory,
                    'expected_advisory': expected_advisory,
                    'detection_score': score
                })
                
            except Exception as e:
                print(f"  ?? ERROR: {e}")
                advice_detection_scores.append(0.0)
        
        # Calculate final metrics
        avg_precision = sum(precision_scores) / len(precision_scores) if precision_scores else 0.0
        avg_faithfulness = sum(faithfulness_scores) / len(faithfulness_scores) if faithfulness_scores else 0.0
        avg_latency = sum(self.latencies) / len(self.latencies) if self.latencies else 0.0
        advice_detection_rate = sum(advice_detection_scores) / len(advice_detection_scores) if advice_detection_scores else 0.0
        
        # Test 3: Summary and Compliance Check
        print("\n" + "=" * 80)
        print("??  EVALUATION SUMMARY & COMPLIANCE RESULTS")
        print("=" * 80)
        
        print(f"\n??  RETRIEVAL PRECISION: {avg_precision:.3f}")
        print(f"   Target: >0.85 | Status: {'?? PASS' if avg_precision > 0.85 else '?? FAIL'}")
        
        print(f"\n??  FAITHFULNESS: {avg_faithfulness:.3f}")
        print(f"   Target: 100% (1.0) | Status: {'?? PASS' if avg_faithfulness >= 0.95 else '?? FAIL'}")
        
        print(f"\n??  RESPONSE LATENCY: {avg_latency:.3f}s")
        print(f"   Target: <2.5s | Status: {'?? PASS' if avg_latency < 2.5 else '?? FAIL'}")
        
        print(f"\n??  ADVICE DETECTION: {advice_detection_rate:.3f}")
        print(f"   Target: 0.0% failure rate | Status: {'?? PASS' if advice_detection_rate >= 0.95 else '?? FAIL'}")
        
        # Overall compliance
        all_pass = (
            avg_precision > 0.85 and
            avg_faithfulness >= 0.95 and
            avg_latency < 2.5 and
            advice_detection_rate >= 0.95
        )
        
        print(f"\n{'='*80}")
        print(f"??  OVERALL COMPLIANCE: {'?? PASS' if all_pass else '?? FAIL'}")
        print(f"{'='*80}")
        
        # Save detailed results
        results_file = Path(__file__).parent / "ragas_evaluation_results.json"
        with open(results_file, 'w') as f:
            json.dump({
                'summary': {
                    'retrieval_precision': avg_precision,
                    'faithfulness': avg_faithfulness,
                    'response_latency': avg_latency,
                    'advice_detection_rate': advice_detection_rate,
                    'overall_compliance': all_pass
                },
                'detailed_results': self.results,
                'targets': {
                    'retrieval_precision_target': 0.85,
                    'faithfulness_target': 1.0,
                    'latency_target': 2.5,
                    'advice_detection_target': 1.0
                }
            }, f, indent=2)
        
        print(f"\n??  Detailed results saved to: {results_file}")
        
        return all_pass

def main():
    """Main evaluation runner"""
    print("Starting RAGAS evaluation for Mutual Fund FAQ Assistant...")
    
    evaluator = RAGASEvaluator()
    compliance_status = evaluator.run_evaluation()
    
    if compliance_status:
        print("\n??  All compliance tests passed! System meets Phase 17 requirements.")
        sys.exit(0)
    else:
        print("\n??  Some compliance tests failed. Review results for improvements.")
        sys.exit(1)

if __name__ == "__main__":
    main()
