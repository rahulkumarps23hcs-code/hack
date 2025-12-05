const { buildApiResponse } = require('../utils/api-response');
const { createAlert, getAlerts } = require('../services/alert-service');

const getAlertsController = async (req, res) => {
  const alerts = await getAlerts();
  res.json(buildApiResponse(true, 'Alerts fetched successfully', alerts));
};

const reportAlert = async (req, res) => {
  const { type, severity, timestamp, location, description } = req.body;

  if (!type || !severity || !location || typeof location.lat !== 'number' || typeof location.lng !== 'number') {
    const error = new Error('type, severity and location { lat, lng } are required');
    error.statusCode = 400;
    throw error;
  }

  const alert = await createAlert({
    type,
    severity,
    timestamp: timestamp ? new Date(timestamp) : undefined,
    location,
    description,
    userId: req.user ? req.user.id : undefined
  });

  res.status(201).json(buildApiResponse(true, 'Alert reported successfully', alert));
};

module.exports = { getAlertsController, reportAlert };
