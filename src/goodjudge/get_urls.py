from request_one_question import craw_gjopen


import requests
from bs4 import BeautifulSoup
import pdb
# 发送 HTTP 请求获取网页内容
page=2
url = f"https://www.gjopen.com/leaderboards/questions?page={page}"
headers = { 'User-Agent': 'Mozilla/5.0' , 'Accept': 'text/html', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate', 'DNT': '1',
            'Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1', 'Cache-Control': 'max-age=0' }

response = requests.get(url,headers=headers)

soup = BeautifulSoup(response.text, 'html.parser')
pdb.set_trace()
# 找到问题发布时间
questions = soup.find_all('div', class_='question')
for question in questions:
    title = question.find('h4', class_='question-title').text.strip()
    time = question.find('div', class_='question-time').text.strip()
    print("问题:", title)
    print("发布时间:", time)
    print("------------------------")

