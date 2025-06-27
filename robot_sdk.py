
import uuid
from web3_interface import create_job, complete_job, confirm_delivery, reward_ubi

class RobotSDK:
    def __init__(self, robot_id, blockchain_address):
        self.robot_id = robot_id
        self.blockchain_address = blockchain_address
        self.assigned_task_id = None

    def submit_task(self, user_id, price, location):
        task_id = uuid.uuid4().hex
        tx_hash = create_job(task_id, self.blockchain_address, price)
        print(f"[{self.robot_id}] Task submitted. TX: {tx_hash}")
        return task_id

    def complete_task(self, task_id):
        tx_hash = complete_job(task_id)
        print(f"[{self.robot_id}] Task completed. TX: {tx_hash}")
        reward_ubi(self.blockchain_address)
        print(f"[{self.robot_id}] UBI rewarded.")
        return tx_hash

    def confirm_delivery(self, task_id):
        tx_hash = confirm_delivery(task_id)
        print(f"[{self.robot_id}] Delivery confirmed. TX: {tx_hash}")
        return tx_hash
