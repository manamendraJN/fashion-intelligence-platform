import React, { useEffect, useState } from 'react';
import { Layout } from '../components/Layout';
import { WardrobeUpload } from '../components/WardrobeUpload';
import { ItemCard } from '../components/ItemCard';
import { motion } from 'framer-motion';
import { Sparkles } from 'lucide-react';

const FEATURES = [
  { icon: '🧠', title: 'AI Classification', desc: 'Auto-detects clothing type, color & fabric from any photo.' },
  { icon: '🎯', title: 'Event Scoring',      desc: 'Rates each piece for office, casual, wedding & more.' },
  { icon: '✨', title: 'Smart Pairing',      desc: 'Suggests perfect outfit combos from your own wardrobe.' },
  { icon: '📈', title: 'Style Analytics',    desc: 'Tracks wear frequency & evolving personal style.' },
];

export function UploadPage() {
  const [items, setItems]   = useState([]);
  const [filter, setFilter] = useState('All Items');

  const fetchWardrobe = () => {
    fetch('http://localhost:5000/api/wardrobe')
      .then(r => r.json())
      .then(data => {
        if (Array.isArray(data)) setItems(data);
        else if (data?.items && Array.isArray(data.items)) setItems(data.items);
        else setItems([]);
      })
      .catch(() => setItems([]));
  };

  useEffect(() => { fetchWardrobe(); }, []);
  const handleUploadComplete = () => fetchWardrobe();
  const handleTypeUpdate = (id, type, scores) =>
    setItems(prev => prev.map(i => i.id === id ? { ...i, type, eventScores: scores } : i));
  const handleDelete = (id) =>
    setItems(prev => prev.filter(i => i.id !== id));
  const handleRecalculateAll = async () => {
    if (!confirm('Recalculate event scores for all items?')) return;
    try {
      const res  = await fetch('http://localhost:5000/api/wardrobe/recalculate-all', { method: 'POST', headers: { 'Content-Type': 'application/json' } });
      const data = await res.json();
      if (data.success) { alert(`✅ ${data.message}`); fetchWardrobe(); }
      else alert('❌ Failed');
    } catch { alert('❌ Error'); }
  };

  return (
    <Layout>

      {/* ══ TOP ROW ═══════════════════════════════════════════════════════════
          Title (left) + Upload widget (right), vertically centred             */}
      <div className="flex items-start justify-between gap-10 mb-7">

        {/* Left: headline */}
        <motion.div
          initial={{ opacity: 0, y: 14 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="pt-1"
        >
          <span className="inline-flex items-center px-3 py-1 rounded-full bg-[#E8E4DE] text-[#8B5A5A] text-xs font-medium tracking-wide uppercase mb-3">
            <Sparkles className="w-3 h-3 mr-1.5" />
            Wardrobe Fashion AI System
          </span>
          <h1 className="text-3xl md:text-4xl font-serif font-medium text-[#2C2C2C] leading-tight">
            Digitize your wardrobe.
            <br />
            <span className="text-[#8B5A5A] italic">Unlock your AURA.</span>
          </h1>
        </motion.div>

        {/* Right: compact upload bar */}
        <motion.div
          initial={{ opacity: 0, x: 16 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.15 }}
          className="flex-shrink-0 w-80 pt-1"
        >
          <WardrobeUpload onUploadComplete={handleUploadComplete} />
        </motion.div>
      </div>

      {/* ══ FEATURE STRIP ════════════════════════════════════════════════════ */}
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.45, delay: 0.22 }}
        className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-8"
      >
        {FEATURES.map(({ icon, title, desc }, i) => (
          <motion.div
            key={title}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.35, delay: 0.28 + i * 0.055 }}
            className="flex items-start gap-3 px-4 py-3.5 rounded-xl bg-white border border-[#EDE8E0] hover:border-[#C8A8A8] hover:shadow-sm transition-all duration-200"
          >
            <span className="text-lg leading-none mt-0.5 flex-shrink-0">{icon}</span>
            <div>
              <p className="text-[12.5px] font-semibold text-[#2C2C2C] leading-tight">{title}</p>
              <p className="text-[11px] text-[#9A9088] leading-relaxed mt-0.5">{desc}</p>
            </div>
          </motion.div>
        ))}
      </motion.div>

      {/* ══ WARDROBE GRID ════════════════════════════════════════════════════ */}
      <div className="border-t border-[#E5E0D8] pt-7">
        <div className="flex justify-between items-center mb-5">
          <div>
            <h2 className="text-xl font-serif text-[#2C2C2C]">Your Wardrobe</h2>
            <p className="text-[#A8A098] text-xs mt-0.5">{items.length} items analyzed and cataloged</p>
          </div>
          <div className="flex gap-2">
            <button
              onClick={handleRecalculateAll}
              className="bg-gradient-to-r from-[#8B5A5A] to-[#A67676] text-white text-xs px-3 py-1.5 rounded-lg hover:shadow-md transition-all font-medium"
            >
              🔄 Update Scores
            </button>
            <select
              value={filter}
              onChange={e => setFilter(e.target.value)}
              className="bg-white border border-[#E5E0D8] text-xs rounded-lg px-3 py-1.5 text-[#2C2C2C] focus:outline-none focus:ring-1 focus:ring-[#8B5A5A]"
            >
              <option>All Items</option>
              <option>Ethnic Wear</option>
              <option>Formal</option>
              <option>Casual</option>
            </select>
          </div>
        </div>

        <div className="grid grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
          {items.map((item, index) => (
            <ItemCard
              key={item.id || item.filename || index}
              item={{ ...item, image: `http://localhost:5000${item.url}` }}
              index={index}
              onTypeUpdate={handleTypeUpdate}
              onDelete={handleDelete}
            />
          ))}
        </div>

        {items.length === 0 && (
          <div className="text-center py-16">
            <div className="w-14 h-14 rounded-full bg-[#F0EBE4] flex items-center justify-center mx-auto mb-3">
              <span className="text-2xl">👗</span>
            </div>
            <p className="text-[#9A9088] font-serif">Your wardrobe is empty</p>
            <p className="text-[#B0A098] text-sm mt-1">Upload clothing above to get started</p>
          </div>
        )}
      </div>

    </Layout>
  );
}