from locust import TaskSet


class BaseTask(TaskSet):
    def on_start(self):
        self.client.headers = {'Authorization': f'Bearer {self.user.token}'}


# tasks/api_tasks.py
import random
from locust import task
from .base_task import BaseTask
from config.loader import load_apis, load_payloads


class APITasks(BaseTask):
    def on_start(self):
        super().on_start()
        self.apis = load_apis()
        self.payloads = load_payloads()

    @task
    def test_api(self):
        api = random.choice(self.apis)
        method = api['method']
        url = api['url']

        if method in ['POST', 'PUT']:
            payload = random.choice(self.payloads)
            response = getattr(self.client, method.lower())(url, json=payload)
        else:
            response = getattr(self.client, method.lower())(url)

        response.raise_for_status()
