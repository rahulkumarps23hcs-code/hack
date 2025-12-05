const Alert = require('../models/alert-model');

const createAlert = async ({ type, severity, timestamp, location, description, userId }) => {
  const alert = await Alert.create({
    type,
    severity,
    timestamp: timestamp || new Date(),
    location,
    description,
    reportedBy: userId || null
  });

  return alert;
};

const getAlerts = async () => {
  const alerts = await Alert.find().sort({ timestamp: -1 }).limit(100);
  return alerts;
};

module.exports = { createAlert, getAlerts };
