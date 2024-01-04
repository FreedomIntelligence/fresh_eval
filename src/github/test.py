import requests
from datetime import datetime, timedelta

def is_repository_created_within_a_week(repo_url='jerryc127/hexo-theme-butterfly'):
    try:
        response = requests.get(repo_url)
        if response.status_code == 200:
            repo_data = response.json()
            created_at_str = repo_data.get("created_at")
            print('created_at_str',created_at_str)
            if created_at_str:
                created_at = datetime.strptime(created_at_str, "%Y-%m-%dT%H:%M:%SZ")
                one_week_ago = datetime.now() - timedelta(weeks=1)
                return created_at >= one_week_ago
    except Exception as e:
        print(f"An error occurred: {e}")
    return False

if __name__ == "__main__":
    repo_url = input("请输入GitHub仓库地址（如 用户名/仓库名）：") or 'jerryc127/hexo-theme-butterfly'
    repo_url='https://api.github.com/repos/'+repo_url
    if is_repository_created_within_a_week(repo_url):
        print("这个仓库是在过去的一周内创建的！")
    else:
        print("这个仓库不是在过去的一周内创建的。")
