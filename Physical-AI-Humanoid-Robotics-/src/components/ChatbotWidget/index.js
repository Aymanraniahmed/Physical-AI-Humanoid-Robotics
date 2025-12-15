import React, { useState } from 'react';
import styles from './styles.module.css';

const API_URL = 'http://localhost:8000';

export default function ChatbotWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([
    { role: 'bot', content: 'Hi! Ask me anything about Physical AI & Humanoid Robotics! 🤖' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const toggleWidget = () => setIsOpen(!isOpen);

  const addMessage = (content, role) => {
    setMessages(prev => [...prev, { role, content }]);
  };

  // Send chat message (no book_id needed - backend uses default book)
  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = input;
    addMessage(userMessage, 'user');
    setInput('');
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/chat/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: userMessage,
          session_id: sessionId
        })
      });

      const data = await response.json();
      if (response.ok) {
        setSessionId(data.session_id);
        addMessage(data.response, 'bot');

        // Show sources if available
        if (data.sources && data.sources.length > 0) {
          const sourcesText = `\n\nSources (${data.sources.length} chunks, avg score: ${(data.sources.reduce((sum, s) => sum + s.score, 0) / data.sources.length).toFixed(2)})`;
          addMessage(sourcesText, 'system');
        }
      } else {
        addMessage(`Error: ${data.detail || 'Failed to get response'}`, 'bot');
      }
    } catch (error) {
      addMessage(`Error: ${error.message}`, 'bot');
    }
    setLoading(false);
  };

  return (
    <>
      {/* Floating Button */}
      <button
        className={`${styles.chatButton} ${isOpen ? styles.active : ''}`}
        onClick={toggleWidget}
        aria-label="Toggle chatbot"
      >
        {isOpen ? '✕' : '💬'}
      </button>

      {/* Chat Widget */}
      {isOpen && (
        <div className={styles.chatWidget}>
          {/* Header */}
          <div className={styles.header}>
            <div className={styles.headerContent}>
              <div className={styles.avatar}>🤖</div>
              <div>
                <h3>Physical AI Assistant</h3>
                <p className={styles.status}>● Online</p>
              </div>
            </div>
            <button onClick={toggleWidget} className={styles.closeBtn}>−</button>
          </div>

          {/* Chat Section */}
          <div className={styles.messages}>
            {messages.map((msg, i) => (
              <div
                key={i}
                className={`${styles.message} ${
                  msg.role === 'user' ? styles.userMessage :
                  msg.role === 'system' ? styles.systemMessage :
                  styles.botMessage
                }`}
              >
                {msg.content}
              </div>
            ))}
            {loading && <div className={styles.loader}>Thinking...</div>}
          </div>

          {/* Input Section */}
          <div className={styles.inputContainer}>
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && !loading && sendMessage()}
              placeholder="Ask about Physical AI, ROS 2, Isaac Sim..."
              className={styles.input}
              disabled={loading}
            />
            <button
              onClick={sendMessage}
              className={styles.sendBtn}
              disabled={loading || !input.trim()}
            >
              ➤
            </button>
          </div>

          {/* Footer */}
          <div className={styles.footer}>
            <small>Powered by Local Embeddings & Gemini</small>
          </div>
        </div>
      )}
    </>
  );
}
