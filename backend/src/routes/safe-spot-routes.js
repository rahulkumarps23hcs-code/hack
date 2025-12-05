const express = require('express');
const { asyncHandler } = require('../utils/async-handler');
const {
  getSafeSpotsController,
  getNearbySafeSpotsController
} = require('../controllers/safe-spot-controller');

const router = express.Router();

router.get('/', asyncHandler(getSafeSpotsController));
router.get('/nearby', asyncHandler(getNearbySafeSpotsController));

module.exports = router;
