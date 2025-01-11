const express = require("express");
const Web3 = require("web3");
const QRCode = require("qrcode");
const cors = require("cors");
require("dotenv").config(); // For environment variables

const app = express();
app.use(cors());
app.use(express.json());

// Environment variables for dynamic configuration
const RPC_URL ="http://127.0.0.1:8545";
const CONTRACT_ADDRESS ="0x8626f6940E2eb28930eFb4CeF49B2d1F2C9C1199";

const web3 = new Web3(RPC_URL);
const contractABI = require('../artifacts/contracts/contract.sol/ProductRegistry.json').abi;
const contract = new web3.eth.Contract(contractABI, CONTRACT_ADDRESS);

// Endpoint to register a product
app.post("/register", async (req, res) => {
    const { productID, productName, manufacturer, manufacturingDate, price } = req.body;

    // Input validation
    if (!productID || !productName || !manufacturer || !manufacturingDate || !price) {
        return res.status(400).json({ error: "All fields are required" });
    }

    try {
        const accounts = await web3.eth.getAccounts();

        // Interact with the smart contract
        await contract.methods
            .registerProduct(productID, productName, manufacturer, manufacturingDate, price)
            .send({ from: accounts[0] });

        // Create a structured QR code content
        const productTag = JSON.stringify({
            productID,
            productName,
            manufacturer,
            manufacturingDate,
            price,
        });

        // Generate the QR code
        const qrCode = await QRCode.toDataURL(productTag);

        res.json({ message: "Product registered successfully", qrCode });
    } catch (error) {
        console.error("Error registering product:", error.message);
        res.status(500).json({ error: "Failed to register product on blockchain" });
    }
});

// Endpoint to verify a product
app.get("/verify/:productID", async (req, res) => {
    const productID = req.params.productID;

    try {
        const product = await contract.methods.getProduct(productID).call();


        // If no exception, the product exists
        res.json({
            productName: product[0],
            manufacturer: product[1],
            manufacturingDate: product[2],
            price: product[3],
            authentic: true,
        });
    } catch (error) {
        console.error("Error verifying product:", error.message);
        res.status(404).json({ authentic: false, message: "Product not found" });
    }
});
app.get("/test", (req, res) => {
    res.send("Test endpoint is working!");
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
