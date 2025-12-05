const express = require('express');
const { asyncHandler } = require('../utils/async-handler');
const { getMe } = require('../controllers/auth-controller');
const { authMiddleware } = require('../middleware/auth-middleware');

const router = express.Router();

router.get('/me', authMiddleware, asyncHandler(getMe));

module.exports = router;
