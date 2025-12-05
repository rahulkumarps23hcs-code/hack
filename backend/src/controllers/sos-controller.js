const { buildApiResponse } = require('../utils/api-response');
const { processSOS } = require('../services/ai-service');

const triggerSos = async (req, res) => {
  const { location, description } = req.body;
  const user = req.user || null;
  const attachmentPath = req.file ? req.file.path : null;

  let normalizedLocation = null;

  if (
    location &&
    typeof location.lat === 'number' &&
    typeof location.lng === 'number'
  ) {
    normalizedLocation = {
      lat: Number(location.lat),
      lng: Number(location.lng)
    };
  }

  const result = await processSOS({
    user,
    location: normalizedLocation,
    description,
    attachmentPath
  });

  res
    .status(201)
    .json(buildApiResponse(true, 'SOS processed successfully', result));
};

module.exports = { triggerSos };
