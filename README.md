# Locust Based Load Testing Framework

This framework provides a modular and extensible load testing framework using Locust library. 
It's designed to test multiple APIs with various methods and payloads, and can be run locally or in a distributed environment using Docker.

## Project Structure

```
loadtest-locust-python/
├── config/
│   ├── __init__.py
│   ├── settings.py
│   └── loader.py
├── tasks/
│   ├── __init__.py
│   ├── base_task.py
│   └── api_tasks.py
├── utils/
│   ├── __init__.py
│   ├── auth.py
│   └── reporting.py
├── locustfile.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── apis.json
└── payloads.json
```

## Setup

1. Clone the repository:

2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. Create `apis.json` and `payloads.json` files in the root directory with your API endpoints and payload variations.

4. If using token-based authentication, create a `token.txt` file with your API token.

## Usage

### Running Locally

To run the load test locally:

```
locust -f locustfile.py
```

Then, open a web browser and go to `http://localhost:8089` to access the Locust web interface.

### Running with Docker Compose

To run the load test using Docker Compose:

```
TARGET_HOST=https://api-host.com USERS=100 SPAWN_RATE=10 RUN_TIME=10m docker-compose up --scale worker=4
```

Adjust the environment variables as needed:
- `TARGET_HOST`: The base URL of your API
- `USERS`: The number of concurrent users to simulate
- `SPAWN_RATE`: The rate at which to spawn users
- `RUN_TIME`: The duration of the test
- `RAMP_UP`: The time to ramp up to full user count (default: 60 seconds)
- `RAMP_DOWN`: The time to ramp down from full user count (default: 60 seconds)

## Customization

- To add new API tasks, create new classes in `tasks/api_tasks.py`.
- To modify authentication, update `utils/auth.py`.
- To change load test settings, modify `config/settings.py`.
- To add new utility functions, add them to the appropriate file in the `utils/` directory.

## Reporting

After the test run, a custom P99 response time graph will be generated as `p99_response_time.png` in the project root directory.
