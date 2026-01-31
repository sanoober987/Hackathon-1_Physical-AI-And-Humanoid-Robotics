import React, { useState, useRef, useEffect } from 'react';
import styles from './ChatWidget.module.css'; // Import the styles from the correct location

// Configuration for backend API endpoint
// Using a function to prevent SSG errors
const getBackendApiUrl = () => {
  if (typeof window !== 'undefined') {
    // Client-side: use the actual backend URL
    return window.BACKEND_API_URL || process?.env?.REACT_APP_BACKEND_URL || 'http://localhost:3001';
  }
  // Server-side: return a placeholder that will be replaced on client
  return 'http://localhost:3001';
};

const ChatWidget = ({ standalone = false, locale = 'en' }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [userId, setUserId] = useState(() => {
    // Generate userId client-side to avoid SSR mismatches
    if (typeof window !== 'undefined') {
      return `user_${Date.now()}`;
    }
    return `user_placeholder`;
  });

  // Set the userId after component mounts if it's a placeholder
  useEffect(() => {
    if (userId === 'user_placeholder' && typeof window !== 'undefined') {
      setUserId(`user_${Date.now()}`);
    }
  }, []); // Only run once after mount
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Get messages based on locale (always English now)
  const t = {
    welcome_message: "Hello! I'm your Physical AI & Humanoid Robotics Assistant. How can I help you today?",

    heading: "Physical AI Assistant",

    placeholder: "Ask about Physical AI & Robotics...",

    quick_questions: {
      embodied_intelligence: "Explain embodied intelligence",
      balance_question: "How do humanoid robots maintain balance?",
      sensorimotor_learning: "What is sensorimotor learning?"
    }
  };

  // Add initial welcome message
  useEffect(() => {
    if (messages.length === 0) {
      setMessages([
        {
          id: Date.now(),
          text: t.welcome_message,
          sender: 'bot',
          timestamp: new Date().toISOString()
        }
      ]);
    }
  }, [messages.length, t.welcome_message]);

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Get user ID from localStorage or generate new one
      let userId = null;
      if (typeof window !== 'undefined' && window.localStorage) {
        userId = localStorage.getItem('user_id');
        if (!userId) {
          userId = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
          localStorage.setItem('user_id', userId);
        }
      } else {
        // Fallback for SSR: generate a temporary ID
        userId = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      }

      // Determine language based on the current locale
      const currentLanguage = locale || 'en';

      // Call backend API for streaming with better error handling
      let response;
      try {
        // Add timeout for the fetch request
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout

        response = await fetch(`${getBackendApiUrl()}/api/v1/chat/stream`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            question: inputValue,
            user_id: userId,
            language: currentLanguage
          }),
          signal: controller.signal
        });

        clearTimeout(timeoutId);
      } catch (networkError) {
        console.error('Network error connecting to backend:', networkError);

        // Check if it's a timeout error
        if (networkError.name === 'AbortError') {
          throw new Error('Timeout: Request took too long to complete. Please try again.');
        }

        throw new Error('Network error: Unable to connect to the AI service. Please make sure the backend server is running on http://localhost:3001');
      }

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}. ${response.statusText}`);
      }

      // Create a new bot message with streaming text
      const botMessageId = Date.now() + 1;
      const initialBotMessage = {
        id: botMessageId,
        text: '',
        sender: 'bot',
        sources: [],
        timestamp: new Date().toISOString(),
        isStreaming: true
      };

      // Add the initial bot message with empty text
      setMessages(prev => [...prev, initialBotMessage]);

      // Check if response body is available
      if (!response.body) {
        throw new Error('Response body is empty. The server may not be returning valid data.');
      }

      // Read the stream and update the message in real-time
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      try {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, { stream: true });

          // Process the buffer looking for complete JSON objects
          let boundary;
          while ((boundary = buffer.indexOf('\n')) !== -1) {
            const line = buffer.substring(0, boundary);
            buffer = buffer.substring(boundary + 1);

            if (line.startsWith('data: ')) {
              const data = line.substring(6); // Remove 'data: ' prefix

              if (data === '[DONE]' || data.trim() === '') {
                break;
              }

              try {
                const parsed = JSON.parse(data);

                if (parsed.type === 'token') {
                  setMessages(prev => prev.map(msg =>
                    msg.id === botMessageId
                      ? { ...msg, text: msg.text + parsed.token }
                      : msg
                  ));
                } else if (parsed.type === 'sources') {
                  setMessages(prev => prev.map(msg =>
                    msg.id === botMessageId
                      ? { ...msg, sources: parsed.sources }
                      : msg
                  ));
                } else if (parsed.type === 'done') {
                  setMessages(prev => prev.map(msg =>
                    msg.id === botMessageId
                      ? { ...msg, isStreaming: false }
                      : msg
                  ));
                  break;
                } else if (parsed.type === 'error') {
                  setMessages(prev => prev.map(msg =>
                    msg.id === botMessageId
                      ? { ...msg, isStreaming: false, text: parsed.message }
                      : msg
                  ));
                  break;
                }
              } catch (e) {
                console.error('Error parsing stream data:', e, 'Data:', data);
                // Continue processing other data if one line fails
              }
            }
          }
        }
      } catch (streamError) {
        console.error('Stream processing error:', streamError);
        // If there's a stream error, mark the message as finished with error
        setMessages(prev => prev.map(msg =>
          msg.id === botMessageId
            ? {
                ...msg,
                isStreaming: false,
                text: msg.text + ` [Error: ${streamError.message}]`
              }
            : msg
        ));
      } finally {
        reader.releaseLock();
      }

    } catch (error) {
      console.error('Error sending message:', error);

      // Remove the streaming message and add error message
      setMessages(prev => prev.filter(msg => !msg.isStreaming));

      let errorMessageText = '';
      if (error.message.includes('Network error')) {
        errorMessageText = 'Network issue: Unable to connect to the AI server. Please ensure the backend server is running.';
      } else if (error.message.includes('Timeout')) {
        errorMessageText = 'Timeout: Request took too long to complete. Please try again.';
      } else if (error.message.includes('HTTP error')) {
        errorMessageText = 'Server issue: Error communicating with the AI service. Please try again later.';
      } else {
        errorMessageText = 'Sorry, I encountered an error connecting to the AI service. Please try again later.';
      }

      const errorMessage = {
        id: Date.now() + 1,
        text: errorMessageText,
        sender: 'bot',
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([
      {
        id: Date.now(),
        text: "Hello! I'm your Physical AI & Humanoid Robotics Assistant. How can I help you today?",
        sender: 'bot',
        timestamp: new Date().toISOString()
      }
    ]);
  };


  return (
    <div className={`${styles.chatContainer} ${standalone ? styles.standalone : ''}`}>
      {/* Chat Header */}
      <div className={styles.chatHeader}>
        <div className={styles.chatHeaderLeft}>
          <h3>🤖 {t.heading}</h3>
        </div>
        <div className={styles.chatHeaderRight}>
          <button
            onClick={clearChat}
            className={styles.headerButton}
            title="Clear chat"
          >
            ✕
          </button>
          {!standalone && (
            <button
              onClick={() => {}}
              className={styles.headerButton}
              title="Close"
            >
              ×
            </button>
          )}
        </div>
      </div>

      {/* Messages Area */}
      <div className={styles.messagesArea}>
        {messages.length === 0 ? (
          <div className={styles.emptyState}>
            <div className={styles.emptyStateIcon}>💬</div>
            <h4 className={styles.emptyStateTitle}>Welcome to AI Assistant</h4>
            <p className={styles.emptyStateDescription}>
              Ask questions about Physical AI, robotics, and humanoid systems
            </p>
            <div className={styles.quickActions}>
              <button
                className={styles.quickActionBtn}
                onClick={() => setInputValue(t.quick_questions.embodied_intelligence)}
              >
                {t.quick_questions.embodied_intelligence}
              </button>
              <button
                className={styles.quickActionBtn}
                onClick={() => setInputValue(t.quick_questions.balance_question)}
              >
                {t.quick_questions.balance_question}
              </button>
              <button
                className={styles.quickActionBtn}
                onClick={() => setInputValue(t.quick_questions.sensorimotor_learning)}
              >
                {t.quick_questions.sensorimotor_learning}
              </button>
            </div>
          </div>
        ) : (
          <>
            {messages.map((message) => (
              <div key={message.id} className={`${styles.message} ${styles[message.sender]}`}>
                <div className={styles.messageContent}>
                  {message.sender === 'bot' && message.isStreaming ? (
                    <div className={styles.streamingContent}>
                      <span>{message.text}</span>
                      <span className={styles.streamingCursor}>|</span>
                    </div>
                  ) : (
                    message.text
                  )}
                  <div className={styles.messageTimestamp}>
                    {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </div>
                </div>

                {message.sources && message.sources.length > 0 && (
                  <div className={styles.messageSources}>
                    <details>
                      <summary>📚 Sources</summary>
                      <ul>
                        {message.sources.map((source, index) => (
                          <li key={index}>
                            <strong>{source.title}</strong> - {source.section}
                          </li>
                        ))}
                      </ul>
                    </details>
                  </div>
                )}
              </div>
            ))}

            {isLoading && !messages.some(msg => msg.isStreaming) && (
              <div className={`${styles.message} ${styles.bot}`}>
                <div className={styles.messageContent}>
                  <div className={styles.typingIndicator}>
                    <span className={styles.typingDot}></span>
                    <span className={styles.typingDot}></span>
                    <span className={styles.typingDot}></span>
                  </div>
                </div>
              </div>
            )}
          </>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className={styles.inputArea}>
        <textarea
          ref={inputRef}
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder={t.placeholder}
          rows="1"
          className={styles.inputField}
          disabled={isLoading}
        />
        <button
          onClick={sendMessage}
          disabled={!inputValue.trim() || isLoading}
          className={styles.sendButton}
        >
          {isLoading && !messages.some(msg => msg.isStreaming) ? (
            <div className={styles.loadingSpinner}></div>
          ) : (
            '➤'
          )}
        </button>
      </div>
    </div>
  );
};

export default ChatWidget;