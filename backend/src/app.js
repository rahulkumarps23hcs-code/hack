const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');

const routes = require('./routes');
const { notFoundHandler } = require('./middleware/not-found-middleware');
const { errorHandler } = require('./middleware/error-middleware');
const { requestLogger } = require('./middleware/request-logger-middleware');

const app = express();

app.use(cors());
app.use(helmet());
app.use(morgan('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(requestLogger);

app.use('/', routes);

app.use(notFoundHandler);
app.use(errorHandler);

module.exports = app;
