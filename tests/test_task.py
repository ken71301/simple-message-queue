from fakeredis import FakeStrictRedis
from rq import Queue
from rq.job import Job

from app.tasks.tasks import enqueue_task

def test_enqueue_task():
    """
    Test the enqueue_task function.

    This test creates a fake Redis connection and enqueues a task to the queue.
    It asserts that the job is finished.

    Raises:
        AssertionError: If the job is not finished.
    """
    queue = Queue(is_async=False, connection=FakeStrictRedis())
    job = queue.enqueue(enqueue_task)
    assert job.is_finished

def test_receive(client, mocker):
    """
    Test the /receive endpoint.

    This test mocks the task queue and sends a POST request to the /receive endpoint.
    It asserts that the response status code is 200 and the response contains a job_id.

    Args:
        client (TestClient): The test client for the FastAPI app.
        mocker (MockerFixture): The mocker fixture to mock objects.

    Raises:
        AssertionError: If the response status code is not 200 or job_id is not in the response.
    """
    mocker.patch("app.tasks.tasks.task_queue", return_value=Queue(is_async=False, connection=FakeStrictRedis()))
    response = client.post("/app/tasks/receive", json={"title": "test_task"})
    assert response.status_code == 200
    assert "job_id" in response.json()

def test_cancel(client, mocker):
    """
    Test the /cancel endpoint.

    This test creates a fake Redis connection and enqueues a task with a specific job_id.
    It mocks the Job.fetch method and sends a POST request to the /cancel endpoint.
    It asserts that the response status code is 200 and the response contains a status.

    Args:
        client (TestClient): The test client for the FastAPI app.
        mocker (MockerFixture): The mocker fixture to mock objects.

    Raises:
        AssertionError: If the response status code is not 200 or status is not in the response.
    """
    redis_client = FakeStrictRedis()
    queue = Queue(is_async=False, connection=redis_client)
    queue.enqueue(enqueue_task, job_id="test_task")

    job = mocker.patch("app.tasks.tasks.Job")
    job.fetch.return_value = Job.fetch("test_task", connection=redis_client)

    cancel_response = client.post("/app/tasks/cancel", json={"job_id": "test_task"})
    assert cancel_response.status_code == 200
    assert "status" in cancel_response.json()

def test_get_queued_jobs(client):
    """
    Test the /queued_jobs endpoint.

    This test sends a GET request to the /queued_jobs endpoint.
    It asserts that the response status code is 200 and the response is a list.

    Args:
        client (TestClient): The test client for the FastAPI app.

    Raises:
        AssertionError: If the response status code is not 200 or the response is not a list.
    """
    response = client.get("/app/tasks/queued_jobs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_canceled_jobs(client):
    """
    Test the /cancelled_jobs endpoint.

    This test sends a GET request to the /cancelled_jobs endpoint.
    It asserts that the response status code is 200 and the response is a list.

    Args:
        client (TestClient): The test client for the FastAPI app.

    Raises:
        AssertionError: If the response status code is not 200 or the response is not a list.
    """
    response = client.get("/app/tasks/cancelled_jobs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_finished_jobs(client):
    """
    Test the /finished_jobs endpoint.

    This test sends a GET request to the /finished_jobs endpoint.
    It asserts that the response status code is 200 and the response is a list.

    Args:
        client (TestClient): The test client for the FastAPI app.

    Raises:
        AssertionError: If the response status code is not 200 or the response is not a list.
    """
    response = client.get("/app/tasks/finished_jobs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_failed_jobs(client):
    """
    Test the /failed_jobs endpoint.

    This test sends a GET request to the /failed_jobs endpoint.
    It asserts that the response status code is 200 and the response is a list.

    Args:
        client (TestClient): The test client for the FastAPI app.

    Raises:
        AssertionError: If the response status code is not 200 or the response is not a list.
    """
    response = client.get("/app/tasks/failed_jobs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)