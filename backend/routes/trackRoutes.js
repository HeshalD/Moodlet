require('dotenv').config();
const express = require('express');
const router = express.Router();
const Track = require("../models/trackModel.js");
const path = require("path");
const axios = require("axios");
const fs = require("fs");

// POST /api/tracks/upload
router.post('/upload', async (req, res) => {
  try {
    const filePath = path.resolve(req.file.path);

    // Send file to FastAPI for analysis
    const response = await axios.post(process.env.FASTAPI_URL, fs.createReadStream(filePath), {
      headers: { "Content-Type": "audio/wav" }
    });

    const track = new Track({
      user: req.user._id,
      filename: req.file.originalname,
      analysis: response.data
    });

    await track.save();
    res.json(track);
  } catch (err) {
    console.error(err);
    res.status(500).send("Error analyzing track");
  }
});

module.exports = router;
