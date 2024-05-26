import datetime
import praw
import config

reddit = praw.Reddit(username=config.username,
                     password=config.password,
                     client_id=config.client_id,
                     client_secret=config.client_secret,
                     user_agent='Frindling streamable links')

subreddit = reddit.subreddit('nba')

# Time frame
target_date = datetime.datetime(2024, 5, 26) # May 25, 2024
start_time = datetime.datetime(target_date.year, target_date.month, target_date.day, 6, 0, 0) # 6am
end_time = datetime.datetime(target_date.year, target_date.month, target_date.day, 9, 0, 0) # 9am

# Search for posts within the specified time range

search_query = 'url:streamable.com AND title:"[Highlight]"'

for highlight in subreddit.search(search_query, sort='new', syntax='lucene'):
    submission_time = datetime.datetime.fromtimestamp(highlight.created_utc)
    if start_time <= submission_time <= end_time:
        print(highlight.title)
        print(highlight.url)
        print()
