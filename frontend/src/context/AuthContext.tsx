import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import {jwtDecode} from "jwt-decode";

interface AuthState {
  token: string | null;
  role: string | null;
  isAuthenticated: boolean;
}

interface AuthProviderProps {
  children: ReactNode;
}

const initialState: AuthState = {
  token: localStorage.getItem('token'),
  role: null,
  isAuthenticated: false
};

export const AuthContext = createContext<AuthState>(initialState);

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [authState, setAuthState] = useState<AuthState>(initialState);

  useEffect(() => {
    const token = authState.token;
    if (token) {
      const decoded: any = jwtDecode(token);
      setAuthState({ ...authState, role: decoded.role, isAuthenticated: true });
    }
  }, [authState.token]);

  return (
    <AuthContext.Provider value={authState}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
