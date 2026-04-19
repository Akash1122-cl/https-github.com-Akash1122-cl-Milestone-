"use client";

/**
 * MessageBubble.js — Renders a single chat message.
 * Handles user messages, factual bot responses, and refusal messages.
 */
export default function MessageBubble({ message }) {
  const isUser = message.role === "user";
  const isAdvisory = message.is_advisory;

  return (
    <div className={`message-row ${isUser ? "user-row" : "bot-row"}`}>
      {/* Avatar */}
      <div className={`avatar ${isUser ? "user-avatar" : "bot-avatar"}`}>
        {isUser ? "You" : "AI"}
      </div>

      {/* Bubble */}
      <div className={`bubble ${isUser ? "user-bubble" : isAdvisory ? "advisory-bubble" : "bot-bubble"}`}>
        {/* Main text */}
        <p className="bubble-text">{message.content}</p>

        {/* Source citation — shown only for factual bot answers */}
        {!isUser && message.citation && (
          <div className="citation-block">
            <span className="citation-label">📎 Source:</span>
            <a
              href={message.citation}
              target="_blank"
              rel="noopener noreferrer"
              className="citation-link"
            >
              {message.citation}
            </a>
          </div>
        )}

        {/* Last Updated timestamp */}
        {!isUser && message.last_updated && (
          <p className="last-updated">🕐 Last scraped: {message.last_updated}</p>
        )}

        {/* SEBI link for advisory refusals */}
        {isAdvisory && (
          <a
            href="https://investor.sebi.gov.in"
            target="_blank"
            rel="noopener noreferrer"
            className="sebi-link"
          >
            📘 Learn more at SEBI Investor Education Portal
          </a>
        )}
      </div>
    </div>
  );
}
