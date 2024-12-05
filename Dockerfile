FROM python:3.9-slim-buster

WORKDIR /locust

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8089

CMD ["sh", "-c", "locust $LOCUST_OPTS"]