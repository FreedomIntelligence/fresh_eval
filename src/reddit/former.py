import praw
import requests
import datetime
import pdb 
# 使用你的Reddit API凭证
reddit = praw.Reddit(
    client_id="deImkPevl0FGZWg9UiY7Vw",
    client_secret="OjVaUP0TdBWUHEZmmDd9GWSzNH_1fA",
    user_agent="RedditCrawler by u/ShadoWJackson"
)


def get_posts(start_epoch, end_epoch, subreddit):
    url = f'https://api.pushshift.io/reddit/search/submission/?subreddit={subreddit}&after={start_epoch}&before={end_epoch}&size=500'
    r = requests.get(url)
    data = r.json()
    pdb.set_trace()
    return data['data']

# 设置日期范围
start_date = datetime.datetime(2020, 1, 1)
end_date = datetime.datetime(2020, 1, 2)
start_epoch = int(start_date.timestamp())
end_epoch = int(end_date.timestamp())

# 获取帖子
subreddit = "all"  # 你可以更改为任何子版
posts = get_posts(start_epoch, end_epoch, subreddit)

for post in posts:
    submission = reddit.submission(id=post['id'])
    print(submission.title)  # 打印帖子的标题
