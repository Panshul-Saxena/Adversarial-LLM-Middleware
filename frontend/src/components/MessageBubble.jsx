import React from 'react';

const MessageBubble = ({ sender, text, adversarial_detected, original_prompt }) => {
  const isUser = sender === 'user';

  return (
    <div className={`bubble ${sender}`}>
      <div className="bubble-content">{text}</div>

      {isUser && adversarial_detected !== undefined && (
        <div className="adversarial-icon-wrapper">
          <span
            className="adv-info-icon"
            title={
              adversarial_detected
                ? `${original_prompt}` // Only show the original typo
                : ''
            }
          >
            ℹ️: {adversarial_detected ? 'Adversarial Input detected' : 'Not detected'}
          </span>
        </div>
      )}
    </div>
  );
};

export default MessageBubble;
