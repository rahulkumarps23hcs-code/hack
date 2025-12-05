import { dummySafeSpots, dummySafeZones, dummyUnsafeZones } from '../utils/dummy-data.js';

export async function fetchSafeSpots() {
  return dummySafeSpots;
}

export async function fetchSafeAndUnsafeZones() {
  return {
    safeZones: dummySafeZones,
    unsafeZones: dummyUnsafeZones,
  };
}
