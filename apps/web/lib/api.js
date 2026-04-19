/**
 * api.js — API connector for the Mutual Fund FAQ Assistant
 * Sends queries to the FastAPI backend and returns structured responses.
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

/**
 * Sends a user query to the FastAPI backend.
 * @param {string} query - The user's question.
 * @param {string|null} schemeName - Optional fund name filter.
 * @param {string} threadId - Unique conversation thread ID.
 * @returns {Promise<{answer: string, citation: string|null, last_updated: string|null, is_advisory: boolean}>}
 */
export async function sendMessage(query, schemeName = null, threadId = "default-thread") {
  const response = await fetch(`${API_BASE}/api/chat/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      thread_id: threadId,
      query,
      scheme_name: schemeName,
    }),
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.status} ${response.statusText}`);
  }

  return response.json();
}
