import os
import random
import requests
import tweepy
from moviepy.editor import VideoFileClip

# Pick a random image/video from the 'assets' folder
def get_random_media():
    path = 'assets'
    objects = os.listdir(path)
    media = random.choice(objects)
    return os.path.join(path, media)

# Extract a 60-second clip from a video
def extract_random_clip(video_path):
    clip = VideoFileClip(video_path)
    duration = clip.duration
    start_time = random.uniform(0, max(duration - 60, 0))  # Ensure the clip duration is valid
    end_time = start_time + 60
    output_path = video_path.replace('.mp4', '_clip.mp4')
    clip.subclip(start_time, end_time).write_videofile(output_path, codec="libx264", audio_codec="aac")
    return output_path

# Authorize Twitter with v1.1 API
def auth_v1(consumer_key, consumer_secret, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)

# Authorize Twitter with v2 API
def auth_v2(consumer_key, consumer_secret, access_token, access_token_secret):
    return tweepy.Client(
        consumer_key=consumer_key, consumer_secret=consumer_secret,
        access_token=access_token, access_token_secret=access_token_secret,
        return_type=requests.Response,
    )

# Tweet picked image/video
def tweet(media) -> requests.Response:
    consumer_key = os.environ['CONSUMER_KEY']
    consumer_secret = os.environ['CONSUMER_SECRET']
    access_token = os.environ['ACCESS_TOKEN']
    access_token_secret = os.environ['ACCESS_TOKEN_SECRET']

    api_v1 = auth_v1(consumer_key, consumer_secret, access_token, access_token_secret)
    client_v2 = auth_v2(consumer_key, consumer_secret, access_token, access_token_secret)

    if media.lower().endswith('.mp4'):
        media = extract_random_clip(media)
    
    media_id = api_v1.media_upload(media).media_id
    return client_v2.create_tweet(media_ids=[media_id])

def main():
    media_path = get_random_media()
    tweet(media_path)

if __name__ == '__main__':
    main()