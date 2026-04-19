# Raw Data Inventory: Mutual Fund Key Facts

This file documents the **6 key data fields** we extract and store for every mutual fund scheme, along with the two-stage storage format and complete data flow.

> [!NOTE]
> Data is stored in a single target JSON file (`data/raw/targeted_schemes.json`) after the Playwright scraper extracts live values from the 5 specific URLs.

---

## 1. What Data is Captured?

For the 5 targeted schemes, we extract exactly these 6 fields directly from the webpage:

| Field | What it Means | Example Value |
| :--- | :--- | :--- |
| **NAV** | Current Net Asset Value (price per unit) | ₹66.84 |
| **Minimum SIP** | Smallest monthly investment allowed | ₹100 |
| **Fund Size (AUM)** | Total money managed by the fund | ₹28,661.27 Cr |
| **Expense Ratio** | Annual fee charged by the fund manager | 0.72% |
| **Exit Load** | Penalty fee for withdrawing early | 1% within 12 months (above 10% units) |
| **Rating** | Groww's quality rating for the fund | 1 Star |

---

## 2. How is it Stored?

The system stores facts in a **consolidated JSON file**:

### Data Output (`data/raw/targeted_schemes.json`)

The ingest script processes the 5 specific URLs and directly writes their extracted factual variables to a single array format. Extraneous document discovery and PDFs have been completely removed.

```json
[
  {
    "scheme_name": "Nippon India Large Cap Fund Direct Growth",
    "source_url": "https://groww.in/mutual-funds/nippon-india-large-cap-fund-direct-growth",
    "last_updated": "2026-04-15",
    "nav":           "₹96.12",
    "min_sip":       "₹100",
    "fund_size_aum": "₹35,160.00 Cr",
    "expense_ratio": "0.75%",
    "exit_load":     "1% if redeemed within 1 month",
    "rating":        "4 Star"
  }
]
```

---

## 3. Complete Data Flow

```text
List of 5 Target Scheme URLs
   └──> Specific scheme page HTML natively
            ├──> Extract 6 Fields (NAV, SIP, AUM, Ratio, Load, Rating)
                       ↓
  Storage Output → data/raw/targeted_schemes.json
                       ↓
  Uploaded to → GitHub Artifact: "mutual-fund-data"
                       ↓
  Read by → scripts/index.py       (Chunking & Embedding phase)
                       ↓
  Stored in → Pinecone Vector DB   (1 vector per field per scheme)
```

---

## 4. Compliance Check

- **PII**: ❌ None stored — no PAN, Aadhaar, or account data.
- **Advisory Content**: ❌ None — only official factual fields.
- **Source Verification**: ✅ All values pulled directly from Groww's official AMC pages.
- **Freshness**: ✅ `last_updated` timestamp auto-populated on every daily run.
