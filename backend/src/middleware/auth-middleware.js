const { verifyToken } = require('../utils/jwt-utils');
const { buildApiResponse } = require('../utils/api-response');
const User = require('../models/user-model');

const authMiddleware = async (req, res, next) => {
  try {
    const authHeader = req.headers.authorization;

    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res
        .status(401)
        .json(buildApiResponse(false, 'Authorization token missing', null));
    }

    const token = authHeader.split(' ')[1];
    const decoded = verifyToken(token);
    const user = await User.findById(decoded.id);

    if (!user) {
      return res
        .status(401)
        .json(buildApiResponse(false, 'User not found', null));
    }

    req.user = user;
    return next();
  } catch (error) {
    return res
      .status(401)
      .json(buildApiResponse(false, 'Invalid or expired token', null));
  }
};

module.exports = { authMiddleware };
