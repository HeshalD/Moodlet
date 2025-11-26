const mongoose = require("mongoose");

const trackSchema = new mongoose.Schema({
  user: { type: mongoose.Schema.Types.ObjectId, ref: "User" },
  filename: String,
  analysis: Object,
}, { timestamps: true });

module.exports = mongoose.model("Track", trackSchema);
