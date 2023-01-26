# reddit-bot
This is a bot that when run, collects recent stories from the dailyillini RSS feed, picks out stories from unique categories, and posts to r/UIUC.

You must make a `keys.py` file in the same directory with the following Reddit API variables:
`CLIENT_ID`
`CLIENT_SECRET`
`USERAGENT`
`REDIRECT_URI`
`REFRESH_TOKEN`

## Dependencies
* feedparser for fetching and parsing RSS feed
* praw for posting to reddit

these can be installed with `python3 -m pip install feedparser praw`
