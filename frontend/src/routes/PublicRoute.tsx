import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LoadingScreen } from '../components/common/LoadingScreen';

export const PublicRoute: React.FC = () => {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return <LoadingScreen message="Loading..." />;
  }

  if (isAuthenticated) {
    // Already authenticated users cannot access /signin or /signup
    return <Navigate to="/app/dashboard" replace />;
  }

  return <Outlet />;
};
