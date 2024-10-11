from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from celery_worker import schedule_post

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, can be restricted to specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, etc.)
    allow_headers=["*"],  # Allows all headers
)

class PostContent(BaseModel):
    content: str
    # schedule_time:str
@app.get('/')
def read_root():
    return {'message': 'Welcome to automating your life.'}

@app.post("/schedule/")
def schedule(post: PostContent):
    task= schedule_post.delay(post.content)
    return {"status": "Scheduled", "task_id": task.id}

@app.get("/task-status/{task_id}")
def get_status(task_id:str):
    task=schedule_post.AsyncResult(task_id)
    return {"task_id":task_id,"status":task.status,"reslt":task.result}

