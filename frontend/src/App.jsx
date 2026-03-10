import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { WardrobeProvider } from './context/WardrobeContext';
import { WardrobePage }  from './pages/AccWardrobe';
import { DiscoverPage }  from './pages/AccDiscover';
import { AnalyticsPage } from './pages/AccAnalytics';

function App() {
  return (
    <WardrobeProvider>
      <Router>
        <Routes>
          <Route path="/"          element={<DiscoverPage />} />
          <Route path="/wardrobe"  element={<WardrobePage />} />
          <Route path="/analytics" element={<AnalyticsPage />} />
        </Routes>
      </Router>
    </WardrobeProvider>
  );
}

export default App;