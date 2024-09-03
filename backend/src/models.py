from typing import Any, Literal, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel


class Playlist(BaseModel):
    name: str
    owner: str | None
    id: UUID = uuid4()
    tracks_count: int


class Artist(BaseModel):
    name: str
    id: UUID = uuid4()


class Track(BaseModel):
    name: str
    id: UUID = uuid4()
    artists: list[Artist]


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
