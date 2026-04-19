# Product Preview: Mutual Fund FAQ Assistant (Focused Scope)

This document provides a text-based mockup of the user interface for the updated "Facts-Only" assistant. It demonstrates how the system interacts with users based on the 5 targeted fund schemes.

---

## 1. The Home Screen (Initial View)

The interface is minimalist, ensuring the focus remains on factual lookup and compliance.

### [Header: Compliance Banner]
> ℹ️ **Note**: This is a facts-only assistant. We do not provide investment advice.
> *This persistent banner ensures users understand the system's limitations.*

---

### [Welcome Message]
**Assistant:**
"Hello! I am your Mutual Fund FAQ Assistant. I can provide the latest factual details for:
- Nippon India Large Cap Fund
- Nippon India Taiwan Equity Fund
- HDFC Mid-Cap Opportunities Fund
- Quant Small Cap Fund
- Nippon India Growth Fund

How can I help you today?"

---

### [Quick-Start Question Chips]
Instead of typing, users can interact using one of these common queries:
- 📊 **"What is the current NAV of Nippon India Large Cap Fund?"**
- 💰 **"What is the minimum SIP for Quant Small Cap Fund?"**
- 📉 **"What is the exit load for HDFC Mid-Cap Opportunities?"**

---

## 2. A Factual Interaction Example

**User:** "What is the Expense Ratio for Nippon India Taiwan Equity Fund?"

**Assistant:**
"The Expense Ratio for the **Nippon India Taiwan Equity Fund (Direct Growth)** is **0.75%**.

**Source**: [Groww - Scheme Details](https://groww.in/mutual-funds/nippon-india-taiwan-equity-fund-direct-growth)
**Last Scraped**: 2026-04-15 09:15 AM IST"

---

## 3. The "Refusal" Flow (Advisory Protection)

The system automatically detects and refuses to answer questions requiring subjective judgment or advice.

**User:** "Is the Quant Small Cap Fund better than the HDFC one for long term?"

**Assistant:**
"I am a facts-only assistant and cannot provide comparisons, investment opinions, or advice on which fund is 'better.' For personalized financial planning, please consult a SEBI-registered investment advisor.

You can find official rules and investor education resources on the [SEBI Investor Website](https://investor.sebi.gov.in)."

---

## 4. UI Design Principles
- **Clarity**: All answers lead with the primary fact in bold.
- **Direct Sourcing**: Every response includes a direct link to the source URL.
- **Timeliness**: Every response shows exactly when the data was last fetched (9:15 AM schedule).
- **Accessibility**: Optimized for quick reading with clear bullet points.
