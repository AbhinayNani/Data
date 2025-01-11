const express = require("express");
const cors = require("cors");
const path = require("path");
const { MongoClient } = require("mongodb");

const serv = express();
const corsOptions = {
  origin: "http://localhost:7200", // Ensure this matches your front-end URL
};

serv.use(cors(corsOptions));
serv.use(express.json());

serv.use(express.static(path.join(__dirname, "public")));
serv.use("/scripts", express.static(path.join(__dirname, "scripts")));

let db;

// Root route - responds with "Hello, world!" for GET requests to "/"
// Connect to the database
const connectToDb = (callback) => {
    MongoClient.connect("mongodb://localhost:27017", { useNewUrlParser: true }) // Removed useUnifiedTopology
    .then((client) => {
        db = client.db("login"); // Ensure this is your correct database
        callback();
    })
    .catch((err) => {
        console.error("Failed to connect to the database", err);
        callback(err);
    });
};

const getDb = () => db;

connectToDb((err) => {
    if (!err) {
        console.log("Connected to database");
    } else {
        console.error("Failed to connect to the database", err);
    }
});

serv.get("/", (req, res) => {
    res.send("Hello, world!");
  });
  
// Fetch all users (from logs collection)
serv.get("/", (req, res) => {
  if (!db) {
    return res.status(500).json({ error: "Database not connected" });
  }
  
  let users = [];
  
  db.collection("logs") // Ensure the collection is correct
    .find()
    .toArray()
    .then((docs) => {
      if (docs.length > 0) {
        console.log("Users fetched: ", docs);
        res.status(200).json(docs); // Respond with user data
      } else {
        console.log("No users found");
        res.status(200).json([]); // Empty response if no users found
      }
    })
    .catch((err) => {
      console.error("Error fetching users:", err);
      res.status(500).json({ error: "Could not fetch users" });
    });
});

// Signup endpoint
// serv.post("/signup", async (req, res) => {
//   if (!db) {
//     return res.status(500).json({ error: "Database not connected" });
//   }

//   const { email, password } = req.body;

//   try {
//     const user = await db.collection("Users").findOne({ email });

//     if (user) {
//       return res.status(409).json({ error: "User with this email already exists" });
//     }

//     const result = await db.collection("Users").insertOne({ email, password });
//     res.status(201).json(result);
//   } catch (err) {
//     res.status(500).json({ error: "Could not create user" });
//   }
// });

// // Signin endpoint
// serv.post("/signin", async (req, res) => {
//   if (!db) {
//     return res.status(500).json({ error: "Database not connected" });
//   }
//   const { email, password } = req.body;

//   try {
//     const user = await db.collection("Users").findOne({ email, password });

//     if (!user) {
//       return res.status(401).json({ error: "Invalid email or password" });
//     }

//     res.status(200).json({ message: "Sign-in successful" });
//   } catch (err) {
//     res.status(500).json({ error: "Could not sign in" });
//   }
// });

// // Home endpoint with query parameter
// serv.get("/Home", async (req, res) => {
//   if (!db) {
//     return res.status(500).json({ error: "Database not connected" });
//   }
//   const email = req.query.email;
  
//   try {
//     const user = await db.collection("Users").findOne({ email });

//     if (!user) {
//       return res.status(401).json({ error: "Invalid email or password" });
//     }

//     res.status(200).json(user);
//   } catch (err) {
//     res.status(500).json({ error: "Could not fetch user" });
//   }
// });

// Server listening on port 7200
serv.listen(7200, () => {
  console.log("Server is running on port 7200");
});
