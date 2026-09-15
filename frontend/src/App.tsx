import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { ProtectedRoute } from './routes/ProtectedRoute';
import { PublicRoute } from './routes/PublicRoute';
import { AppLayout } from './components/layout/AppLayout';
import { SignIn } from './pages/SignIn';
import { SignUp } from './pages/SignUp';
import { Dashboard } from './pages/Dashboard';
import { PlaceholderPage } from './pages/PlaceholderPage';
import { Profile } from './pages/Profile';
import { Resumes } from './pages/Resumes';
import { Claims } from './pages/Claims';
import { CareerData } from './pages/CareerData';
import { Jobs } from './pages/Jobs';
import { UserCheck, GitCompare, Wand2, Settings } from 'lucide-react';

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
              <Route path="profile" element={<Profile />} />
              <Route path="claims" element={<Claims />} />
              <Route path="career-data" element={<CareerData />} />

              {/* Future Modules Planned in Architecture */}
              <Route
                path="profile-legacy"
                element={
                  <PlaceholderPage
                    title="Career Profile & Evidence Anchor"
                    moduleName="Module 2: Career Profile"
                    description="Maintain your persistent career history, verified factual claims, and supporting evidence sources."
                    icon={UserCheck}
                  />
                }
              />
              <Route path="resumes" element={<Resumes />} />
              <Route path="jobs" element={<Jobs />} />
              <Route
                path="matching"
                element={
                  <PlaceholderPage
                    title="Candidate-Job Matching Engine"
                    moduleName="Module 5: Compatibility Engine"
                    description="Transparent exact, normalized, and semantic matching with explainable gap breakdowns."
                    icon={GitCompare}
                  />
                }
              />
              <Route
                path="optimization"
                element={
                  <PlaceholderPage
                    title="Truth-Validated Resume Optimizer"
                    moduleName="Module 6: Resume Optimizer"
                    description="Generate job-specific resumes strictly validated against your trusted career claims and candidate evidence."
                    icon={Wand2}
                  />
                }
              />
              <Route
                path="settings"
                element={
                  <PlaceholderPage
                    title="Account & Security Settings"
                    moduleName="Security"
                    description="Manage account credentials, active login sessions, and data privacy options."
                    icon={Settings}
                  />
                }
              />
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
