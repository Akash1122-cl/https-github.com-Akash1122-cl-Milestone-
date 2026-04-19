# Problem Statement for Testing: Mutual Fund FAQ Assistant

## Goal
Build a **Facts-Only FAQ Assistant** for mutual fund schemes using a Retrieval-Augmented Generation (RAG) approach. The system prioritizes accuracy, transparency, and compliance, strictly avoiding any form of investment advice.

## Core pillars

### 1. Factual Rigor & Compliance
*   **Strictly Factual**: The system must only answer objective queries (e.g., expense ratios, exit loads, minimum SIPs) and **strictly refuse** any investment advice or opinions.
*   **Official Sources Only**: Information must be retrieved exclusively from official AMC, AMFI, or SEBI URLs. Third-party or aggregator sites are forbidden.
*   **Response Constraints**: Every answer must be concise (max 3 sentences), include exactly one source citation, and a "Last updated" footer.

### 2. Guardrails & Refusals
*   **Advisory Shield**: If a user asks "Should I invest?" or "Which fund is better?", the assistant must politely decline, reinforce its factual nature, and point to educational resources.
*   **Privacy First**: The system must never collect or process PII or sensitive financial data (PAN, account numbers, etc.).

### 3. Technical Requirements
*   **RAG Architecture**: A retrieval-based system using official documents as its knowledge base.
*   **Thread Support**: Capability to handle multiple independent chat threads.
*   **Minimal UI**: A clean interface featuring a clear disclaimer ("Facts-only. No investment advice") and example questions.

### 4. Implementation Details
*   **Corpus**: 1 AMC, 3-5 schemes, 15-25 official URLs (factsheets, KIM, SID).
*   **UI Elements**: Welcome message, 3 example questions, visible disclaimer.
*   **Backend**: API supporting RAG and thread management.
