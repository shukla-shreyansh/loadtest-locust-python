import os
from config.settings import TOKEN_FILE, TOKEN

def get_token():
    if TOKEN_FILE and os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as f:
            return f.read().strip()
    return TOKEN

# utils/reporting.py
from locust import events
from datetime import datetime
import matplotlib.pyplot as plt

@events.test_stop.add_listener
def generate_custom_report(environment, **kwargs):
    if environment.stats.total.num_requests > 0:
        stats = environment.stats.sort_stats('name')
        timestamps = [datetime.fromtimestamp(stat.last_request_timestamp) for stat in stats]
        p99_values = [stat.get_response_time_percentile(0.99) for stat in stats]

        plt.figure(figsize=(12, 6))
        plt.plot(timestamps, p99_values, marker='o')
        plt.title('P99 Response Time Over Time')
        plt.xlabel('Time')
        plt.ylabel('P99 Response Time (ms)')
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('p99_response_time.png')
        print("Custom P99 report generated: p99_response_time.png")