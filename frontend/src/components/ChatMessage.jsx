import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { cn } from '../lib/utils';
import { Sparkles, User, X } from 'lucide-react';
import { ItemCard } from './ItemCard';

export function ChatMessage({ role, content, suggestions, timestamp, onTypeUpdate }) {
  const isUser = role === 'user';
  const [localSuggestions, setLocalSuggestions] = useState(suggestions || []);
  const [pairingResults, setPairingResults]     = useState(null);
  const [isMarkingPair, setIsMarkingPair]       = useState(false);
  const [selectedPairingItem, setSelectedPairingItem] = useState(null);

  const handleTypeUpdate = (itemId, newType, newEventScores) => {
    setLocalSuggestions(prev => prev.map(i => i.id === itemId ? { ...i, type: newType, eventScores: newEventScores } : i));
    if (pairingResults) {
      setPairingResults(prev => ({
        ...prev,
        matches: prev.matches.map(i => i.id === itemId ? { ...i, type: newType } : i),
        selectedItem: prev.selectedItem.id === itemId ? { ...prev.selectedItem, type: newType } : prev.selectedItem
      }));
    }
    if (onTypeUpdate) onTypeUpdate(itemId, newType, newEventScores);
  };

  const handleMarkWorn = async (item) => {
    try {
      const res = await fetch(`http://localhost:5000/api/wardrobe/${item.id}/mark-worn`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ occasion: 'Current Event', date: new Date().toISOString() })
      });
      if (res.ok) {
        setLocalSuggestions(prev => prev.map(i =>
          i.id === item.id ? { ...i, lastWorn: new Date().toISOString(), wearCount: (i.wearCount || 0) + 1 } : i
        ));
      }
    } catch (err) { console.error(err); }
  };

  const handleFindPair = async (item) => {
    try {
      const res  = await fetch(`http://localhost:5000/api/outfit-pairing/${item.id}`);
      const data = await res.json();
      if (data.success && data.matches.length > 0) {
        setPairingResults({
          selectedItem: { ...item, image: `http://localhost:5000${item.url || item.image}` },
          category:     data.pairingCategory,
          matches:      data.matches.map(m => ({ ...m, image: `http://localhost:5000${m.url}` })),
          message:      data.message
        });
      } else {
        alert(data.message || 'No matching items found in your wardrobe.');
      }
    } catch (err) { console.error(err); }
  };

  const handleMarkPairAsWorn = async (pairItem) => {
    if (!pairingResults || !window.confirm(`Mark ${pairingResults.selectedItem.type} + ${pairItem.type} as worn together?`)) return;
    setIsMarkingPair(true);
    setSelectedPairingItem(pairItem.id);
    try {
      const res  = await fetch('http://localhost:5000/api/wardrobe/mark-pair-worn', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ itemIds: [pairingResults.selectedItem.id, pairItem.id], occasion: 'Outfit Pairing', date: new Date().toISOString() })
      });
      if (res.ok) { setPairingResults(null); }
    } catch (err) { console.error(err); }
    finally { setIsMarkingPair(false); setSelectedPairingItem(null); }
  };

  // Render bold **text** simply
  const renderContent = (text) => {
    return text.split('\n').map((line, i) => {
      const parts = line.split(/\*\*(.*?)\*\*/g);
      return (
        <span key={i}>
          {parts.map((part, j) => j % 2 === 1 ? <strong key={j}>{part}</strong> : part)}
          {i < text.split('\n').length - 1 && <br />}
        </span>
      );
    });
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={cn('flex w-full mb-6', isUser ? 'justify-end' : 'justify-start')}
    >
      <div className={cn('flex gap-3', isUser ? 'flex-row-reverse max-w-[85%]' : 'flex-row max-w-full')}>

        {/* Avatar */}
        <div className={cn(
          'flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center mt-0.5 shadow-sm',
          isUser ? 'bg-[#2C2C2C]' : 'bg-[#8B5A5A]'
        )}>
          {isUser ? <User className="w-3.5 h-3.5 text-white" /> : <Sparkles className="w-3.5 h-3.5 text-white" />}
        </div>

        <div className="flex flex-col gap-1 flex-1 min-w-0">

          {/* Bubble */}
          <div className={cn(
            'px-4 py-3 rounded-2xl text-[13px] leading-relaxed shadow-sm',
            isUser
              ? 'bg-[#2C2C2C] text-white rounded-tr-none'
              : 'bg-[#F5F0EB] text-[#2C2C2C] rounded-tl-none border border-[#EDE8E0]'
          )}>
            {renderContent(content)}
          </div>

          {/* Time */}
          <span className={cn('text-[10px] text-[#B0A898] px-1', isUser ? 'text-right' : 'text-left')}>
            {timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </span>

          {/* ── Outfit suggestions grid ── */}
          {localSuggestions?.length > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="mt-2 grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 lg:grid-cols-6 gap-2.5 max-w-5xl"
            >
              {localSuggestions.map((item, idx) => (
                <div key={item.id} className="relative w-full max-w-[160px]">
                  <ItemCard
                    item={item}
                    index={idx}
                    showWearHistory={true}
                    onMarkWorn={handleMarkWorn}
                    onFindPair={handleFindPair}
                    onTypeUpdate={handleTypeUpdate}
                    compact={true}
                  />
                  {item.suitabilityScore && (
                    <div className="absolute -top-1.5 -right-1.5 bg-[#8B5A5A] text-white text-[9px] font-bold px-1.5 py-0.5 rounded-full shadow-md z-10">
                      {Math.round(item.suitabilityScore * 100)}%
                    </div>
                  )}
                </div>
              ))}
            </motion.div>
          )}

          {/* ── Outfit Pairing — SIDE BY SIDE panel ── */}
          <AnimatePresencePairing pairingResults={pairingResults} onClose={() => setPairingResults(null)}>
            {pairingResults && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="mt-3 bg-white rounded-2xl border border-[#EDE8E0] shadow-sm overflow-hidden"
              >
                {/* Pairing header */}
                <div className="flex items-center justify-between px-4 py-3 bg-[#F8F5F0] border-b border-[#EDE8E0]">
                  <div className="flex items-center gap-2">
                    <Sparkles className="w-4 h-4 text-[#8B5A5A]" />
                    <p className="text-[13px] font-semibold text-[#2C2C2C]">
                      Matching {pairingResults.category} for <span className="text-[#8B5A5A]">{pairingResults.selectedItem.type}</span>
                    </p>
                  </div>
                  <button onClick={() => setPairingResults(null)} className="p-1 hover:bg-[#EDE8E0] rounded-lg transition-colors">
                    <X className="w-3.5 h-3.5 text-[#9A9A9A]" />
                  </button>
                </div>

                {/* Side-by-side: selected item + matches */}
                <div className="p-4">
                  <p className="text-[11px] text-[#9A9A9A] mb-3">{pairingResults.message}</p>
                  <div className="flex gap-4 overflow-x-auto scrollbar-hide pb-2">

                    {/* Selected item — left anchor */}
                    <div className="flex-shrink-0 w-32">
                      <p className="text-[9px] font-semibold text-[#8B5A5A] uppercase tracking-wider mb-1.5 text-center">Selected</p>
                      <div className="relative">
                        <ItemCard item={pairingResults.selectedItem} index={0} showWearHistory={false} onTypeUpdate={handleTypeUpdate} compact={true} />
                        <div className="absolute -top-1.5 -right-1.5 bg-[#8B5A5A] text-white text-[9px] font-bold px-1.5 py-0.5 rounded-full shadow-md z-10">
                          Base
                        </div>
                      </div>
                    </div>

                    {/* Arrow divider */}
                    <div className="flex-shrink-0 flex items-center justify-center">
                      <div className="flex flex-col items-center gap-1 text-[#C8C0B8]">
                        <div className="w-px h-8 bg-[#EDE8E0]"></div>
                        <span className="text-lg">+</span>
                        <div className="w-px h-8 bg-[#EDE8E0]"></div>
                      </div>
                    </div>

                    {/* Match items — scrollable row */}
                    <div className="flex gap-2.5 overflow-x-auto scrollbar-hide">
                      {pairingResults.matches.map((match, idx) => (
                        <div key={match.id} className="flex-shrink-0 w-32 flex flex-col gap-1.5">
                          <p className="text-[9px] font-semibold text-[#7A9B8E] uppercase tracking-wider text-center">
                            Match {idx + 1}
                          </p>
                          <div className="relative">
                            <ItemCard item={match} index={idx} showWearHistory={false} onTypeUpdate={handleTypeUpdate} compact={true} />
                            <div className="absolute -top-1.5 -right-1.5 bg-[#7A9B8E] text-white text-[9px] font-bold px-1.5 py-0.5 rounded-full shadow-md z-10">
                              {match.matchScore}%
                            </div>
                          </div>
                          <button
                            onClick={() => handleMarkPairAsWorn(match)}
                            disabled={isMarkingPair}
                            className="w-full py-1.5 bg-gradient-to-r from-[#8B5A5A] to-[#A67676] text-white text-[10px] font-semibold rounded-lg hover:shadow-md transition-all disabled:opacity-50"
                          >
                            {isMarkingPair && selectedPairingItem === match.id ? 'Marking…' : 'Wear Together'}
                          </button>
                        </div>
                      ))}
                    </div>

                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresencePairing>
        </div>
      </div>
    </motion.div>
  );
}

// tiny wrapper to avoid importing AnimatePresence at top level
function AnimatePresencePairing({ children }) {
  return <>{children}</>;
}