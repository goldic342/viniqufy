from fastapi import HTTPException


class CustomHTTPException(HTTPException):
    """Base class for all custom HTTP exceptions."""

    def __init__(self, detail: str, status_code: int = 400, error_code='INTERNAL_ERROR'):
        super().__init__(status_code=status_code, detail={
            'message': detail,
            'error_code': error_code
        })
        self.error_code = error_code

    def __str__(self):
        return f"Error: {self.detail} (HTTP {self.status_code}, Code: {self.error_code})"

    def to_dict(self):
        return {
            "detail": self.detail,
            "status_code": self.status_code,
            "error_code": self.error_code,
        }


class TaskException(CustomHTTPException):
    """Base class for all celery task exceptions."""

    def __init__(self, task_id: str, detail: str = "Task error", status_code: int = 500, error_code: str = 'INTERNAL'):
        super().__init__(detail=detail, status_code=status_code, error_code=f"TASK_{error_code}_ERROR")
        self.task_id = task_id  # Celery task id

    def __str__(self) -> str:
        return f"Task ID: {self.task_id} - {self.detail} (HTTP {self.status_code}) Code: TASK_{self.error_code}_ERROR"


class TaskNotCompleted(TaskException):
    def __init__(self, task_id: str):
        detail = "Task not completed yet"
        super().__init__(task_id, detail, error_code='NOT_COMPLETED', status_code=400)


# NOTE: In celery vanilla there is no implementation of `not found task`,
# but we can use task from db (Analysis) to raise such error
# None of these solutions work properly: https://stackoverflow.com/questions/9824172/find-out-whether-celery-task-exists
# See this issues on github: https://github.com/celery/celery/issues/3596
class TaskNotFound(TaskException):
    def __init__(self, task_id: str):
        detail = "Task not found"
        super().__init__(task_id, detail, error_code='NOT_FOUND', status_code=404)
