const { buildApiResponse } = require('../utils/api-response');
const { logger } = require('../utils/logger');

const errorHandler = (err, req, res, next) => {
  const statusCode = err.statusCode || 500;
  const message = err.message || (statusCode === 500 ? 'Internal server error' : 'Request failed');

  logger.error('Request error', {
    statusCode,
    message,
    stack: err.stack
  });

  res.status(statusCode).json(buildApiResponse(false, message, null));
};

module.exports = { errorHandler };
