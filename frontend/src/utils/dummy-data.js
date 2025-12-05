export const dummyAlerts = [
  {
    id: 'alert-1',
    type: 'harassment',
    severity: 'high',
    timestamp: '2025-12-01T21:15:00Z',
    location: { lat: 12.9721, lng: 77.5933 },
    description: 'Harassment reported near the main city library entrance.',
  },
  {
    id: 'alert-2',
    type: 'suspicious-activity',
    severity: 'medium',
    timestamp: '2025-12-01T20:40:00Z',
    location: { lat: 12.9755, lng: 77.6012 },
    description: 'Suspicious loitering around the south campus parking area.',
  },
  {
    id: 'alert-3',
    type: 'escort-available',
    severity: 'low',
    timestamp: '2025-12-01T19:55:00Z',
    location: { lat: 12.969, lng: 77.59 },
    description: 'Volunteer safe-walk escorts are available at the north gate.',
  },
  {
    id: 'alert-4',
    type: 'patrol-update',
    severity: 'low',
    timestamp: '2025-12-01T19:20:00Z',
    location: { lat: 12.968, lng: 77.585 },
    description: 'Police patrol active around central metro station.',
  },
];

export const dummySafeSpots = [
  {
    id: 'spot-1',
    name: '24x7 Pharmacy',
    type: 'pharmacy',
    address: 'Central Avenue, Block A',
    location: { lat: 12.9728, lng: 77.5951 },
  },
  {
    id: 'spot-2',
    name: 'Campus Security Kiosk',
    type: 'security',
    address: 'North Campus Gate',
    location: { lat: 12.978, lng: 77.598 },
  },
  {
    id: 'spot-3',
    name: 'Women Help Center',
    type: 'support-center',
    address: 'Student Union Building, Level 1',
    location: { lat: 12.9712, lng: 77.6023 },
  },
  {
    id: 'spot-4',
    name: 'Women-Only Cab Zone',
    type: 'transport',
    address: 'Metro Station, Exit 2',
    location: { lat: 12.9675, lng: 77.6 },
  },
];

export const dummySafeZones = [
  {
    id: 'zone-safe-1',
    name: 'Main Campus Spine',
    type: 'safe-zone',
    severity: 'low',
    description: 'Well-lit pedestrian spine with active CCTV and patrols.',
    location: { lat: 12.9735, lng: 77.594 },
  },
  {
    id: 'zone-safe-2',
    name: 'Student Union Quadrangle',
    type: 'safe-zone',
    severity: 'low',
    description: 'High footfall area near student union building.',
    location: { lat: 12.9715, lng: 77.601 },
  },
];

export const dummyUnsafeZones = [
  {
    id: 'zone-unsafe-1',
    name: 'South Parking Lot',
    type: 'unsafe-zone',
    severity: 'high',
    description: 'Poor lighting and lower foot traffic reported after 9 PM.',
    location: { lat: 12.9678, lng: 77.5895 },
  },
  {
    id: 'zone-unsafe-2',
    name: 'Old Town Underpass',
    type: 'unsafe-zone',
    severity: 'medium',
    description: 'Reported incidents of harassment and theft.',
    location: { lat: 12.965, lng: 77.582 },
  },
];

export const dummyUser = {
  id: 'user-1',
  name: 'Safe-Zone Demo User',
  phone: '+91-98765-43210',
  email: 'demo.user@safezone.app',
};

export const dummyUserHistory = [
  {
    id: 'history-1',
    type: 'sos',
    timestamp: '2025-11-30T21:45:00Z',
    description: 'SOS triggered and shared with 3 emergency contacts.',
  },
  {
    id: 'history-2',
    type: 'route',
    timestamp: '2025-11-29T20:15:00Z',
    description: 'Smart night route suggested from Library to Hostel.',
  },
  {
    id: 'history-3',
    type: 'check-in',
    timestamp: '2025-11-27T19:05:00Z',
    description: 'Safe check-in confirmed at Home location.',
  },
];
