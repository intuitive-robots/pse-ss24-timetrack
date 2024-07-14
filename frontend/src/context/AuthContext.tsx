import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import {jwtDecode} from 'jwt-decode';
import { getProfile, login as loginService, logout as logoutService } from '../services/AuthService';
import {User} from "../interfaces/User";

interface AuthState {
  token: string | null;
  role: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  justLoggedIn: boolean;
  user: User | null;
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
  isLoading: true,
  justLoggedIn: false,
  user: null,
  login: async () => {},
  logout: async () => {},
};

export const AuthContext = createContext<AuthState>(initialState);

/**
 * AuthProvider component that wraps the application and provides authentication state and methods.
 *
 * @component
 * @param {AuthProviderProps} props - The props passed to the AuthProvider component.
 * @returns {React.ReactElement} A React Element that provides the authentication context.
 */
export const AuthProvider: React.FC<AuthProviderProps> = ({ children }: AuthProviderProps): React.ReactElement => {
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
          isLoading: false,
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
    } else {
      setAuthState(prevState => ({ ...prevState, isLoading: false }));
    }

  }, []);

  /**
   * Handles user login by calling the login service and updating the authentication state.
   *
   * @param {string} username - The username of the user.
   * @param {string} password - The password of the user.
   * @throws Error if login fails.
   */
  const handleLogin = async (username: string, password: string) => {
    try {
      const response = await loginService(username, password);
      localStorage.setItem('token', response.accessToken);
      const decoded: any = jwtDecode(response.accessToken);
      const profile = await getProfile();
      setAuthState({
        token: response.accessToken,
        role: decoded.role,
        isAuthenticated: true,
        isLoading: false,
        justLoggedIn: true,
        user: profile,
        login: handleLogin,
        logout: handleLogout,
      });
    } catch (error) {
      throw new Error('Login failed');
    }
  };

  /**
   * Handles user logout by calling the logout service and resetting the authentication state.
   *
   * @throws Error if logout fails.
   */
  const handleLogout = async () => {
    try {
      await logoutService();
      localStorage.removeItem('token');
      setAuthState({
        ...initialState,
        justLoggedIn: false
      });
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

/**
 * Custom hook to use the AuthContext.
 *
 * @returns {AuthState} The authentication state and methods.
 */
export const useAuth = (): AuthState => useContext(AuthContext);
