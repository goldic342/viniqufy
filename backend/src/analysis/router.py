from fastapi import APIRouter, Depends

from src.analysis.dependencies import get_analysis_task
from src.analysis.exceptions import InvalidSpotifyId
from src.analysis.schemas import AnalysisTaskInit, AnalysisTaskResult, SPlaylistCreate
from src.analysis.service import AnalysisService
from src.analysis.tasks import analyse_playlist
from src.analysis.utils import encode_uuid, decode_uuid
from src.analysis.utils import validate_spotify_id
from src.exceptions import TaskNotCompleted
from src.models import TaskStatus

router = APIRouter(prefix='/analysis', tags=['analysis'])


@router.post('/start', response_model=AnalysisTaskInit)
async def start_analysis(playlist: SPlaylistCreate):
    if not validate_spotify_id(playlist.spotify_playlist_id):
        raise InvalidSpotifyId(playlist.spotify_playlist_id)

    async with AnalysisService() as spotify:
        playlist_info, version_id = await spotify.playlist_info(playlist.spotify_playlist_id)

    task = analyse_playlist.delay(playlist, version_id)
    task_id = encode_uuid(task.task_id)  # base-64 task-id (only for better look of id on frontend)

    return AnalysisTaskInit(task_id=task_id, info=playlist_info)


# PyCharm only ↓ because of celery.status return Any
# noinspection PyTypeChecker
@router.get('/status', response_model=TaskStatus)
async def get_analysis_status(task=Depends(get_analysis_task)):
    base_64_task_id = encode_uuid(task.task_id)
    return TaskStatus(task_id=base_64_task_id, status=task.status)


@router.get('/result', response_model=AnalysisTaskResult)
async def get_analysis_result(task=Depends(get_analysis_task)):
    base_64_task_id = encode_uuid(task.task_id)

    if task.status != 'SUCCESS':
        raise TaskNotCompleted(task_id=task.task_id)

    return AnalysisTaskResult(task_id=base_64_task_id, result=task.result)
