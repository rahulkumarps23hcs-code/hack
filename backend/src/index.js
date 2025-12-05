const dotenv = require('dotenv');

dotenv.config();

const app = require('./app');
const { connectDb } = require('./config/db');

const port = process.env.PORT || 5000;

connectDb()
  .then(() => {
    app.listen(port, () => {
      console.log(`Server listening on port ${port}`);
    });
  })
  .catch((error) => {
    console.error('Failed to start server due to DB connection error', error);
    process.exit(1);
  });
