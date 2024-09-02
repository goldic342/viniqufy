from uuid import UUID, uuid4

from fastapi import APIRouter, BackgroundTasks, HTTPException

from src.spotify.schemas import SpotifyPlaylistStart, SpotifyTask, SpotifyTaskInitialization
from src.spotify.service import SpotifyService
from src.spotify.utils import validate_spotify_id

router = APIRouter(prefix='/spotify', tags=['spotify'])

# Later on tasks will be stored in database (Postgres or redis), this is MVP for now
# WARNING: DO NOT USE THIS IN PRODUCTION
tasks: list[SpotifyTask] = []


def get_task(task: SpotifyTask | UUID) -> SpotifyTask | None:
    # May moved to utils, but standing here for global tasks scope
    global tasks

    if isinstance(task, UUID):
        try:
            task = [t for t in tasks if task == t.task_id][0]
        except IndexError:
            return None
    try:
        return tasks[tasks.index(task)]
    except ValueError:
        return None


async def service_analysis_wrapper(task: SpotifyTask, playlist: SpotifyPlaylistStart):
    # In context of MVP index won't be changed during analysis
    current_task = get_task(task)
    current_task.status = "in_progress"

    async with SpotifyService() as spotify:
        uniqueness = await spotify.get_uniqueness(playlist)
        current_task.status = "completed"
        current_task.result = uniqueness


@router.post('/analysis', response_model=SpotifyTaskInitialization)
async def start_analysis(playlist: SpotifyPlaylistStart, background_tasks: BackgroundTasks):
    if not validate_spotify_id(playlist.spotify_id):
        raise HTTPException(status_code=400, detail='Spotify id is not valid')

    task = SpotifyTask(task_id=uuid4(), status="created")
    tasks.append(task)

    # Add task to tasks list
    background_tasks.add_task(service_analysis_wrapper, task, playlist)

    async with SpotifyService() as spotify:
        playlist_info = await spotify.playlist_info(playlist.spotify_id)

    return SpotifyTaskInitialization(task_id=task.task_id, info=playlist_info, status=task.status)


@router.get('/analysis-status', response_model=SpotifyTask)
async def get_analysis_status(task_id: UUID):
    task = get_task(task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task