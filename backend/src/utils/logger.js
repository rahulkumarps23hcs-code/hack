const formatTimestamp = () => new Date().toISOString();

const log = (level, message, meta) => {
  const base = `[${formatTimestamp()}] [${level.toUpperCase()}] ${message}`;

  if (meta) {
    // eslint-disable-next-line no-console
    console.log(base, JSON.stringify(meta));
  } else {
    // eslint-disable-next-line no-console
    console.log(base);
  }
};

const logger = {
  info: (message, meta) => log('info', message, meta),
  warn: (message, meta) => log('warn', message, meta),
  error: (message, meta) => log('error', message, meta)
};

module.exports = { logger };
