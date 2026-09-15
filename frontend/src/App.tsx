import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { ProtectedRoute } from './routes/ProtectedRoute';
import { PublicRoute } from './routes/PublicRoute';
import { AppLayout } from './components/layout/AppLayout';
import { SignIn } from './pages/SignIn';
import { SignUp } from './pages/SignUp';
import { Dashboard } from './pages/Dashboard';
import { Profile } from './pages/Profile';
import { Resumes } from './pages/Resumes';
import { Claims } from './pages/Claims';
import { CareerData } from './pages/CareerData';
import { Jobs } from './pages/Jobs';
import { Matching } from './pages/Matching';
import { Optimization } from './pages/Optimization';
import { Settings } from './pages/Settings';

export const App: React.FC = () => {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Public Routes (Redirect to /app/dashboard if already authenticated) */}
          <Route element={<PublicRoute />}>
            <Route path="/signin" element={<SignIn />} />
            <Route path="/signup" element={<SignUp />} />
          </Route>

          {/* Protected Application Routes (Enforce authentication) */}
          <Route element={<ProtectedRoute />}>
            <Route path="/app" element={<AppLayout />}>
              <Route index element={<Navigate to="/app/dashboard" replace />} />
              <Route path="dashboard" element={<Dashboard />} />

              {/* Module 2: Career Source of Truth */}
              <Route path="profile" element={<Profile />} />
              <Route path="claims" element={<Claims />} />
              <Route path="career-data" element={<CareerData />} />

              {/* Module 3: Resume Ingestion */}
              <Route path="resumes" element={<Resumes />} />

              {/* Module 4: Job Description Analysis */}
              <Route path="jobs" element={<Jobs />} />

              {/* Module 5: Candidate-Job Matching */}
              <Route path="matching" element={<Matching />} />

              {/* Module 6 & 7: Truth-Validated Optimization & Resume Generation */}
              <Route path="optimization" element={<Optimization />} />

              {/* Account & Security Settings */}
              <Route path="settings" element={<Settings />} />
            </Route>
          </Route>

          {/* Default Fallback Redirect */}
          <Route path="/" element={<Navigate to="/app/dashboard" replace />} />
          <Route path="*" element={<Navigate to="/app/dashboard" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
};

export default App;
