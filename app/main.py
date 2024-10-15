from app.tasks.router import router as task_router
import logging

from rq_dashboard_fast import RedisQueueDashboard
from fastapi import FastAPI
from app.config import Config

# Initialize the logger
log = logging.getLogger(__name__)

# Load configuration settings
config = Config()

# Create a FastAPI application instance
app = FastAPI(title='Message Queue API', version=config.version)

# Initialize the Redis Queue Dashboard with the specified Redis URL and mount it at the /rq endpoint
dashboard = RedisQueueDashboard(config.redis_url, "/rq")
app.mount("/rq", dashboard)

# Include the task router in the FastAPI application
app.include_router(task_router)