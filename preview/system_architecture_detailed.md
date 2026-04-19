# System Architecture: The Mutual Fund FAQ Assistant (Detailed Analysis)

## 1. Executive Summary: The "Facts-Only" Mission

The **Mutual Fund FAQ Assistant** is a production-grade, Retrieval-Augmented Generation (RAG) platform designed to bridge the gap between complex financial data and user accessibility. 

Unlike general-purpose conversational AI, this system is built on a foundational principle of **Strict Compliance**. By utilizing official scraped metrics and a dual-layer guardrail engine, the assistant provides high-fidelity, citation-grounded answers while explicitly refusing to provide investment advice or subjective opinions.

---

## 2. Phase 1: High-Fidelity Data Ingestion

The journey of a fact begins with our **Ingestion Pipeline** (implemented in Phase 12 and 14). To ensure 100% data reliability, the system does not rely on broad web searches. Instead, it employs a targeted extraction strategy:

### The Targeted Scraping Strategy
- **Precision Extraction**: Using **Playwright**, the system navigates directly to 5 pre-validated official Groww AMC scheme pages (e.g., Nippon India Large Cap, HDFC Mid-Cap).
- **Core Factual Fields**: The scraper targets exactly 6 critical attributes:
    1. **Current NAV**: Real-time pricing.
    2. **Minimum SIP**: Entry barriers.
    3. **AUM (Fund Size)**: Market reach.
    4. **Expense Ratio**: Operational costs.
    5. **Exit Load**: Liquidity restrictions.
    6. **Rating**: Performance context.
- **The "No PDF" Rule**: To prevent "hallucination-by-misinterpretation" from complex statutory PDFs, only the clean, structured HTML data from officialAMC sources is ingested.

---

## 3. Phase 2: The Vector Intelligence Layer (Cloud)

Data is only useful if it can be found instantly. Our **Indexing Engine** (Phase 13) converts raw text into mathematical intelligence:

### Local Embedding & Cloud Storage
- **Local Processing**: Queries and facts are vectorized using the **BAAI/bge-small-en-v1.5** model locally. This ensures that the most computationally expensive part of the retrieval process remains fast and private.
- **Chroma Cloud Integration**: Vectors are synchronized to a remote **Chroma Cloud** tenant. This cloud-native approach ensures that the backend API can be deployed globally without maintaining complex local database state.
- **AMC Collection Isolation**: Data is stored in specialized collections (e.g., `nippon_india`, `general`) to avoid cross-fund confusion during retrieval.

---

## 4. Phase 3: The Intelligent Gateway (Backend API)

The **Backend Integration** (Phase 15) serves as the system's "Pre-Frontal Cortex," managing user queries with safety at the forefront:

### Step 1: The Refusal Guardrail (Safety Engine)
Before any AI logic is invoked, the **Intent Classifier** scans for advisory keywords (e.g., "should I invest?", "which is better?"). If detected, the system immediately triggers the **Refusal Disclaimer**, providing educational links to SEBI instead of risky financial speculation.

### Step 2: Retrieval-Augmented Synthesis
If the query is factual (e.g., "What is the exit load?"), the system:
1. Performs a **Semantic Search** on Chroma Cloud to find the exact chunks of relevant facts.
2. Identifies the **Source URL** and **Last Updated** timestamp.
3. Packages this context for the Generator.

### Step 3: Minimalist Generation (Gemini 2.5)
We utilize the **Google Gemini 2.5 Flash Lite** model to synthesize the final answer. The AI is constrained by a "Zero Temperature" setting and a strict prompt: *Answer only with the facts provided. Cited sources are mandatory.*

---

## 5. Phase 4: The Automated Lifecycle (DevOps)

Financial data is perishable. To prevent stale information, the entire project is governed by a **GitHub Actions Scheduler** (Phase 6):

- **The 9:15 AM Pulse**: Every morning at 9:15 AM IST (to align with the start of the Indian market day), the GitHub runner awakens.
- **Full Refresh**: It executes the scraper, vectorizes the new NAVs/metrics, and pushes the updated intelligence to Chroma Cloud.
- **Audit Compliance**: All logs and metadata are synchronized, ensuring that every answer provided throughout the day is backed by the most recent official scrape.

---

## 6. Step-by-Step Phase Execution Details

To provide full transparency, the system's core capabilities were implemented across the following structured phases:

### Phase 12: Automated Ingestion
*   **Action**: Deployment of the **Ingestion Service** (`scripts/ingest.py`). 
*   **Execution**: Automated Playwright scripts navigate to official AMC URLs and perform "Precision Scraping" to extract 6 clean factual fields without any noise.

### Phase 13: Chunking & Embedding 
*   **Action**: Implementation of the **Data Processing Pipeline** (`scripts/index.py`).
*   **Chunking**: Raw JSON data is normalized into scheme-specific document objects.
*   **Embedding**: High-density vectorization using the **BGE-small** model (384 dimensions) to map semantic meaning.
*   **Sync**: Automatic push of these vectors to **Chroma Cloud** for global accessibility.

### Phase 14: Data Integrity Validation
*   **Action**: Development of the **JSON Schema Guardian**.
*   **Execution**: Multi-point validation of the `targeted_schemes.json` file to ensure 100% field coverage and zero data corruption before the vectorizing process begins.

### Phase 15: The Complete Retrieval & Generation Layer
*   **Action**: Backend deployment of the **Retrieval-Augmented Logic** via FastAPI (`apps/api/main.py`, `core/retriever.py`, `core/generator.py`).
*   **1. The Safety Refusal Engine**: 
    * Before a query is processed, it is intercepted by a strict heuristic filter (`is_advisory_query`). 
    * If investment advice requests are detected (e.g., "should I invest?", "which is the best fund?"), the system immediately kills the retrieval process and replies with a pre-configured SEBI compliance warning.
*   **2. Detailed Retrieval Execution**: 
    * A safe factual query undergoes local vectorization (BAAI/bge-small-en-v1.5) to translate the user’s wording into mathematical intent.
    * The system establishes a secure `CloudClient` handshake with the remote **Chroma Cloud** tenant.
    * A semantic proximity search is executed, leveraging metadata filtering to isolate the target mutual fund scheme (eliminating cross-fund contamination).
    * The top 3 closest factual chunks are extracted from the cloud, complete with their official "Groww URL" citations and "Last Updated" timestamps.
*   **3. Zero-Hallucination Generation**: 
    * The retrieved raw facts and the user's question are packaged into a strict Context-Bound Prompt.
    * This package is passed to **Google Gemini 2.5 Flash Lite** with temperature set to `0.0`.
    * Gemini is strictly instructed to answer using *only* the retrieved chunk, limited to a maximum of 3 sentences. If the context is missing, Gemini will default to "I cannot find official info for this," ensuring absolute factual integrity.

---

## 7. Future Horizons: Phase 16 & Beyond

As we move toward the **Frontend Deployment**, the system is architected for seamless expansion. The Next.js UI will leverage this robust, cloud-native API to present a sleek, emerald-themed dashboard that converts this complex RAG logic into a simple, trusted chat experience.
