const { buildApiResponse } = require('../utils/api-response');
const { analyzeUnsafeZone } = require('../services/ai-service');

const buildLocationFromQuery = (query) => {
  const lat = query.lat ? parseFloat(query.lat) : null;
  const lng = query.lng ? parseFloat(query.lng) : null;

  if (
    typeof lat === 'number' &&
    !Number.isNaN(lat) &&
    typeof lng === 'number' &&
    !Number.isNaN(lng)
  ) {
    return { lat, lng };
  }

  return null;
};

const getUnsafeZones = async (req, res) => {
  const location = buildLocationFromQuery(req.query);
  const analysis = await analyzeUnsafeZone({ location });

  res.json(
    buildApiResponse(true, 'Unsafe zone analysis generated successfully', {
      zoneType: 'unsafe',
      ...analysis
    })
  );
};

const getSafeZones = async (req, res) => {
  const location = buildLocationFromQuery(req.query);
  const analysis = await analyzeUnsafeZone({ location });

  res.json(
    buildApiResponse(true, 'Safe zone suggestions generated successfully', {
      zoneType: 'safe',
      ...analysis
    })
  );
};

module.exports = { getUnsafeZones, getSafeZones };
