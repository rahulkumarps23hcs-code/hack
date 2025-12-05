const { logger } = require('../utils/logger');

const requestLogger = (req, res, next) => {
  logger.info('Incoming request', {
    method: req.method,
    path: req.originalUrl,
    ip: req.ip
  });

  next();
};

module.exports = { requestLogger };
