import uuid
import json
import time
from enum import Enum

class CommandType(Enum):
    STATUS = "STATUS"
    MOVE = "MOVE"
    HELP = "HELP"
    ACK = "ACK"
    BROADCAST = "BROADCAST"
    TASK_ASSIGN = "TASK_ASSIGN"
    PAYMENT = "PAYMENT"

class Message:
    def __init__(self, sender_id, target_ids, command: CommandType, payload=None):
        self.message_id = str(uuid.uuid4())
        self.timestamp = time.time()
        self.sender_id = sender_id
        self.target_ids = target_ids
        self.command = command.value
        self.payload = payload or {}

    def to_json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json(data: str):
        msg = json.loads(data)
        return Message(
            sender_id=msg["sender_id"],
            target_ids=msg["target_ids"],
            command=CommandType(msg["command"]),
            payload=msg["payload"]
        )
