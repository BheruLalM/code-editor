import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';

import AdminDashboard from './pages/admin/AdminDashboard';
import CreateSessionPage from './pages/admin/CreateSessionPage';
import SessionDetailPage from './pages/admin/SessionDetailPage';
import CandidateResultPage from './pages/admin/CandidateResultPage';

import CandidateRegisterPage from './pages/candidate/CandidateRegisterPage';
import CandidateSolvePage from './pages/candidate/CandidateSolvePage';
import ApplyPage from './pages/candidate/ApplyPage';
import WaitingRoomPage from './pages/candidate/WaitingRoomPage';

function UrlNormalizer({ children }) {
  const location = useLocation();
  const normalized = location.pathname.replace(/\/\/+/g, '/');
  if (normalized !== location.pathname) {
    return <Navigate to={normalized + location.search + location.hash} replace />;
  }
  return children;
}

function App() {
  return (
    <BrowserRouter>
      <Toaster position="top-right" />
      <UrlNormalizer>
      <Routes>
        {/* PUBLIC ROUTES */}
        <Route path="/apply" element={<ApplyPage />} />
        <Route path="/waiting/:token" element={<WaitingRoomPage />} />
        <Route path="/test/:token" element={<CandidateRegisterPage />} />
        <Route path="/solve/:token" element={<CandidateSolvePage />} />

        {/* ADMIN ROUTES (NOW PUBLIC) */}
        <Route path="/admin" element={<AdminDashboard />} />
        <Route path="/admin/sessions/new" element={<CreateSessionPage />} />
        <Route path="/admin/sessions/:id" element={<SessionDetailPage />} />
        <Route path="/admin/candidates/:id" element={<CandidateResultPage />} />

        {/* DEFAULT REDIRECT */}
        <Route path="*" element={<Navigate to="/admin" replace />} />
      </Routes>
      </UrlNormalizer>
    </BrowserRouter>
  );
}

export default App;
