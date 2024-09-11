from typing import Any, Literal, Optional

from pydantic import BaseModel


class Task(BaseModel):
    task_id: str
    status: Literal["created", "in_progress", "completed"]
    result: Optional[Any] = None


class TaskInitialization(Task):
    """
    Represents a task with additional initialization data.
    Use this class when you need to provide supplementary information during task initialization
    """
    info: Any | None


class TaskStatusOutput(BaseModel):
    """
    Represents a task status response
    Use this if you need to show only task status, without any additional data
    """
    task_id: str
    status: Literal["created", "in_progress", "completed"]
