import React, { useEffect, useState } from 'react';
import { Layout } from '../components/Layout';
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
} from 'recharts';
import { motion } from 'framer-motion';
import { Shirt, Calendar, Target, TrendingUp, RefreshCw } from 'lucide-react';

const COLORS = ['#8B5A5A', '#2C2C2C', '#A8A8A8', '#7A9B8E', '#E8E4DE', '#D4AF37'];

export function AnalyticsPage() {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/analytics');
      const data = await response.json();
      setAnalytics(data);
    } catch (error) {
      console.error('Failed to fetch analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-64">
          <div className="text-gray-500">Loading analytics...</div>
        </div>
      </Layout>
    );
  }

  const stats = analytics?.stats || {};
  const compositionData = analytics?.charts?.composition || [];

  // Add colors to composition data
  const coloredCompositionData = compositionData.map((item, index) => ({
    ...item,
    fill: COLORS[index % COLORS.length]
  }));

  return (
    <Layout>
      <div className="mb-10 flex items-start justify-between">
        <div>
          <h1 className="text-3xl font-serif text-[#2C2C2C] mb-2">
            Wardrobe Analytics
          </h1>
          <p className="text-gray-600">
            Insights into your style patterns and AI learning progress.
          </p>
        </div>
        <button
          onClick={fetchAnalytics}
          className="flex items-center gap-2 px-4 py-2 bg-[#8B5A5A] text-white rounded-lg hover:bg-[#7A4949] transition-colors"
        >
          <RefreshCw className="w-4 h-4" />
          Refresh
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-10">
        {[
          { label: 'Total Items', value: stats.totalItems || 0, icon: Shirt, color: 'bg-[#8B5A5A]' },
          { label: 'Events Covered', value: `${stats.eventsCovered || 0}/${stats.totalEvents || 7}`, icon: Target, color: 'bg-[#2C2C2C]' },
          { label: 'Avg. Wear/Item', value: (stats.avgWearCount || 0).toFixed(1), icon: Calendar, color: 'bg-[#7A9B8E]' },
          { label: 'Unworn Items', value: stats.unwornItems || 0, icon: TrendingUp, color: 'bg-[#A8A8A8]' }
        ].map((stat, i) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
            className="bg-white p-6 rounded-xl border border-[#E5E0D8] shadow-sm flex items-center space-x-4"
          >
            <div className={`p-3 rounded-full ${stat.color} text-white`}>
              <stat.icon className="w-5 h-5" />
            </div>
            <div>
              <p className="text-xs text-gray-500 uppercase tracking-wider">
                {stat.label}
              </p>
              <p className="text-2xl font-serif font-medium text-[#2C2C2C]">
                {stat.value}
              </p>
            </div>
          </motion.div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Composition Chart */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="bg-white p-8 rounded-2xl border border-[#E5E0D8] shadow-sm"
        >
          <h3 className="text-lg font-serif mb-6 text-[#2C2C2C]">
            Wardrobe Composition
          </h3>
          
          {coloredCompositionData.length > 0 ? (
            <>
              <div className="h-[300px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={coloredCompositionData}
                      cx="50%"
                      cy="50%"
                      innerRadius={60}
                      outerRadius={100}
                      paddingAngle={5}
                      dataKey="value"
                    >
                      {coloredCompositionData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.fill} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </div>
              <div className="flex flex-wrap justify-center gap-4 mt-4">
                {coloredCompositionData.map((entry) => (
                  <div key={entry.name} className="flex items-center text-xs text-gray-500">
                    <span
                      className="w-3 h-3 rounded-full mr-2"
                      style={{ backgroundColor: entry.fill }}
                    ></span>
                    {entry.name} ({entry.value})
                  </div>
                ))}
              </div>
            </>
          ) : (
            <div className="h-[300px] flex items-center justify-center text-gray-400">
              No wardrobe data yet. Upload some items to see composition.
            </div>
          )}
        </motion.div>

        {/* Summary Card */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.1 }}
          className="bg-white p-8 rounded-2xl border border-[#E5E0D8] shadow-sm"
        >
          <h3 className="text-lg font-serif mb-6 text-[#2C2C2C]">
            Wardrobe Summary
          </h3>
          <div className="space-y-6">
            <div className="border-b border-[#E5E0D8] pb-4">
              <p className="text-sm text-gray-500 mb-2">Total Collection</p>
              <p className="text-4xl font-serif font-medium text-[#2C2C2C]">
                {stats.totalItems || 0} <span className="text-lg text-gray-400">items</span>
              </p>
            </div>
            
            <div className="border-b border-[#E5E0D8] pb-4">
              <p className="text-sm text-gray-500 mb-2">Usage Statistics</p>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Average Wear per Item</span>
                  <span className="font-semibold text-[#8B5A5A]">
                    {(stats.avgWearCount || 0).toFixed(1)}×
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Unworn Items</span>
                  <span className="font-semibold text-orange-500">
                    {stats.unwornItems || 0}
                  </span>
                </div>
              </div>
            </div>

            <div>
              <p className="text-sm text-gray-500 mb-2">Recommendations</p>
              <div className="space-y-2">
                {stats.unwornItems > 0 && (
                  <div className="p-3 bg-orange-50 rounded-lg border border-orange-200">
                    <p className="text-xs text-orange-700">
                      💡 You have {stats.unwornItems} unworn item{stats.unwornItems !== 1 ? 's' : ''}. 
                      Try incorporating them into your outfits!
                    </p>
                  </div>
                )}
                {stats.totalItems < 10 && (
                  <div className="p-3 bg-blue-50 rounded-lg border border-blue-200">
                    <p className="text-xs text-blue-700">
                      📸 Upload more items to get better recommendations!
                    </p>
                  </div>
                )}
                {stats.totalItems >= 20 && (
                  <div className="p-3 bg-green-50 rounded-lg border border-green-200">
                    <p className="text-xs text-green-700">
                      ✨ Great wardrobe! You have enough variety for all occasions.
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </Layout>
  );
}
