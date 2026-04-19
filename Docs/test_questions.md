# 10 Test Questions for Mutual Fund FAQ Assistant

## Overview
These 10 questions are designed to comprehensively test all aspects of the Mutual Fund FAQ Assistant system, including chat functionality, metrics integration, multi-session support, and compliance features.

---

## ? Test Questions

### **1. Basic Factual Query**
**Question**: "What is the expense ratio for Nippon India Large Cap Fund?"

**Expected Response**: 
- Should return "0.71%" with source citation
- Response should include last updated date
- Should be facts-only, no investment advice
- Response time: <3 seconds

**Testing**: Chat API + Structured Data Integration

---

### **2. Advisory Query Guardrail**
**Question**: "Should I invest in HDFC or Nippon?"

**Expected Response**:
- Should refuse with advisory refusal message
- Should include SEBI educational link
- Should be marked as `is_advisory: true`
- Response should be polite but firm

**Testing**: Compliance Guardrail System

---

### **3. Multi-Session Isolation**
**Steps**:
1. Create Session A, ask: "What is the exit load for Quant Small Cap Fund?"
2. Create Session B, ask: "What is the lock-in period for Nippon India Growth Fund?"
3. Switch back to Session A, check if conversation history is preserved

**Expected Results**:
- Each session maintains independent conversation history
- No cross-session data contamination
- Session switching works correctly

**Testing**: Multi-Session Architecture

---

### **4. Metrics Dashboard Overview**
**Steps**:
1. Switch to Metrics view
2. Check Overview tab for portfolio statistics
3. Verify all 5 funds are displayed
4. Check summary cards for total funds, average expense ratio

**Expected Results**:
- Portfolio shows 5 total funds
- Average expense ratio ~0.81%
- Risk distribution shows "Low: 5"
- All funds displayed with correct metrics

**Testing**: Frontend Metrics Integration

---

### **5. Expense Ratio Comparison**
**Steps**:
1. Go to Metrics view
2. Click on Comparison tab
3. Verify funds are sorted by expense ratio (lowest first)
4. Check top performer is Nippon India Large Cap Fund (0.71%)

**Expected Results**:
- Funds sorted: 0.71% (Nippon Large Cap) to 0.98% (Nippon Taiwan)
- Top performer highlighted
- Comparison insights displayed correctly

**Testing**: Data Analysis Features

---

### **6. Complex Query with Context**
**Question**: "Tell me about the risk level and benchmark for HDFC Mid-Cap Opportunities Fund"

**Expected Response**:
- Should return risk level: "Low"
- Should return benchmark: "NIFTY 50"
- Should include source citation
- Response should be concise and factual

**Testing**: Enhanced Retrieval System

---

### **7. Error Handling Test**
**Question**: "What is the expense ratio for NonExistent Fund XYZ?"

**Expected Response**:
- Should handle gracefully without system error
- Should indicate fund not found
- Should suggest available funds
- Should not crash or timeout

**Testing**: Error Handling Resilience

---

### **8. Session Persistence Test**
**Steps**:
1. Create a session and ask a question
2. Refresh the browser page
3. Verify session and conversation history are preserved
4. Test session switching after refresh

**Expected Results**:
- Session data persists across browser refresh
- Conversation history maintained
- Session switching continues to work

**Testing**: Session Storage Implementation

---

### **9. API Integration Test**
**Steps**:
1. Test multiple rapid questions in succession
2. Verify backend API responds correctly each time
3. Check for any rate limiting or timeout issues
4. Monitor response times

**Expected Results**:
- All queries processed successfully
- Response times <3 seconds
- No API failures or timeouts
- Consistent performance

**Testing**: Backend API Performance

---

### **10. Mobile Responsiveness Test**
**Steps**:
1. Access the application on mobile device or use browser dev tools
2. Test chat interface on mobile screen
3. Test metrics dashboard on mobile
4. Verify all features work correctly on small screens

**Expected Results**:
- Interface adapts to mobile screen size
- All buttons and controls are accessible
- Text is readable without horizontal scrolling
- Session management works on mobile

**Testing**: Responsive Design Implementation

---

## ? Testing Checklist

For each question, verify:

### **Functionality** ? PASS/FAIL
- [ ] Response is accurate and factual
- [ ] Response includes source citation
- [ ] Response time is acceptable (<3s)
- [ ] No system errors or crashes

### **Compliance** ? PASS/FAIL
- [ ] Facts-only responses for factual queries
- [ ] Proper refusal for advisory queries
- [ ] No investment advice or recommendations
- [ ] SEBI compliance maintained

### **User Experience** ? PASS/FAIL
- [ ] Interface is responsive and intuitive
- [ ] Session management works correctly
- [ ] Error handling is user-friendly
- [ ] Mobile compatibility maintained

### **Technical** ? PASS/FAIL
- [ ] Backend API responds correctly
- [ ] Frontend renders without errors
- [ ] Data integration works seamlessly
- [ ] Performance is acceptable

---

## ? Success Criteria

**Overall System Health**: All 10 questions should pass with:
- **90%+ Success Rate** for factual queries
- **100% Compliance Rate** for advisory refusal
- **<3s Response Time** for all queries
- **Zero System Crashes** across all tests
- **Complete Session Isolation** verified

---

## ? Test Execution Guide

1. **Sequential Testing**: Execute questions 1-10 in order
2. **Document Results**: Record pass/fail for each test
3. **Performance Monitoring**: Note response times
4. **Error Logging**: Document any issues encountered
5. **Mobile Testing**: Use browser dev tools for mobile simulation

---

*These comprehensive test questions ensure all system components are working correctly and the Mutual Fund FAQ Assistant meets all specified requirements.*
