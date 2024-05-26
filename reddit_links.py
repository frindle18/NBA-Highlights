from bs4 import BeautifulSoup
import datetime
import os
import praw
import requests
import time
import config

def download_video(video_download_url, file_name):
    folder = 'highlights'
    os.makedirs(folder, exist_ok=True) # Create the folder if it doesn't exist
    file_path = os.path.join(folder, file_name)

    r = requests.get(video_download_url)
    if r.ok:
        with open(file_path, 'wb') as f:
            f.write(r.content)
        print("Video downloaded successfully!")
    else:
        print("Failed to download video.")

reddit = praw.Reddit(username=config.username,
                     password=config.password,
                     client_id=config.client_id,
                     client_secret=config.client_secret,
                     user_agent='Frindling streamable links')

subreddit = reddit.subreddit('nba')

# Time frame
target_date = datetime.datetime(2024, 5, 26) # May 26, 2024
start_time = datetime.datetime(target_date.year, target_date.month, target_date.day, 6, 0, 0) # 6am
end_time = datetime.datetime(target_date.year, target_date.month, target_date.day, 9, 0, 0) # 9am

# Search for posts within the specified time range

search_query = 'url:streamable.com AND title:"[Highlight]"'

for index, highlight in enumerate(subreddit.search(search_query, sort='new', syntax='lucene')):
    submission_time = datetime.datetime.fromtimestamp(highlight.created_utc)
    if start_time <= submission_time <= end_time:
        print(highlight.title.replace('[Highlight] ', ''))
        print(highlight.url)
       
        max_retries = 20
        retry_delay = 2  # in seconds

        for retry in range(max_retries): # Backoff strategy
            try:
                r = requests.get(highlight.url)
                if r.ok:
                    print("Request successful.")

                break # Exit loop if successful
            except:
                time.sleep(retry_delay)
        else:
            print("Maximum retries exceeded. Unable to establish connection.")
            continue

        soup = BeautifulSoup(r.text, 'html.parser')

        video_download_url = soup.find("meta", property="og:video:url")['content']

        print(video_download_url)

        download_video(video_download_url, str(index) + '.mp4')
