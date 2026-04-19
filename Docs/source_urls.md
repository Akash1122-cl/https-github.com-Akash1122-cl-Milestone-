# Source URLs List

## Overview
This document contains all URLs used in the Mutual Fund FAQ Assistant system, including data sources, API endpoints, and reference materials.

---

## ? Primary Data Sources (15-25 URLs)

### **Target Scheme URLs (5 URLs)**
These are the primary data sources for fund information extraction:

| # | URL | AMC | Fund Name | Category |
|---|-----|-----|-----------|----------|
| 1 | https://groww.in/mutual-funds/nippon-india-large-cap-fund-direct-growth | Nippon India | Large Cap Fund | Large-Cap |
| 2 | https://groww.in/mutual-funds/nippon-india-taiwan-equity-fund-direct-growth | Nippon India | Taiwan Equity Fund | Thematic |
| 3 | https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth | HDFC | Mid-Cap Opportunities Fund | Mid-Cap |
| 4 | https://groww.in/mutual-funds/quant-small-cap-fund-direct-plan-growth | Quant | Small Cap Fund | Small-Cap |
| 5 | https://groww.in/mutual-funds/nippon-india-growth-mid-cap-fund-direct-growth | Nippon India | Growth Fund | Mid-Cap |

### **SEBI Reference URLs (3 URLs)**
These URLs are used for compliance and educational purposes:

| # | URL | Purpose |
|---|-----|---------|
| 6 | https://www.sebi.gov.in/sebiweb/ | SEBI Official Website |
| 7 | https://www.sebi.gov.in/sebiweb/Investor-Education/Investor-Education_Main.jsp | SEBI Investor Education |
| 8 | https://www.sebi.gov.in/sebiweb/home/Action-against-illegal-accumulation-schemes.html | SEBI Action Against Illegal Schemes |

### **API Documentation URLs (2 URLs)**
| # | URL | Purpose |
|---|-----|---------|
| 9 | https://fastapi.tiangolo.com/ | FastAPI Documentation |
| 10 | https://docs.trychroma.com/ | ChromaDB Documentation |

### **Technology Reference URLs (5 URLs)**
| # | URL | Purpose |
|---|-----|---------|
| 11 | https://nextjs.org/docs | Next.js Documentation |
| 12 | https://playwright.dev/docs/intro | Playwright Documentation |
| 13 | https://github.com/features/actions | GitHub Actions Documentation |
| 14 | https://ai.google.dev/docs | Google Gemini API Documentation |
| 15 | https://huggingface.co/docs | Hugging Face Documentation |

---

## ? System URLs

### **Application Endpoints (4 URLs)**
| # | URL | Purpose |
|---|-----|---------|
| 16 | http://localhost:3000 | Frontend Application |
| 17 | http://127.0.0.1:8000 | Backend API Server |
| 18 | http://127.0.0.1:8000/health | Health Check Endpoint |
| 19 | http://127.0.0.1:8000/docs | API Documentation (Swagger) |

### **API Endpoints (10 URLs)**
| # | URL | Purpose |
|---|-----|---------|
| 20 | http://127.0.0.1:8000/api/chat/query | Chat Query Endpoint |
| 21 | http://127.0.0.1:8000/api/metrics/funds | All Funds Data |
| 22 | http://127.0.0.1:8000/api/metrics/summary | Portfolio Summary |
| 23 | http://127.0.0.1:8000/api/metrics/expense-ratio-comparison | Expense Ratio Comparison |
| 24 | http://127.0.0.1:8000/api/metrics/funds/category/{category} | Category Filter |
| 25 | http://127.0.0.1:8000/api/metrics/funds/risk/{risk} | Risk Level Filter |
| 26 | http://127.0.0.1:8000/api/metrics/funds/lock-in | Lock-in Period Filter |
| 27 | http://127.0.0.1:8000/api/metrics/search?q={query} | Fund Search |
| 28 | http://127.0.0.1:8000/api/metrics/validate/{fund} | Data Validation |
| 29 | http://127.0.0.1:8000/api/metrics/categories | Available Categories |

---

## ? Data Extraction URLs

### **Chroma Cloud Collections (2 URLs)**
| # | URL | Purpose |
|---|-----|---------|
| 30 | https://api.trychroma.com/v1/collections/nippon_india | Nippon India Collection |
| 31 | https://api.trychroma.com/v1/collections/general | General Collection |

---

## ? Summary Statistics

- **Total URLs Listed**: 31
- **Primary Data Sources**: 5 (Target Scheme URLs)
- **SEBI References**: 3
- **API Endpoints**: 14
- **Documentation**: 5
- **System URLs**: 4

---

## ? URL Categories

### **Data Sources (5 URLs)**
- All from Groww.in platform
- Focus on specific mutual fund schemes
- Real-time fund information

### **Compliance (3 URLs)**
- SEBI official website
- Investor education resources
- Regulatory compliance materials

### **Technology Stack (5 URLs)**
- Framework documentation
- API references
- Development tools

### **Application Infrastructure (18 URLs)**
- Frontend and backend servers
- API endpoints for data access
- Documentation and testing

---

## ? Data Freshness

- **Last Updated**: April 19, 2026
- **Extraction Method**: Automated Playwright scraping
- **Update Frequency**: Daily via GitHub Actions
- **Data Validation**: Structured JSON format

---

## ? Notes

1. **Primary Focus**: The 5 target scheme URLs are the core data sources
2. **Compliance**: SEBI URLs ensure regulatory compliance
3. **Technology**: Documentation URLs support development and maintenance
4. **API**: System URLs provide access to all application features
5. **Automation**: GitHub Actions scheduled for daily data updates

---

*This source list provides complete transparency about all URLs used in the Mutual Fund FAQ Assistant system.*
