import os
import re
from datetime import timedelta
from googleapiclient.discovery import build

api_key = os.environ.get('GENERATED_API_KEY')

youtube = build('youtube', 'v3', developerKey=api_key)

hours_patrn = re.compile(r'(\d+)H')
minutes_patrn = re.compile(r'(\d+)M')
seconds_patrn = re.compile(r'(\d+)S')

total_sec = 0


nextPageToken = None
while True:
    pl_request = youtube.playlistItems().list(
        part='contentDetails',
        playlistId="PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU",
        maxResults=50,
        pageToken=nextPageToken
    )

    pl_response = pl_request.execute()

    video_ids = []
    for item in pl_response['items']:
        video_ids.append(item['contentDetails']['videoId'])

    video_request = youtube.videos().list(
        part="contentDetails",
        id=','.join(video_ids)
    )

    video_response = video_request.execute()

    for item in video_response['items']:
        duration = item['contentDetails']['duration']

        hours = hours_patrn.search(duration)
        minutes = minutes_patrn.search(duration)
        seconds = seconds_patrn.search(duration)

        hours = int(hours.group(1)) if hours else 0
        minutes = int(minutes.group(1)) if minutes else 0
        seconds = int(seconds.group(1)) if seconds else 0

        video_seconds = timedelta(
            hours=hours,
            minutes=minutes,
            seconds=seconds
        ).total_seconds()

        total_sec += video_seconds

    nextPageToken = pl_response.get('nextPageToken')

    if not nextPageToken:
        break

total_sec = int(total_sec)

minutes, seconds = divmod(total_sec, 60)
hours, minutes = divmod(minutes, 60)

print(f'{hours}:{minutes}:{seconds}')