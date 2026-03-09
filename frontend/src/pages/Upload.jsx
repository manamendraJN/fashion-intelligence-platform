import React, { useEffect, useState } from 'react';
import { Layout } from '../components/Layout';
import { WardrobeUpload } from '../components/WardrobeUpload';
import { ItemCard } from '../components/ItemCard';
import { motion } from 'framer-motion';
import { Sparkles } from 'lucide-react';

export function UploadPage() {
  const [items, setItems] = useState([]);
  const [showNewItems, setShowNewItems] = useState(false);

  // Load wardrobe from backend
  const fetchWardrobe = () => {
    fetch('http://localhost:5000/api/wardrobe')
      .then(res => res.json())
      .then(data => {
        // Ensure data is an array (handle error responses)
        if (Array.isArray(data)) {
          setItems(data);
        } else if (data && data.items && Array.isArray(data.items)) {
          setItems(data.items);
        } else {
          console.error('Invalid data format:', data);
          setItems([]);
        }
      })
      .catch(err => {
        console.error('Failed to load wardrobe:', err);
        setItems([]);
      });
  };

  useEffect(() => {
    fetchWardrobe();
  }, []);

  // After uploading, reload wardrobe
  const handleUploadComplete = () => {
    setShowNewItems(true);
    fetchWardrobe();
    setTimeout(() => setShowNewItems(false), 2000);
  };

  // Handle clothing type update
  const handleTypeUpdate = (itemId, newType, newEventScores) => {
    setItems(prevItems => 
      prevItems.map(item => 
        item.id === itemId 
          ? { ...item, type: newType, eventScores: newEventScores }
          : item
      )
    );
  };

  // Handle item deletion
  const handleDelete = (itemId) => {
    setItems(prevItems => prevItems.filter(item => item.id !== itemId));
  };

  // Handle recalculating all event scores
  const handleRecalculateAll = async () => {
    if (!confirm('Recalculate event scores for all items using updated rules? This will update office scores for shirts, blazers, trousers, etc.')) {
      return;
    }

    try {
      const response = await fetch('http://localhost:5000/api/wardrobe/recalculate-all', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });

      const data = await response.json();
      
      if (data.success) {
        alert(`✅ ${data.message}`);
        fetchWardrobe(); // Reload items with new scores
      } else {
        alert('❌ Failed to recalculate scores');
      }
    } catch (error) {
      console.error('Recalculate error:', error);
      alert('❌ Error recalculating scores');
    }
  };

  return (
    <Layout>
      <div className="max-w-4xl mx-auto mb-16 text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <span className="inline-flex items-center px-3 py-1 rounded-full bg-[#E8E4DE] text-[#8B5A5A] text-xs font-medium tracking-wide uppercase mb-4">
            <Sparkles className="w-3 h-3 mr-1.5" />
            Wardrobe Fashion AI System
          </span>
          <h1 className="text-4xl md:text-5xl font-serif font-medium text-[#2C2C2C] mb-6 leading-tight">
            Digitize your wardrobe.
            <br />
            <span className="text-[#8B5A5A] italic">Unlock your AURA.</span>
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto mb-10 leading-relaxed">
            Upload your clothing items to let our dual-phase AI learn your
            preferences. We analyze visual features instantly, then learn your
            personal style over time.
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          <WardrobeUpload onUploadComplete={handleUploadComplete} />
        </motion.div>
      </div>

      <div className="border-t border-[#E5E0D8] pt-12">
        <div className="flex justify-between items-end mb-8">
          <div>
            <h2 className="text-2xl font-serif text-[#2C2C2C]">
              Your Wardrobe
            </h2>
            <p className="text-gray-500 mt-1">
              {items.length} items analyzed and cataloged
            </p>
          </div>
          <div className="flex gap-2">
            <button
              onClick={handleRecalculateAll}
              className="bg-gradient-to-r from-[#8B5A5A] to-[#A67676] text-white text-sm px-4 py-2 rounded-lg hover:shadow-md transition-all font-medium"
              title="Update all items with latest event scoring rules"
            >
              🔄 Update Scores
            </button>
            <select className="bg-white border border-[#E5E0D8] text-sm rounded-lg px-3 py-2 text-[#2C2C2C] focus:outline-none focus:ring-1 focus:ring-[#8B5A5A]">
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
              item={{
                ...item,
                image: `http://localhost:5000${item.url}`
              }}
              index={index}
              onTypeUpdate={handleTypeUpdate}
              onDelete={handleDelete}
            />
          ))}
        </div>

        {items.length === 0 && (
          <div className="text-center py-20">
            <p className="text-gray-400 text-lg">
              No items in your wardrobe yet. Upload some clothing to get started!
            </p>
          </div>
        )}
      </div>
    </Layout>
  );
}
