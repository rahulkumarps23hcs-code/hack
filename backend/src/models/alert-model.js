const mongoose = require('mongoose');

const locationSchema = new mongoose.Schema(
  {
    lat: { type: Number, required: true },
    lng: { type: Number, required: true }
  },
  { _id: false }
);

const alertSchema = new mongoose.Schema(
  {
    type: { type: String, required: true, trim: true },
    severity: { type: String, required: true, trim: true },
    timestamp: { type: Date, default: Date.now, required: true },
    location: { type: locationSchema, required: true },
    description: { type: String, trim: true },
    reportedBy: { type: mongoose.Schema.Types.ObjectId, ref: 'User' }
  },
  { timestamps: true }
);

alertSchema.set('toJSON', {
  transform: (doc, ret) => {
    ret.id = ret._id.toString();
    delete ret._id;
    delete ret.__v;
    return ret;
  }
});

const Alert = mongoose.model('Alert', alertSchema);

module.exports = Alert;
