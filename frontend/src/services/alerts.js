import { dummyAlerts } from '../utils/dummy-data.js';

export async function fetchAlerts() {
  return dummyAlerts;
}

export async function reportAlert(payload) {
  return {
    success: true,
    message: 'Alert reported (dummy, no network call).',
    data: {
      ...payload,
    },
  };
}
