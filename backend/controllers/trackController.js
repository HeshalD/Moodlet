const Track = require("../models/Track");
const path = require("path");
const axios = require("axios");
const fs = require("fs");

exports.uploadTrack = async (req, res) => {
  try {
    const filePath = path.resolve(req.file.path);

    // Send file to FastAPI for analysis
    const response = await axios.post("http://127.0.0.1:8000/analyze/", fs.createReadStream(filePath), {
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
};
