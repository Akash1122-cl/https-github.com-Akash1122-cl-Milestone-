"use client";

/**
 * SessionManager.js - Multi-session chat management component
 * Allows users to create, switch between, and delete isolated chat sessions
 */

export default function SessionManager({ 
  currentSession, 
  allSessions, 
  onNewSession, 
  onSwitchSession, 
  onDeleteSession 
}) {
  const sessionList = Object.entries(allSessions);
  
  return (
    <div className="session-manager">
      <div className="session-header">
        <h3>Chat Sessions</h3>
        <button 
          className="new-session-btn"
          onClick={onNewSession}
          title="Start new chat session"
        >
          + New Session
        </button>
      </div>
      
      <div className="session-list">
        {sessionList.map(([sessionId, sessionData]) => (
          <div 
            key={sessionId}
            className={`session-item ${sessionId === currentSession ? 'active' : ''}`}
          >
            <div 
              className="session-info"
              onClick={() => onSwitchSession(sessionId)}
            >
              <div className="session-name">
                Session {sessionId.substring(0, 8)}...
              </div>
              <div className="session-meta">
                {sessionData.messages?.length || 0} messages
                {sessionData.lastActive && (
                  <span className="session-time">
                    {new Date(sessionData.lastActive).toLocaleTimeString()}
                  </span>
                )}
              </div>
            </div>
            
            {sessionList.length > 1 && (
              <button 
                className="delete-session-btn"
                onClick={() => onDeleteSession(sessionId)}
                title="Delete session"
              >
                ×
              </button>
            )}
          </div>
        ))}
      </div>
      
      <div className="session-footer">
        <small>
          Total: {sessionList.length} session{sessionList.length !== 1 ? 's' : ''}
        </small>
      </div>
    </div>
  );
}
