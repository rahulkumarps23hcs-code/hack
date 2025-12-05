const Joi = require('joi');

const locationSchema = Joi.object({
  lat: Joi.number().required(),
  lng: Joi.number().required()
});

const signupSchema = Joi.object({
  name: Joi.string().min(2).max(100).required(),
  phone: Joi.string().min(5).max(20).required(),
  email: Joi.string().email().required(),
  password: Joi.string().min(6).max(100).required()
});

const loginSchema = Joi.object({
  email: Joi.string().email(),
  phone: Joi.string().min(5).max(20),
  password: Joi.string().min(6).max(100).required()
}).xor('email', 'phone');

const alertReportSchema = Joi.object({
  type: Joi.string().min(2).max(100).required(),
  severity: Joi.string().min(2).max(50).required(),
  timestamp: Joi.date().iso().optional(),
  location: locationSchema.required(),
  description: Joi.string().max(1000).allow('', null)
});

const sosTriggerSchema = Joi.object({
  location: locationSchema.optional(),
  description: Joi.string().max(2000).allow('', null)
});

module.exports = {
  signupSchema,
  loginSchema,
  alertReportSchema,
  sosTriggerSchema
};
