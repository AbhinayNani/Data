//SPDX-License-Identifier:MIT
pragma solidity ^0.7.2;

contract pay{
 
    address payable public owner;

    constructor()  {
	owner=payable(msg.sender);
    }

    function deposit() external payable {}
    function getBalance() external view returns (uint) {
	return address(this).balance;
    }

}
