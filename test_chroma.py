#!/usr/bin/env python3
"""
test_chroma.py - Test Chroma Cloud connectivity and data retrieval
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'apps/api'))

from core.retriever import chroma_client

def test_chroma_connectivity():
    """Test Chroma Cloud connectivity and data retrieval"""
    print("=" * 60)
    print("🔍 CHROMA CLOUD CONNECTIVITY TEST")
    print("=" * 60)
    
    try:
        # Test 1: Basic connectivity
        print("\n1. Testing basic connectivity...")
        collections = chroma_client.list_collections()
        print(f"✅ Connected successfully!")
        print(f"📊 Available collections: {len(collections)}")
        
        for col in collections:
            try:
                count = col.count()
                print(f"   - {col.name}: {count} documents")
            except Exception as e:
                print(f"   - {col.name}: Error getting count - {e}")
        
        # Test 2: Specific collection access
        print("\n2. Testing collection access...")
        
        nippon_col = chroma_client.get_collection('nippon_india')
        general_col = chroma_client.get_collection('general')
        
        nippon_count = nippon_col.count()
        general_count = general_col.count()
        
        print(f"✅ Nippon India collection: {nippon_count} documents")
        print(f"✅ General collection: {general_count} documents")
        
        # Test 3: Query functionality
        print("\n3. Testing query functionality...")
        
        test_queries = [
            "What is the expense ratio for HDFC Mid Cap Fund?",
            "What is the exit load for Quant Small Cap Fund?",
            "What is the current NAV of Nippon India Large Cap Fund?",
            "What is the minimum SIP for Nippon India Growth Fund?"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n   Query {i}: {query[:50]}...")
            
            try:
                # Test on nippon_india collection
                results = nippon_col.query(
                    query_texts=[query],
                    n_results=3
                )
                
                docs = results['documents'][0] if results['documents'] else []
                metas = results['metadatas'][0] if results['metadatas'] else []
                
                print(f"      Results: {len(docs)} documents found")
                
                if docs:
                    print(f"      Sample: {docs[0][:100]}...")
                    if metas:
                        print(f"      Source: {metas[0].get('source_url', 'N/A')}")
                else:
                    print("      ⚠️  No documents found")
                    
            except Exception as e:
                print(f"      ❌ Query error: {e}")
        
        # Test 4: Architecture scheme URLs
        print("\n4. Testing architecture-defined schemes...")
        
        scheme_urls = [
            "https://groww.in/mutual-funds/nippon-india-large-cap-fund-direct-growth",
            "https://groww.in/mutual-funds/nippon-india-taiwan-equity-fund-direct-growth", 
            "https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth"
        ]
        
        for url in scheme_urls:
            try:
                # Search for documents containing this URL in metadata
                results = nippon_col.query(
                    query_texts=[url.split('/')[-1]],  # Use fund name from URL
                    n_results=1
                )
                
                docs = results['documents'][0] if results['documents'] else []
                metas = results['metadatas'][0] if results['metadatas'] else []
                
                if docs:
                    print(f"   ✅ {url.split('/')[-1]}: Found {len(docs)} documents")
                    if metas:
                        print(f"      Source: {metas[0].get('source_url', 'N/A')}")
                else:
                    print(f"   ⚠️  {url.split('/')[-1]}: No documents found")
                    
            except Exception as e:
                print(f"   ❌ {url.split('/')[-1]}: Error - {e}")
        
        print("\n" + "=" * 60)
        print("🎯 CHROMA CLOUD TEST COMPLETE")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ CHROMA CLOUD CONNECTION FAILED: {e}")
        print("=" * 60)
        return False

if __name__ == "__main__":
    test_chroma_connectivity()
