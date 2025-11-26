const express = require("express");
const mongoose = require("mongoose");
const trackRoutes = require("./routes/trackRoutes");

const app = express();
app.use(express.json());

mongoose.connect("mongodb+srv://heshal:12345@moodlet.qbw9mkj.mongodb.net/");

app.use("/api/tracks", trackRoutes);

app.listen(3000, () => console.log("Server running on port 3000"));
