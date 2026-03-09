import React from 'react';
import { motion } from 'framer-motion';
import { Tag, Calendar } from 'lucide-react';

export function ItemCard({ item, index = 0 }) {
  const topEvent = Object.entries(item.eventScores).reduce((a, b) =>
    a[1] > b[1] ? a : b
  );

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: index * 0.1 }}
      className="group relative bg-white rounded-xl overflow-hidden shadow-sm hover:shadow-md transition-shadow duration-300 border border-[#E5E0D8]"
    >
      <div className="aspect-[3/4] overflow-hidden bg-gray-100">
        <img
          src={item.image}
          alt={`${item.color} ${item.articleType}`}
          className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
        />
        <div className="absolute top-3 right-3 bg-white/90 backdrop-blur-sm px-2 py-1 rounded-full text-xs font-medium text-[#2C2C2C] border border-gray-100">
          {item.usage}
        </div>
      </div>

      <div className="p-4">
        <div className="flex justify-between items-start mb-2">
          <div>
            <h3 className="font-serif text-lg font-medium text-[#2C2C2C]">
              {item.color} {item.articleType}
            </h3>
            <p className="text-xs text-gray-500 uppercase tracking-wider mt-0.5">
              ID: #{item.id}
            </p>
          </div>
        </div>

        <div className="space-y-2 mt-3">
          <div className="flex items-center text-sm text-gray-600">
            <Tag className="h-3.5 w-3.5 mr-2 text-[#8B5A5A]" />
            <span>
              Best for: <span className="font-medium text-[#2C2C2C]">{topEvent[0]}</span>
            </span>
            <span className="ml-auto text-xs font-medium bg-[#FAF8F5] px-1.5 py-0.5 rounded text-[#8B5A5A]">
              {Math.round(topEvent[1] * 100)}%
            </span>
          </div>

          {item.lastWorn && (
            <div className="flex items-center text-xs text-gray-500">
              <Calendar className="h-3.5 w-3.5 mr-2" />
              <span>Last worn: {item.lastWorn}</span>
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
}
