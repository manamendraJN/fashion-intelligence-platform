import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { UploadCard } from './components/UploadCard';
import { ImagePreview } from './components/ImagePreview';
import { PredictionTable } from './components/PredictionTable';
import { HairGeneration } from './components/HairGeneration';
import { NailCare } from './components/NailCare';
import { DentalHygiene } from './components/DentalHygiene';
import { predictImage } from './api';
import { UploadState } from './types';
import './App.css';

function SkinAnalysis() {
  const [state, setState] = useState<UploadState>({
    image: null,
    preview: null,
    loading: false,
    error: null,
    result: null
  });

  const handleImageSelect = async (file: File) => {
    setState(prev => ({
      ...prev,
      image: file,
      preview: URL.createObjectURL(file),
      loading: true,
      error: null
    }));

    try {
      const result = await predictImage(file);
      setState(prev => ({
        ...prev,
        result,
        loading: false
      }));
    } catch (error) {
      setState(prev => ({
        ...prev,
        error: 'Failed to get predictions',
        loading: false
      }));
    }
  };

  return (
    <div className="app">
      <h1>🔬 Skin Analysis</h1>
      <p className="app-subtitle">Advanced skin tone, color, and blackhead detection</p>
      
      <div className="container">
        <div className="upload-section">
          <UploadCard onImageSelect={handleImageSelect} loading={state.loading} />
        </div>
        
        <div className="content-grid">
          <ImagePreview preview={state.preview} />
          <PredictionTable result={state.result} />
        </div>
        
        {state.error && <div className="error">❌ {state.error}</div>}
      </div>
    </div>
  );
}

function Navigation() {
  const location = useLocation();
  
  return (
    <nav className="navigation">
      <div className="nav-container">
        <div className="nav-brand">✨ Grooming AI</div>
        <div className="nav-links">
          <Link 
            to="/" 
            className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}
          >
            🔬 Skin Analysis
          </Link>
          <Link 
            to="/hair-generation" 
            className={`nav-link ${location.pathname === '/hair-generation' ? 'active' : ''}`}
          >
            💇 Hair Generation
          </Link>
          <Link 
            to="/nail-care" 
            className={`nav-link ${location.pathname === '/nail-care' ? 'active' : ''}`}
          >
            💅 Nail Care
          </Link>
          <Link 
            to="/dental-hygiene" 
            className={`nav-link ${location.pathname === '/dental-hygiene' ? 'active' : ''}`}
          >
            🦷 Dental Hygiene
          </Link>
        </div>
      </div>
    </nav>
  );
}

function App() {
  return (
    <Router>
      <div className="app-wrapper">
        <Navigation />
        <Routes>
          <Route path="/" element={<SkinAnalysis />} />
          <Route path="/hair-generation" element={<HairGeneration />} />
          <Route path="/nail-care" element={<NailCare />} />
          <Route path="/dental-hygiene" element={<DentalHygiene />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
