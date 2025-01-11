const { ethers } = require("hardhat");

async function main() {
    const contractAddress = "0xd9145CCE52D386f254917e481eB44e9943F39138"; // Replace with your deployed contract address
    const ProductRegistry = await ethers.getContractFactory("ProductRegistry");
    const productRegistry = await ProductRegistry.attach(contractAddress);

    // Register a new product
    const tx = await productRegistry.registerProduct(
        "prod123",                // productID
        "Laptop",                 // productName
        "TechCorp",               // manufacturer
        "2024-11-01",             // manufacturingDate
        ethers.utils.parseEther("1.5") // price in Ether
    );

    console.log("Transaction sent. Waiting for confirmation...");
    const receipt = await tx.wait();
    console.log("Product Registered in Tx:", receipt.transactionHash);

    // Fetch block details for the transaction
    const block = await ethers.provider.getBlock(receipt.blockNumber);
    console.log("Block Details:");
    console.log({
        blockNumber: block.number,
        timestamp: block.timestamp,
        miner: block.miner,
        transactions: block.transactions,
    });

    // Retrieve the product details
    const product = await productRegistry.getProduct("prod123");
    console.log("Product Details:");
    console.log({
        productName: product[0],
        manufacturer: product[1],
        manufacturingDate: product[2],
        price: ethers.utils.formatEther(product[3]) + " ETH",
    });
}

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});
