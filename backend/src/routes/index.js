const express = require('express');

const authRoutes = require('./auth-routes');
const userRoutes = require('./user-routes');
const alertRoutes = require('./alert-routes');
const sosRoutes = require('./sos-routes');
const zoneRoutes = require('./zone-routes');
const routeRoutes = require('./route-routes');
const safeSpotRoutes = require('./safe-spot-routes');
const reportRoutes = require('./report-routes');

const router = express.Router();

router.use('/auth', authRoutes);
router.use('/user', userRoutes);
router.use('/alerts', alertRoutes);
router.use('/sos', sosRoutes);
router.use('/zones', zoneRoutes);
router.use('/routes', routeRoutes);
router.use('/safe-spots', safeSpotRoutes);
router.use('/report', reportRoutes);

module.exports = router;
