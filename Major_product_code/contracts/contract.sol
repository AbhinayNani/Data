// SPDX-License-Identifier: MIT
pragma solidity ^0.7.4;

contract ProductRegistry {
    struct Product {
        string productName;
        string manufacturer;
        string manufacturingDate;
        uint256 price;
        bool exists;
    }

    mapping(string => Product) private products;

    event ProductRegistered(string productID, string productName);

    // Add a product to the blockchain
    function registerProduct(
        string memory productID,
        string memory productName,
        string memory manufacturer,
        string memory manufacturingDate,
        uint256 price
    ) public {
        require(!products[productID].exists, "Product already registered");

        products[productID] = Product({
            productName: productName,
            manufacturer: manufacturer,
            manufacturingDate: manufacturingDate,
            price: price,
            exists: true
        });

        emit ProductRegistered(productID, productName);
    }

    // Retrieve product details
    function getProduct(string memory productID)
        public
        view
        returns (
            string memory productName,
            string memory manufacturer,
            string memory manufacturingDate,
            uint256 price
        )
    {
        require(products[productID].exists, "Product not found");

        Product memory product = products[productID];
        return (
            product.productName,
            product.manufacturer,
            product.manufacturingDate,
            product.price
        );
    }
}
