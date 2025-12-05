const express = require('express');
const { asyncHandler } = require('../utils/async-handler');
const { getUnsafeZones, getSafeZones } = require('../controllers/zone-controller');

const router = express.Router();

router.get('/unsafe', asyncHandler(getUnsafeZones));
router.get('/safe', asyncHandler(getSafeZones));

module.exports = router;
