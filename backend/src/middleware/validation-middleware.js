const { buildApiResponse } = require('../utils/api-response');

const validate = (schema, property = 'body') => (req, res, next) => {
  const dataToValidate = req[property];

  const options = {
    abortEarly: false,
    allowUnknown: true,
    stripUnknown: true
  };

  const { error, value } = schema.validate(dataToValidate, options);

  if (error) {
    const errors = error.details.map((detail) => detail.message);

    return res
      .status(400)
      .json(buildApiResponse(false, 'Validation failed', { errors }));
  }

  req[property] = value;
  return next();
};

module.exports = { validate };
