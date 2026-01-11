'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { authAPI } from '@/lib/api';
import Cookies from 'js-cookie';

interface User {
  id: string;
  email: string;
  first_name?: string;
  last_name?: string;
  created_at: string;
  updated_at: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  register: (email: string, password: string, first_name?: string, last_name?: string) => Promise<void>;
  checkAuthStatus: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    const storedToken = Cookies.get('access_token') || localStorage.getItem('access_token');
    
    if (storedToken) {
      try {
        setToken(storedToken);
        const response = await authAPI.getCurrentUser();
        setUser(response.data);
      } catch (error) {
        console.error('Auth check failed:', error);
        // Don't call logout() here if it causes loops, just clear local state
        localStorage.removeItem('access_token');
        Cookies.remove('access_token', { path: '/' });
        setToken(null);
        setUser(null);
      }
    }
    setLoading(false);
  };

  const login = async (email: string, password: string) => {
    try {
      // We don't set global loading to true here to prevent the whole app 
      // from showing the "Loading..." spinner on the login page.
      const response = await authAPI.login({ email, password });
      const { access_token } = response.data;

      localStorage.setItem('access_token', access_token);
      Cookies.set('access_token', access_token, { expires: 7, path: '/' });
      setToken(access_token);

      const userResponse = await authAPI.getCurrentUser();
      setUser(userResponse.data);
    } catch (error: any) {
      console.error('Login error:', error);
      // Re-throw the error so the UI can catch it
      throw error;
    }
  };

  const register = async (email: string, password: string, first_name?: string, last_name?: string) => {
    try {
      await authAPI.register({ email, password, first_name, last_name });
    } catch (error: any) {
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    Cookies.remove('access_token', { path: '/' });
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, loading, login, logout, register, checkAuthStatus }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) throw new Error('useAuth must be used within AuthProvider');
  return context;
};