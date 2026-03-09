import React, { useEffect, useState, useRef } from 'react';
import { Layout } from '../components/Layout';
import { ChatMessage } from '../components/ChatMessage';
import { SAMPLE_QUERIES, INITIAL_WARDROBE } from '../data/mockData';
import { Send, Sparkles } from 'lucide-react';
import { motion } from 'framer-motion';

export function ChatPage() {
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);
  const [messages, setMessages] = useState([
    {
      id: '1',
      role: 'assistant',
      content:
        "Hello! I've analyzed your wardrobe and I'm ready to help. I know which items work for different events based on general fashion rules, and I'm learning your personal preferences with every interaction. What's on your calendar?",
      timestamp: new Date(),
    },
  ]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSend = (text = input) => {
    if (!text.trim()) return;

    const newMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: text,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, newMessage]);
    setInput('');
    setIsTyping(true);

    setTimeout(() => {
      let responseContent = 'I can help with that. Here are some options from your wardrobe.';
      let suggestions = [];

      const lowerText = text.toLowerCase();
      if (lowerText.includes('wedding')) {
        responseContent =
          'For a wedding, I recommend these ethnic wear options. The red kurta has a high suitability score (95%) for Tamil weddings based on our training data.';
        suggestions = INITIAL_WARDROBE.filter((item) => item.eventScores['Tamil Wedding'] > 0.8);
      } else if (lowerText.includes('office') || lowerText.includes('meeting')) {
        responseContent =
          "For your office meeting, these formal items would be perfect. I've noticed you haven't worn the Navy Shirt in a while.";
        suggestions = INITIAL_WARDROBE.filter((item) => item.eventScores['Office Meeting'] > 0.8);
      } else if (lowerText.includes('casual') || lowerText.includes('weekend')) {
        responseContent = "Here's a comfortable casual look for the weekend.";
        suggestions = INITIAL_WARDROBE.filter((item) => item.eventScores['Casual Outing'] > 0.6).slice(0, 2);
      } else {
        responseContent = "I've found a few items that might work for that occasion.";
        suggestions = [INITIAL_WARDROBE[0], INITIAL_WARDROBE[3]];
      }

      const aiResponse = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: responseContent,
        suggestions: suggestions,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, aiResponse]);
      setIsTyping(false);
    }, 1500);
  };

  return (
    <Layout>
      <div className="max-w-3xl mx-auto h-[calc(100vh-140px)] flex flex-col">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-serif text-[#2C2C2C] mb-2">Style Assistant</h1>
          <p className="text-sm text-gray-500">
            Powered by dual-phase learning:{' '}
            <span className="text-[#8B5A5A]">General Knowledge</span> +{' '}
            <span className="text-[#8B5A5A]">Personal Preferences</span>
          </p>
        </div>

        <div className="flex-1 overflow-y-auto scrollbar-hide px-4 pb-4">
          {messages.map((msg) => (
            <ChatMessage key={msg.id} {...msg} />
          ))}

          {isTyping && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex items-center space-x-2 text-gray-400 text-sm ml-12 mb-8"
            >
              <Sparkles className="w-4 h-4 animate-pulse" />
              <span>Thinking...</span>
            </motion.div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="mt-4 px-4">
          {messages.length === 1 && (
            <div className="flex flex-wrap gap-2 mb-4 justify-center">
              {SAMPLE_QUERIES.map((query) => (
                <button
                  key={query}
                  onClick={() => handleSend(query)}
                  className="px-4 py-2 bg-white border border-[#E5E0D8] rounded-full text-sm text-[#6B6B6B] hover:border-[#8B5A5A] hover:text-[#8B5A5A] transition-colors"
                >
                  {query}
                </button>
              ))}
            </div>
          )}

          <div className="relative">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Ask for an outfit recommendation..."
              className="w-full pl-6 pr-14 py-4 bg-white border border-[#E5E0D8] rounded-full shadow-sm focus:outline-none focus:ring-2 focus:ring-[#8B5A5A]/20 focus:border-[#8B5A5A] transition-all text-[#2C2C2C] placeholder:text-gray-400"
            />
            <button
              onClick={() => handleSend()}
              disabled={!input.trim() || isTyping}
              className="absolute right-2 top-2 p-2 bg-[#2C2C2C] text-white rounded-full hover:bg-black disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
          <p className="text-center text-[10px] text-gray-400 mt-3">
            AI can make mistakes. Please verify important outfit decisions.
          </p>
        </div>
      </div>
    </Layout>
  );
}
