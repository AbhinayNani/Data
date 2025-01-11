// SPDX-License-Identifier: MIT
pragma solidity ^0.7.4;

contract a {
    struct s {
        string s1;
        uint num;
    }

    event LogMessage(string message);

    string public a1 = "One string";
    uint public a2 = 12;
    address public adde = 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4;
    address public send = msg.sender;
    // uint[] public a = [1, 2];
    uint public d = block.timestamp;

    function hello() public view {
        require(a2 > 20, "a2 is not greater than 20");
        // emit LogMessage("Hello");
    }

    uint public oneWei = 1 ether;
    bool public isOneWei = 1 ether == 1e18;
    uint public i = 0;
    mapping(address => uint) public atoi;

    function forever() public returns (uint) {
        // Here we run a loop until all of the gas is spent
        // and the transaction fails
        while (i < 10) {
            i += 1;
        }
        return atoi[adde];
    }

    s public sw;

    // Constructor to initialize the struct sw
    constructor() {
        sw.num = 10;
        sw.s1 = "memory";
    }

    // Function to return the value of sw.num
    function getSw() public view returns (uint) {
        return sw.num;
    }
    
}
