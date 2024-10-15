from fastapi import APIRouter, HTTPException
import logging
from .tasks import cancel_task, job_list, canceled_job_list, finished_job_list, failed_job_list, \
    receive_task
from pydantic import BaseModel

# Create a new APIRouter instance with a prefix and tags
router = APIRouter(
    tags=["tasks"],
    prefix="/app/tasks",
)

# Initialize the logger
log = logging.getLogger(__name__)

# Define the input model for receiving a task
class TaskReceiveInput(BaseModel):
    title: str

# Define the input model for canceling a task
class TaskCancelInput(BaseModel):
    job_id: str

@router.post('/receive')
async def receive(task: TaskReceiveInput):
    """
    Endpoint to receive a new task.

    Args:
        task (TaskReceiveInput): The input model containing the task title.

    Returns:
        dict: A dictionary containing the job ID.

    """
    try:
        job = receive_task(task.title)
        return {"job_id": job.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/cancel')
async def cancel(task: TaskCancelInput):
    """
    Endpoint to cancel a task.

    Args:
        task (TaskCancelInput): The input model containing the job ID.

    Returns:
        dict: A dictionary containing the cancellation status.

    """
    try:
        res = cancel_task(task.job_id)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/queued_jobs')
async def get_queued_jobs():
    """
    Endpoint to get the list of queued jobs.

    Returns:
        list: A list of queued jobs.

    """
    try:
        res = job_list()
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/cancelled_jobs')
async def get_canceled_jobs():
    """
    Endpoint to get the list of canceled jobs.

    Returns:
        list: A list of canceled jobs.

    """
    try:
        res = canceled_job_list()
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/finished_jobs')
async def get_finished_jobs():
    """
    Endpoint to get the list of finished jobs.

    Returns:
        list: A list of finished jobs.

    """
    try:
        res = finished_job_list()
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/failed_jobs')
async def get_failed_jobs():
    """
    Endpoint to get the list of failed jobs.

    Returns:
        list: A list of failed jobs.

    """
    try:
        res = failed_job_list()
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))