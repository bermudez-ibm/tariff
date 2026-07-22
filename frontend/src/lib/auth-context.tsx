import React, { createContext, useContext, useState, useEffect } from 'react';
import sharedConfig from '../../../shared_config.json';
import { request } from './api-client';
import { LoginRequest, LoginResponse, UserResponse } from '../types/api';

interface AuthContextType {
  user: UserResponse | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<UserResponse | null>(null);
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    const storedToken = localStorage.getItem(sharedConfig.auth.storage_key);
    if (storedToken) {
      setToken(storedToken);
    }
  }, []);

  const login = async (email: string, password: string) => {
    const loginData: LoginRequest = {
      [sharedConfig.auth.login_request.field_names[0]]: email,
      [sharedConfig.auth.login_request.field_names[1]]: password,
    };

    const response = await request<LoginResponse>(
      sharedConfig.auth.login_endpoint.replace(sharedConfig.api_base_path, ''),
      {
        method: 'POST',
        body: JSON.stringify(loginData),
      }
    );

    const accessToken = response[sharedConfig.auth.login_response.token_field as keyof LoginResponse] as string;
    const userData = response[sharedConfig.auth.login_response.user_field as keyof LoginResponse] as UserResponse;

    localStorage.setItem(sharedConfig.auth.storage_key, accessToken);
    setToken(accessToken);
    setUser(userData);
  };

  const logout = () => {
    localStorage.removeItem(sharedConfig.auth.storage_key);
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        login,
        logout,
        isAuthenticated: !!token,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
