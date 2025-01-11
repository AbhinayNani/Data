const { MongoClient } = require('mongodb');

let dbConnection;

module.exports = {
  connectToDb: (cb) => {
    const uri = 'mongodb://localhost:27017/';

    // MongoDB connection without deprecated options
    MongoClient.connect(uri, { useNewUrlParser: true })
      .then(client => {
        dbConnection = client.db(); // Optionally specify your DB name here
        console.log("Connected to MongoDB");
        return cb();
      })
      .catch(err => {
        console.error("Error connecting to MongoDB:", err);
        return cb(err);
      });
  },

  getDb: () => dbConnection,
};
