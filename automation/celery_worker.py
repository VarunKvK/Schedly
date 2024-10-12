from celery import Celery
import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

# Set up Twitter API credentials
auth = tweepy.OAuthHandler(os.getenv("TWITTER_API_KEY"), os.getenv("TWITTER_API_SECRET"))
auth.set_access_token(os.getenv("TWITTER_ACCESS_TOKEN"), os.getenv("TWITTER_ACCESS_TOKEN_SECRET"))
twitter_api = tweepy.API(auth)

celery = Celery(
    'tasks',
    broker='redis://localhost:6379/0',  # Redis as the message broker
    backend='redis://localhost:6379/0'  # Redis as the result backend
)

celery.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

@celery.task
def generate_twitter_content(content):
    try:
        print(f"Received content: {content}")  # Log the content being passed to the task

        # Attempt to post to Twitter
        twitter_api.update_status(content)  # This is the Twitter post
        print(f"Post successful: {content}")  # Confirm that the post was successful
        
        return f"Post is scheduled: {content}"
    except tweepy.TweepyException as e:
        print(f"Error occurred while tweeting: {e}")
        return str(e)
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        return str(e)
