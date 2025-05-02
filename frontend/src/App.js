import React, { useState } from 'react';
import { ThemeProvider } from './context/ThemeContext';
import Header from './components/Header';
import ChatWindow from './components/ChatWindow';
import InputBar from './components/InputBar';
import './App.css';
import './themes.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [detectActive, setDetectActive] = useState(false);

  const handleToggleDetect = () => {
    setDetectActive((prev) => !prev);
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    const rawInput = input;
    setInput('');
    setLoading(true);

    try {
      const res = await fetch('http://localhost:8000/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt: rawInput,
          middleware: detectActive
        })
      });

      const data = await res.json();

      const userMessage = {
        sender: 'user',
        text: data.corrected_prompt || rawInput,
        adversarial_detected: data.adversarial_detected,
        original_prompt: data.original_prompt
      };

      const botMessage = {
        sender: 'bot',
        text: data.response
      };

      setMessages((prev) => [...prev, userMessage, botMessage]);

    } catch {
      setMessages((prev) => [
        ...prev,
        { sender: 'user', text: rawInput },
        { sender: 'bot', text: '⚠️ Request failed.' }
      ]);
    }

    setLoading(false);
  };

  return (
    <ThemeProvider>
      <div className="app">
        <Header />
        <ChatWindow messages={messages} loading={loading} />
        <InputBar
          input={input}
          setInput={setInput}
          onSend={sendMessage}
          onToggleDetect={handleToggleDetect}
          detectActive={detectActive}
        />
      </div>
    </ThemeProvider>
  );
}

export default App;
