import { createContext, useContext, useEffect, useState } from 'react';
import { login as loginService, signup as signupService, logout as logoutService } from '../services/auth.js';

const AuthContext = createContext(undefined);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [initializing, setInitializing] = useState(true);

  useEffect(() => {
    const stored = window.localStorage.getItem('safeZoneUser');
    if (stored) {
      try {
        const parsed = JSON.parse(stored);
        setUser(parsed);
      } catch {
        setUser(null);
      }
    }
    setInitializing(false);
  }, []);

  const login = async (payload) => {
    const response = await loginService(payload);
    setUser(response);
    window.localStorage.setItem('safeZoneUser', JSON.stringify(response));
    return response;
  };

  const signup = async (payload) => {
    const response = await signupService(payload);
    setUser(response);
    window.localStorage.setItem('safeZoneUser', JSON.stringify(response));
    return response;
  };

  const logout = async () => {
    await logoutService();
    setUser(null);
    window.localStorage.removeItem('safeZoneUser');
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        initializing,
        isAuthenticated: !!user,
        login,
        signup,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
