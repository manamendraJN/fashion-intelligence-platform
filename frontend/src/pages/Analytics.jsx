import React from 'react';
import { Layout } from '../components/Layout';
import { ANALYTICS_DATA } from '../data/mockData';
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
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  LineChart,
  Line,
} from 'recharts';
import { motion } from 'framer-motion';
import { Shirt, Calendar, Target, TrendingUp } from 'lucide-react';

export function AnalyticsPage() {
  return (
    <Layout>
      <div className="mb-10">
        <h1 className="text-3xl font-serif text-[#2C2C2C] mb-2">Wardrobe Analytics</h1>
        <p className="text-gray-600">Insights into your style patterns and AI learning progress.</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-10">
        {[
          { label: 'Total Items', value: '42', icon: Shirt, color: 'bg-[#8B5A5A]' },
          { label: 'Events Covered', value: '12', icon: Target, color: 'bg-[#2C2C2C]' },
          { label: 'Avg. Wear/Item', value: '4.5', icon: Calendar, color: 'bg-[#7A9B8E]' },
          { label: 'AI Accuracy', value: '88%', icon: TrendingUp, color: 'bg-[#A8A8A8]' },
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
              <p className="text-xs text-gray-500 uppercase tracking-wider">{stat.label}</p>
              <p className="text-2xl font-serif font-medium text-[#2C2C2C]">{stat.value}</p>
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
          <h3 className="text-lg font-serif mb-6 text-[#2C2C2C]">Wardrobe Composition</h3>
          <div className="h-[300px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={ANALYTICS_DATA.composition}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {ANALYTICS_DATA.composition.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.fill} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="flex justify-center gap-6 mt-4">
            {ANALYTICS_DATA.composition.map((entry) => (
              <div key={entry.name} className="flex items-center text-xs text-gray-500">
                <span
                  className="w-3 h-3 rounded-full mr-2"
                  style={{ backgroundColor: entry.fill }}
                />
                {entry.name}
              </div>
            ))}
          </div>
        </motion.div>

        {/* Wear Frequency */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.1 }}
          className="bg-white p-8 rounded-2xl border border-[#E5E0D8] shadow-sm"
        >
          <h3 className="text-lg font-serif mb-6 text-[#2C2C2C]">Most Worn Items</h3>
          <div className="h-[300px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={ANALYTICS_DATA.wearFrequency} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#E5E0D8" />
                <XAxis type="number" hide />
                <YAxis dataKey="name" type="category" width={100} tick={{ fontSize: 12 }} />
                <Tooltip cursor={{ fill: '#FAF8F5' }} />
                <Bar dataKey="count" fill="#2C2C2C" radius={[0, 4, 4, 0]} barSize={20} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        {/* Event Coverage */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
          className="bg-white p-8 rounded-2xl border border-[#E5E0D8] shadow-sm"
        >
          <h3 className="text-lg font-serif mb-6 text-[#2C2C2C]">Event Suitability Coverage</h3>
          <div className="h-[300px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart cx="50%" cy="50%" outerRadius="80%" data={ANALYTICS_DATA.eventCoverage}>
                <PolarGrid stroke="#E5E0D8" />
                <PolarAngleAxis dataKey="subject" tick={{ fontSize: 12, fill: '#6B6B6B' }} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                <Radar
                  name="Coverage"
                  dataKey="A"
                  stroke="#8B5A5A"
                  strokeWidth={2}
                  fill="#8B5A5A"
                  fillOpacity={0.2}
                />
                <Tooltip />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        {/* Learning Progress */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3 }}
          className="bg-white p-8 rounded-2xl border border-[#E5E0D8] shadow-sm"
        >
          <h3 className="text-lg font-serif mb-6 text-[#2C2C2C]">AI Learning Curve</h3>
          <div className="h-[300px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={ANALYTICS_DATA.learningProgress}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E0D8" />
                <XAxis dataKey="month" tick={{ fontSize: 12 }} axisLine={false} tickLine={false} />
                <YAxis
                  domain={[0, 100]}
                  tick={{ fontSize: 12 }}
                  axisLine={false}
                  tickLine={false}
                />
                <Tooltip />
                <Line
                  type="monotone"
                  dataKey="accuracy"
                  stroke="#2C2C2C"
                  strokeWidth={3}
                  dot={{ fill: '#2C2C2C', strokeWidth: 2 }}
                  activeDot={{ r: 8 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
          <p className="text-xs text-center text-gray-500 mt-4">
            Accuracy improves as you accept/reject recommendations
          </p>
        </motion.div>
      </div>
    </Layout>
  );
}
