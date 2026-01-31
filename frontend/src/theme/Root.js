// Docusaurus Root wrapper for internationalization
import React from 'react';
import { IntlProvider } from 'react-intl';
import ErrorBoundary from '../components/ErrorBoundary';

// Default messages for English
const defaultMessages = {
  title: "AI-Powered Physical AI Assistant",
  description: "Advanced AI assistant for Physical AI & Humanoid Robotics textbook with RAG capabilities",
  heading: "AI-Powered Physical AI Assistant",
  subtitle: "Advanced AI assistant powered by RAG technology. Ask questions about Physical AI, robotics, and humanoid systems. Our intelligent assistant understands context and provides precise answers from the textbook.",
  placeholder: "Ask about Physical AI & Robotics...",
  welcome_message: "Hello! I'm your Physical AI & Humanoid Robotics Assistant. How can I help you today?",
  powered_by: "Powered by Retrieval-Augmented Generation (RAG) technology • Real-time context retrieval • Context-aware responses",
  'quick_questions.embodied_intelligence': "Explain embodied intelligence",
  'quick_questions.balance_question': "How do humanoid robots maintain balance?",
  'quick_questions.sensorimotor_learning': "What is sensorimotor learning?",
};

const Root = ({ children, locale = 'en' }) => {
  // Only support English now that Urdu has been removed
  const messages = defaultMessages;

  return (
    <ErrorBoundary>
      <IntlProvider locale="en" messages={messages} defaultLocale="en">
        {children}
      </IntlProvider>
    </ErrorBoundary>
  );
};

export default Root;
