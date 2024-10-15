import time
import logging
from rq.job import Job
from app.tasks.config import Config
from rq.registry import CanceledJobRegistry, FinishedJobRegistry, FailedJobRegistry
from rq.command import send_stop_job_command
from rq import Queue
from redis import Redis

# Initialize the logger
log = logging.getLogger(__name__)

# Load configuration settings
config = Config()

# Create a Redis connection using the URL from the configuration
redis = Redis.from_url(config.redis_url)

# Create a task queue named 'rq' with the Redis connection
task_queue = Queue('rq', connection=redis)

def enqueue_task():
    """
    Simulate a task by sleeping for 3 seconds.
    """
    time.sleep(3)
    return

def receive_task(title: str):
    """
    Enqueue a new task with the given title as the job ID.

    Args:
        title (str): The title of the task, used as the job ID.

    Returns:
        Job: The enqueued job.
    """
    job = task_queue.enqueue(enqueue_task, job_id=title)
    return job

def cancel_task(job_id: str):
    """
    Cancel a task with the given job ID.

    Args:
        job_id (str): The ID of the job to cancel.

    Returns:
        dict: A dictionary containing the status of the job.
    """
    job = Job.fetch(job_id, connection=redis)
    if job.get_status() == 'queued':
        job.cancel()
        return {"status": job.get_status()}
    elif job.get_status() == 'started':
        send_stop_job_command(redis, job_id)
        return {"status": job.get_status()}
    else:
        return {"status": "neither queued nor started, cannot cancel"}

def job_list():
    """
    Get the list of queued jobs.

    Returns:
        list: A list of job IDs.
    """
    jobs = task_queue.get_job_ids()
    return jobs

def canceled_job_list():
    """
    Get the list of canceled jobs.

    Returns:
        list: A list of canceled job IDs.
    """
    registry = CanceledJobRegistry(queue=task_queue)
    log.debug('IDs in CanceledJobRegistry registry %s' % registry.get_job_ids())
    return registry.get_job_ids()

def finished_job_list():
    """
    Get the list of finished jobs.

    Returns:
        list: A list of finished job IDs.
    """
    registry = FinishedJobRegistry(queue=task_queue)
    log.debug('IDs in FinishedJobRegistry registry %s' % registry.get_job_ids())
    return registry.get_job_ids()

def failed_job_list():
    """
    Get the list of failed jobs.

    Returns:
        list: A list of failed job IDs.
    """
    registry = FailedJobRegistry(queue=task_queue)
    log.debug('IDs in FailedJobRegistry registry %s' % registry.get_job_ids())
    return registry.get_job_ids()