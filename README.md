# Message Queue API

This project demonstrates how to build a simple message queue using `rq` (Redis Queue) and `FastAPI`. The API allows receiving jobs via FastAPI endpoints and automatically creates workers to process these jobs.

## Features

- **Message Queue**: Utilizes `rq` to manage job queues.
- **FastAPI Integration**: Provides endpoints to receive, cancel, and query jobs.
- **Automatic Worker Creation**: Automatically creates workers to process jobs.
- **Docker Compose**: Uses `docker-compose` to manage and run the application and its dependencies.
- **Swagger Documentation**: Available at `http://localhost:8080/docs`.
- **RQ Dashboard**: For simple monitoring. Available at `http://localhost:8080/rq`.

## Setup

This project is designed to run as a set of Docker containers. You will need to [install Docker](https://www.docker.com/) to complete the setup tasks.

First, clone this repository and build the Docker images for the project:

```sh
docker-compose build
```

## Running the API

Use the following command to start the application, Redis, and the worker:

```sh
docker-compose up
```

This command starts the Redis server, the FastAPI application, the test, and the worker.

## API Endpoints

- **Receive Task**: `POST /app/tasks/receive` - Enqueue a new task.
- **Cancel Task**: `POST /app/tasks/cancel` - Cancel a task.
- **Get Queued Jobs**: `GET /app/tasks/queued_jobs` - Get the list of queued jobs.
- **Get Canceled Jobs**: `GET /app/tasks/cancelled_jobs` - Get the list of canceled jobs.
- **Get Finished Jobs**: `GET /app/tasks/finished_jobs` - Get the list of finished jobs.
- **Get Failed Jobs**: `GET /app/tasks/failed_jobs` - Get the list of failed jobs.

## Job Statuses

Jobs can have several statuses:  
- Queued: The job is waiting to be processed.
- Started: The job is currently being processed.
- Canceled: The job has been canceled.
- Failed: The job has failed or stopped during processing.
- Finished: The job has been successfully processed.
The status of a job changes as it moves through the queue and is processed by workers.

## License

This project is licensed under the MIT License.

## Future Improvements

Here are some potential improvements that can be made to the project:

- [ ] Implement pub / sub without rq, make it more customizable.
- [ ] Using async test.
- [ ] Add more comprehensive logging and monitoring.
- [ ] Optimize the Docker setup for faster builds and smaller image sizes, it's way too bulky.

## Special Thanks
This project is my first experience working with FastAPI and Redis. Its an interesting project to try and figure out the knowledge that I haven't touched before. 
Here are some resources that helped me along the way: 

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Redis Documentation](https://redis.io/documentation)
- [RQ](https://python-rq.org/)
- [fastapi-redis-tutorial](https://github.com/redis-developer/fastapi-redis-tutorial)