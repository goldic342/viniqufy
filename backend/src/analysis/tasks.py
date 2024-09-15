from asyncio import run

from src.analysis.schemas import SPlaylistCreate
from src.analysis.service import AnalysisService
from src.tasks import celery


@celery.task
def analyse_playlist(playlist: SPlaylistCreate):
    return run(analyse_playlist_wrapper(playlist))


async def analyse_playlist_wrapper(playlist: SPlaylistCreate):
    async with AnalysisService() as service:
        return await service.get_uniqueness(playlist)
