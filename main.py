import os
import random
import requests
import tweepy
from moviepy.video.io.VideoFileClip import VideoFileClip

# Pick a random image/video from the 'assets' folder
def get_random_media():
    path = 'assets'
    objects = os.listdir(path)

    # Filter only video files (optional)
    media = random.choice(objects)

    media_path = os.path.join(path, media)
    
    # If the selected media is a video, extract a clip from it
    if media.endswith(('.mp4', '.mov', '.avi')):  # Assuming these are video formats
        return extract_random_clip(media_path)
    
    return media_path  # If it's an image or non-video media, return as is


# Extract a random 60-second clip from the video
def extract_random_clip(video_path):
    with VideoFileClip(video_path) as video:
        duration = video.duration  # Get the duration of the video in seconds
        
        # Choose a random start time (making sure it leaves enough time for a 60-second clip)
        if duration > 60:
            start_time = random.uniform(0, max(0, duration - 60))  # 60-second long clip
        else:
            start_time = 0  # If the video is shorter than 60 seconds, start from the beginning
        
        # Extract a subclip from the video
        clip = video.subclip(start_time, start_time + 60)  # 60 seconds duration
        
        # Save the clip to a new file
        output_path = "clip.mp4"
        clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
        
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
    # Get the keys from environment variables
    consumer_key = os.environ['CONSUMER_KEY']
    consumer_secret = os.environ['CONSUMER_SECRET']
    access_token = os.environ['ACCESS_TOKEN']
    access_token_secret = os.environ['ACCESS_TOKEN_SECRET']

    api_v1 = auth_v1(consumer_key, consumer_secret,
                     access_token, access_token_secret)
    client_v2 = auth_v2(consumer_key, consumer_secret,
                        access_token, access_token_secret)

    media_id = api_v1.media_upload(media).media_id

    return client_v2.create_tweet(media_ids=[media_id])


def main():
    media = get_random_media()
    tweet(media)


if __name__ == '__main__':
    main()
