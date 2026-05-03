import { useState, useEffect } from 'react';
import { Layout } from '../components/Layout';
import { motion } from 'framer-motion';
import { 
  DollarSign, TrendingUp, Brain, Calendar, 
  ShoppingBag, AlertCircle, Award, Palette,
  TrendingDown, RefreshCw, Sparkles, Target
} from 'lucide-react';

const API_BASE_URL = 'http://localhost:5000';

export default function AdvancedAnalytics() {
  const [analytics, setAnalytics] = useState(null);
  const [styleProfile, setStyleProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    fetchAnalyticsData();
  }, []);

  const fetchAnalyticsData = async () => {
    try {
      setLoading(true);
      
      // Fetch comprehensive analytics
      const analyticsRes = await fetch(`${API_BASE_URL}/api/analytics/advanced`);
      const analyticsData = await analyticsRes.json();
      
      // Fetch style profile
      const profileRes = await fetch(`${API_BASE_URL}/api/style/profile`);
      const profileData = await profileRes.json();
      
      setAnalytics(analyticsData.analytics);
      setStyleProfile(profileData.styleProfile);
    } catch (error) {
      console.error('Error fetching analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading Analytics...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">📊 Advanced Analytics Dashboard</h1>
          <p className="text-gray-600">AI-powered insights into your wardrobe</p>
        </div>
        <button 
          onClick={fetchAnalyticsData}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          Refresh
        </button>
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="style">Style Profile</TabsTrigger>
          <TabsTrigger value="cost">Cost Analysis</TabsTrigger>
          <TabsTrigger value="patterns">Wear Patterns</TabsTrigger>
          <TabsTrigger value="insights">Insights</TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-6">
          {/* Key Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <Card>
              <CardHeader className="pb-2">
                <CardDescription>Total Value</CardDescription>
                <CardTitle className="text-2xl">
                  ${analytics?.wearPatterns?.totalValue?.toFixed(2) || 0}
                </CardTitle>
              </CardHeader>
            </Card>
            
            <Card>
              <CardHeader className="pb-2">
                <CardDescription>Avg Cost/Wear</CardDescription>
                <CardTitle className="text-2xl">
                  ${analytics?.wearPatterns?.averageCostPerWear?.toFixed(2) || 0}
                </CardTitle>
              </CardHeader>
            </Card>
            
            <Card>
              <CardHeader className="pb-2">
                <CardDescription>Style Confidence</CardDescription>
                <CardTitle className="text-2xl">
                  {styleProfile?.styleConfidence?.score || 0}/100
                </CardTitle>
              </CardHeader>
            </Card>
            
            <Card>
              <CardHeader className="pb-2">
                <CardDescription>Forgotten Items</CardDescription>
                <CardTitle className="text-2xl text-orange-500">
                  {analytics?.forgottenItems?.totalForgotten || 0}
                </CardTitle>
              </CardHeader>
            </Card>
          </div>

          {/* LSTM Prediction Alert */}
          {styleProfile?.futurePrediction?.available && (
            <Alert className="border-purple-300 bg-purple-50">
              <AlertDescription>
                <div className="flex items-center justify-between">
                  <div>
                    <span className="font-bold">🔮 LSTM Prediction:</span> Next event likely to be{' '}
                    <Badge variant="secondary">{styleProfile.futurePrediction.nextLikelyEvent}</Badge>
                    {' '}({(styleProfile.futurePrediction.confidence * 100).toFixed(0)}% confidence)
                  </div>
                  <Badge>{styleProfile.futurePrediction.modelUsed}</Badge>
                </div>
              </AlertDescription>
            </Alert>
          )}

          {/* Forgotten Items Alert */}
          {analytics?.forgottenItems?.totalForgotten > 0 && (
            <Alert className="border-orange-300 bg-orange-50">
              <AlertDescription>
                <div className="space-y-2">
                  <p className="font-bold">⚠️ {analytics.forgottenItems.message}</p>
                  <ul className="list-disc list-inside space-y-1">
                    {analytics.forgottenItems.suggestions?.slice(0, 3).map((suggestion, idx) => (
                      <li key={idx} className="text-sm">{suggestion}</li>
                    ))}
                  </ul>
                </div>
              </AlertDescription>
            </Alert>
          )}

          {/* Quick Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Most Worn Items */}
            <Card>
              <CardHeader>
                <CardTitle>🏆 Most Worn Items</CardTitle>
                <CardDescription>Your wardrobe MVPs</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {analytics?.wearPatterns?.mostWorn?.slice(0, 5).map((item, idx) => (
                    <div key={idx} className="flex items-center justify-between border-b pb-2">
                      <div className="flex items-center gap-3">
                        <img 
                          src={`${API_BASE_URL}${item.url}`} 
                          alt={item.filename}
                          className="w-12 h-12 object-cover rounded"
                        />
                        <div>
                          <p className="font-medium">{item.type}</p>
                          <p className="text-sm text-gray-500">{item.primaryColor}</p>
                        </div>
                      </div>
                      <Badge>{item.wearCount} wears</Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Event Preferences */}
            <Card>
              <CardHeader>
                <CardTitle>🎉 Event Preferences</CardTitle>
                <CardDescription>Where you go most</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {analytics?.eventPreferences?.eventStats?.slice(0, 5).map((event, idx) => (
                    <div key={idx} className="flex items-center justify-between border-b pb-2">
                      <div>
                        <p className="font-medium">{event.event}</p>
                        <p className="text-sm text-gray-500">{event.itemsForEvent} items</p>
                      </div>
                      <Badge variant="outline">{event.attendanceCount} times</Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Seasonal Distribution */}
          <Card>
            <CardHeader>
              <CardTitle>🌸 Seasonal Distribution</CardTitle>
              <CardDescription>Your items by season</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-4 gap-4">
                {['spring', 'summer', 'fall', 'winter'].map((season) => {
                  const data = analytics?.seasonalAnalysis?.[season];
                  return (
                    <div key={season} className="text-center p-4 bg-gray-50 rounded-lg">
                      <div className="text-3xl mb-2">
                        {season === 'spring' && '🌸'}
                        {season === 'summer' && '☀️'}
                        {season === 'fall' && '🍂'}
                        {season === 'winter' && '❄️'}
                      </div>
                      <p className="font-bold capitalize">{season}</p>
                      <p className="text-2xl font-bold text-blue-600">{data?.items?.length || 0}</p>
                      <p className="text-sm text-gray-500">{data?.totalWears || 0} wears</p>
                    </div>
                  );
                })}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Style Profile Tab */}
        <TabsContent value="style" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>👔 Your Personal Style Profile</CardTitle>
              <CardDescription>LSTM-powered analysis of your fashion preferences</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Dominant Style */}
              <div>
                <h3 className="font-bold text-lg mb-2">Dominant Style</h3>
                <Badge variant="default" className="text-lg px-4 py-2">
                  {styleProfile?.dominantStyle}
                </Badge>
              </div>

              {/* Style Breakdown */}
              <div>
                <h3 className="font-bold text-lg mb-3">Style Breakdown</h3>
                <div className="space-y-2">
                  {Object.entries(styleProfile?.styleBreakdown || {}).map(([style, percentage]) => (
                    <div key={style} className="space-y-1">
                      <div className="flex justify-between text-sm">
                        <span className="capitalize">{style}</span>
                        <span className="font-bold">{percentage}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-blue-500 h-2 rounded-full transition-all"
                          style={{ width: `${percentage}%` }}
                        ></div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Color Palette */}
              <div>
                <h3 className="font-bold text-lg mb-3">🎨 Your Color Palette</h3>
                <div className="flex flex-wrap gap-2">
                  {styleProfile?.colorPalette?.topColors?.slice(0, 10).map((color, idx) => (
                    <Badge 
                      key={idx} 
                      variant="outline"
                      className="px-3 py-1"
                    >
                      <div 
                        className="w-4 h-4 rounded-full mr-2 inline-block"
                        style={{ backgroundColor: color }}
                      ></div>
                      {color}
                    </Badge>
                  ))}
                </div>
              </div>

              {/* Style Confidence */}
              <div>
                <h3 className="font-bold text-lg mb-3">🎯 Style Confidence Score</h3>
                <div className="bg-gradient-to-r from-purple-50 to-blue-50 p-4 rounded-lg">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-3xl font-bold">
                      {styleProfile?.styleConfidence?.score}/100
                    </span>
                    <Badge variant="secondary">{styleProfile?.styleConfidence?.level}</Badge>
                  </div>
                  <p className="text-gray-700">{styleProfile?.styleConfidence?.description}</p>
                  
                  <div className="mt-4 space-y-2">
                    {Object.entries(styleProfile?.styleConfidence?.components || {}).map(([key, value]) => (
                      <div key={key} className="flex justify-between text-sm">
                        <span className="capitalize">{key.replace(/([A-Z])/g, ' $1')}</span>
                        <span className="font-bold">{value}%</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Cost Analysis Tab */}
        <TabsContent value="cost" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <Card>
              <CardHeader>
                <CardTitle>Total Invested</CardTitle>
                <CardDescription className="text-2xl font-bold text-green-600">
                  ${analytics?.costAnalysis?.totalInvested?.toFixed(2) || 0}
                </CardDescription>
              </CardHeader>
            </Card>
            
            <Card>
              <CardHeader>
                <CardTitle>Avg Cost/Wear</CardTitle>
                <CardDescription className="text-2xl font-bold text-blue-600">
                  ${analytics?.costAnalysis?.averageCostPerWear?.toFixed(2) || 0}
                </CardDescription>
              </CardHeader>
            </Card>
            
            <Card>
              <CardHeader>
                <CardTitle>Best Value Item</CardTitle>
                <CardDescription className="text-sm font-medium">
                  {analytics?.costAnalysis?.bestValue?.[0]?.type || 'N/A'}
                  <br />
                  <span className="text-lg font-bold text-purple-600">
                    ${analytics?.costAnalysis?.bestValue?.[0]?.costPerWear?.toFixed(2) || 0}/wear
                  </span>
                </CardDescription>
              </CardHeader>
            </Card>
          </div>

          {/* Best Value Items */}
          <Card>
            <CardHeader>
              <CardTitle>⭐ Best Value Items</CardTitle>
              <CardDescription>Lowest cost per wear - your smart investments</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {analytics?.costAnalysis?.bestValue?.slice(0, 10).map((item, idx) => (
                  <div key={idx} className="flex items-center justify-between border-b pb-3">
                    <div className="flex items-center gap-3">
                      <img 
                        src={`${API_BASE_URL}${item.url}`} 
                        alt={item.filename}
                        className="w-16 h-16 object-cover rounded"
                      />
                      <div>
                        <p className="font-medium">{item.type}</p>
                        <p className="text-sm text-gray-500">
                          Worn {item.wearCount} times | Paid ${item.purchasePrice}
                        </p>
                        <Badge variant="outline" className="mt-1">{item.valueRating}</Badge>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-2xl font-bold text-green-600">
                        ${item.costPerWear.toFixed(2)}
                      </p>
                      <p className="text-xs text-gray-500">per wear</p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Unworn Expensive Items */}
          {analytics?.costAnalysis?.unwornExpensive?.length > 0 && (
            <Card className="border-orange-300">
              <CardHeader>
                <CardTitle>⚠️ Unworn Expensive Items</CardTitle>
                <CardDescription>High-value items not getting used</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {analytics.costAnalysis.unwornExpensive.slice(0, 5).map((item, idx) => (
                    <div key={idx} className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <img 
                          src={`${API_BASE_URL}${item.url}`} 
                          alt={item.filename}
                          className="w-12 h-12 object-cover rounded"
                        />
                        <div>
                          <p className="font-medium">{item.type}</p>
                          <p className="text-sm text-gray-500">Never worn</p>
                        </div>
                      </div>
                      <p className="text-lg font-bold text-orange-600">
                        ${item.purchasePrice.toFixed(2)}
                      </p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        {/* Wear Patterns Tab */}
        <TabsContent value="patterns" className="space-y-6">
          {/* Timeline Chart Placeholder */}
          <Card>
            <CardHeader>
              <CardTitle>📈 Wear Frequency Timeline</CardTitle>
              <CardDescription>Your wardrobe activity over time</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {analytics?.frequencyTimeline?.timeline?.map((entry, idx) => (
                  <div key={idx} className="flex items-center justify-between">
                    <span className="text-sm font-medium">{entry.period}</span>
                    <div className="flex items-center gap-2">
                      <div className="w-48 bg-gray-200 rounded-full h-4">
                        <div 
                          className="bg-blue-500 h-4 rounded-full"
                          style={{ width: `${Math.min(100, (entry.wears / 30) * 100)}%` }}
                        ></div>
                      </div>
                      <span className="text-sm font-bold w-12">{entry.wears}</span>
                    </div>
                  </div>
                ))}
              </div>
              <p className="text-sm text-gray-500 mt-4">
                Total wears: {analytics?.frequencyTimeline?.totalWears}
              </p>
            </CardContent>
          </Card>

          {/* Seasonal Distribution */}
          <Card>
            <CardHeader>
              <CardTitle>🌸 Seasonal Distribution</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {Object.entries(analytics?.seasonalAnalysis || {}).slice(0, 4).map(([season, data]) => {
                  if (season === 'totalWears' || season === 'percentages' || season === 'mostActiveSeasons') return null;
                  return (
                    <div key={season} className="bg-gray-50 p-4 rounded-lg text-center">
                      <p className="text-3xl mb-2">
                        {season === 'spring' && '🌸'}
                        {season === 'summer' && '☀️'}
                        {season === 'fall' && '🍂'}
                        {season === 'winter' && '❄️'}
                      </p>
                      <p className="font-bold capitalize">{season}</p>
                      <p className="text-2xl font-bold text-blue-600">{data?.items?.length || 0}</p>
                      <p className="text-sm text-gray-500">{data?.totalWears || 0} wears</p>
                      {data?.topColors?.[0] && (
                        <Badge variant="outline" className="mt-2">
                          {data.topColors[0].color}
                        </Badge>
                      )}
                    </div>
                  );
                })}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Insights Tab */}
        <TabsContent value="insights" className="space-y-6">
          {/* Combination Patterns */}
          <Card>
            <CardHeader>
              <CardTitle>👕 Outfit Combination Patterns</CardTitle>
              <CardDescription>What you wear together most often</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {styleProfile?.combinationPatterns?.frequentCombinations?.slice(0, 8).map((combo, idx) => (
                  <div key={idx} className="flex items-center justify-between border-b pb-2">
                    <div className="flex items-center gap-2">
                      {combo.types.map((type, i) => (
                        <Badge key={i} variant="secondary">{type}</Badge>
                      ))}
                    </div>
                    <span className="text-sm font-bold">{combo.frequency}x</span>
                  </div>
                ))}
              </div>
              <p className="text-sm text-gray-500 mt-4">
                Total unique combinations: {styleProfile?.combinationPatterns?.totalUniqueCombinations}
              </p>
            </CardContent>
          </Card>

          {/* Color Personality */}
          <Card>
            <CardHeader>
              <CardTitle>🎨 Color Personality</CardTitle>
            </CardHeader>
            <CardContent>
              <Alert className="mb-4">
                <AlertDescription>
                  {styleProfile?.colorPalette?.colorDistribution?.[0]?.color && (
                    <div>
                      <p className="font-bold">Your signature color: {styleProfile.colorPalette.colorDistribution[0].color}</p>
                      <p className="text-sm mt-1">
                        Worn {styleProfile.colorPalette.colorDistribution[0].percentage}% of the time
                      </p>
                    </div>
                  )}
                </AlertDescription>
              </Alert>

              <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                {styleProfile?.colorPalette?.colorDistribution?.slice(0, 10).map((colorData, idx) => (
                  <div key={idx} className="text-center p-3 bg-gray-50 rounded-lg">
                    <div 
                      className="w-12 h-12 rounded-full mx-auto mb-2 border-2"
                      style={{ backgroundColor: colorData.color }}
                    ></div>
                    <p className="text-xs font-medium">{colorData.color}</p>
                    <p className="text-sm font-bold">{colorData.percentage}%</p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Most Worn Types */}
          <Card>
            <CardHeader>
              <CardTitle>📊 Most Worn Clothing Types</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {styleProfile?.mostWornTypes?.slice(0, 10).map((typeData, idx) => (
                  <div key={idx} className="flex items-center justify-between">
                    <span className="font-medium">{typeData.type}</span>
                    <div className="flex items-center gap-2">
                      <div className="w-32 bg-gray-200 rounded-full h-4">
                        <div 
                          className="bg-purple-500 h-4 rounded-full"
                          style={{ width: `${Math.min(100, (typeData.count / 30) * 100)}%` }}
                        ></div>
                      </div>
                      <span className="font-bold w-8">{typeData.count}</span>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
