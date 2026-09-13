import React from 'react';
import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LoadingScreen } from '../components/common/LoadingScreen';

export const ProtectedRoute: React.FC = () => {
  const { isAuthenticated, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return <LoadingScreen message="Validating candidate authorization..." />;
  }

  if (!isAuthenticated) {
    // Redirect to /signin, preserving requested path for seamless redirect after login
    return <Navigate to="/signin" state={{ from: location }} replace />;
  }

  return <Outlet />;
};
