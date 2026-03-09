import React from 'react';
import { motion } from 'framer-motion';
import { cn } from '../lib/utils';
import { Sparkles, User } from 'lucide-react';
import { ItemCard } from './ItemCard';

export function ChatMessage({ role, content, suggestions, timestamp }) {
  const isUser = role === 'user';

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={cn('flex w-full mb-8', isUser ? 'justify-end' : 'justify-start')}
    >
      <div className={cn('flex max-w-[85%] md:max-w-[75%]', isUser ? 'flex-row-reverse' : 'flex-row')}>
        {/* Avatar */}
        <div
          className={cn(
            'flex-shrink-0 h-8 w-8 rounded-full flex items-center justify-center mt-1',
            isUser ? 'bg-[#2C2C2C] ml-3' : 'bg-[#8B5A5A] mr-3'
          )}
        >
          {isUser ? (
            <User className="h-4 w-4 text-white" />
          ) : (
            <Sparkles className="h-4 w-4 text-white" />
          )}
        </div>

        {/* Message Content */}
        <div className="flex flex-col">
          <div
            className={cn(
              'px-6 py-4 rounded-2xl text-sm leading-relaxed shadow-sm',
              isUser
                ? 'bg-white text-[#2C2C2C] rounded-tr-none border border-[#E5E0D8]'
                : 'bg-[#2C2C2C] text-[#FAF8F5] rounded-tl-none'
            )}
          >
            {content}
          </div>

          <span
            className={cn(
              'text-[10px] text-gray-400 mt-1.5',
              isUser ? 'text-right' : 'text-left'
            )}
          >
            {timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </span>

          {/* Outfit Suggestions */}
          {suggestions && suggestions.length > 0 && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              transition={{ delay: 0.3 }}
              className="mt-4 grid grid-cols-2 gap-4"
            >
              {suggestions.map((item) => (
                <div key={item.id} className="relative">
                  <ItemCard item={item} />
                  <div className="absolute -top-2 -right-2 bg-[#8B5A5A] text-white text-[10px] font-bold px-2 py-1 rounded-full shadow-md">
                    Match
                  </div>
                </div>
              ))}
            </motion.div>
          )}
        </div>
      </div>
    </motion.div>
  );
}
