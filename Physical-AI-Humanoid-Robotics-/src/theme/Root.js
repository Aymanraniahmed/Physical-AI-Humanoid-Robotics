import React from 'react';
import ChatbotWidget from '../components/ChatbotWidget';

// Root component wraps the entire app
export default function Root({children}) {
  return (
    <>
      {children}
      <ChatbotWidget />
    </>
  );
}
