import { dummySafeSpots } from './dummy-data.js';

export function getMockLocation() {
  return {
    lat: 12.9716,
    lng: 77.5946,
    city: 'Bengaluru',
    area: 'Central District',
  };
}

export function isNightAtLocation(date = new Date()) {
  const hour = date.getHours();
  return hour >= 19 || hour < 6;
}

export function getNightSafetyScore(isNight, baseScore = 84) {
  if (!isNight) {
    return baseScore;
  }
  const adjusted = baseScore - 18;
  return adjusted < 35 ? 35 : adjusted;
}

export function getNearestSafeSpots(limit = 3) {
  const userLocation = getMockLocation();
  const scored = dummySafeSpots.map((spot) => {
    const distance = Math.sqrt(
      (spot.location.lat - userLocation.lat) ** 2 +
        (spot.location.lng - userLocation.lng) ** 2
    );
    return { ...spot, distance };
  });

  const sorted = scored.sort((a, b) => a.distance - b.distance);
  return sorted.slice(0, limit);
}
