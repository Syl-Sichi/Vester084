from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Task:
    command: str
    id: str = field(default_factory=lambda: str(uuid4()))
    status: TaskStatus = TaskStatus.PENDING
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    result: dict = field(default_factory=dict)


class TaskManager:
    def __init__(self) -> None:
        self.tasks: dict[str, Task] = {}

    def create(self, command: str) -> Task:
        task = Task(command=command)
        self.tasks[task.id] = task
        return task

    def update(self, task_id: str, status: TaskStatus, result: dict | None = None) -> Task:
        task = self.tasks[task_id]
        task.status = status
        if result is not None:
            task.result = result
        return task
