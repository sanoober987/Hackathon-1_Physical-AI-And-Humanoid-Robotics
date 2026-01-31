import React, { createContext, useContext, useState } from 'react';
import ChatWidget from '../ChatWidget'; // Import from parent directory where the main ChatWidget.jsx is located

const ChatContext = createContext();

export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
};

export const ChatProvider = ({ children }) => {
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [selectedText, setSelectedText] = useState('');

  const value = {
    isChatOpen,
    setIsChatOpen,
    selectedText,
    setSelectedText,
  };

  return (
    <ChatContext.Provider value={value}>
      {children}
      <ChatWidget />
    </ChatContext.Provider>
  );
};