import random
from locust import task, SequentialTaskSet, FastHttpUser, between
from config.loader import load_apis, get_payload_for_api
from utils.auth import get_token

class APITasks(SequentialTaskSet):
    def on_start(self):
        self.apis = load_apis()
        self.token = get_token()
        if self.token:
            self.client.headers['Authorization'] = f'Bearer {self.token}'

    @task
    def perform_api_call(self):
        api = random.choice(self.apis)
        method = api['method'].lower()
        url = api['url']
        name = api['name']

        kwargs = {
            'name': name,
        }

        # Add payload for POST and PUT requests
        if method in ['post', 'put']:
            kwargs['json'] = get_payload_for_api(name)

        # Handle potential path parameters
        if '{' in url:
            url = url.replace('{id}', '1')

        # Perform the request
        try:
            response = getattr(self.client, method)(url, **kwargs)
            response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        except Exception as e:
            print(f"Request failed for API '{name}': {str(e)}")
            self.environment.runner.stats.log_error(method, url, str(e))

    @task
    def wait_between_requests(self):
        self.wait()

class APIUser(FastHttpUser):
    tasks = [APITasks]
    wait_time = between(1, 5)  # Wait 1-5 seconds between tasks

    def on_start(self):
        self.token = get_token()