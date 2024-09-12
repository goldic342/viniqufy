from typing import Any, Literal

from pydantic import BaseModel


class Task(BaseModel):
    task_id: str


class TaskStatus(Task):
    status: Literal['PENDING', 'FAILED', 'SUCCESS', 'REVOKED', 'STARTED']


class TaskResult(Task):
    result: Any


class TaskInit(Task):
    """
    Represents a task with additional initialization data.
    Use this class when you need to provide supplementary information during task initialization
    """
    info: Any
