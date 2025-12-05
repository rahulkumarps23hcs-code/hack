const SafeSpot = require('../models/safe-spot-model');

const getSafeSpots = async () => {
  const safeSpots = await SafeSpot.find().sort({ createdAt: -1 });
  return safeSpots;
};

module.exports = { getSafeSpots };
