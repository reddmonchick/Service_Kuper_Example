from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
logger = logging.getLogger(__name__)

def run_in_threads(tasks, max_workers=20):
    """
    Complete tasks in many thread
    :param tasks: List of function.
    :param max_workers: Max threads.
    :return: Gerenator result of tasks.
    """
    logger.info(f"Запуск {len(tasks)} задач в {max_workers} потоках")
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(task) for task in tasks]
        for future in as_completed(futures):
            try:
                yield future.result()
            except Exception as e:
                logger.error(f"Ошибка в потоке: {str(e)}", exc_info=True)