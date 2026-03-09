import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Clock, Check, Sparkles, Heart, ThumbsDown, Edit2, X, Trash2 } from 'lucide-react';

const CLOTHING_TYPES = [
  'Blouse', 'Dresses', 'Jeans', 'Trousers', 'Shorts', 'Skirts',
  'Tshirts', 'Shirts', 'Tops', 'Sweaters', 'Jackets', 'Hoodies',
  'Leggings', 'Track Pants', 'Blazers', 'Sweatshirts', 'Tunics', 'Jumpsuit', 'Swimwear',
  'Salwar', 'Patiala', 'Kurtis',
  // Saree categories (specific for different occasions)
  'Casual Saree', 'Office Saree', 'Wedding Saree', 'Traditional Saree',
  // Kurta categories (specific for different occasions)
  'Casual Kurta', 'Traditional Kurta',
  // Lehenga categories
  'Lehenga', 'Wedding Lehenga',
  // Other traditional wear
  'Sherwani'
];

export function ItemCard({
  item,
  index = 0,
  showWearHistory = false,
  onMarkWorn = null,
  onFindPair = null,
  onToggleFavorite = null,
  onTypeUpdate = null,
  onDelete = null,
  compact = false,  // New: compact mode for chat display
}) {
  const [isMarking, setIsMarking]         = useState(false);
  const [isFindingPair, setIsFindingPair] = useState(false);
  const [isFavorite, setIsFavorite]       = useState(item.isFavorite || false);
  const [isDisliked, setIsDisliked]       = useState(item.isDisliked || false);
  const [isEditing, setIsEditing]         = useState(false);
  const [editedType, setEditedType]       = useState(item.type || '');
  const [currentType, setCurrentType]     = useState(item.type || '');
  const [isDeleting, setIsDeleting]       = useState(false);

  const handleMarkWorn = async (e) => {
    e.stopPropagation();
    if (!onMarkWorn || isMarking) return;
    setIsMarking(true);
    await onMarkWorn(item);
    setIsMarking(false);
  };

  const handleFindPair = async (e) => {
    e.stopPropagation();
    if (!onFindPair || isFindingPair) return;
    setIsFindingPair(true);
    await onFindPair(item);
    setIsFindingPair(false);
  };

  const handleToggleFavorite = async (e) => {
    e.stopPropagation();
    try {
      const res = await fetch(`http://localhost:5000/api/wardrobe/${item.id}/favorite`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
      });
      if (res.ok) {
        const data = await res.json();
        setIsFavorite(data.isFavorite);
        if (data.isFavorite && isDisliked) setIsDisliked(false);
        if (onToggleFavorite) onToggleFavorite(item);
      }
    } catch (err) { console.error(err); }
  };

  const handleToggleDislike = async (e) => {
    e.stopPropagation();
    try {
      const res = await fetch(`http://localhost:5000/api/wardrobe/${item.id}/dislike`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
      });
      if (res.ok) {
        const data = await res.json();
        setIsDisliked(data.isDisliked);
        if (data.isDisliked && isFavorite) setIsFavorite(false);
      }
    } catch (err) { console.error(err); }
  };

  const handleSaveType = async (e) => {
    e.stopPropagation();
    if (!editedType || editedType === currentType) { setIsEditing(false); return; }
    try {
      const res = await fetch(`http://localhost:5000/api/wardrobe/${item.id}/update-type`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type: editedType }),
      });
      if (res.ok) {
        const data = await res.json();
        setCurrentType(data.type);
        setIsEditing(false);
        if (onTypeUpdate) onTypeUpdate(item.id, data.type, data.eventScores);
      }
    } catch (err) { console.error(err); }
  };

  const handleDelete = async (e) => {
    e.stopPropagation();
    if (!window.confirm(`Delete "${currentType || 'this item'}"?`)) return;
    setIsDeleting(true);
    try {
      const res = await fetch(`http://localhost:5000/api/wardrobe/${item.id}`, { method: 'DELETE' });
      if (res.ok) { if (onDelete) onDelete(item.id); }
      else { alert('Failed to delete item'); setIsDeleting(false); }
    } catch (err) { console.error(err); setIsDeleting(false); }
  };

  const formatLastWorn = (dateString) => {
    if (!dateString) return null;
    const diffDays = Math.ceil(Math.abs(new Date() - new Date(dateString)) / (1000 * 60 * 60 * 24));
    if (diffDays === 0) return 'Worn today';
    if (diffDays === 1) return 'Worn yesterday';
    if (diffDays < 7)  return `${diffDays}d ago`;
    if (diffDays < 30) return `${Math.floor(diffDays / 7)}w ago`;
    return `${Math.floor(diffDays / 30)}mo ago`;
  };

  const wearCount   = item.wearCount || 0;
  const bestEvent   = item.best_event || item.bestEvent || '';
  const lastWornStr = formatLastWorn(item.lastWorn);
  const confidence  = item.confidence;

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35, delay: index * 0.06 }}
      className={`group relative bg-white rounded-xl overflow-hidden border border-[#EDE8E0] hover:shadow-lg transition-all duration-300 ${
        compact ? 'hover:-translate-y-0.5' : 'hover:-translate-y-1 hover:shadow-[0_8px_30px_rgba(0,0,0,0.09)]'
      }`}
    >
      {/* ── Image ── */}
      <div className="relative overflow-hidden bg-[#F8F5F0]" style={{ aspectRatio: '3/4' }}>
        <img
          src={item.image}
          alt={currentType || 'Wardrobe item'}
          className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-[1.04]"
        />

        {/* Category / best-event pill — bottom left */}
        {bestEvent && (
          <div className="absolute bottom-2.5 left-2.5">
            <span className="bg-white/95 backdrop-blur-sm text-[#3C3C3C] text-[10px] font-medium px-2.5 py-1 rounded-full shadow-sm border border-white/60">
              {bestEvent}
            </span>
          </div>
        )}

        {/* Wear count — top right */}
        {showWearHistory && (
          <div className={`absolute ${compact ? 'top-1.5 right-1.5' : 'top-2.5 right-2.5'}`}>
            <span className={`bg-white/90 backdrop-blur-sm text-[#6B6B6B] font-medium ${compact ? 'text-[9px] px-1.5 py-0.5' : 'text-[10px] px-2 py-0.5'} rounded-full border border-[#EDE8E0] flex items-center gap-1`}>
              <Clock className={compact ? 'w-2 h-2' : 'w-2.5 h-2.5'} />
              {wearCount}×
            </span>
          </div>
        )}

        {/* Low-confidence badge */}
        {confidence !== undefined && confidence < 0.75 && (
          <div className="absolute bottom-2.5 right-2.5">
            <span className="bg-amber-400/90 text-white text-[10px] font-semibold px-2 py-0.5 rounded-full">
              {Math.round(confidence * 100)}%
            </span>
          </div>
        )}

        {/* Heart — top left */}
        <button
          onClick={handleToggleFavorite}
          className={`absolute ${compact ? 'top-1.5 left-1.5 w-6 h-6' : 'top-2.5 left-2.5 w-8 h-8'} rounded-full flex items-center justify-center transition-all duration-200
            ${isFavorite
              ? 'bg-[#8B5A5A] text-white shadow-md'
              : 'bg-white/90 text-[#C8C0B8] hover:text-[#8B5A5A] border border-[#EDE8E0] shadow-sm'
            }`}
        >
          <Heart className={`${compact ? 'w-2.5 h-2.5' : 'w-3.5 h-3.5'} ${isFavorite ? 'fill-current' : ''}`} />
        </button>

        {/* Dislike — appears on hover (hidden in compact mode) */}
        {!compact && (
          <button
            onClick={handleToggleDislike}
            className={`absolute top-12 left-2.5 w-8 h-8 rounded-full flex items-center justify-center transition-all duration-200
              opacity-0 group-hover:opacity-100
              ${isDisliked
                ? 'bg-[#6B6B6B] text-white shadow-md'
                : 'bg-white/90 text-[#C8C0B8] hover:text-[#6B6B6B] border border-[#EDE8E0] shadow-sm'
              }`}
          >
            <ThumbsDown className={`w-3.5 h-3.5 ${isDisliked ? 'fill-current' : ''}`} />
          </button>
        )}
      </div>

      {/* ── Info area ── */}
      <div className={compact ? 'px-2 pt-2 pb-2' : 'px-3.5 pt-3 pb-3.5'}>

        {/* Name / editable type */}
        {!isEditing ? (
          <h3 className={`font-serif font-semibold text-[#1E1E1E] leading-snug truncate ${compact ? 'text-[11px] mb-0' : 'text-[14px] mb-0.5'}`}>
            {currentType || 'Unknown Type'}
          </h3>
        ) : (
          <div className="flex items-center gap-1.5 mb-2" onClick={e => e.stopPropagation()}>
            <select
              value={editedType}
              onChange={e => setEditedType(e.target.value)}
              className="flex-1 text-xs border border-[#8B5A5A]/40 rounded-lg px-2 py-1.5 focus:outline-none focus:border-[#8B5A5A] text-[#2C2C2C] bg-white"
            >
              {CLOTHING_TYPES.map(t => <option key={t} value={t}>{t}</option>)}
            </select>
            <button onClick={handleSaveType} className="w-7 h-7 bg-[#7A9B8E] text-white rounded-lg flex items-center justify-center flex-shrink-0 hover:bg-[#6A8B7E] transition-colors">
              <Check className="w-3.5 h-3.5" />
            </button>
            <button onClick={e => { e.stopPropagation(); setIsEditing(false); }} className="w-7 h-7 bg-[#C8C0B8] text-white rounded-lg flex items-center justify-center flex-shrink-0 hover:bg-[#B0A898] transition-colors">
              <X className="w-3.5 h-3.5" />
            </button>
          </div>
        )}

        {/* Subtitle: confidence/filename */}
        {!compact && (
          <p className="text-[11px] text-[#A8A098] truncate mb-2 leading-tight">
            {confidence
              ? `${Math.round(confidence * 100)}% confidence`
              : item.filename
                ? item.filename.replace(/\.[^.]+$/, '')
                : ''}
            {confidence && lastWornStr ? ` · ${lastWornStr}` : (lastWornStr || '')}
          </p>
        )}

        {/* Tags row */}
        {!compact && (
          <>
            {bestEvent && (
              <div className="flex items-center gap-2 mb-3 flex-wrap">
                <span className="inline-flex items-center gap-1 text-[10px] text-[#8B8078] bg-[#F5F0EB] px-2 py-0.5 rounded-full">
                  🏷️ {bestEvent}
                </span>
                {item.reason && (
                  <span className="inline-flex items-center text-[10px] text-[#7A9B8E] italic truncate max-w-full">
                    {item.reason}
                  </span>
                )}
              </div>
            )}
          </>
        )}

        {/* ── Action link row ── */}
        <div className={`flex items-center border-t border-[#F2EDE6] gap-0.5 ${compact ? 'pt-1.5 text-[10px]' : 'pt-2.5'}`}>

          {/* Edit - hidden in compact mode */}
          {!compact && (
            <>
              <button
                onClick={e => { e.stopPropagation(); setIsEditing(true); setEditedType(currentType); }}
                className="inline-flex items-center gap-1 text-[11px] text-[#6B6B6B] hover:text-[#2C2C2C] transition-colors px-1.5 py-0.5 rounded-md hover:bg-[#F5F0EB]"
              >
                <Edit2 className="w-3 h-3" /> Edit
              </button>
              <span className="text-[#DDD5CA] text-xs mx-0.5 select-none">·</span>
            </>
          )}

          {/* Mark Worn */}
          {onMarkWorn && (
            <>
              <button
                onClick={handleMarkWorn}
                disabled={isMarking}
                className={`inline-flex items-center gap-1 ${compact ? 'text-[10px]' : 'text-[11px]'} text-[#7A9B8E] hover:text-[#5A7B6E] transition-colors px-1.5 py-0.5 rounded-md hover:bg-[#F0F5F3] disabled:opacity-40`}
              >
                <Check className={compact ? 'w-2.5 h-2.5' : 'w-3 h-3'} />
                {isMarking ? 'Marking…' : (compact ? 'Worn' : 'Mark Worn')}
              </button>
              {!compact && <span className="text-[#DDD5CA] text-xs mx-0.5 select-none">·</span>}
            </>
          )}

          {/* Pair */}
          {onFindPair && (
            <>
              <button
                onClick={handleFindPair}
                disabled={isFindingPair}
                className={`inline-flex items-center gap-1 ${compact ? 'text-[10px]' : 'text-[11px]'} text-[#9B8A5A] hover:text-[#7B6A3A] transition-colors px-1.5 py-0.5 rounded-md hover:bg-[#F5F2EB] disabled:opacity-40`}
              >
                <Sparkles className={compact ? 'w-2.5 h-2.5' : 'w-3 h-3'} />
                {isFindingPair ? 'Finding…' : 'Pair'}
              </button>
              {!compact && <span className="text-[#DDD5CA] text-xs mx-0.5 select-none">·</span>}
            </>
          )}

          {/* Delete — pushed to right, subtle red */}
          {onDelete && !compact && (
            <button
              onClick={handleDelete}
              disabled={isDeleting}
              className="inline-flex items-center gap-1 text-[11px] text-[#C07060] hover:text-[#A05040] transition-colors px-1.5 py-0.5 rounded-md hover:bg-[#FDF0EE] disabled:opacity-40 ml-auto"
            >
              <Trash2 className="w-3 h-3" />
              {isDeleting ? 'Deleting…' : 'Delete'}
            </button>
          )}
        </div>
      </div>
    </motion.div>
  );
}