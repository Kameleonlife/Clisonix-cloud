import Head from 'next/head';
import LiveChatTools from '../components/LiveChatTools';
import React, { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';

interface Message {
  id: string;
  sender: 'user' | 'agi' | 'system';
  content: string;
  timestamp: string;
}

const ChatPage = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const chatRef = useRef<HTMLDivElement>(null);

  // Auto-scroll kur vijnÃ« mesazhe tÃ« reja
  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  }, [messages]);

  const sendMessage = async () => {
    if (!inputValue.trim()) return;

    const newMsg: Message = {
      id: crypto.randomUUID(),
      sender: 'user',
      content: inputValue.trim(),
      timestamp: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, newMsg]);
    setInputValue('');
    setLoading(true);

    try {
      const response = await fetch('/api/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: newMsg.content }),
      });

      const data = await response.json();

      const aiResponse =
        data?.response ||
        data?.result ||
        data?.output ||
        '⚠️ Asnjë përgjigje e kthyer nga AGI/ASI.';

      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          sender: 'agi',
          content: aiResponse,
          timestamp: new Date().toISOString(),
        },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          sender: 'system',
          content:
            'Asi Nuk u arrit lidhja me backend. Kontrollo që `Clisonix` po punon në portin 8000.',
          timestamp: new Date().toISOString(),
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Head>
        <title>Clisonix â€¢ Live Chat Toolkit</title>
        <meta
          name="description"
          content="Trigger Clisonix diagnostics, ASI automations, and neural symphony actions directly from the live chat console."
        />
      </Head>
      <main className="min-h-screen bg-[#050b1a] text-slate-50 px-6 py-10">
        <div className="mx-auto max-w-5xl space-y-8">
          <header className="space-y-2">
            <p className="text-sm uppercase tracking-[0.25em] text-cyan-300/70">Clisonix Control Center</p>
            <h1 className="text-3xl font-semibold">Live Chat Automation Toolkit</h1>
            <p className="text-slate-300">
              Launch mesh diagnostics, ALBI pattern detectors, and ASI safety sweeps alongside the operator dialogue.
              Every tool is synced with the backend `/api/asi/tools` registry, so the chat stays aligned with production runbooks.
            </p>
          </header>
          <LiveChatTools />
          <div
            ref={chatRef}
            className="w-full max-w-4xl h-[70vh] bg-gray-900/70 rounded-2xl p-5 overflow-y-auto border border-gray-700 shadow-lg backdrop-blur-md"
          >
            {messages.length === 0 && (
              <p className="text-gray-400 text-center mt-10">
                Filloni një bisedë me inteligjencën AGI...
              </p>
            )}

            {messages.map((msg) => (
              <motion.div
                key={msg.id}
                className={`my-3 flex ${
                  msg.sender === 'user' ? 'justify-end' : 'justify-start'
                }`}
                initial={{ opacity: 0, y: 5 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.2 }}
              >
                <div
                  className={`max-w-[75%] p-3 rounded-2xl ${
                    msg.sender === 'user'
                      ? 'bg-blue-600 text-white'
                      : msg.sender === 'agi'
                      ? 'bg-green-700 text-white'
                      : 'bg-gray-600 text-yellow-200'
                  }`}
                >
                  <p className="whitespace-pre-wrap leading-relaxed">
                    {msg.content}
                  </p>
                  <p className="text-xs mt-1 opacity-60">
                    {new Date(msg.timestamp).toLocaleTimeString()}
                  </p>
                </div>
              </motion.div>
            ))}
          </div>

          <div className="w-full max-w-4xl flex mt-5 gap-2">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
              placeholder="Shkruaj një pyetje ose komandë për AGI..."
              className="flex-grow p-3 rounded-xl bg-gray-800 text-white border border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              type="button"
              onClick={sendMessage}
              disabled={loading || !inputValue.trim()}
              className="px-5 py-3 rounded-xl bg-blue-600 text-white font-medium hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? 'Duke menduar...' : 'Dërgo'}
            </button>
          </div>
        </div>
      </main>
    </>
  );
};

export default ChatPage;

export async function getServerSideProps() {
  return {
    props: {},
  };
}
