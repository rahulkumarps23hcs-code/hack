const { buildApiResponse } = require('../utils/api-response');
const { getSafeSpots } = require('../services/safe-spot-service');
const { getNearestSafeSpots } = require('../services/ai-service');

const getSafeSpotsController = async (req, res) => {
  const safeSpots = await getSafeSpots();
  res.json(buildApiResponse(true, 'Safe spots fetched successfully', safeSpots));
};

const getNearbySafeSpotsController = async (req, res) => {
  const lat = req.query.lat ? parseFloat(req.query.lat) : null;
  const lng = req.query.lng ? parseFloat(req.query.lng) : null;
  const limit = req.query.limit ? parseInt(req.query.limit, 10) : 5;

  const location =
    typeof lat === 'number' &&
    !Number.isNaN(lat) &&
    typeof lng === 'number' &&
    !Number.isNaN(lng)
      ? { lat, lng }
      : null;

  const safeSpots = await getNearestSafeSpots({ location, limit });

  res.json(
    buildApiResponse(true, 'Nearby safe spots fetched successfully', safeSpots)
  );
};

module.exports = { getSafeSpotsController, getNearbySafeSpotsController };
