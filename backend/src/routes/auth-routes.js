const express = require('express');
const { asyncHandler } = require('../utils/async-handler');
const { signup, login } = require('../controllers/auth-controller');
const { validate } = require('../middleware/validation-middleware');
const { signupSchema, loginSchema } = require('../middleware/validation-schemas');

const router = express.Router();

router.post('/signup', validate(signupSchema), asyncHandler(signup));
router.post('/login', validate(loginSchema), asyncHandler(login));

module.exports = router;
