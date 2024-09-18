from celery.result import AsyncResult

from src.analysis.exceptions import InvalidTaskId
from src.analysis.utils import is_valid_base64, decode_uuid

async def get_analysis_task(task_id: str) -> AsyncResult:
    if not is_valid_base64(task_id):
        raise InvalidTaskId(task_id=task_id)

    # FIXME: analysis can have only one task_id, so we can't found analysis be task_id,
    # FIXME: I guess add o2m relation task_id and analysis_id
    # analysis = await analyzes.get(task_id=decode_uuid(task_id))
    #
    # if not analysis:
    #     raise TaskNotFound(task_id=task_id)
    analysis = AsyncResult(decode_uuid(task_id))

    return analysis
