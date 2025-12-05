const mongoose = require('mongoose');

const locationSchema = new mongoose.Schema(
  {
    lat: { type: Number, required: true },
    lng: { type: Number, required: true }
  },
  { _id: false }
);

const safeSpotSchema = new mongoose.Schema(
  {
    name: { type: String, required: true, trim: true },
    type: { type: String, required: true, trim: true },
    address: { type: String, required: true, trim: true },
    location: { type: locationSchema, required: true }
  },
  { timestamps: true }
);

safeSpotSchema.set('toJSON', {
  transform: (doc, ret) => {
    ret.id = ret._id.toString();
    delete ret._id;
    delete ret.__v;
    return ret;
  }
});

const SafeSpot = mongoose.model('SafeSpot', safeSpotSchema);

module.exports = SafeSpot;
