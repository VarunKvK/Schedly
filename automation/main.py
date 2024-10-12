from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from celery_worker import generate_twitter_content
from datetime import datetime

app = FastAPI()

class PostContent(BaseModel):
    content: str
    schedule_time: str

@app.post("/schedule/")
async def schedule_post(post: PostContent):
    # Calculate delay in seconds
    try:
        schedule_time = datetime.strptime(post.schedule_time, "%Y-%m-%d %H:%M:%S")
        delay = (schedule_time - datetime.utcnow()).total_seconds()

        print("Current time",datetime.utcnow())
        print("Scheduled time",schedule_time)

        if delay <= 0:
            raise HTTPException(status_code=400, detail="Scheduled time must be in the future.")
        
        print(f"Scheduling task with delay: {delay} seconds")  # Log the delay value
        
        # Schedule task to post on Twitter
        task = generate_twitter_content.apply_async(args=[post.content], countdown=delay)

        # Log the task ID
        print(f"Task scheduled with task ID: {task.id}")
        
        return {"message": "Post scheduled successfully", "task_id": task.id}
    except Exception as e:
        print(f"Error in scheduling post: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
