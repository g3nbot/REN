import time
import random
from typing import Dict
from communication import Message, CommandType

class TaskRequest:
    def __init__(self, user_id, description, price, location):
        self.task_id = str(uuid.uuid4())
        self.user_id = user_id
        self.description = description
        self.price = price
        self.location = location
        self.status = "PENDING"
        self.assigned_robot = None

class Robot:
    def __init__(self, robot_id, location):
        self.robot_id = robot_id
        self.location = location
        self.status = "IDLE"
        self.wallet = 100.0
        robot_registry[self.robot_id] = self

    def receive_task(self, task: TaskRequest):
        print(f"[{self.robot_id}] 📥 Task: {task.description} @ {task.location}")
        if self.status == "IDLE":
            accept = random.choice([True, False])
            if accept:
                self.status = "BUSY"
                task.status = "ASSIGNED"
                task.assigned_robot = self.robot_id
                print(f"[{self.robot_id}] ✅ Accepted {task.task_id}")
                return True
        return False

    def complete_task(self, task: TaskRequest):
        self.wallet += task.price
        task.status = "COMPLETED"
        self.status = "IDLE"
        print(f"[{self.robot_id}] 🏁 Completed {task.task_id}, Balance: ${self.wallet:.2f}")

class DispatchHub:
    def __init__(self):
        self.tasks: Dict[str, TaskRequest] = {}

    def request_task(self, user_id, description, price, location):
        task = TaskRequest(user_id, description, price, location)
        self.tasks[task.task_id] = task
        self.dispatch_task(task)

    def dispatch_task(self, task: TaskRequest):
        print(f"[DISPATCH] 🚦 Task: {task.description} @ {task.location}")
        for robot in robot_registry.values():
            if robot.location == task.location and robot.status == "IDLE":
                if robot.receive_task(task):
                    print(f"[DISPATCH] 🚗 Task {task.task_id} -> {robot.robot_id}")
                    return
        print(f"[DISPATCH] ❌ No robots accepted. Retrying...")
        time.sleep(5)
        self.dispatch_task(task)

robot_registry: Dict[str, Robot] = {}

if __name__ == "__main__":
    import uuid
    r1 = Robot("R1", "Downtown")
    r2 = Robot("R2", "Downtown")
    r3 = Robot("R3", "Uptown")

    hub = DispatchHub()
    hub.request_task("UserA", "Deliver sushi", 10.0, "Downtown")
    hub.request_task("UserB", "Pick up groceries", 12.0, "Uptown")

    for task in hub.tasks.values():
        if task.status == "ASSIGNED":
            robot = robot_registry[task.assigned_robot]
            robot.complete_task(task)
