import React, { useContext } from 'react';
import { Navigate } from 'react-router-dom';
import {useAuth} from "../../context/AuthContext";

interface RoleBasedRouteProps {
  children: React.ReactNode;
  roleRequired: string;
}

/**
 * RoleBasedRoute Component to control access based on user roles.
 * @param {Object} props - The props for the component.
 * @param {React.ReactNode} props.children - The child components to render if access is granted.
 * @param {string} props.roleRequired - The role required to access the children components.
 * @returns {React.ReactElement} - A React Element that either renders the children or redirects.
 */
const RoleBasedRoute: React.FC<RoleBasedRouteProps> = ({ children, roleRequired }) => {
  const { role } = useAuth();

  if (role !== roleRequired) {
    return <Navigate to="/unauthorized" replace />;
  }

  return <>{children}</>;
};

export default RoleBasedRoute;
