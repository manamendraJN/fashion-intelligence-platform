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
  LineChart,
  Line,
  Legend,
} from 'recharts';
import { motion } from 'framer-motion';
import { 
  Shirt, Calendar, Target, TrendingUp, RefreshCw, 
  AlertCircle, DollarSign, Sparkles, TrendingDown,
  Sun, Cloud, Snowflake, Leaf, Crown, Zap
} from 'lucide-react';

const COLORS = ['#8B5A5A', '#2C2C2C', '#A8A8A8', '#7A9B8E', '#E8E4DE', '#D4AF37'];

const seasonIcons = {
  spring: Leaf,
  summer: Sun,
  fall: Cloud,
  winter: Snowflake
};

export function AnalyticsPage() {
  const [analytics, setAnalytics] = useState(null);
  const [advancedAnalytics, setAdvancedAnalytics] = useState(null);
  const [styleProfile, setStyleProfile] = useState(null);
  const [forgottenItems, setForgottenItems] = useState(null);
  const [costEfficiency, setCostEfficiency] = useState(null);
  const [wearTimeline, setWearTimeline] = useState(null);
  const [seasonalData, setSeasonalData] = useState(null);
  const [predictions, setPredictions] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    fetchAllAnalytics();
  }, []);

  const fetchAllAnalytics = async () => {
    setLoading(true);
    try {
      // Fetch all analytics in parallel
      const [
        basicRes,
        advancedRes,
        styleRes,
        forgottenRes,
        costRes,
        timelineRes,
        seasonalRes,
        predictionsRes
      ] = await Promise.all([
        fetch('http://localhost:5000/api/analytics').catch(() => null),
        fetch('http://localhost:5000/api/analytics/advanced').catch(() => null),
        fetch('http://localhost:5000/api/analytics/style-profile').catch(() => null),
        fetch('http://localhost:5000/api/analytics/forgotten-items?threshold=90').catch(() => null),
        fetch('http://localhost:5000/api/analytics/cost-efficiency').catch(() => null),
        fetch('http://localhost:5000/api/analytics/wear-timeline?days=90&granularity=weekly').catch(() => null),
        fetch('http://localhost:5000/api/analytics/seasonal').catch(() => null),
        fetch('http://localhost:5000/api/analytics/predictions').catch(() => null),
      ]);

      if (basicRes?.ok) setAnalytics(await basicRes.json());
      if (advancedRes?.ok) setAdvancedAnalytics(await advancedRes.json());
      if (styleRes?.ok) setStyleProfile(await styleRes.json());
      if (forgottenRes?.ok) setForgottenItems(await forgottenRes.json());
      if (costRes?.ok) setCostEfficiency(await costRes.json());
      if (timelineRes?.ok) setWearTimeline(await timelineRes.json());
      if (seasonalRes?.ok) setSeasonalData(await seasonalRes.json());
      if (predictionsRes?.ok) setPredictions(await predictionsRes.json());
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
          <div className="flex items-center gap-3">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#8B5A5A]"></div>
            <div className="text-gray-500">Loading analytics...</div>
          </div>
        </div>
      </Layout>
    );
  }

  const stats = analytics?.stats || {};
  const compositionData = analytics?.charts?.composition || [];
  const coloredCompositionData = compositionData.map((item, index) => ({
    ...item,
    fill: COLORS[index % COLORS.length]
  }));

  return (
    <Layout>
      {/* Header */}
      <div className="mb-8 flex items-start justify-between">
        <div>
          <h1 className="text-4xl font-serif text-[#2C2C2C] mb-2">
            📊 Advanced Analytics
          </h1>
          <p className="text-gray-600">
            AI-powered insights into your style patterns and wardrobe optimization
          </p>
        </div>
        <button
          onClick={fetchAllAnalytics}
          className="flex items-center gap-2 px-4 py-2 bg-[#8B5A5A] text-white rounded-lg hover:bg-[#7A4949] transition-colors"
        >
          <RefreshCw className="w-4 h-4" />
          Refresh All
        </button>
      </div>

      {/* Tab Navigation */}
      <div className="mb-6 flex gap-2 border-b border-gray-200 overflow-x-auto">
        {[
          { id: 'overview', label: '📈 Overview' },
          { id: 'wear-patterns', label: '👔 Wear Patterns' },
          { id: 'style-profile', label: '✨ Style Profile' },
          { id: 'cost-analysis', label: '💰 Cost Analysis' },
        ].map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-3 text-sm font-medium transition-colors border-b-2 whitespace-nowrap ${
              activeTab === tab.id
                ? 'border-[#8B5A5A] text-[#8B5A5A]'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      {activeTab === 'overview' && (
        <OverviewTab 
          stats={stats} 
          compositionData={coloredCompositionData}
          forgottenItems={forgottenItems}
          wearTimeline={wearTimeline}
        />
      )}

      {activeTab === 'wear-patterns' && (
        <WearPatternsTab 
          advancedAnalytics={advancedAnalytics}
          wearTimeline={wearTimeline}
          seasonalData={seasonalData}
          predictions={predictions}
          stats={stats}
        />
      )}

      {activeTab === 'style-profile' && (
        <StyleProfileTab 
          styleProfile={styleProfile}
          advancedAnalytics={advancedAnalytics}
        />
      )}

      {activeTab === 'cost-analysis' && (
        <CostAnalysisTab 
          costEfficiency={costEfficiency}
        />
      )}
    </Layout>
  );
}

// ==================== Overview Tab ====================
function OverviewTab({ stats, compositionData, forgottenItems, wearTimeline }) {
  return (
    <div className="space-y-8">
      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
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

      {/* Forgotten Items Alert */}
      {forgottenItems && forgottenItems.count > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gradient-to-r from-orange-50 to-red-50 p-6 rounded-xl border border-orange-200"
        >
          <div className="flex items-start gap-4">
            <AlertCircle className="w-6 h-6 text-orange-600 flex-shrink-0 mt-1" />
            <div className="flex-1">
              <h3 className="text-lg font-semibold text-orange-900 mb-2">
                🚨 Forgotten Items Alert
              </h3>
              <p className="text-orange-700 mb-4">
                {forgottenItems.message}
              </p>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {forgottenItems.items.slice(0, 8).map(item => (
                  <div key={item.id} className="bg-white p-3 rounded-lg border border-orange-100">
                    <img 
                      src={`http://localhost:5000${item.url}`} 
                      alt={item.filename}
                      className="w-full h-24 object-cover rounded mb-2"
                    />
                    <p className="text-xs text-gray-600 truncate font-medium">{item.type}</p>
                    <p className="text-xs text-orange-600 font-bold">{item.daysSinceWorn} days</p>
                    <p className="text-xs text-gray-500 mt-1 italic">{item.suggestion}</p>
                  </div>
                ))}
              </div>
              {forgottenItems.count > 8 && (
                <p className="text-sm text-orange-600 mt-3 text-center">
                  + {forgottenItems.count - 8} more forgotten items
                </p>
              )}
            </div>
          </div>
        </motion.div>
      )}

      {/* Charts Row */}
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
          
          {compositionData.length > 0 ? (
            <>
              <div className="h-[300px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={compositionData}
                      cx="50%"
                      cy="50%"
                      innerRadius={60}
                      outerRadius={100}
                      paddingAngle={5}
                      dataKey="value"
                    >
                      {compositionData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.fill} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </div>
              <div className="flex flex-wrap justify-center gap-4 mt-4">
                {compositionData.map((entry) => (
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

        {/* Wear Frequency Timeline */}
        {wearTimeline && wearTimeline.timeline && wearTimeline.timeline.length > 0 && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-white p-8 rounded-2xl border border-[#E5E0D8] shadow-sm"
          >
            <h3 className="text-lg font-serif mb-2 text-[#2C2C2C]">
              Wear Frequency (Last 90 Days)
            </h3>
            <p className="text-sm text-gray-500 mb-4">
              Trend: <span className={`font-semibold ${wearTimeline.trend === 'increasing' ? 'text-green-600' : 'text-orange-600'}`}>
                {wearTimeline.trend.toUpperCase()}
              </span>
            </p>
            <div className="h-[250px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={wearTimeline.timeline}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#E5E0D8" />
                  <XAxis 
                    dataKey="date" 
                    tick={{ fontSize: 10 }}
                    angle={-30}
                    textAnchor="end"
                    height={60}
                    tickFormatter={(value) => {
                      try {
                        return new Date(value).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
                      } catch {
                        return value;
                      }
                    }}
                  />
                  <YAxis tick={{ fontSize: 11 }} />
                  <Tooltip />
                  <Line type="monotone" dataKey="wears" stroke="#8B5A5A" strokeWidth={2} dot={{ fill: '#8B5A5A', r: 3 }} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
}

// ==================== Wear Patterns Tab ====================
function WearPatternsTab({ advancedAnalytics, wearTimeline, seasonalData, predictions, stats }) {
  return (
    <div className="space-y-8">
      {/* Most & Least Worn Items */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Most Worn */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="bg-white p-6 rounded-xl border border-[#E5E0D8] shadow-sm"
        >
          <div className="flex items-center gap-2 mb-4">
            <Crown className="w-5 h-5 text-yellow-600" />
            <h3 className="text-lg font-serif text-[#2C2C2C]">Most Worn Items</h3>
          </div>
          <div className="space-y-3 max-h-[450px] overflow-y-auto">
            {advancedAnalytics?.mostWorn?.slice(0, 10).map((item, idx) => (
              <div key={item.id} className="flex items-center gap-3 p-3 bg-green-50 rounded-lg hover:bg-green-100 transition">
                <span className="text-lg font-bold text-gray-400">#{idx + 1}</span>
                <img 
                  src={`http://localhost:5000${item.url}`} 
                  alt={item.filename}
                  className="w-16 h-16 object-cover rounded"
                />
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-sm text-gray-800 truncate">{item.type}</p>
                  <p className="text-xs text-gray-500 capitalize">{item.primaryColor || 'N/A'}</p>
                </div>
                <div className="text-right">
                  <p className="text-lg font-bold text-green-600">{item.wearCount}×</p>
                  <p className="text-xs text-gray-500">wears</p>
                </div>
              </div>
            )) || <p className="text-gray-400 text-sm text-center py-8">No worn items yet</p>}
          </div>
        </motion.div>

        {/* Least Worn */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="bg-white p-6 rounded-xl border border-[#E5E0D8] shadow-sm"
        >
          <div className="flex items-center gap-2 mb-4">
            <TrendingDown className="w-5 h-5 text-orange-600" />
            <h3 className="text-lg font-serif text-[#2C2C2C]">Least Worn Items</h3>
          </div>
          <div className="space-y-3 max-h-[450px] overflow-y-auto">
            {advancedAnalytics?.leastWorn?.slice(0, 10).map((item, idx) => (
              <div key={item.id} className="flex items-center gap-3 p-3 bg-orange-50 rounded-lg hover:bg-orange-100 transition">
                <img 
                  src={`http://localhost:5000${item.url}`} 
                  alt={item.filename}
                  className="w-16 h-16 object-cover rounded"
                />
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-sm text-gray-800 truncate">{item.type}</p>
                  <p className="text-xs text-gray-500 capitalize">{item.primaryColor || 'N/A'}</p>
                </div>
                <div className="text-right">
                  <p className="text-lg font-bold text-orange-600">{item.wearCount}×</p>
                  <p className="text-xs text-gray-500">wears</p>
                </div>
              </div>
            )) || <p className="text-gray-400 text-sm text-center py-8">All items equally worn</p>}
          </div>
        </motion.div>
      </div>

      {/* Event Frequency & Seasonal Analysis */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Event Frequency */}
        {advancedAnalytics?.eventFrequency && advancedAnalytics.eventFrequency.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white p-6 rounded-xl border border-[#E5E0D8] shadow-sm"
          >
            <h3 className="text-lg font-serif mb-4 text-[#2C2C2C]">Event Frequency</h3>
            <p className="text-xs text-gray-500 mb-3">Which events do you attend most?</p>
            <div className="h-[300px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={advancedAnalytics.eventFrequency.slice(0, 8)}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#E5E0D8" />
                  <XAxis dataKey="event" tick={{ fontSize: 10 }} angle={-35} textAnchor="end" height={90} />
                  <YAxis tick={{ fontSize: 11 }} />
                  <Tooltip />
                  <Bar dataKey="count" fill="#7A9B8E" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </motion.div>
        )}

        {/* Season Distribution */}
        {advancedAnalytics?.seasonDistribution && advancedAnalytics.seasonDistribution.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white p-6 rounded-xl border border-[#E5E0D8] shadow-sm"
          >
            <h3 className="text-lg font-serif mb-4 text-[#2C2C2C]">Seasonal Distribution</h3>
            <div className="space-y-4">
              {advancedAnalytics.seasonDistribution.map((season) => {
                const IconComponent = seasonIcons[season.season?.toLowerCase()] || Sun;
                const percentage = ((season.count / stats.totalItems) * 100).toFixed(0);
                return (
                  <div key={season.season} className="flex items-center gap-3">
                    <IconComponent className="w-5 h-5 text-[#8B5A5A]" />
                    <div className="flex-1">
                      <div className="flex justify-between mb-1">
                        <span className="text-sm font-medium text-gray-700 capitalize">{season.season}</span>
                        <span className="text-sm text-gray-500">{season.count} items ({percentage}%)</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-[#8B5A5A] h-2 rounded-full" 
                          style={{ width: `${percentage}%` }}
                        ></div>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </motion.div>
        )}
      </div>

      {/* LSTM Predictions */}
      {predictions && predictions.predictions && predictions.predictions.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gradient-to-br from-purple-50 to-blue-50 p-6 rounded-xl border border-purple-200"
        >
          <div className="flex items-center gap-2 mb-4">
            <Zap className="w-5 h-5 text-purple-600" />
            <h3 className="text-lg font-serif text-[#2C2C2C]">🤖 AI Predictions: Items You'll Likely Wear Next</h3>
          </div>
          <p className="text-sm text-gray-600 mb-4">Based on LSTM temporal pattern analysis of your wear history</p>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            {predictions.predictions.slice(0, 10).map((pred) => (
              <div key={pred.item.id} className="bg-white p-3 rounded-lg border border-purple-100 hover:shadow-md transition">
                <img 
                  src={`http://localhost:5000${pred.item.url}`} 
                  alt={pred.item.filename}
                  className="w-full h-24 object-cover rounded mb-2"
                />
                <p className="text-xs text-gray-700 truncate font-medium">{pred.item.type}</p>
                <p className="text-xs text-purple-600 font-semibold">Score: {pred.score}</p>
              </div>
            ))}
          </div>
        </motion.div>
      )}
    </div>
  );
}

// ==================== Style Profile Tab ====================
function StyleProfileTab({ styleProfile, advancedAnalytics }) {
  if (!styleProfile) {
    return (
      <div className="text-center py-12 text-gray-500">
        Loading style profile...
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Style Personality Card */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gradient-to-br from-[#8B5A5A] to-[#7A4949] p-8 rounded-2xl text-white shadow-lg"
      >
        <div className="flex items-start justify-between">
          <div>
            <h2 className="text-3xl font-serif mb-2">Your Style Personality</h2>
            <p className="text-2xl font-medium opacity-90 capitalize">
              {styleProfile.dominantStyle?.replace('-', ' ') || 'Discovering...'}
            </p>
            <p className="text-sm opacity-75 mt-2">
              Based on {styleProfile.totalAnalyzedWears} analyzed wears
            </p>
          </div>
          <Sparkles className="w-12 h-12 opacity-50" />
        </div>

        {/* Style Scores */}
        <div className="grid grid-cols-3 gap-4 mt-6">
          <div className="bg-white/10 backdrop-blur p-4 rounded-lg">
            <p className="text-sm opacity-75 mb-1">Classic</p>
            <p className="text-2xl font-bold">{styleProfile.stylePersonality?.classicScore || 0}%</p>
          </div>
          <div className="bg-white/10 backdrop-blur p-4 rounded-lg">
            <p className="text-sm opacity-75 mb-1">Adventurous</p>
            <p className="text-2xl font-bold">{styleProfile.stylePersonality?.adventurousScore || 0}%</p>
          </div>
          <div className="bg-white/10 backdrop-blur p-4 rounded-lg">
            <p className="text-sm opacity-75 mb-1">Confidence</p>
            <p className="text-2xl font-bold">{styleProfile.styleConfidenceScore || 0}</p>
          </div>
        </div>

        {/* Insights */}
        {styleProfile.insights && styleProfile.insights.length > 0 && (
          <div className="mt-6 space-y-2">
            {styleProfile.insights.map((insight, idx) => (
              <p key={idx} className="text-sm opacity-90">✨ {insight}</p>
            ))}
          </div>
        )}
      </motion.div>

      {/* Color Palette & Preferences */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Color Palette */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="bg-white p-6 rounded-xl border border-[#E5E0D8] shadow-sm"
        >
          <h3 className="text-lg font-serif mb-4 text-[#2C2C2C]">🎨 Your Color Palette</h3>
          <p className="text-sm text-gray-500 mb-4">
            Favorite: <span className="font-semibold text-[#8B5A5A] capitalize">
              {styleProfile.colorPalette?.favoriteColor || 'Unknown'}
            </span>
          </p>
          
          {styleProfile.colorPalette?.topColors && styleProfile.colorPalette.topColors.length > 0 ? (
            <div className="space-y-3">
              {styleProfile.colorPalette.topColors.map((colorData) => (
                <div key={colorData.color} className="flex items-center gap-3">
                  <div 
                    className="w-10 h-10 rounded-full border-2 border-gray-300 flex-shrink-0"
                    style={{ 
                      backgroundColor: colorData.color.toLowerCase(),
                      border: colorData.color.toLowerCase() === 'white' ? '2px solid #ccc' : 'none'
                    }}
                  ></div>
                  <div className="flex-1">
                    <div className="flex justify-between mb-1">
                      <span className="text-sm font-medium text-gray-700 capitalize">{colorData.color}</span>
                      <span className="text-sm text-gray-500">{colorData.percentage}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-[#8B5A5A] h-2 rounded-full" 
                        style={{ width: `${colorData.percentage}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-400 text-sm text-center py-8">No color data available yet</p>
          )}
        </motion.div>

        {/* Wear Preferences */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="bg-white p-6 rounded-xl border border-[#E5E0D8] shadow-sm"
        >
          <h3 className="text-lg font-serif mb-4 text-[#2C2C2C]">👗 Wear Preferences</h3>
          
          {styleProfile.wearPreference && Object.keys(styleProfile.wearPreference).length > 0 ? (
            <div className="space-y-3">
              {Object.entries(styleProfile.wearPreference)
                .sort((a, b) => b[1] - a[1])
                .map(([category, percentage]) => (
                  <div key={category} className="flex items-center gap-3">
                    <div className="flex-1">
                      <div className="flex justify-between mb-1">
                        <span className="text-sm font-medium text-gray-700 capitalize">{category}</span>
                        <span className="text-sm text-gray-500 font-semibold">{percentage}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-[#8B5A5A] h-2 rounded-full" 
                          style={{ width: `${percentage}%` }}
                        ></div>
                      </div>
                    </div>
                  </div>
                ))}
            </div>
          ) : (
            <p className="text-gray-400 text-sm text-center py-8">Start wearing items to see preferences</p>
          )}
        </motion.div>
      </div>

      {/* Event Frequency Bar Chart */}
      {advancedAnalytics?.eventFrequency && advancedAnalytics.eventFrequency.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white p-6 rounded-xl border border-[#E5E0D8] shadow-sm"
        >
          <h3 className="text-lg font-serif mb-4 text-[#2C2C2C]">📅 Event Attendance Patterns</h3>
          <p className="text-sm text-gray-500 mb-4">Track which events you attend most frequently</p>
          <div className="h-[320px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={advancedAnalytics.eventFrequency.slice(0, 10)}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E5E0D8" />
                <XAxis dataKey="event" tick={{ fontSize: 10 }} angle={-30} textAnchor="end" height={100} />
                <YAxis tick={{ fontSize: 11 }} />
                <Tooltip />
                <Bar dataKey="count" fill="#7A9B8E" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </motion.div>
      )}

      {/* Category Breakdown */}
      {styleProfile?.categoryBreakdown && Object.keys(styleProfile.categoryBreakdown).length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white p-6 rounded-xl border border-[#E5E0D8] shadow-sm"
        >
          <h3 className="text-lg font-serif mb-4 text-[#2C2C2C]">Category Breakdown</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {Object.entries(styleProfile.categoryBreakdown)
              .sort((a, b) => b[1] - a[1])
              .slice(0, 8)
              .map(([category, percentage]) => (
                <div key={category} className="text-center p-4 bg-gradient-to-br from-gray-50 to-gray-100 rounded-lg border border-gray-200">
                  <p className="text-3xl font-bold text-[#8B5A5A]">{percentage}%</p>
                  <p className="text-xs text-gray-600 mt-1 capitalize">{category}</p>
                </div>
              ))}
          </div>
        </motion.div>
      )}
    </div>
  );
}

// ==================== Cost Analysis Tab ====================
function CostAnalysisTab({ costEfficiency }) {
  if (!costEfficiency || !costEfficiency.items || costEfficiency.items.length === 0) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white p-12 rounded-xl border border-[#E5E0D8] shadow-sm text-center"
      >
        <DollarSign className="w-16 h-16 text-gray-300 mx-auto mb-4" />
        <h3 className="text-xl font-serif text-gray-600 mb-2">No Purchase Data Yet</h3>
        <p className="text-gray-500 text-sm mb-4">
          Add purchase prices to your items to see cost per wear analysis
        </p>
        <p className="text-xs text-gray-400">
          Cost per wear helps you understand the true value of your wardrobe investments
        </p>
      </motion.div>
    );
  }

  // Calculate summary stats
  const avgCostPerWear = costEfficiency.items.reduce((sum, item) => sum + item.costPerWear, 0) / costEfficiency.items.length;
  const totalSpent = costEfficiency.items.reduce((sum, item) => sum + item.purchasePrice, 0);
  const totalWears = costEfficiency.items.reduce((sum, item) => sum + item.wearCount, 0);
  const bestValue = costEfficiency.items[0]; // Already sorted by cost per wear

  return (
    <div className="space-y-8">
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white p-6 rounded-xl border border-[#E5E0D8] shadow-sm"
        >
          <div className="flex items-center gap-3 mb-2">
            <DollarSign className="w-5 h-5 text-[#8B5A5A]" />
            <p className="text-xs text-gray-500 uppercase tracking-wider">Total Tracked</p>
          </div>
          <p className="text-3xl font-serif font-bold text-[#2C2C2C]">
            ${totalSpent.toFixed(2)}
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white p-6 rounded-xl border border-[#E5E0D8] shadow-sm"
        >
          <div className="flex items-center gap-3 mb-2">
            <Target className="w-5 h-5 text-[#7A9B8E]" />
            <p className="text-xs text-gray-500 uppercase tracking-wider">Avg Cost/Wear</p>
          </div>
          <p className="text-3xl font-serif font-bold text-[#7A9B8E]">
            ${avgCostPerWear.toFixed(2)}
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white p-6 rounded-xl border border-[#E5E0D8] shadow-sm"
        >
          <div className="flex items-center gap-3 mb-2">
            <Crown className="w-5 h-5 text-yellow-600" />
            <p className="text-xs text-gray-500 uppercase tracking-wider">Best Value</p>
          </div>
          <p className="text-lg font-medium text-[#2C2C2C] truncate">
            {bestValue?.type || 'N/A'}
          </p>
          <p className="text-sm text-green-600 font-semibold">
            ${bestValue?.costPerWear.toFixed(2) || 0}/wear
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-white p-6 rounded-xl border border-[#E5E0D8] shadow-sm"
        >
          <div className="flex items-center gap-3 mb-2">
            <Calendar className="w-5 h-5 text-purple-600" />
            <p className="text-xs text-gray-500 uppercase tracking-wider">Total Wears</p>
          </div>
          <p className="text-3xl font-serif font-bold text-purple-600">
            {totalWears}
          </p>
        </motion.div>
      </div>

      {/* Cost Efficiency Table */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white p-6 rounded-xl border border-[#E5E0D8] shadow-sm"
      >
        <h3 className="text-lg font-serif mb-4 text-[#2C2C2C]">💎 Cost Per Wear Analysis</h3>
        <p className="text-sm text-gray-500 mb-4">Items ranked by best value (lower cost per wear = better value)</p>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b-2 border-gray-200 bg-gray-50">
                <th className="text-left py-3 px-4 font-semibold text-gray-700">Rank</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-700">Item</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-700">Type</th>
                <th className="text-right py-3 px-4 font-semibold text-gray-700">Purchase</th>
                <th className="text-center py-3 px-4 font-semibold text-gray-700">Wears</th>
                <th className="text-right py-3 px-4 font-semibold text-gray-700">Cost/Wear</th>
                <th className="text-center py-3 px-4 font-semibold text-gray-700">Rating</th>
              </tr>
            </thead>
            <tbody>
              {costEfficiency.items.slice(0, 20).map((item, idx) => (
                <tr key={item.id} className={`border-b border-gray-100 hover:bg-gray-50 transition ${idx < 3 ? 'bg-green-50' : ''}`}>
                  <td className="py-3 px-4 text-center">
                    {idx < 3 ? (
                      <span className="text-xl">{idx === 0 ? '🥇' : idx === 1 ? '🥈' : '🥉'}</span>
                    ) : (
                      <span className="text-gray-400 font-medium">#{idx + 1}</span>
                    )}
                  </td>
                  <td className="py-3 px-4">
                    <img 
                      src={`http://localhost:5000${item.url}`} 
                      alt={item.filename}
                      className="w-14 h-14 object-cover rounded"
                    />
                  </td>
                  <td className="py-3 px-4 text-gray-700 font-medium">{item.type}</td>
                  <td className="py-3 px-4 text-right font-medium text-gray-600">${item.purchasePrice.toFixed(2)}</td>
                  <td className="py-3 px-4 text-center text-[#8B5A5A] font-bold">{item.wearCount}×</td>
                  <td className="py-3 px-4 text-right font-bold text-green-600 text-lg">
                    ${item.costPerWear.toFixed(2)}
                  </td>
                  <td className="py-3 px-4 text-center">
                    <span className={`text-xs px-2 py-1 rounded-full font-medium ${
                      item.valueRating === 'Excellent Value' ? 'bg-green-100 text-green-700' :
                      item.valueRating === 'Good Value' ? 'bg-blue-100 text-blue-700' :
                      item.valueRating === 'Fair Value' ? 'bg-yellow-100 text-yellow-700' :
                      'bg-orange-100 text-orange-700'
                    }`}>
                      {item.valueRating}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </motion.div>

      {/* Color Distribution */}
      {advancedAnalytics?.colorDistribution && advancedAnalytics.colorDistribution.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white p-6 rounded-xl border border-[#E5E0D8] shadow-sm"
        >
          <h3 className="text-lg font-serif mb-4 text-[#2C2C2C]">🌈 Color Distribution</h3>
          <div className="flex flex-wrap gap-3">
            {advancedAnalytics.colorDistribution.slice(0, 15).map((colorData) => (
              <div 
                key={colorData.color} 
                className="flex items-center gap-2 px-4 py-2 bg-gray-50 rounded-full border border-gray-200 hover:shadow-md transition"
              >
                <div 
                  className="w-6 h-6 rounded-full border border-gray-300"
                  style={{ 
                    backgroundColor: colorData.color.toLowerCase(),
                    border: colorData.color.toLowerCase() === 'white' ? '2px solid #ccc' : 'none'
                  }}
                ></div>
                <span className="text-sm font-medium text-gray-700 capitalize">{colorData.color}</span>
                <span className="text-xs text-gray-500 font-bold bg-white px-2 py-1 rounded">×{colorData.count}</span>
              </div>
            ))}
          </div>
        </motion.div>
      )}
    </div>
  );
}
