# infrastructure/utils/concurrency_utils.py (или просто внутри парсера)

import asyncio
import logging

logger = logging.getLogger(__name__)

async def run_concurrently(coroutines, max_concurrent=20):
    """
    Выполняет корутины конкурентно с ограничением.
    """
    results = []
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def run_with_semaphore(coro):
        async with semaphore:
            return await coro

    tasks = [run_with_semaphore(coro) for coro in coroutines]
    

    task_results = await asyncio.gather(*tasks, return_exceptions=True)

    for res in task_results:
        if isinstance(res, Exception):
            logger.error(f"Ошибка в конкурентной задаче: {res}", exc_info=True)
        else:
            if isinstance(res, list):
                results.extend(res)
            else:
                results.append(res)
    return results