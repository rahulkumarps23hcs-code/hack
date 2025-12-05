const buildApiResponse = (success, message, data) => {
  const response = {
    success: Boolean(success),
    message: message || ''
  };

  if (typeof data === 'undefined') {
    response.data = null;
  } else {
    response.data = data;
  }

  return response;
};

module.exports = { buildApiResponse };
