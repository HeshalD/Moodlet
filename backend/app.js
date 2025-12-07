require('dotenv').config();
const express = require("express");
const mongoose = require("mongoose");
const trackRoutes = require("./routes/trackRoutes");
const authRoutes= require('./routes/authRoutes');

const app = express();
app.use(express.json());

// Connect to MongoDB
mongoose.connect(process.env.MONGODB_URI)
  .then(() => console.log('Connected to MongoDB'))
  .catch(err => console.error('MongoDB connection error:', err));

app.use("/api/tracks", trackRoutes);
app.use('/api/auth', authRoutes);

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
