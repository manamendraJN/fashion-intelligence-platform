import React, { useState } from 'react';
import { Layout } from '../components/Layout';
import { WardrobeUpload } from '../components/WardrobeUpload';
import { ItemCard } from '../components/ItemCard';
import { INITIAL_WARDROBE } from '../data/mockData';
import { motion } from 'framer-motion';
import { Sparkles } from 'lucide-react';

export function UploadPage() {
  const [items, setItems] = useState(INITIAL_WARDROBE);
  const [showNewItems, setShowNewItems] = useState(false);

  const handleUploadComplete = () => {
    setShowNewItems(true);
    setTimeout(() => setShowNewItems(false), 2000);
  };

  return (
    <Layout>
      <div className="max-w-4xl mx-auto mb-16 text-center">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}>
          <span className="inline-flex items-center px-3 py-1 rounded-full bg-[#E8E4DE] text-[#8B5A5A] text-xs font-medium tracking-wide uppercase mb-4">
            <Sparkles className="w-3 h-3 mr-1.5" />
            AI-Powered Style Assistant
          </span>
          <h1 className="text-4xl md:text-5xl font-serif font-medium text-[#2C2C2C] mb-6 leading-tight">
            Digitize your wardrobe.
            <br />
            <span className="text-[#8B5A5A] italic">Unlock your style.</span>
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto mb-10 leading-relaxed">
            Upload your clothing items to let our dual-phase AI learn your preferences. We analyze visual features instantly, then learn your personal style over time.
          </p>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6, delay: 0.2 }}>
          <WardrobeUpload onUploadComplete={handleUploadComplete} />
        </motion.div>
      </div>

      <div className="border-t border-[#E5E0D8] pt-12">
        <div className="flex justify-between items-end mb-8">
          <div>
            <h2 className="text-2xl font-serif text-[#2C2C2C]">Your Wardrobe</h2>
            <p className="text-gray-500 mt-1">{items.length} items analyzed and cataloged</p>
          </div>
          <div className="flex gap-2">
            <select className="bg-white border border-[#E5E0D8] text-sm rounded-lg px-3 py-2 text-[#2C2C2C] focus:outline-none focus:ring-1 focus:ring-[#8B5A5A]">
              <option>All Items</option>
              <option>Ethnic Wear</option>
              <option>Formal</option>
              <option>Casual</option>
            </select>
          </div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {items.map((item, index) => (
            <ItemCard key={item.id} item={item} index={index} />
          ))}
        </div>
      </div>
    </Layout>
  );
}
