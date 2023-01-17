# import tools for getting rss feed, current date, reddit API
from datetime import date
import feedparser
import praw
import logging
import sys

# import reddit API keys from gitignored file
from keys import CLIENT_ID, CLIENT_SECRET, USERAGENT, REDIRECT_URI, REFRESH_TOKEN
logging.basicConfig(filename='logs.txt', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(message)s')

# authenticate reddit api and get RSS feed of stories
try:
    reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=USERAGENT, redirect_uri=REDIRECT_URI, refresh_token=REFRESH_TOKEN)
    NewsFeed = feedparser.parse("https://dailyillini.com/feed")
except Exception as e:
    logging.critical(e)
    sys.exit(1)

logging.info("Successfully authenticated and gathered RSS.")

# assemble basic submission strings
subreddit = reddit.subreddit('UIUC') 
todays_date = date.today().strftime("%m/%d/%Y")
submission_title = f"Recent dailyillini.com Stories - {todays_date}"
submission_text = "Greetings, I am a robot created by [The Daily Illini](https://dailyillini.com) to serve your eyeholes with the latest and greatest student journalism. Here's the latest campus news you may have missed:\n\n\n\n"

# format and append 5 stories to submission body
used_tags = []
counter = 0
for entry in NewsFeed.entries:
    story_tag = entry["tags"][0]["term"]
    if story_tag not in used_tags:
        story_title = entry["title"]
        story_link = entry["link"]
        used_tags.append(story_tag)
        submission_text += f"{story_tag} - [{story_title}]({story_link})\n\n"
        used_tags.append(story_tag)
        counter += 1
    if counter == 5:
        break

submission_text += "\n\n^(This post was made by a bot. If you want to learn more, join our team or just complain, email us at online@dailyillini.com)"

# submit !
try:
    subreddit.submit(submission_title,selftext=submission_text, flair_id="a3994b2e-d384-11ea-bf32-0e7e74729027")

except Exception as e:
    logging.critical(e)
    sys.exit(1)

logging.info("Successfully posted to reddit.")
