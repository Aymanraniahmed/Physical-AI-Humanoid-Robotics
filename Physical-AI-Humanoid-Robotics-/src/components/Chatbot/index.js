import React, { useState, useEffect, useRef } from 'react';
import styles from './styles.module.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export default function Chatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [selectedText, setSelectedText] = useState('');
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Handle text selection
  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection();
      const text = selection.toString().trim();

      if (text && text.length > 10 && text.length < 5000) {
        setSelectedText(text);
        // Show notification that text is selected
        if (!isOpen) {
          setIsOpen(true);
        }
      }
    };

    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('touchend', handleSelection);

    return () => {
      document.removeEventListener('mouseup', handleSelection);
      document.removeEventListener('touchend', handleSelection);
    };
  }, [isOpen]);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = {
      role: 'user',
      content: input,
      selected_text: selectedText || null
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: sessionId,
          query: input,
          selected_text: selectedText || null
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to get response');
      }

      const data = await response.json();

      // Update session ID
      if (!sessionId) {
        setSessionId(data.session_id);
      }

      // Add assistant message
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: data.answer,
        sources: data.sources
      }]);

      // Clear selected text after using it
      setSelectedText('');

    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        error: true
      }]);
    } finally {
      setLoading(false);
    }
  };

  const clearChat = async () => {
    try {
      if (sessionId) {
        const response = await fetch(`${API_URL}/chat/clear/${sessionId}`, {
          method: 'POST'
        });
        const data = await response.json();
        setSessionId(data.new_session_id);
      }
      setMessages([]);
      setSelectedText('');
    } catch (error) {
      console.error('Error clearing chat:', error);
    }
  };

  return (
    <>
      {/* Floating Chat Button */}
      <button
        className={`${styles.chatButton} ${isOpen ? styles.chatButtonOpen : ''}`}
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Toggle chatbot"
      >
        {isOpen ? '✕' : (
          <>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
            </svg>
            {selectedText && (
              <span className={styles.badge}>1</span>
            )}
          </>
        )}
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div className={styles.chatWindow}>
          <div className={styles.chatHeader}>
            <div>
              <h3>📚 Book Assistant</h3>
              <p>Ask me anything about the book</p>
            </div>
            <button onClick={clearChat} className={styles.clearButton}>
              Clear
            </button>
          </div>

          {/* Selected Text Indicator */}
          {selectedText && (
            <div className={styles.selectedTextIndicator}>
              <span>📋 Text selected ({selectedText.length} chars)</span>
              <button onClick={() => setSelectedText('')}>✕</button>
            </div>
          )}

          {/* Messages */}
          <div className={styles.messagesContainer}>
            {messages.length === 0 && (
              <div className={styles.welcomeMessage}>
                <h4>👋 Welcome!</h4>
                <p>I can help you with:</p>
                <ul>
                  <li>Understanding concepts from the book</li>
                  <li>Finding specific information</li>
                  <li>Explaining code examples</li>
                  <li>Answering questions about selected text</li>
                </ul>
                <p className={styles.tip}>
                  <strong>Tip:</strong> Select any text from the book and ask me about it!
                </p>
              </div>
            )}

            {messages.map((msg, idx) => (
              <div key={idx} className={`${styles.message} ${styles[msg.role]}`}>
                {msg.role === 'assistant' && <div className={styles.avatar}>🤖</div>}
                <div className={styles.messageContent}>
                  <div className={styles.messageText}>
                    {msg.content}
                  </div>
                  {msg.sources && msg.sources.length > 0 && (
                    <div className={styles.sources}>
                      <strong>Sources:</strong>
                      {msg.sources.map((source, i) => (
                        <span key={i} className={styles.sourceTag}>
                          {source.chapter} / {source.section}
                        </span>
                      ))}
                    </div>
                  )}
                  {msg.selected_text && (
                    <div className={styles.selectedTextQuote}>
                      "{msg.selected_text.substring(0, 100)}..."
                    </div>
                  )}
                </div>
                {msg.role === 'user' && <div className={styles.avatar}>👤</div>}
              </div>
            ))}

            {loading && (
              <div className={`${styles.message} ${styles.assistant}`}>
                <div className={styles.avatar}>🤖</div>
                <div className={styles.messageContent}>
                  <div className={styles.typing}>
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Form */}
          <form onSubmit={sendMessage} className={styles.inputForm}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder={selectedText ? "Ask about selected text..." : "Ask a question..."}
              disabled={loading}
              className={styles.input}
            />
            <button type="submit" disabled={loading || !input.trim()} className={styles.sendButton}>
              <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
              </svg>
            </button>
          </form>
        </div>
      )}
    </>
  );
}
