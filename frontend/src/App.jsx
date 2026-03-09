import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { UploadPage } from './pages/Upload';
import { ChatPage } from './pages/Chat';
import { AnalyticsPage } from './pages/Analytics';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<UploadPage />} />
        <Route path="/chat" element={<ChatPage />} />
        <Route path="/analytics" element={<AnalyticsPage />} />
      </Routes>
    </Router>
  );
}

export default App
