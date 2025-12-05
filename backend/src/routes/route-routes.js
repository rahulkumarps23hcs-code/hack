const express = require('express');
const { asyncHandler } = require('../utils/async-handler');
const { getSaferRouteController } = require('../controllers/route-controller');

const router = express.Router();

router.get('/safer', asyncHandler(getSaferRouteController));

module.exports = router;
