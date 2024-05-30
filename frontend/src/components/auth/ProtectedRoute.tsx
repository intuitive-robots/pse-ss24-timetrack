import React, { ReactNode } from 'react';
import { Navigate } from 'react-router-dom';

interface ProtectedRouteProps {
  children: ReactNode;
}

/**
 * Hook to check if user is authenticated
 */
const useAuth = () => {
  const user = localStorage.getItem('user');
  return !!user;
};

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const isAuthenticated = useAuth();

  if (!isAuthenticated) {
    console.log("Not authenticated, redirecting to login");
    return <Navigate to="/login" replace />; // Redirect them to the /login page
  }

  return <>{children}</>;
};

export default ProtectedRoute;
