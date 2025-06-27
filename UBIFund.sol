// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IERC20 {
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
    function transfer(address to, uint256 amount) external returns (bool);
}

contract UBIFund {
    address public admin;
    IERC20 public stablecoin;

    mapping(address => uint256) public accumulatedUBI;
    mapping(address => uint256) public lastClaim;

    uint256 public ubiRatePerService = 10 * 1e6; // 10 USDC per service

    event ServiceRewarded(address indexed recipient, uint256 amount);
    event UBIDistributed(address indexed recipient, uint256 amount);

    constructor(address _stablecoin) {
        admin = msg.sender;
        stablecoin = IERC20(_stablecoin);
    }

    function rewardServiceUsage(address recipient) external {
        // Only trusted systems (like escrow) should call this
        accumulatedUBI[recipient] += ubiRatePerService;
        emit ServiceRewarded(recipient, ubiRatePerService);
    }

    function claimUBI() external {
        uint256 amount = accumulatedUBI[msg.sender];
        require(amount > 0, "No UBI available");
        accumulatedUBI[msg.sender] = 0;
        lastClaim[msg.sender] = block.timestamp;
        require(stablecoin.transfer(msg.sender, amount), "Transfer failed");
        emit UBIDistributed(msg.sender, amount);
    }

    function updateRate(uint256 newRate) external {
        require(msg.sender == admin, "Only admin");
        ubiRatePerService = newRate;
    }

    function fundUBIPool(uint256 amount) external {
        require(stablecoin.transferFrom(msg.sender, address(this), amount), "Funding failed");
    }

    function emergencyWithdraw(address to, uint256 amount) external {
        require(msg.sender == admin, "Only admin");
        stablecoin.transfer(to, amount);
    }
}
