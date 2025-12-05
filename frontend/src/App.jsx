import { Navigate, Route, Routes } from 'react-router-dom';
import MainLayout from './layouts/main-layout.jsx';
import AuthLayout from './layouts/auth-layout.jsx';
import Landing from './pages/Landing.jsx';
import Login from './pages/Login.jsx';
import Signup from './pages/Signup.jsx';
import Dashboard from './pages/Dashboard.jsx';
import Alerts from './pages/Alerts.jsx';
import MapView from './pages/MapView.jsx';
import SOS from './pages/SOS.jsx';
import SafeSpots from './pages/SafeSpots.jsx';
import { useAuth } from './context/auth-context.jsx';

function ProtectedRoute({ children }) {
  const { isAuthenticated, initializing } = useAuth();

  if (initializing) {
    return null;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return children;
}

function App() {
  return (
    <Routes>
      <Route element={<MainLayout />}>
        <Route path="/" element={<Landing />} />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/alerts"
          element={
            <ProtectedRoute>
              <Alerts />
            </ProtectedRoute>
          }
        />
        <Route
          path="/map"
          element={
            <ProtectedRoute>
              <MapView />
            </ProtectedRoute>
          }
        />
        <Route
          path="/sos"
          element={
            <ProtectedRoute>
              <SOS />
            </ProtectedRoute>
          }
        />
        <Route
          path="/safe-spots"
          element={
            <ProtectedRoute>
              <SafeSpots />
            </ProtectedRoute>
          }
        />
      </Route>
      <Route element={<AuthLayout />}>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default App;
