// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IERC20 {
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
    function transfer(address to, uint256 amount) external returns (bool);
}

contract RobotEscrow {
    address public owner;
    IERC20 public stablecoin;

    struct Job {
        address user;
        address robot;
        uint256 amount;
        bool isCompleted;
        bool isConfirmed;
    }

    mapping(bytes32 => Job) public jobs;

    event JobCreated(bytes32 taskId, address indexed user, address indexed robot, uint256 amount);
    event JobCompleted(bytes32 taskId);
    event JobConfirmed(bytes32 taskId);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this.");
        _;
    }

    constructor(address _stablecoin) {
        owner = msg.sender;
        stablecoin = IERC20(_stablecoin);
    }

    function createJob(bytes32 taskId, address robot, uint256 amount) external {
        require(jobs[taskId].user == address(0), "Job already exists");

        // Transfer stablecoin from user to contract
        require(stablecoin.transferFrom(msg.sender, address(this), amount), "Transfer failed");

        jobs[taskId] = Job({
            user: msg.sender,
            robot: robot,
            amount: amount,
            isCompleted: false,
            isConfirmed: false
        });

        emit JobCreated(taskId, msg.sender, robot, amount);
    }

    function completeJob(bytes32 taskId) external {
        Job storage job = jobs[taskId];
        require(msg.sender == job.robot, "Only assigned robot can complete");
        require(!job.isCompleted, "Already completed");

        job.isCompleted = true;
        emit JobCompleted(taskId);
    }

    function confirmDelivery(bytes32 taskId) external {
        Job storage job = jobs[taskId];
        require(msg.sender == job.user, "Only user can confirm");
        require(job.isCompleted, "Job not completed yet");
        require(!job.isConfirmed, "Already confirmed");

        job.isConfirmed = true;
        require(stablecoin.transfer(job.robot, job.amount), "Payout failed");

        emit JobConfirmed(taskId);
    }

    // Emergency function
    function withdraw(address to, uint256 amount) external onlyOwner {
        stablecoin.transfer(to, amount);
    }
}
