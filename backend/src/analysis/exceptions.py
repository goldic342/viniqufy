from src.exceptions import CustomHTTPException, TaskException


class InvalidSpotifyId(CustomHTTPException):
    def __init__(self, spotify_id: str):
        detail = f"Invalid Spotify ID: {spotify_id}"
        super().__init__(detail, status_code=400, error_code='INVALID_SPOTIFY_ID')


class InvalidTaskId(TaskException):
    def __init__(self, task_id: str):
        detail = f"Invalid base-64 Task ID: {task_id}"
        super().__init__(task_id, detail, status_code=400, error_code='INVALID_TASK_ID')
