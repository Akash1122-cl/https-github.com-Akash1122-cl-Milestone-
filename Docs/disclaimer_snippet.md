# Disclaimer Snippet (UI)

## Primary Disclaimer Badge
```
?? No Investment Advice
```

## Complete Disclaimer Text
```
?? No Investment Advice

This assistant provides factual information only and does not constitute investment advice. 
All responses are for educational purposes only. Please consult with a SEBI-registered 
financial advisor before making any investment decisions.

Learn more: https://www.sebi.gov.in/sebiweb/Investor-Education/Investor-Education_Main.jsp
```

## Implementation in UI

### **Header Badge**
```javascript
<div className="disclaimer-badge">?? No Investment Advice</div>
```

### **Welcome Message Disclaimer**
```javascript
const getWelcomeMessage = (threadId) => ({
  role: "bot",
  content: `?? Welcome to the Mutual Fund FAQ Assistant! I provide verified, facts-only answers about mutual fund schemes. Ask me about NAV, expense ratios, exit loads, or minimum SIP amounts.\n\nSession ID: ${threadId.substring(0, 8)}...`,
  citation: null,
  last_updated: null,
  is_advisory: false,
});
```

### **Advisory Response Disclaimer**
```javascript
REFUSAL_PROMPT = `I cannot provide investment advice or recommendations. For investment decisions, please consult with a SEBI-registered financial advisor. Learn more about investment guidelines at https://www.sebi.gov.in/sebiweb/Investor-Education/Investor-Education_Main.jsp`;
```

## CSS Styling
```css
.disclaimer-badge {
  background: var(--warning-color);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}
```

## Compliance Features

### **1. Visual Indicators**
- **Warning Badge**: "?? No Investment Advice" in header
- **Color Coding**: Warning color (amber/orange) for disclaimer
- **Placement**: Prominent position in UI header

### **2. Text Disclaimers**
- **Welcome Message**: Facts-only clarification in initial message
- **Advisory Responses**: SEBI links in refusal messages
- **Educational Focus**: Emphasis on informational responses only

### **3. Regulatory Compliance**
- **SEBI References**: Links to official SEBI resources
- **No Predictions**: No future performance discussions
- **Educational Purpose**: Clear statement of educational intent

## User Experience

### **Visibility**
- Disclaimer appears in multiple locations
- Consistent messaging across interface
- Clear visual indicators for compliance

### **Accessibility**
- Text is readable and accessible
- Links are functional and relevant
- Language is clear and understandable

### **Enforcement**
- System automatically refuses advisory queries
- Responses include compliance messaging
- No investment advice provided under any circumstances

---

*This disclaimer snippet ensures complete compliance with SEBI regulations while maintaining user-friendly interface design.*
