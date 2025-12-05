const bcrypt = require('bcryptjs');
const User = require('../models/user-model');
const { signToken } = require('../utils/jwt-utils');

const SALT_ROUNDS = 10;

const signupUser = async ({ name, phone, email, password }) => {
  const existingUser = await User.findOne({
    $or: [{ email }, { phone }]
  });

  if (existingUser) {
    const error = new Error('User with this email or phone already exists');
    error.statusCode = 409;
    throw error;
  }

  const passwordHash = await bcrypt.hash(password, SALT_ROUNDS);

  const user = await User.create({
    name,
    phone,
    email,
    passwordHash
  });

  const token = signToken({ id: user.id });

  return { user, token };
};

const loginUser = async ({ email, phone, password }) => {
  if (!email && !phone) {
    const error = new Error('Email or phone is required to login');
    error.statusCode = 400;
    throw error;
  }

  const query = email ? { email } : { phone };
  const user = await User.findOne(query);

  if (!user) {
    const error = new Error('Invalid credentials');
    error.statusCode = 401;
    throw error;
  }

  const isMatch = await bcrypt.compare(password, user.passwordHash);

  if (!isMatch) {
    const error = new Error('Invalid credentials');
    error.statusCode = 401;
    throw error;
  }

  const token = signToken({ id: user.id });

  return { user, token };
};

module.exports = { signupUser, loginUser };
