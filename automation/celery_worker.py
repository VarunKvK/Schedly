from celery import Celery

celery=Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery.task
def schedule_post(content:str):
    print(f"Scheduled the post:{content}")
    return f"Post is scheduled:{content}"