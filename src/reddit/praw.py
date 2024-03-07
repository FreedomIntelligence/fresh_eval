




def praw_reddit(config=None):
    import datetime
    import json
    if  config is None:
        config={}
        config['save_path']='.data/reddit_data.jsonl'
    import praw


    reddit = praw.Reddit(
        client_id="deImkPevl0FGZWg9UiY7Vw",
        client_secret="OjVaUP0TdBWUHEZmmDd9GWSzNH_1fA",
        user_agent="RedditCrawler by u/ShadoWJackson",
    )

    subreddit = reddit.subreddit("all")


    posts = subreddit.new(limit=30000) 


    for post in posts:
        if not  '/www.reddit.com/r/'  in post.url:
            with open(config['save_path'], "a",encoding='utf-8') as f:
                # f.write(f"Title: {post.title}\n")
                # f.write(f"Content: {post.selftext}\n")
                # f.write(f"Link: {post.url}\n\n")
                entry = {"date": datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"), "error": False, "url": post.url,'text_blocks':post.selftext}
                if len(post.selftext)>10:
                    json.dump(entry, f, ensure_ascii=False)
                    f.write("\n")
            # else:
                # print(f"{post.url} not a reddit link")