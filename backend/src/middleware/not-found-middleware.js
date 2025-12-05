const { buildApiResponse } = require('../utils/api-response');

const notFoundHandler = (req, res, next) => {
  res.status(404).json(buildApiResponse(false, 'Route not found', null));
};

module.exports = { notFoundHandler };
