Report

This project demonstrates the process of installing Docker, containerizing a Python Flask web application, and orchestrating multiple services (a web app, a Redis cache, and a PostgreSQL database) using Docker Compose. The primary goal is to gain practical experience with containerized environments and multi-container application deployment.

Learning Objectives
Through this hands-on lab, I was able to:

Understand the fundamentals of working with containerized environments.

Gain experience in setting up and configuring services in a local development environment.

Learn how to connect and orchestrate multiple components in a system using Docker Compose.

Develop skills in testing, monitoring, and documenting a deployed application.

Execution Steps
Here are the steps taken to set up the environment, build the application, and run the services.

1. Install and Verify Docker Desktop
First, I installed Docker Desktop on my operating system and verified the installation was successful by running the following command in the terminal:

Bash

docker --version
2. Set Up PostgreSQL Container
Next, I pulled the official PostgreSQL image from Docker Hub and ran it as a container.

Pull the PostgreSQL image:

Bash

docker pull postgres
Run the PostgreSQL container: This command starts a PostgreSQL instance named postgres1, maps port 5432 to the host, and sets the password.

Bash

docker run -d -p 5432:5432 --name postgres1 -e POSTGRES_PASSWORD=pass12345 postgres
3. Build the Multi-Container Web Application
The core of the project involved creating a Python Flask application that uses a Redis cache. This was orchestrated using Docker Compose.

Create Project Files: I created the following four files in the project directory.

requirements.txt: Defines the Python dependencies.

flask
redis
app.py: The main Flask application logic.

Python

import time
import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)
Dockerfile: Instructions to build the web application image.

Dockerfile

FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]
compose.yaml: Defines and configures the web and redis services.

YAML

version: "3.9"
services:
  web:
    build: .
    ports:
      - "8000:5000"
    depends_on:
      - redis
  redis:
    image: "redis:alpine"
Build and Run with Docker Compose: With all the files in place, I used a single command to build the images and start the containers.

Bash

docker compose up
4. Verify the Application
After running docker compose up, the application was accessible in a web browser at http://localhost:8000. Each time the page is refreshed, the hit counter, which is stored in the Redis cache, increments


