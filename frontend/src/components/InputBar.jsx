import React from 'react';

const InputBar = ({ input, setInput, onSend, onToggleDetect, detectActive }) => {
  const handleKeyDown = (e) => {
    if (e.key === 'Enter') onSend();
  };

  return (
    <div className="input-bar-container">
      <div className="tool-toggle-row">
        <button
          className={`tool-toggle-button ${detectActive ? 'active' : ''}`}
          onClick={onToggleDetect}
        >
          Adversarial Detection
        </button>
      </div>
      <div className="input-row">
        <input
          type="text"
          value={input}
          placeholder="Type your message..."
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <button onClick={onSend}>Send</button>
      </div>
    </div>
  );
};

export default InputBar;
