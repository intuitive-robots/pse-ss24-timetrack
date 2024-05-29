import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import {jwtDecode} from 'jwt-decode';
import { getProfile, login as loginService, logout as logoutService } from '../services/AuthService'; // Adjust path as necessary

interface AuthState {
  token: string | null;
  role: string | null;
  isAuthenticated: boolean;
  user: any | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
}

interface AuthProviderProps {
  children: ReactNode;
}

const initialState: AuthState = {
  token: localStorage.getItem('token'),
  role: null,
  isAuthenticated: false,
  user: null,
  login: async () => {},
  logout: async () => {},
};

export const AuthContext = createContext<AuthState>(initialState);

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [authState, setAuthState] = useState<AuthState>(initialState);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const decoded: any = jwtDecode(token);
        setAuthState((prevState) => ({
          ...prevState,
          token,
          role: decoded.role,
          isAuthenticated: true,
        }));

        (async () => {
          try {
            const profile = await getProfile();
            setAuthState((prevState) => ({
              ...prevState,
              user: profile,
            }));
          } catch (error) {
            console.log('Not authenticated');
          }
        })();
      } catch (error) {
        console.error('Error decoding token:', error);
      }
    }
  }, []);

  const handleLogin = async (username: string, password: string) => {
    try {
      const response = await loginService(username, password);
      const decoded: any = jwtDecode(response.accessToken);
      localStorage.setItem('token', response.accessToken);
      const profile = await getProfile();
      setAuthState({
        token: response.accessToken,
        role: decoded.role,
        isAuthenticated: true,
        user: profile,
        login: handleLogin,
        logout: handleLogout,
      });
    } catch (error) {
      throw new Error('Login failed');
    }
  };

  const handleLogout = async () => {
    try {
      await logoutService();
      localStorage.removeItem('token');
      setAuthState(initialState);
    } catch (error) {
      console.error('Logout failed');
    }
  };

  return (
    <AuthContext.Provider value={{ ...authState, login: handleLogin, logout: handleLogout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
