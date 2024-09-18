from asyncio import get_event_loop
from uuid import UUID

from src.analysis.schemas import SPlaylistCreate
from src.analysis.service import AnalysisService
from src.tasks import celery
from celery import Task


@celery.task(bind=True)
def analyse_playlist(self: Task, playlist: SPlaylistCreate, version_id: UUID):
    loop = get_event_loop()
    return loop.run_until_complete(analyse_playlist_wrapper(playlist, version_id, self.request.id))


async def analyse_playlist_wrapper(playlist: SPlaylistCreate, version_id: UUID, task_id: UUID):
    async with AnalysisService() as service:
        return await service.analyze_playlist(playlist, version_id, task_id)
