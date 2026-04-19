# Mutual Fund FAQ Assistant

## Overview
A facts-only mutual fund FAQ assistant powered by RAG (Retrieval Augmented Generation) architecture. Provides verified answers about mutual fund schemes with strict compliance to SEBI regulations.

## ? Working Prototype

**Live Demo**: http://localhost:3000

### **Features**
- **Multi-Session Chat**: Create and manage multiple conversation threads
- **Facts-Only Responses**: Source-backed answers with citations
- **Advisory Guardrails**: Automatic refusal of investment advice
- **Real-Time Metrics**: Live fund data and comparison tools
- **SEBI Compliant**: Educational responses with regulatory compliance

---

## ? Setup Instructions

### **Prerequisites**
- Node.js 18+ and npm
- Python 3.9+
- Playwright browsers
- Environment variables for API keys

### **1. Clone Repository**
```bash
git clone <repository-url>
cd Milestone-2
```

### **2. Backend Setup**
```bash
# Navigate to API directory
cd apps/api

# Install Python dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your API keys:
# CHROMA_API_KEY=your-chroma-cloud-api-key
# GOOGLE_API_KEY=your-gemini-api-key

# Start backend server
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

### **3. Frontend Setup**
```bash
# Navigate to web directory (new terminal)
cd apps/web

# Install Node.js dependencies
npm install

# Start frontend server
npm start
```

### **4. Data Extraction (Optional)**
```bash
# Extract latest fund metrics
python scripts/extract_key_metrics.py

# Run data ingestion pipeline
python scripts/ingest.py
```

---

## ? Scope

### **Asset Management Companies (AMCs)**
- **Nippon India Mutual Fund**
  - Large Cap Fund
  - Taiwan Equity Fund  
  - Growth Fund
- **HDFC Mutual Fund**
  - Mid-Cap Opportunities Fund
- **Quant Mutual Fund**
  - Small Cap Fund

### **Fund Categories Covered**
- **Large-Cap**: Blue-chip, stable investments
- **Mid-Cap**: Growth-focused medium-sized companies
- **Small-Cap**: High-growth small companies
- **Thematic**: Sector-specific (Taiwan equity)

### **Data Points Available**
- Expense Ratio
- Exit Load
- Minimum SIP Amount
- Lock-in Period (ELSS)
- Riskometer Classification
- Benchmark Index
- Statement Download Instructions

---

## ? Known Limits & Constraints

### **Data Limitations**
- **5 Funds Only**: Limited to specified target schemes
- **Static Data**: Updated daily via automated scraping
- **Source Dependency**: Relies on Groww.in data availability
- **No Historical Data**: Current information only

### **Functional Constraints**
- **No Investment Advice**: Strict facts-only responses
- **Limited Queries**: Only fund-specific factual questions
- **No Personalization**: No user-specific recommendations
- **English Only**: Single language support

### **Technical Constraints**
- **Local Deployment**: Requires local server setup
- **API Dependencies**: Requires Chroma Cloud and Gemini API keys
- **Browser Requirements**: Modern browser with JavaScript
- **No Mobile App**: Web-based interface only

### **Compliance Constraints**
- **SEBI Regulations**: Cannot provide investment advice
- **No Predictions**: No future performance predictions
- **Educational Only**: Informational responses only
- **Disclaimer Required**: All responses include compliance notices

---

## ? Sample Q&A

### **Sample Queries & Responses**

**Q1**: "What is the expense ratio for Nippon India Large Cap Fund?"
**A1**: "The expense ratio for Nippon India Large Cap Fund is 0.71%. This is a fee payable to a mutual fund house for managing your mutual fund investments, representing the percentage of assets deducted each year. [Source: https://groww.in/mutual-funds/nippon-india-large-cap-fund-direct-growth]"

**Q2**: "Should I invest in HDFC or Nippon?"
**A2**: "I cannot provide investment advice or recommendations. For investment decisions, please consult with a SEBI-registered financial advisor. Learn more about investment guidelines at [SEBI Investor Education](https://www.sebi.gov.in/sebiweb/Investor-Education/Investor-Education_Main.jsp)"

**Q3**: "What is the lock-in period for these funds?"
**A3**: "All target funds have a 3-year lock-in period as they are ELSS (Equity Linked Savings Scheme) funds eligible for tax benefits under Section 80C. [Source: Fund data extraction]"

**Q4**: "Which fund has the lowest expense ratio?"
**A4**: "Nippon India Large Cap Fund has the lowest expense ratio at 0.71%, followed by HDFC Mid-Cap Opportunities Fund at 0.77%. [Source: Expense ratio comparison data]"

**Q5**: "What is the risk level for Quant Small Cap Fund?"
**A5**: "Quant Small Cap Fund has a 'Low' riskometer classification according to the latest available data. [Source: https://groww.in/mutual-funds/quant-small-cap-fund-direct-plan-growth]"

---

## ? Disclaimer Snippet (UI)

```
?? No Investment Advice

This assistant provides factual information only and does not constitute investment advice. 
All responses are for educational purposes only. Please consult with a SEBI-registered 
financial advisor before making any investment decisions.

Learn more: https://www.sebi.gov.in/sebiweb/Investor-Education/Investor-Education_Main.jsp
```

---

## ? Architecture

### **Backend Stack**
- **FastAPI**: Python web framework
- **Chroma Cloud**: Vector database for semantic search
- **Google Gemini**: AI model for response generation
- **Playwright**: Web scraping for data extraction

### **Frontend Stack**
- **Next.js 16**: React framework
- **JavaScript**: Client-side logic
- **CSS**: Responsive styling
- **Session Storage**: Multi-session support

### **Data Pipeline**
1. **Daily Scraping**: Automated data extraction from Groww.in
2. **Processing**: Structured data extraction and validation
3. **Embedding**: Vector storage in Chroma Cloud
4. **Retrieval**: Hybrid search (Chroma + structured data)
5. **Generation**: AI-powered response synthesis

---

## ? API Documentation

**Swagger UI**: http://127.0.0.1:8000/docs

### **Key Endpoints**
- `POST /api/chat/query` - Chat interface
- `GET /api/metrics/funds` - All fund data
- `GET /api/metrics/summary` - Portfolio statistics
- `GET /api/metrics/expense-ratio-comparison` - Cost analysis

---

## ? Testing

### **Test Questions**
1. "What is the expense ratio for Nippon India Large Cap Fund?"
2. "Should I invest in HDFC or Nippon?"
3. "What is the riskometer rating for Quant Small Cap Fund?"
4. "What is the benchmark for Nippon India Taiwan Equity Fund?"
5. "What is the lock-in period for these funds?"

### **Multi-Session Testing**
1. Create multiple chat sessions
2. Verify conversation isolation
3. Test session persistence
4. Check data consistency

---

## ? Troubleshooting

### **Common Issues**
- **Backend Not Starting**: Check Python dependencies and API keys
- **Frontend Not Loading**: Verify Node.js version and npm installation
- **Data Not Available**: Run data extraction scripts
- **API Errors**: Check environment variables and network connectivity

### **Performance**
- **Response Time**: <3 seconds for most queries
- **Memory Usage**: Moderate (vector database operations)
- **Network**: Requires internet for API calls

---

## ? License & Compliance

- **Educational Use Only**: Not for commercial investment advice
- **SEBI Compliant**: Follows regulatory guidelines
- **Open Source**: MIT License for code
- **Data Sources**: Publicly available fund information

---

## ? Support

For technical issues or questions:
1. Check the troubleshooting section
2. Verify API keys and environment setup
3. Review the documentation
4. Test with provided sample questions

---

*Last Updated: April 19, 2026*
