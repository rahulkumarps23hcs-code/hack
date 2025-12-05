const express = require('express');
const { asyncHandler } = require('../utils/async-handler');
const { getAlertsController, reportAlert } = require('../controllers/alert-controller');
const { authMiddleware } = require('../middleware/auth-middleware');
const { validate } = require('../middleware/validation-middleware');
const { alertReportSchema } = require('../middleware/validation-schemas');

const router = express.Router();

router.get('/', asyncHandler(getAlertsController));
router.post('/report', authMiddleware, validate(alertReportSchema), asyncHandler(reportAlert));

module.exports = router;
