require('dotenv').config();

const { connectDb } = require('../config/db');
const Alert = require('../models/alert-model');
const { logger } = require('../utils/logger');

const now = new Date();

const alertSeeds = [
  {
    type: 'harassment',
    severity: 'high',
    timestamp: new Date(now.getTime() - 60 * 60 * 1000),
    location: { lat: 12.9716, lng: 77.5946 },
    description: 'Reported harassment incident near central bus stop.'
  },
  {
    type: 'suspicious-activity',
    severity: 'medium',
    timestamp: new Date(now.getTime() - 2 * 60 * 60 * 1000),
    location: { lat: 12.975, lng: 77.59 },
    description: 'Group of people loitering late at night.'
  },
  {
    type: 'theft',
    severity: 'medium',
    timestamp: new Date(now.getTime() - 3 * 60 * 60 * 1000),
    location: { lat: 12.978, lng: 77.6 },
    description: 'Reported bag theft near park entrance.'
  },
  {
    type: 'harassment',
    severity: 'low',
    timestamp: new Date(now.getTime() - 4 * 60 * 60 * 1000),
    location: { lat: 12.98, lng: 77.59 },
    description: 'Verbal harassment reported on main street.'
  },
  {
    type: 'unsafe-driving',
    severity: 'medium',
    timestamp: new Date(now.getTime() - 5 * 60 * 60 * 1000),
    location: { lat: 12.965, lng: 77.6 },
    description: 'High-speed driving near school zone.'
  }
];

const seedAlerts = async () => {
  try {
    await connectDb();
    logger.info('Connected to MongoDB for alert seeding');

    let createdCount = 0;

    for (const seed of alertSeeds) {
      const existing = await Alert.findOne({
        type: seed.type,
        severity: seed.severity,
        description: seed.description,
        'location.lat': seed.location.lat,
        'location.lng': seed.location.lng
      });

      if (existing) {
        logger.info('Alert already exists, skipping', {
          type: seed.type,
          description: seed.description
        });
        // eslint-disable-next-line no-continue
        continue;
      }

      await Alert.create(seed);
      createdCount += 1;
      logger.info('Alert created', {
        type: seed.type,
        description: seed.description
      });
    }

    logger.info('Alert seeding completed', { createdCount });
    process.exit(0);
  } catch (error) {
    logger.error('Alert seeding failed', { error: error.message });
    // eslint-disable-next-line no-console
    console.error(error);
    process.exit(1);
  }
};

seedAlerts();
