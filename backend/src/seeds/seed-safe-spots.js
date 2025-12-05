require('dotenv').config();

const { connectDb } = require('../config/db');
const SafeSpot = require('../models/safe-spot-model');
const { logger } = require('../utils/logger');

const safeSpotSeeds = [
  {
    name: 'City Central Police Station',
    type: 'police-station',
    address: 'MG Road, Central City, 560001',
    location: { lat: 12.9716, lng: 77.5946 }
  },
  {
    name: 'General Hospital',
    type: 'hospital',
    address: 'Health Street, Central City, 560002',
    location: { lat: 12.975, lng: 77.59 }
  },
  {
    name: 'Women Help Center',
    type: 'help-center',
    address: 'Safety Lane, East City, 560003',
    location: { lat: 12.978, lng: 77.6 }
  },
  {
    name: 'Community Safe House',
    type: 'community-center',
    address: 'Lake View Road, North City, 560004',
    location: { lat: 12.98, lng: 77.59 }
  },
  {
    name: 'Metro Station - Safe Zone',
    type: 'public-transport',
    address: 'Metro Line 1, South City, 560005',
    location: { lat: 12.965, lng: 77.6 }
  }
];

const seedSafeSpots = async () => {
  try {
    await connectDb();
    logger.info('Connected to MongoDB for safe spot seeding');

    let createdCount = 0;

    for (const seed of safeSpotSeeds) {
      const existing = await SafeSpot.findOne({
        name: seed.name,
        'location.lat': seed.location.lat,
        'location.lng': seed.location.lng
      });

      if (existing) {
        logger.info('SafeSpot already exists, skipping', { name: seed.name });
        // eslint-disable-next-line no-continue
        continue;
      }

      await SafeSpot.create(seed);
      createdCount += 1;
      logger.info('SafeSpot created', { name: seed.name });
    }

    logger.info('Safe spot seeding completed', { createdCount });
    process.exit(0);
  } catch (error) {
    logger.error('Safe spot seeding failed', { error: error.message });
    // eslint-disable-next-line no-console
    console.error(error);
    process.exit(1);
  }
};

seedSafeSpots();
