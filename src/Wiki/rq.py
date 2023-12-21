import time
import urllib.request
import re
import json
from datetime import datetime

# 定义起始页和种子页
starting_page = "https://en.wikipedia.org/wiki/Special:NewPages"
# seed_page = "https://en.wikipedia.org"

# 下载网页内容
def download_page(url):
    try:
        headers = {'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req)
        respData = resp.read().decode('utf-8')
        return respData
    except Exception as e:
        print(str(e))
        return None

# 提取页面标题
def extract_title(page):
    start_title = page.find("<span dir")
    end_start_title = page.find(">", start_title+1)
    stop_title = page.find("</span>", end_start_title + 1)
    title = page[end_start_title + 1 : stop_title]
    return title

# 提取页面简介
def extract_introduction(page):
    start_introduction = page.find("<p>")
    stop_introduction = page.find('<div id="toctitle">', start_introduction + 1)
    if '<div id="toctitle">' not in page:
        stop_introduction = page.find('</p>', start_introduction + 1)
    raw_introduction = page[start_introduction : stop_introduction]
    return raw_introduction

# 清洗简介文本
def extract_pure_introduction(page):
    pure_introduction = re.sub(r'<.+?>', '', page)
    return pure_introduction

# URL 解析
def url_parse(url):
    from urllib.parse import urlparse
    s = urlparse(url)
    if not s.scheme:
        url = "http://" + url
    return url

# 主爬虫函数
def web_crawl():  
    crawled = []
    data = []

    raw_html = download_page(starting_page)
    if raw_html:
        title = extract_title(raw_html)
        pure_introduction = extract_pure_introduction(extract_introduction(raw_html))

        entry = {
            "date": datetime.now().strftime("%Y-%m-%d-%H-%M"),
            "error": False,
            "url": starting_page,
            "title": title,
            "text_blocks": pure_introduction
        }

        data.append(entry)

        with open("WikipediaNewPages.jsonl", "a", encoding="utf-8") as file:
            json.dump(entry, file, ensure_ascii=False)
            file.write("\n")

    return data

# 运行爬虫
web_crawl()
