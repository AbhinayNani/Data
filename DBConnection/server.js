const express = require('express');
const path = require('path');
const { MongoClient } = require('mongodb');

const app = express();
const port = 7200; // Port for the server

const uri = "mongodb://localhost:27017";
const dbName = "login"; // Replace with your database name
const collectionName = "logs"; // Replace with your collection name

let db;

app.use(express.json());

// Serve static files from the "public" directory
app.use(express.static(path.join(__dirname, 'public')));

// Connect to MongoDB
const connectToDb = async () => {
  try {
    const client = new MongoClient(uri); // No options needed for MongoDB Driver v4.0.0+
    await client.connect();
    db = client.db(dbName);
    console.log("Connected to database");
  } catch (err) {
    console.error("Failed to connect to the database", err);
  }
};

// Endpoint to get location by name and beach
app.get('/location/:name/:beaches', async (req, res) => {
  if (!db) {
    return res.status(500).json({ error: "Database not connected" });
  }

  const locationName = req.params.name; // Get the location name from the URL
  const beachName = req.params.beaches; // Get the beach name from the URL
  const frontendUrl = req.headers['frontend-url']; // Retrieve the frontend URL from headers

  console.log(`Request received from frontend URL: ${frontendUrl}`);

  try {
    const location = await db.collection(collectionName)
      .findOne({ name: beachName }, { projection: { _id: 0, latitude: 1, longitude: 1 } });

    if (!location) {
      return res.status(404).json({ error: "Location or beach not found" });
    }

    res.status(200).json(location);
  } catch (err) {
    console.error("Error fetching location:", err);
    res.status(500).json({ error: "Could not fetch location" });
  }
});

// Start the server
app.listen(port, async () => {
  await connectToDb(); // Ensure DB connection is established before starting the server
  console.log(`Server is running on port ${port}`);
});
