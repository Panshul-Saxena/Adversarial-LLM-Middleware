import React, { useEffect, useRef } from 'react';
import MessageBubble from './MessageBubble';
import '../App.css'; // Styling defined in App.css

const ChatWindow = ({ messages, loading }) => {
  const bottomRef = useRef();

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  return (
    <div className="chat-window">
      {messages.map((msg, idx) => (
        <MessageBubble
          key={idx}
          sender={msg.sender}
          text={msg.text}
          adversarial_detected={msg.adversarial_detected}
          original_prompt={msg.original_prompt}
        />
      ))}
      {loading && <MessageBubble sender="bot" text="Typing..." />}
      <div ref={bottomRef} />
    </div>
  );
};

export default ChatWindow;
