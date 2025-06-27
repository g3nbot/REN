
from web3 import Web3
import json

# Configure your connection and contract details
INFURA_URL = "https://sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID"
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

ESCROW_ADDRESS = "0xYourEscrowContractAddress"
UBI_ADDRESS = "0xYourUBIContractAddress"
STABLECOIN_ADDRESS = "0xYourUSDCAddress"
PRIVATE_KEY = "0xYourPrivateKey"
ACCOUNT_ADDRESS = web3.eth.account.from_key(PRIVATE_KEY).address

# Load ABI files (save your ABI from compilation)
with open("RobotEscrowABI.json") as f:
    escrow_abi = json.load(f)
with open("UBIFundABI.json") as f:
    ubi_abi = json.load(f)

escrow = web3.eth.contract(address=ESCROW_ADDRESS, abi=escrow_abi)
ubi = web3.eth.contract(address=UBI_ADDRESS, abi=ubi_abi)

def build_and_send_tx(function_call):
    nonce = web3.eth.get_transaction_count(ACCOUNT_ADDRESS)
    tx = function_call.build_transaction({
        "from": ACCOUNT_ADDRESS,
        "nonce": nonce,
        "gas": 200000,
        "gasPrice": web3.eth.gas_price
    })
    signed_tx = web3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return tx_hash.hex()

# Example calls:
def create_job(task_id, robot_address, amount_usdc):
    function = escrow.functions.createJob(task_id, robot_address, int(amount_usdc * 1e6))
    return build_and_send_tx(function)

def complete_job(task_id):
    function = escrow.functions.completeJob(task_id)
    return build_and_send_tx(function)

def confirm_delivery(task_id):
    function = escrow.functions.confirmDelivery(task_id)
    return build_and_send_tx(function)

def reward_ubi(recipient_address):
    function = ubi.functions.rewardServiceUsage(recipient_address)
    return build_and_send_tx(function)

def claim_ubi():
    function = ubi.functions.claimUBI()
    return build_and_send_tx(function)
