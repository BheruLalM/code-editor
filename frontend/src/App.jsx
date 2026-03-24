import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';

import AdminLoginPage from './pages/admin/AdminLoginPage';
import AdminDashboard from './pages/admin/AdminDashboard';
import CreateSessionPage from './pages/admin/CreateSessionPage';
import SessionDetailPage from './pages/admin/SessionDetailPage';
import CandidateResultPage from './pages/admin/CandidateResultPage';

import CandidateRegisterPage from './pages/candidate/CandidateRegisterPage';
import CandidateSolvePage from './pages/candidate/CandidateSolvePage';

import ProtectedRoute from './components/ProtectedRoute';

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
        <Route path="/admin/login" element={<AdminLoginPage />} />
        <Route path="/test/:token" element={<CandidateRegisterPage />} />
        <Route path="/solve/:token" element={<CandidateSolvePage />} />

        {/* PROTECTED ADMIN ROUTES */}
        <Route path="/admin" element={
          <ProtectedRoute>
            <AdminDashboard />
          </ProtectedRoute>
        } />
        <Route path="/admin/sessions/new" element={
          <ProtectedRoute>
            <CreateSessionPage />
          </ProtectedRoute>
        } />
        <Route path="/admin/sessions/:id" element={
          <ProtectedRoute>
            <SessionDetailPage />
          </ProtectedRoute>
        } />
        <Route path="/admin/candidates/:id" element={
          <ProtectedRoute>
            <CandidateResultPage />
          </ProtectedRoute>
        } />

        {/* DEFAULT REDIRECT */}
        <Route path="*" element={<Navigate to="/admin/login" replace />} />
      </Routes>
      </UrlNormalizer>
    </BrowserRouter>
  );
}

export default App;
