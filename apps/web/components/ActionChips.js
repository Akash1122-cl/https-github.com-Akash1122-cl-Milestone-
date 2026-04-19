"use client";

/**
 * ActionChips.js — Quick-start prompt launchers for the chat UI.
 * Clicking a chip pre-fills and submits a factual question.
 */

const EXAMPLE_QUESTIONS = [
  "What is the expense ratio for HDFC Mid Cap Fund?",
  "What is the exit load for Quant Small Cap Fund?",
  "What is the current NAV of Nippon India Large Cap Fund?",
  "What is the minimum SIP for Nippon India Growth Fund?",
];

export default function ActionChips({ onChipClick, disabled }) {
  return (
    <div className="chips-container">
      <p className="chips-label">✨ Try asking:</p>
      <div className="chips-grid">
        {EXAMPLE_QUESTIONS.map((q, i) => (
          <button
            key={i}
            className="chip"
            onClick={() => onChipClick(q)}
            disabled={disabled}
          >
            {q}
          </button>
        ))}
      </div>
    </div>
  );
}
