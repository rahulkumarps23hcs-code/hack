import { useEffect, useMemo, useState } from 'react';
import { getMockLocation, getNightSafetyScore, getNearestSafeSpots, isNightAtLocation } from '../utils/geo.js';

export function useNightSafety() {
  const [location, setLocation] = useState(() => getMockLocation());
  const [now, setNow] = useState(() => new Date());

  useEffect(() => {
    const interval = window.setInterval(() => {
      setNow(new Date());
    }, 60000);

    return () => window.clearInterval(interval);
  }, []);

  const isNight = useMemo(() => isNightAtLocation(now), [now]);

  const safetyScore = useMemo(() => getNightSafetyScore(isNight), [isNight]);

  const nearbySafeSpots = useMemo(() => getNearestSafeSpots(3), []);

  const primaryMessage = useMemo(() => {
    if (!isNight) {
      return 'Daytime conditions look stable in your area.';
    }
    if (safetyScore >= 70) {
      return 'Night-time looks reasonably safe, but stay aware.';
    }
    if (safetyScore >= 50) {
      return 'Night-time risk is elevated. Prefer guided or group routes.';
    }
    return 'Night-time risk is high. Avoid isolated routes and use SOS if needed.';
  }, [isNight, safetyScore]);

  const secondaryMessage = useMemo(() => {
    if (!isNight) {
      return 'Smart Night Mode will automatically adjust once it gets dark.';
    }
    return 'Smart Night Mode prioritises well-lit, monitored and populated paths.';
  }, [isNight]);

  return {
    location,
    isNight,
    safetyScore,
    primaryMessage,
    secondaryMessage,
    nearbySafeSpots,
  };
}
