import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App.jsx';
import './styles/globals.css';
import { ThemeProvider } from './context/theme-context.jsx';
import { AuthProvider } from './context/auth-context.jsx';
import { AlertProvider } from './context/alert-context.jsx';
import { ToastProvider } from './context/toast-context.jsx';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ThemeProvider>
      <AuthProvider>
        <AlertProvider>
          <ToastProvider>
            <BrowserRouter>
              <App />
            </BrowserRouter>
          </ToastProvider>
        </AlertProvider>
      </AuthProvider>
    </ThemeProvider>
  </React.StrictMode>
);
