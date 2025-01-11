const express = require("express");
const cors = require("cors");
const path = require("path");
const { MongoClient } = require("mongodb");

const serv = express();
const corsOptions = {
  origin: "http://localhost:5173", // Ensure this matches your front-end URL
};

serv.use(cors(corsOptions));
serv.use(express.json());

serv.use(express.static(path.join(__dirname, "public")));
serv.use("/scripts", express.static(path.join(__dirname, "scripts")));

serv.get("/", (req, res) => {
  res.send("Hello, world!");
});

let db;

const connectToDb = (callback) => {
  MongoClient.connect("mongodb://localhost:27017", { useUnifiedTopology: true })
    .then((client) => {
      db = client.db("LoginUserData"); // Replace with your database name
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

// Endpoint to get all users
serv.get("/", (req, res) => {
  if (!db) {
    return res.status(500).json({ error: "Database not connected" });
  }
  let users = [];
  db.collection("Users")
    .find()
    .sort()
    .forEach((user) => users.push(user))
    .then(() => {
      res.status(200).json(users);
    })
    .catch((err) => {
      console.error("Error fetching documents:", err);
      res.status(500).json({ error: "Could not fetch the documents" });
    });
});

// Endpoint to add a new user with duplicate check
serv.post("/signup", async (req, res) => {
  if (!db) {
    return res.status(500).json({ error: "Database not connected" });
  }

  const { email, password } = req.body;

  try {
    const user = await db.collection("Users").findOne({ email });

    if (user) {
      return res.status(409).json({ error: "User with this email already exists" });
    }

    // If the user does not exist, create a new user
    const result = await db.collection("Users").insertOne({ email, password });
    res.status(201).json(result);
  } catch (err) {
    res.status(500).json({ error: "Could not create user" });
  }
});

serv.post("/signin", async (req, res) => {
  if (!db) {
    return res.status(500).json({ error: "Database not connected" });
  }
  const { email, password } = req.body;

  try {
    const user = await db.collection("Users").findOne({ email, password });

    if (!user) {
      return res.status(401).json({ error: "Invalid email or password" });
    }

    res.status(200).json({ message: "Sign-in successful" });
  } catch (err) {
    res.status(500).json({ error: "Could not sign in" });
  }
});


serv.get("/Home", async (req, res) => {
  if (!db) {
    return res.status(500).json({ error: "Database not connected" });
  }
  const  email = req.query.email;
  try {
    const user = await db.collection("Users").findOne({ email});
    if (!user) {
      return res.status(401).json({ error: "Invalid email or password" });
    }
    // const token = generateToken(userData); // Implement token generation
    //   return res.json({ user: userData, token });
    res.status(200).json(user);
  } catch (err) {
    res.status(500).json({ error: "Could not sign in" });
  }
});
serv.listen(9200, () => {
  console.log("Server is running on port 9200");
});