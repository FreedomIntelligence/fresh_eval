import praw


reddit = praw.Reddit(
    client_id="deImkPevl0FGZWg9UiY7Vw",
    client_secret="OjVaUP0TdBWUHEZmmDd9GWSzNH_1fA",
    user_agent="RedditCrawler by u/ShadoWJackson"
)

subreddit = reddit.subreddit("WormFanfic")
# new_post = subreddit.new(limit=500)
# file = open("links.txt", 'w')
posts = subreddit.new(limit=10) 


with open("Reddit_data.txt", "a") as f:
    for post in posts:
        f.write(f"Title: {post.title}\n")
        f.write(f"Content: {post.selftext}\n")
        f.write(f"Link: {post.url}\n\n")

# pattern = "Taylor"
# posts_titles = {}
# posts_link = {}
# final_posts = {}

# for post in new_post:
#     posts_titles[post.id] = post.title.split()
#     posts_link[post.id] = post.url

# for key in posts_titles:
#     for value in posts_titles[key]:
#         if value.lower() == pattern.lower():
#             final_posts[key] = posts_link.get(key)

# for post in final_posts:
#     file.write(final_posts.get(post))
#     file.write('\n')