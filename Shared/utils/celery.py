import os
from threading import Thread

from celery import Celery
from celery.result import allow_join_result
from specifications.tasks import Statuses


class CeleryApp(Celery):
    RMQ_USER = os.getenv('RMQ_USER')
    RMQ_PORT = os.getenv('RMQ_PORT')
    RMQ_HOST = os.getenv('RMQ_HOST')
    REDIS_PORT = os.getenv('REDIS_PORT')
    REDIS_HOST = os.getenv('REDIS_HOST')

    def __init__(self, name='celery'):
        super().__init__(
            main=name,
            broker=self._get_broker_string(),
            backend=self._get_backend_string()
        )

    def _get_broker_string(self):
        return f"amqp://{self.RMQ_USER}@{self.RMQ_HOST}:{self.RMQ_PORT}/"

    def _get_backend_string(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"


class CeleryConsumer(CeleryApp):
    """
    Task consumer
    """
    def __init__(self, name, tasks_list):
        super().__init__(name)
        self.name = name
        self.tasks_list = tasks_list

    def start_worker(self) -> None:
        for task in self.tasks_list:
            self.register_task(task)
        worker = self.Worker(
            queues=[task.name for task in self.tasks_list],
            hostname=self.name,
            loglevel='INFO'
        )
        worker.start()

    def start_thread(self) -> None:
        thread = Thread(
            target=self.start_worker,
            name='celery'
        )
        thread.start()


def produce_task(task_name: str, parameters: dict):
    """
    Synchronous task producer
    """
    celery_app = CeleryApp()
    task = celery_app.send_task(
        queue=task_name,
        name=task_name,
        kwargs=parameters
    )

    try:
        with allow_join_result():
            while not task.ready():
                continue
            result = task.get()
        return {
            'status': Statuses.SUCCESS,
            'result': result
        }
    except Exception as err:
        return {
            'status': Statuses.FAILURE,
            'error': err
        }
