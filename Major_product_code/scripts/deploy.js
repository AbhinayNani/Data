const hre = require("hardhat");

async function main() {
    // Get the contract factory
    const ProductRegistry = await hre.ethers.getContractFactory("ProductRegistry");

    // Deploy the contract
    const productRegistry = await ProductRegistry.deploy();

    // Wait for deployment to complete
    await productRegistry.deployed();

    console.log("ProductRegistry deployed to:", productRegistry.address);
}

// Execute the script
main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});
