const { buildApiResponse } = require('../utils/api-response');
const { signupUser, loginUser } = require('../services/auth-service');

const signup = async (req, res) => {
  const { name, phone, email, password } = req.body;

  if (!name || !phone || !email || !password) {
    const error = new Error('Name, phone, email and password are required');
    error.statusCode = 400;
    throw error;
  }

  const { user, token } = await signupUser({ name, phone, email, password });

  res.status(201).json(
    buildApiResponse(true, 'User signed up successfully', {
      user,
      token
    })
  );
};

const login = async (req, res) => {
  const { email, phone, password } = req.body;

  if (!password || (!email && !phone)) {
    const error = new Error('Password and either email or phone are required');
    error.statusCode = 400;
    throw error;
  }

  const { user, token } = await loginUser({ email, phone, password });

  res.json(
    buildApiResponse(true, 'User logged in successfully', {
      user,
      token
    })
  );
};

const getMe = async (req, res) => {
  const user = req.user;

  res.json(buildApiResponse(true, 'Current user fetched successfully', user));
};

module.exports = { signup, login, getMe };
