from uuid import UUID, uuid4

from fastapi import APIRouter, BackgroundTasks, HTTPException

from src.spotify.schemas import SpotifyPlaylistStart
from src.spotify.service import SpotifyService
from src.spotify.utils import validate_spotify_id

router = APIRouter(prefix='/spotify', tags=['spotify'])

# Later on tasks will be stored in database (Postgres or redis), this is MVP for now
# WARNING: DO NOT USE THIS IN PRODUCTION
tasks: dict[UUID, dict[str | float]] = {}


async def service_analysis_wrapper(task_id: UUID, playlist: SpotifyPlaylistStart):
    tasks[task_id]["status"] = "in_progress"

    async with SpotifyService() as spotify:
        uniqueness = await spotify.get_uniqueness(playlist)
        tasks[task_id]["status"] = "completed"
        tasks[task_id]["result"] = uniqueness


@router.post('/analysis')
async def start_analysis(playlist: SpotifyPlaylistStart, background_tasks: BackgroundTasks):
    if not validate_spotify_id(playlist.spotify_id):
        raise HTTPException(status_code=400, detail='Spotify id is not valid')

    task_id = uuid4()
    tasks[task_id] = {"status": "created"}
    background_tasks.add_task(service_analysis_wrapper, task_id, playlist)

    return {'task_id': task_id}


@router.get('/analysis_status')
async def get_analysis_status(task_id: UUID):
    task = tasks.get(task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "id": task_id,
        "status": task["status"],
    }


@router.get('/analysis_result')
async def analysis(task_id: UUID):
    task = tasks.get(task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task["status"] != "completed":
        raise HTTPException(status_code=400, detail="Task not completed yet")

    return {"result": task["result"]}
