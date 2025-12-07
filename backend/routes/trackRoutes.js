require('dotenv').config();
const express = require('express');
const router = express.Router();
const Track = require("../models/trackModel.js");
const path = require("path");
const axios = require("axios");
const fs = require("fs");
const multer = require('multer');
const FormData = require('form-data');
const auth = require('../middleware/auth');

// Configure multer for file uploads
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const uploadDir = 'uploads/';
    // Create uploads directory if it doesn't exist
    if (!fs.existsSync(uploadDir)) {
      fs.mkdirSync(uploadDir, { recursive: true });
    }
    cb(null, uploadDir);
  },
  filename: (req, file, cb) => {
    cb(null, Date.now() + '-' + file.originalname);
  }
});

const upload = multer({ 
  storage: storage,
  limits: { fileSize: 10 * 1024 * 1024 } // 10MB limit
});

// POST /api/tracks/upload - Protected route
router.post('/upload', auth, upload.single('file'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ message: 'No file uploaded' });
    }
    
    const filePath = path.resolve(req.file.path);

    // Create form data to send to FastAPI
    const formData = new FormData();
    // FastAPI expects the file to be the only content in the form data
    formData.append('file', fs.createReadStream(filePath));

    // Get the headers from form-data
    const headers = {
      ...formData.getHeaders(),
      'Accept': 'application/json',
    };

    // Send file to FastAPI for analysis
    const response = await axios.post(process.env.FASTAPI_URL, formData, {
      headers,
      maxBodyLength: Infinity,
      maxContentLength: Infinity,
      // FastAPI expects the file in a specific format
      transformRequest: (data, headers) => {
        // Remove the Content-Type header, let form-data set it with the boundary
        delete headers['Content-Type'];
        return data;
      }
    });

    const track = new Track({
      user: req.user._id,
      filename: req.file.originalname,
      analysis: response.data
    });

    await track.save();
    
    // Clean up the uploaded file after processing
    fs.unlink(filePath, (err) => {
      if (err) console.error('Error deleting file:', err);
    });
    
    res.json(track);
  } catch (err) {
    console.error('Error in /upload:', err);
    
    // Clean up the uploaded file if there was an error
    if (req.file && req.file.path) {
      fs.unlink(req.file.path, (unlinkErr) => {
        if (unlinkErr) console.error('Error cleaning up file after error:', unlinkErr);
      });
    }
    
    // More specific error messages based on the error type
    if (err.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      res.status(err.response.status).json({
        message: 'Error from FastAPI service',
        error: err.response.data
      });
    } else if (err.request) {
      // The request was made but no response was received
      res.status(503).json({
        message: 'FastAPI service unavailable',
        error: 'Could not connect to the analysis service'
      });
    } else {
      // Something happened in setting up the request that triggered an Error
      res.status(500).json({
        message: 'Error processing your request',
        error: err.message
      });
    }
  }
});

module.exports = router;
