import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { UploadPage } from './pages/Upload';
import { ChatPage } from './pages/Chat';
import { AnalyticsPage } from './pages/Analytics';
import { MeasurementsPage } from './pages/Measurements';
import SizeMatching from './pages/SizeMatching';
import { AdminPage } from './pages/AdminPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<UploadPage />} />
        <Route path="/chat" element={<ChatPage />} />
        <Route path="/analytics" element={<AnalyticsPage />} />
        <Route path="/measurements" element={<MeasurementsPage />} />
        <Route path="/size-matching" element={<SizeMatching />} />
        <Route path="/admin" element={<AdminPage />} />
      </Routes>
    </Router>
  );
}

export default App;
