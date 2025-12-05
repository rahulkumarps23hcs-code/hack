const { buildApiResponse } = require('../utils/api-response');
const { getSaferRoute } = require('../services/ai-service');

const getSaferRouteController = async (req, res) => {
  const fromLat = req.query.fromLat ? parseFloat(req.query.fromLat) : null;
  const fromLng = req.query.fromLng ? parseFloat(req.query.fromLng) : null;
  const toLat = req.query.toLat ? parseFloat(req.query.toLat) : null;
  const toLng = req.query.toLng ? parseFloat(req.query.toLng) : null;

  const from =
    typeof fromLat === 'number' &&
    !Number.isNaN(fromLat) &&
    typeof fromLng === 'number' &&
    !Number.isNaN(fromLng)
      ? { lat: fromLat, lng: fromLng }
      : null;

  const to =
    typeof toLat === 'number' &&
    !Number.isNaN(toLat) &&
    typeof toLng === 'number' &&
    !Number.isNaN(toLng)
      ? { lat: toLat, lng: toLng }
      : null;

  const route = await getSaferRoute({ from, to });

  res.json(buildApiResponse(true, 'Safer route generated successfully', route));
};

module.exports = { getSaferRouteController };
