from celery.result import AsyncResult
from fastapi import APIRouter

from src.analysis.exceptions import InvalidTaskId, InvalidSpotifyId
from src.analysis.schemas import AnalysisTaskInit, AnalysisTaskResult, SPlaylistCreate
from src.analysis.service import AnalysisService
from src.analysis.tasks import analyse_playlist
from src.analysis.utils import encode_uuid, decode_uuid, is_valid_base64
from src.analysis.utils import validate_spotify_id
from src.exceptions import TaskNotCompleted
from src.models import TaskStatus

router = APIRouter(prefix='/analysis', tags=['analysis'])


@router.post('/start', response_model=AnalysisTaskInit)
async def start_analysis(playlist: SPlaylistCreate):
    if not validate_spotify_id(playlist.spotify_playlist_id):
        raise InvalidSpotifyId(playlist.spotify_playlist_id)

    task = analyse_playlist.delay(playlist)
    task_id = encode_uuid(task.task_id)  # base-64 task-id (only for better look of id on frontend)

    async with AnalysisService() as spotify:
        playlist_info = await spotify.playlist_info(playlist.spotify_id)

    return AnalysisTaskInit(task_id=task_id, info=playlist_info)


# PyCharm only ↓ because of celery.status return Any
# noinspection PyTypeChecker
@router.get('/status', response_model=TaskStatus)
async def get_analysis_status(task_id: str):
    if not is_valid_base64(task_id):
        raise InvalidTaskId(task_id=task_id)

    task = AsyncResult(decode_uuid(task_id))
    return TaskStatus(task_id=task.task_id, status=task.status)


@router.get('/result', response_model=AnalysisTaskResult)
async def get_analysis_result(task_id: str):
    if not is_valid_base64(task_id):
        raise InvalidTaskId(task_id=task_id)

    task = AsyncResult(decode_uuid(task_id))

    if task.status != 'SUCCESS':
        raise TaskNotCompleted(task_id=task.task_id)

    return AnalysisTaskResult(task_id=task.task_id, result=task.result)
