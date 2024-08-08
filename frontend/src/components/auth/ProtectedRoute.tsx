import React, { ReactNode } from 'react';
import { Navigate } from 'react-router-dom';
import {useAuth} from "../../context/AuthContext";

interface ProtectedRouteProps {
  children: ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const {isAuthenticated, isLoading} = useAuth();

  if (isLoading) {
    // console.log("Loading authentication status");
    return <div></div>;
  }

  if (!isAuthenticated) {
    console.log("Not authenticated, redirecting to login");
    return <Navigate to="/login" replace />; // Redirect them to the /login page
  }

  return <>{children}</>;
};

export default ProtectedRoute;
