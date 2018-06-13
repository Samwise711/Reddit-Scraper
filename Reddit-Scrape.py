import praw
import pandas as pd
import datetime as dt

reddit = praw.Reddit(client_id='PERSONAL_USE_SCRIPT_14_CHARS', \
                     client_secret='SECRET_KEY_27_CHARS ', \
                     user_agent='YOUR_APP_NAME', \
                     username='YOUR_REDDIT_USER_NAME', \
                     password='YOUR_REDDIT_LOGIN_PASSWORD')

#print(reddit.user.me())

field = input('Enter the subreddit to scrape: ')
subreddit = reddit.subreddit(field.lower())

#options are: .hot, .new, .controversial, .top, and .gilded.
#You can also use .search("SEARCH_KEYWORDS") to get only results matching an engine search.
#That will return a list-like object with the top-100 submission in r/Nootropics.
# You can control the size of the sample by passing a limit to .top(), but be aware that Reddit’s request limit* is 1000, like this:
top_subreddit = subreddit.hot()

topics_dict = { "title":[], \
                "score":[], \
                "id":[], \
                "url":[], \
                "comms_num": [], \
                "created": []}

for submission in top_subreddit:
    topics_dict["title"].append(submission.title)
    topics_dict["score"].append(submission.score)
    topics_dict["id"].append(submission.id)
    topics_dict["url"].append(submission.url)
    topics_dict["comms_num"].append(submission.num_comments)
    topics_dict["created"].append(submission.created)

topics_data = pd.DataFrame(topics_dict)


def get_date(created):
    return dt.datetime.fromtimestamp(created)

_timestamp = topics_data["created"].apply(get_date)

topics_data = topics_data.assign(timestamp = _timestamp)

topics_data = topics_data.drop(['created'], axis=1)

title = field+" top posts.csv"

topics_data.to_csv(title, index=False)
