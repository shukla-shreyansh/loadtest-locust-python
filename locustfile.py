import gevent
from locust import FastHttpUser, between, events
from locust.runners import MasterRunner

from tasks.api_tasks import APITasks
from utils.auth import get_token
from config.settings import RAMP_UP, RAMP_DOWN, TEST_DURATION

class APILoadTest(FastHttpUser):
    tasks = [APITasks]
    wait_time = between(1, 3)

    def on_start(self):
        self.token = get_token()

@events.init.add_listener
def on_locust_init(environment, **kwargs):
    if isinstance(environment.runner, MasterRunner):
        environment.runner.register_message('ramp_up', ramp_up)
        environment.runner.register_message('ramp_down', ramp_down)

def ramp_up(environment):
    target_users = environment.runner.target_user_count
    step = target_users / (RAMP_UP / environment.runner.heartbeat_interval)
    while environment.runner.user_count < target_users:
        environment.runner.user_count = min(environment.runner.user_count + step, target_users)
        environment.runner.send_message('update_user_count', environment.runner.user_count)
        gevent.sleep(environment.runner.heartbeat_interval)

def ramp_down(environment):
    step = environment.runner.user_count / (RAMP_DOWN / environment.runner.heartbeat_interval)
    while environment.runner.user_count > 0:
        environment.runner.user_count = max(environment.runner.user_count - step, 0)
        environment.runner.send_message('update_user_count', environment.runner.user_count)
        gevent.sleep(environment.runner.heartbeat_interval)

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    if isinstance(environment.runner, MasterRunner):
        gevent.spawn_later(1, environment.runner.send_message, 'ramp_up')
        gevent.spawn_later(TEST_DURATION, environment.runner.send_message, 'ramp_down')

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    pass