import { createContext, useContext, useMemo, useState } from 'react';
import { dummyAlerts } from '../utils/dummy-data.js';

const AlertContext = createContext(undefined);

export function AlertProvider({ children }) {
  const [alerts, setAlerts] = useState(dummyAlerts);
  const [severityFilter, setSeverityFilter] = useState('all');
  const [streaming, setStreaming] = useState(true);

  const filteredAlerts = useMemo(() => {
    if (severityFilter === 'all') {
      return alerts;
    }
    return alerts.filter((alert) => alert.severity === severityFilter);
  }, [alerts, severityFilter]);

  const pushAlert = (alert) => {
    setAlerts((prev) => [alert, ...prev].slice(0, 50));
  };

  return (
    <AlertContext.Provider
      value={{
        alerts,
        filteredAlerts,
        severityFilter,
        setSeverityFilter,
        streaming,
        setStreaming,
        pushAlert,
      }}
    >
      {children}
    </AlertContext.Provider>
  );
}

export function useAlerts() {
  const context = useContext(AlertContext);
  if (!context) {
    throw new Error('useAlerts must be used within AlertProvider');
  }
  return context;
}
