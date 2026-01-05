import React, { useState, useEffect } from 'react';
import { Upload, Activity, Ruler, Loader2, CheckCircle, XCircle } from 'lucide-react';
import { apiService } from './services/api';
import ImageUpload from './components/ImageUpload';
import MeasurementsDisplay from './components/MeasurementsDisplay';
import MaskPreview from './components/MaskPreview';

function App() {
  // State management
  const [frontImage, setFrontImage] = useState(null);
  const [sideImage, setSideImage] = useState(null);
  const [frontPreview, setFrontPreview] = useState(null);
  const [sidePreview, setSidePreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [apiStatus, setApiStatus] = useState('checking');
  const [showFrontPreview, setShowFrontPreview] = useState(false);
  const [showSidePreview, setShowSidePreview] = useState(false);
  const [frontMaskData, setFrontMaskData] = useState(null);
  const [sideMaskData, setSideMaskData] = useState(null);
  const [processingPreview, setProcessingPreview] = useState(false);

  // Check API health on mount and retry on disconnection
  useEffect(() => {
    checkApiHealth();
    
    // Auto-retry health check every 3 seconds if disconnected
    const interval = setInterval(() => {
      if (apiStatus === 'error') {
        checkApiHealth();
      }
    }, 3000);
    
    return () => clearInterval(interval);
  }, [apiStatus]);

  const checkApiHealth = async () => {
    try {
      const health = await apiService.healthCheck();
      if (health.status === 'healthy' && health.model_loaded) {
        setApiStatus('connected');
        setError(null); // Clear any previous errors
      } else {
        setApiStatus('error');
        setError('Backend API is not ready. Please start the backend server.');
      }
    } catch (err) {
      setApiStatus('error');
      // Only set error message if not already set (avoid spam during auto-retry)
      if (!error || !error.includes('Cannot connect')) {
        setError('Cannot connect to backend API. Retrying...');
      }
    }
  };

  // Handle image uploads
const handleImageUpload = async (e, type) => {
  const file = e.target.files[0];
  if (file) {
    // Validate file
    if (!file.type.startsWith('image/')) {
      setError('Please upload a valid image file');
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      setError('Image size must be less than 10MB');
      return;
    }

    const previewUrl = URL.createObjectURL(file);
    
    if (type === 'front') {
      setFrontImage(file);
      setFrontPreview(previewUrl);
      
      // Generate preview
      setProcessingPreview(true);
      try {
        const maskData = await apiService.previewMask(file);
        if (maskData.success) {
          setFrontMaskData(maskData.data);
          setShowFrontPreview(true);
        }
      } catch (err) {
        console.error('Preview generation failed:', err);
        setError('Failed to generate preview. You can still proceed with analysis.');
      } finally {
        setProcessingPreview(false);
      }
    } else {
      setSideImage(file);
      setSidePreview(previewUrl);
      
      // Generate preview
      setProcessingPreview(true);
      try {
        const maskData = await apiService.previewMask(file);
        if (maskData.success) {
          setSideMaskData(maskData.data);
          setShowSidePreview(true);
        }
      } catch (err) {
        console.error('Preview generation failed:', err);
        setError('Failed to generate preview. You can still proceed with analysis.');
      } finally {
        setProcessingPreview(false);
      }
    }
    
    setError(null);
  }
};

  // Remove image
  const handleRemoveImage = (type) => {
    if (type === 'front') {
      setFrontImage(null);
      setFrontPreview(null);
    } else {
      setSideImage(null);
      setSidePreview(null);
    }
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validation
    if (!frontImage || !sideImage) {
      setError('Please upload both front and side images');
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);

    try {
      // Call complete analysis API
      const result = await apiService.completeAnalysis(
        frontImage,
        sideImage
      );

      if (result.success) {
        setResults(result.data);
        
        // Scroll to results
        setTimeout(() => {
          document.getElementById('results-section')?.scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
          });
        }, 100);
      } else {
        setError(result.error || 'Analysis failed. Please try again.');
      }
    } catch (err) {
      console.error('Analysis error:', err);
      setError(
        err.response?.data?.error || 
        err.message || 
        'Failed to analyze images. Please check your backend server.'
      );
    } finally {
      setLoading(false);
    }
  };

  // Reset form
  const handleReset = () => {
    setFrontImage(null);
    setSideImage(null);
    setFrontPreview(null);
    setSidePreview(null);
    setResults(null);
    setError(null);
  };

  return (
    <div className="min-h-screen from-slate-50 via-blue-50 to-indigo-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="bg-indigo-600 p-3 rounded-lg">
                <Ruler className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  Fashion Intelligence Platform
                </h1>
                <p className="text-sm text-gray-600 mt-0.5">
                  AI-powered body measurement prediction
                </p>
              </div>
            </div>
            
            {/* API Status Indicator */}
            <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-gray-50 border border-gray-200">
              {apiStatus === 'connected' && (
                <>
                  <CheckCircle className="w-5 h-5 text-green-600" />
                  <span className="text-sm font-medium text-green-700">Connected</span>
                </>
              )}
              {apiStatus === 'checking' && (
                <>
                  <Loader2 className="w-5 h-5 text-blue-600 animate-spin" />
                  <span className="text-sm font-medium text-blue-700">Checking...</span>
                </>
              )}
              {apiStatus === 'error' && (
                <>
                  <XCircle className="w-5 h-5 text-red-600" />
                  <span className="text-sm font-medium text-red-700">Disconnected</span>
                </>
              )}
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Upload Section */}
        <div className="bg-white rounded-xl shadow-sm p-8 mb-8 border border-gray-200">
          <div className="flex items-center justify-between mb-8">
            <h2 className="text-xl font-semibold text-gray-900 flex items-center gap-2">
              <Upload className="w-6 h-6 text-indigo-600" />
              Upload Images
            </h2>
            {(frontImage || sideImage) && (
              <button
                type="button"
                onClick={handleReset}
                className="text-sm text-gray-500 hover:text-red-600 font-medium transition-colors"
              >
                Reset All
              </button>
            )}
          </div>

          <form onSubmit={handleSubmit} className="space-y-8">
            {/* Image Uploads */}
            <div className="grid md:grid-cols-2 gap-6">
              <ImageUpload
                label="Front View (Required) *"
                image={frontImage}
                preview={frontPreview}
                onChange={(e) => handleImageUpload(e, 'front')}
                onRemove={() => handleRemoveImage('front')}
              />
              
              <ImageUpload
                label="Side View (Required) *"
                image={sideImage}
                preview={sidePreview}
                onChange={(e) => handleImageUpload(e, 'side')}
                onRemove={() => handleRemoveImage('side')}
              />
            </div>

            {/* Mask Preview Modals */}
            {showFrontPreview && frontMaskData && (
              <MaskPreview
                original={frontPreview}
                preview={frontMaskData.preview}
                mask={frontMaskData.mask}
                onAccept={() => setShowFrontPreview(false)}
                onRetry={() => {
                  setShowFrontPreview(false);
                  handleRemoveImage('front');
                }}
              />
            )}

            {showSidePreview && sideMaskData && (
              <MaskPreview
                original={sidePreview}
                preview={sideMaskData.preview}
                mask={sideMaskData.mask}
                onAccept={() => setShowSidePreview(false)}
                onRetry={() => {
                  setShowSidePreview(false);
                  handleRemoveImage('side');
                }}
              />
            )}

            {processingPreview && (
              <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                <div className="bg-white rounded-xl p-8 text-center">
                  <Loader2 className="w-12 h-12 text-primary-600 animate-spin mx-auto mb-4" />
                  <p className="text-lg font-semibold">Processing image...</p>
                  <p className="text-sm text-gray-600">Removing background and creating mask</p>
                </div>
              </div>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading || !frontImage || !sideImage || apiStatus !== 'connected'}
              className="w-full bg-indigo-600 text-white py-3 rounded-lg font-semibold hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-sm flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Analyzing...
                </>
              ) : (
                <>
                  <Activity className="w-5 h-5" />
                  Analyze Measurements
                </>
              )}
            </button>
          </form>

          {/* Error Message */}
          {error && (
            <div className="mt-6 bg-red-50 border border-red-200 text-red-800 px-5 py-4 rounded-lg flex items-start gap-3">
              <XCircle className="w-5 h-5 shrink-0 mt-0.5" />
              <div>
                <p className="font-semibold text-sm">Error</p>
                <p className="text-sm mt-0.5">{error}</p>
              </div>
            </div>
          )}
        </div>

        {/* Results Section */}
        {results && (
          <div id="results-section" className="space-y-6 animate-in fade-in duration-500">
            {/* Success Message */}
            <div className="bg-green-50 border border-green-200 text-green-800 px-5 py-4 rounded-lg flex items-center gap-3">
              <CheckCircle className="w-5 h-5" />
              <div>
                <p className="font-semibold text-sm">Analysis Complete</p>
                <p className="text-sm mt-0.5">Your measurements have been successfully analyzed</p>
              </div>
            </div>

            {/* Measurements */}
            {results.measurements && (
              <MeasurementsDisplay measurements={results.measurements} />
            )}

            {/* Model Info */}
            {results.model && (
              <div className="bg-white rounded-lg shadow-sm p-5 border border-gray-200">
                <p className="text-sm text-gray-600">
                  <span className="font-medium">Model:</span> {results.model}
                </p>
              </div>
            )}
          </div>
        )}

        {/* Instructions */}
        {!results && (
        <div className="bg-blue-50 border border-blue-200 p-6 rounded-lg">
          <h4 className="font-semibold text-blue-900 mb-3 text-sm">📸 Photo Guidelines</h4>
          <div className="grid md:grid-cols-2 gap-6 text-sm text-blue-800">
            <div>
              <p className="font-medium mb-2">✅ Best Practices</p>
              <ul className="list-disc list-inside space-y-1.5 text-sm">
                <li>Plain white or solid background</li>
                <li>Stand straight, arms slightly away</li>
                <li>Wear fitted clothing</li>
                <li>Good, even lighting</li>
                <li>Same distance for both views</li>
              </ul>
            </div>
            <div>
              <p className="font-medium mb-2">❌ Avoid</p>
              <ul className="list-disc list-inside space-y-1.5 text-sm">
                <li>Cluttered backgrounds</li>
                <li>Arms crossed or touching body</li>
                <li>Baggy clothing</li>
                <li>Poor lighting or shadows</li>
                <li>Partial body shots</li>
              </ul>
            </div>
          </div>
        </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white mt-16 py-6 border-t border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p className="text-sm text-gray-600">
            Fashion Intelligence Platform · Powered by AI
          </p>
          <p className="text-xs text-gray-500 mt-1">
            © 2025 All rights reserved
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;