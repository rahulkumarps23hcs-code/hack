const express = require('express');
const { asyncHandler } = require('../utils/async-handler');
const { triggerSos } = require('../controllers/sos-controller');
const { upload } = require('../middleware/upload-middleware');
const { authMiddleware } = require('../middleware/auth-middleware');
const { validate } = require('../middleware/validation-middleware');
const { sosTriggerSchema } = require('../middleware/validation-schemas');

const router = express.Router();

router.post(
  '/trigger',
  authMiddleware,
  upload.single('attachment'),
  validate(sosTriggerSchema),
  asyncHandler(triggerSos)
);

module.exports = router;
