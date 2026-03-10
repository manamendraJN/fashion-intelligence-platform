import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { cn } from '../lib/utils';
import { Sparkles, User, X, ChevronLeft, ChevronRight } from 'lucide-react';
import { ItemCard } from './ItemCard';

export function ChatMessage({ role, content, suggestions, timestamp, onTypeUpdate, eventContext: _unusedProp }) {
  // NOTE: eventContext is read from each item directly (item.eventContext),
  // not from a prop — because {...msg} spread in Chat.jsx doesn't carry it.
  const isUser = role === 'user';
  const [localSuggestions, setLocalSuggestions] = useState(suggestions || []);
  const [pairingResults, setPairingResults]     = useState(null);
  const [isMarkingPair, setIsMarkingPair]       = useState(false);
  const [selectedPairingItem, setSelectedPairingItem] = useState(null);
  const [showOutfitModal, setShowOutfitModal]   = useState(false);
  const [outfitToConfirm, setOutfitToConfirm]   = useState(null);
  const [currentMatchIndex, setCurrentMatchIndex] = useState(0);

  const handleTypeUpdate = (itemId, newType, newEventScores) => {
    setLocalSuggestions(prev =>
      prev.map(i => i.id === itemId ? { ...i, type: newType, eventScores: newEventScores } : i)
    );
    if (pairingResults) {
      setPairingResults(prev => ({
        ...prev,
        matches:      prev.matches.map(i => i.id === itemId ? { ...i, type: newType } : i),
        selectedItem: prev.selectedItem.id === itemId
          ? { ...prev.selectedItem, type: newType }
          : prev.selectedItem
      }));
    }
    if (onTypeUpdate) onTypeUpdate(itemId, newType, newEventScores);
  };

  const handleMarkWorn = async (item) => {
    try {
      const res = await fetch(`http://localhost:5000/api/wardrobe/${item.id}/mark-worn`, {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({ occasion: 'Current Event', date: new Date().toISOString() })
      });
      if (res.ok) {
        setLocalSuggestions(prev => prev.map(i =>
          i.id === item.id
            ? { ...i, lastWorn: new Date().toISOString(), wearCount: (i.wearCount || 0) + 1 }
            : i
        ));
      }
    } catch (err) { console.error(err); }
  };

  // ── Key fix: pass event_type and weather as query params so the backend uses
  //    dress-code-aware and weather-aware pairing rules
  const handleFindPair = async (item) => {
    try {
      // item.eventContext and item.weatherContext are attached in Chat.jsx
      const eventContext = item.eventContext || null;
      const weatherContext = item.weatherContext || null;
      
      let url = `http://localhost:5000/api/outfit-pairing/${item.id}`;
      const params = [];
      if (eventContext) params.push(`event_type=${encodeURIComponent(eventContext)}`);
      if (weatherContext) params.push(`weather=${encodeURIComponent(weatherContext)}`);
      if (params.length > 0) url += `?${params.join('&')}`;

      const res  = await fetch(url);
      const data = await res.json();

      if (data.success && data.matches.length > 0) {
        setPairingResults({
          selectedItem:    { ...item, image: `http://localhost:5000${item.url || item.image}` },
          category:        data.pairingCategory || data.pairingNote || 'Outfit Pairing',
          matches:         data.matches.map(m => ({ ...m, image: `http://localhost:5000${m.url}` })),
          message:         data.message,
          avoidTypes:      data.avoidTypes || [],
          pairingNote:     data.pairingNote || '',
        });
      } else {
        alert(data.message || 'No matching items found in your wardrobe for this event.');
      }
    } catch (err) { console.error(err); }
  };

  const handleMarkPairAsWorn = async (pairItem) => {
    // Show the interactive modal with all matches
    setCurrentMatchIndex(pairingResults.matches.findIndex(m => m.id === pairItem.id));
    setOutfitToConfirm({
      baseItem: pairingResults.selectedItem,
      allMatches: pairingResults.matches
    });
    setShowOutfitModal(true);
  };

  const confirmMarkAsWorn = async () => {
    if (!outfitToConfirm || !outfitToConfirm.allMatches[currentMatchIndex]) return;

    const selectedMatch = outfitToConfirm.allMatches[currentMatchIndex];
    setIsMarkingPair(true);
    setSelectedPairingItem(selectedMatch.id);
    try {
      const res = await fetch('http://localhost:5000/api/wardrobe/mark-pair-worn', {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({
          itemIds:  [outfitToConfirm.baseItem.id, selectedMatch.id],
          occasion: 'Outfit Pairing',
          date:     new Date().toISOString()
        })
      });
      if (res.ok) {
        setPairingResults(null);
        setShowOutfitModal(false);
        setOutfitToConfirm(null);
        setCurrentMatchIndex(0);
      }
    } catch (err) { console.error(err); }
    finally {
      setIsMarkingPair(false);
      setSelectedPairingItem(null);
    }
  };

  const renderContent = (text) =>
    text.split('\n').map((line, i) => {
      const parts = line.split(/\*\*(.*?)\*\*/g);
      return (
        <span key={i}>
          {parts.map((part, j) => j % 2 === 1 ? <strong key={j}>{part}</strong> : part)}
          {i < text.split('\n').length - 1 && <br />}
        </span>
      );
    });

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
          {isUser
            ? <User className="w-3.5 h-3.5 text-white" />
            : <Sparkles className="w-3.5 h-3.5 text-white" />}
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
              className="mt-2 grid grid-cols-3 gap-3 max-w-4xl"
            >
              {localSuggestions.map((item, idx) => (
                <div key={item.id} className="relative w-full max-w-[160px]">
                  <ItemCard
                    item={item}
                    index={idx}
                    showWearHistory={true}
                    onMarkWorn={handleMarkWorn}
                    onFindPair={handleFindPair}   // passes eventContext via item prop
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

          {/* ── Outfit Pairing panel ── */}
          {pairingResults && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mt-3 bg-white rounded-2xl border border-[#EDE8E0] shadow-sm overflow-hidden"
            >
              {/* Header */}
              <div className="flex items-center justify-between px-4 py-3 bg-[#F8F5F0] border-b border-[#EDE8E0]">
                <div className="flex items-center gap-2">
                  <Sparkles className="w-4 h-4 text-[#8B5A5A]" />
                  <div>
                    <p className="text-[13px] font-semibold text-[#2C2C2C]">
                      {pairingResults.category} for{' '}
                      <span className="text-[#8B5A5A]">{pairingResults.selectedItem.type}</span>
                    </p>
                    {pairingResults.pairingNote && (
                      <p className="text-[10px] text-[#9A9A9A] mt-0.5">{pairingResults.pairingNote}</p>
                    )}
                  </div>
                </div>
                <button onClick={() => setPairingResults(null)}
                  className="p-1 hover:bg-[#EDE8E0] rounded-lg transition-colors">
                  <X className="w-3.5 h-3.5 text-[#9A9A9A]" />
                </button>
              </div>

              {/* Side-by-side items */}
              <div className="p-4">
                <p className="text-[11px] text-[#9A9A9A] mb-3">{pairingResults.message}</p>
                <div className="flex gap-4 overflow-x-auto scrollbar-hide pb-2">

                  {/* Selected item */}
                  <div className="flex-shrink-0 w-32">
                    <p className="text-[9px] font-semibold text-[#8B5A5A] uppercase tracking-wider mb-1.5 text-center">
                      Selected
                    </p>
                    <div className="relative">
                      <ItemCard item={pairingResults.selectedItem} index={0}
                        showWearHistory={false} onTypeUpdate={handleTypeUpdate} compact={true} />
                      <div className="absolute -top-1.5 -right-1.5 bg-[#8B5A5A] text-white text-[9px] font-bold px-1.5 py-0.5 rounded-full shadow-md z-10">
                        Base
                      </div>
                    </div>
                  </div>

                  {/* Divider */}
                  <div className="flex-shrink-0 flex items-center justify-center">
                    <div className="flex flex-col items-center gap-1 text-[#C8C0B8]">
                      <div className="w-px h-8 bg-[#EDE8E0]" />
                      <span className="text-lg">+</span>
                      <div className="w-px h-8 bg-[#EDE8E0]" />
                    </div>
                  </div>

                  {/* Match items */}
                  <div className="flex gap-2.5 overflow-x-auto scrollbar-hide">
                    {pairingResults.matches.map((match, idx) => (
                      <div key={match.id} className="flex-shrink-0 w-32 flex flex-col gap-1.5">
                        <p className="text-[9px] font-semibold text-[#7A9B8E] uppercase tracking-wider text-center">
                          Match {idx + 1}
                        </p>
                        <div className="relative">
                          <ItemCard item={match} index={idx}
                            showWearHistory={false} onTypeUpdate={handleTypeUpdate} compact={true} />
                          <div className="absolute -top-1.5 -right-1.5 bg-[#7A9B8E] text-white text-[9px] font-bold px-1.5 py-0.5 rounded-full shadow-md z-10">
                            {match.matchScore}%
                          </div>
                        </div>
                        <button
                          onClick={() => handleMarkPairAsWorn(match)}
                          disabled={isMarkingPair}
                          className="w-full py-1.5 bg-gradient-to-r from-[#8B5A5A] to-[#A67676] text-white text-[10px] font-semibold rounded-lg hover:shadow-md transition-all disabled:opacity-50"
                        >
                          {isMarkingPair && selectedPairingItem === match.id
                            ? 'Marking…' : 'Wear Together'}
                        </button>
                      </div>
                    ))}
                  </div>

                </div>
              </div>
            </motion.div>
          )}

          {/* ── Outfit Selection Modal ── */}
          {showOutfitModal && outfitToConfirm && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 px-4"
              onClick={() => { setShowOutfitModal(false); setCurrentMatchIndex(0); }}
            >
              <motion.div
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ type: "spring", duration: 0.4 }}
                className="bg-white rounded-2xl shadow-2xl max-w-md w-full overflow-hidden max-h-[90vh] overflow-y-auto"
                onClick={(e) => e.stopPropagation()}
              >
                {/* Header */}
                <div className="bg-gradient-to-r from-[#8B5A5A] to-[#A67676] px-6 py-4 text-white">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Sparkles className="w-5 h-5" />
                      <h2 className="text-base font-serif font-semibold">Select Your Outfit</h2>
                    </div>
                    <button
                      onClick={() => { setShowOutfitModal(false); setCurrentMatchIndex(0); }}
                      className="p-1 hover:bg-white/20 rounded-lg transition-colors"
                    >
                      <X className="w-5 h-5" />
                    </button>
                  </div>
                  <p className="text-sm text-white/90 mt-1">Perfect combination for your event!</p>
                </div>

                {/* Outfit Display */}
                <div className="p-6" style={{ perspective: '1000px' }}>
                  
                  {/* Match counter and navigation */}
                  <div className="flex items-center justify-center gap-4 mb-4">
                    <button
                      onClick={() => setCurrentMatchIndex(prev => (prev - 1 + outfitToConfirm.allMatches.length) % outfitToConfirm.allMatches.length)}
                      className="p-2 bg-[#F5F0EB] hover:bg-[#EDE8E0] rounded-full transition-colors shadow-sm"
                    >
                      <ChevronLeft className="w-5 h-5 text-[#8B5A5A]" />
                    </button>
                    
                    <span className="text-sm font-semibold text-[#6B6B6B]">
                      Match {currentMatchIndex + 1} of {outfitToConfirm.allMatches.length}
                    </span>
                    
                    <button
                      onClick={() => setCurrentMatchIndex(prev => (prev + 1) % outfitToConfirm.allMatches.length)}
                      className="p-2 bg-[#F5F0EB] hover:bg-[#EDE8E0] rounded-full transition-colors shadow-sm"
                    >
                      <ChevronRight className="w-5 h-5 text-[#8B5A5A]" />
                    </button>
                  </div>

                  {/* Single card with outfit preview */}
                  <div className="flex justify-center mb-4">
                    {(() => {
                      const currentMatch = outfitToConfirm.allMatches[currentMatchIndex];
                      const topTypes = ['Blouse', 'Tshirts', 'Sweaters', 'Blazers', 'Jackets', 'Formal Shirt', 'Casual Shirt', 'Tank Top', 'Crop Top', 'Sweatshirts', 'Hoodies', 'Cardigan', 'Shirt'];
                      const baseIsTop = topTypes.some(t => outfitToConfirm.baseItem.type?.includes(t));
                      const matchIsTop = topTypes.some(t => currentMatch.type?.includes(t));
                      
                      let topItem, bottomItem;
                      if (baseIsTop && !matchIsTop) {
                        topItem = outfitToConfirm.baseItem;
                        bottomItem = currentMatch;
                      } else if (matchIsTop && !baseIsTop) {
                        topItem = currentMatch;
                        bottomItem = outfitToConfirm.baseItem;
                      } else {
                        topItem = outfitToConfirm.baseItem;
                        bottomItem = currentMatch;
                      }

                      return (
                        <motion.div
                          key={currentMatchIndex}
                          initial={{ opacity: 0, x: 20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ duration: 0.3 }}
                          className="relative bg-gradient-to-br from-white to-[#F8F5F0] rounded-2xl overflow-hidden w-52 transition-transform duration-500 hover:scale-105"
                          style={{ 
                            transformStyle: 'preserve-3d',
                            boxShadow: '0 20px 60px rgba(0,0,0,0.3), 0 0 0 1px rgba(139,90,90,0.2)'
                          }}
                        >
                          {/* Top Item with 3D layering */}
                          <div className="relative border-b-2 border-[#C8C0B8]/30" style={{ transform: 'translateZ(20px)' }}>
                            <img
                              src={topItem.image}
                              alt={topItem.type}
                              className="w-full h-44 object-cover"
                              style={{ 
                                filter: 'drop-shadow(0 4px 8px rgba(0,0,0,0.15))'
                              }}
                            />
                            <div 
                              className="absolute top-2 left-2 bg-[#8B5A5A] text-white text-[10px] font-semibold px-2 py-1 rounded-full"
                              style={{ 
                                transform: 'translateZ(30px)',
                                boxShadow: '0 4px 12px rgba(139,90,90,0.4)'
                              }}
                            >
                              {topItem.type}
                            </div>
                          </div>

                          {/* Center Plus Badge with depth */}
                          <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-20"
                            style={{ transform: 'translateZ(40px) translateX(-50%) translateY(-50%)' }}>
                            <div 
                              className="w-10 h-10 rounded-full bg-gradient-to-br from-[#8B5A5A] to-[#7A9B8E] flex items-center justify-center border-2 border-white"
                              style={{
                                boxShadow: '0 8px 20px rgba(0,0,0,0.3), 0 0 0 3px rgba(255,255,255,0.5)'
                              }}
                            >
                              <span className="text-lg font-bold text-white">+</span>
                            </div>
                          </div>

                          {/* Bottom Item with 3D layering */}
                          <div className="relative" style={{ transform: 'translateZ(20px)' }}>
                            <img
                              src={bottomItem.image}
                              alt={bottomItem.type}
                              className="w-full h-44 object-cover"
                              style={{ 
                                filter: 'drop-shadow(0 4px 8px rgba(0,0,0,0.15))'
                              }}
                            />
                            <div 
                              className="absolute bottom-2 left-2 bg-[#7A9B8E] text-white text-[10px] font-semibold px-2 py-1 rounded-full"
                              style={{ 
                                transform: 'translateZ(30px)',
                                boxShadow: '0 4px 12px rgba(122,155,142,0.4)'
                              }}
                            >
                              {bottomItem.type}
                            </div>
                          </div>

                          {/* Match score badge */}
                          <div 
                            className="absolute top-2 right-2 bg-[#7A9B8E] text-white text-[11px] font-bold px-2.5 py-1 rounded-full"
                            style={{ 
                              transform: 'translateZ(35px)',
                              boxShadow: '0 4px 12px rgba(122,155,142,0.5)'
                            }}
                          >
                            {currentMatch.matchScore}%
                          </div>

                          {/* Subtle 3D edge highlight */}
                          <div className="absolute inset-0 pointer-events-none" style={{
                            background: 'linear-gradient(135deg, rgba(255,255,255,0.4) 0%, transparent 50%, rgba(0,0,0,0.1) 100%)'
                          }}></div>
                        </motion.div>
                      );
                    })()}
                  </div>

                  {/* Compact description with match info */}
                  <p className="text-xs text-[#6B6B6B] text-center mb-4">
                    {outfitToConfirm.allMatches[currentMatchIndex].matchScore}% match • Use arrows to explore other options
                  </p>

                  {/* Action buttons */}
                  <div className="flex gap-3">
                    <button
                      onClick={() => { setShowOutfitModal(false); setCurrentMatchIndex(0); }}
                      className="flex-1 py-3 bg-[#F5F0EB] text-[#6B6B6B] text-sm font-semibold rounded-xl hover:bg-[#EDE8E0] transition-colors"
                    >
                      Cancel
                    </button>
                    <button
                      onClick={confirmMarkAsWorn}
                      disabled={isMarkingPair}
                      className="flex-1 py-3 bg-gradient-to-r from-[#8B5A5A] to-[#A67676] text-white text-sm font-semibold rounded-xl hover:shadow-lg transition-all disabled:opacity-50"
                    >
                      {isMarkingPair ? 'Marking...' : '✓ Wear This Outfit'}
                    </button>
                  </div>
                </div>
              </motion.div>
            </motion.div>
          )}

        </div>
      </div>
    </motion.div>
  );
}