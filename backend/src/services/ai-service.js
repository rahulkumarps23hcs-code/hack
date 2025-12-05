const Alert = require('../models/alert-model');
const SafeSpot = require('../models/safe-spot-model');
const { logger } = require('../utils/logger');

const analyzeUnsafeZone = async ({ location }) => {
  logger.info('AI analyzeUnsafeZone called', { location });
  const alerts = await Alert.find().sort({ timestamp: -1 }).limit(20);

  const riskLevel = alerts.length > 0 ? 'high' : 'low';

  return {
    zoneId: 'zone-placeholder',
    location: location || null,
    riskLevel,
    alerts: alerts.map((alert) => alert.toJSON()),
    recommendation:
      riskLevel === 'high'
        ? 'Avoid this area during late hours. Stay in groups and use well-lit paths.'
        : 'Area currently appears relatively safe based on recent alerts.'
  };
};

const getSaferRoute = async ({ from, to }) => {
  logger.info('AI getSaferRoute called', { from, to });
  return {
    routeId: 'route-placeholder',
    from,
    to,
    riskScore: 0.3,
    checkpoints: [
      {
        lat: from?.lat,
        lng: from?.lng,
        label: 'Start',
        riskLevel: 'medium'
      },
      {
        lat: to?.lat,
        lng: to?.lng,
        label: 'Destination',
        riskLevel: 'low'
      }
    ]
  };
};

const processSOS = async ({ user, location, description, attachmentPath }) => {
  logger.info('AI processSOS called', {
    userId: user ? user.id : null,
    location,
    hasAttachment: Boolean(attachmentPath)
  });
  const safeSpots = await SafeSpot.find().limit(3);

  return {
    sosId: 'sos-placeholder',
    status: 'dispatched',
    priority: 'high',
    user: user ? user.toJSON() : null,
    location: location || null,
    description: description || 'SOS triggered',
    attachmentPath: attachmentPath || null,
    nearestSafeSpots: safeSpots.map((spot) => spot.toJSON())
  };
};

const getNearestSafeSpots = async ({ location, limit = 5 }) => {
  logger.info('AI getNearestSafeSpots called', { location, limit });
  const spots = await SafeSpot.find();

  if (!location || typeof location.lat !== 'number' || typeof location.lng !== 'number') {
    return spots.slice(0, limit).map((spot) => spot.toJSON());
  }

  const withDistance = spots.map((spot) => {
    const spotLocation = spot.location;
    const distance = Math.sqrt(
      Math.pow(spotLocation.lat - location.lat, 2) + Math.pow(spotLocation.lng - location.lng, 2)
    );

    return { spot, distance };
  });

  withDistance.sort((a, b) => a.distance - b.distance);

  return withDistance.slice(0, limit).map((item) => item.spot.toJSON());
};

module.exports = { analyzeUnsafeZone, getSaferRoute, processSOS, getNearestSafeSpots };
