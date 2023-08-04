# dispatcher that allows only one task of each type to execute at once
import threading
from typing import Callable


class TaskDispatcher(object):
    """Ensures only one task of each type can execute at once."""

    _locks = {}

    @staticmethod
    def execute_task(task_type: str, task: Callable[[], None]):
        task_lock = TaskDispatcher._get_task_lock(task_type)
        task_lock.acquire()

        try:
            task()
        finally:
            task_lock.release()
            del TaskDispatcher._locks[task_type]

    @staticmethod
    def _get_task_lock(task_type):
        # Get the lock for the given task type from the dictionary
        # If the lock does not exist, create a new lock and store it in the dictionary
        if task_type not in TaskDispatcher._locks:
            TaskDispatcher._locks[task_type] = threading.Lock()
        return TaskDispatcher._locks[task_type]
