# from playwright.sync_api import Playwright, sync_playwright, expect


# def run(playwright: Playwright) -> None:
#     browser = playwright.chromium.launch(headless=False)
#     context = browser.new_context()
#     page = context.new_page()
#     page.goto("https://www.bbc.com/news")
#     page.get_by_role("link", name="A volcano spews lava and").click()

#     # ---------------------
#     context.close()
#     browser.close()


# with sync_playwright() as playwright:
#     run(playwright)



from playwright.sync_api import sync_playwright
import json
import datetime
import json
import os
import pickle
import time
import requests
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
# import playwright


def extract_text(page, selector):
    elements = page.query_selector_all(selector)
    # print(page.content())
    return "\n".join([element.inner_text() for element in elements if element.inner_text().strip()])


# def download_leecode():
def download(problem_num, url, title, solution_slug,playwright):
    print(f"Fetching problem num {problem_num} with url {url}")
    n = len(title)
    browser = playwright.chromium.launch(headless=False,executable_path='C:\Program Files\Google\Chrome\Application\chrome.exe')
    # browser = playwright.chromium.launch(headless=False)
    # browser = playwright.chromium.launch(headless=True)
    # browser = playwright.chromium.launch(headless=config['headless'])

    context = browser.new_context()
    # context.set_extra_http_headers({
    #     'Accept-Language': 'en-US,en;q=0.9'  # 优先请求英语内容
    #     })

    context.set_extra_http_headers({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        # 可以根据需要添加其他头部信息
    })

    error=True
    # 请求拦截函数
    def intercept_request(route, request):
        if "leetcode-cn.com" in request.url:
            route.abort()  # 如果请求的URL包含leetcode-cn.com，则取消请求
        else:
            route.continue_()  # 其他请求正常继续

    # 添加请求拦截器
    # context.route('**/*', intercept_request)# weism #TODO 中文跳转的问题

    page = context.new_page()
    page.goto(url)
    try:
        # 使用 Playwright
        # with playwright.chromium.launch(headless=True) as browser:
        #     page = browser.new_page()
        #     page.goto(url)
        #     page.wait_for_selector("._1l1MA")  # 等待元素加载

        #     # 获取页面源代码
        # qd-content > div.h-full.flex-col.ssg__qd-splitter-primary-w > div > div > div > div.flex.h-full.w-full.overflow-y-auto.rounded-b > div > div > div:nth-child(3) > div.xFUwe
        page.wait_for_selector("div[data-track-load='description_content']")  # 等待元素加载
        text_blocks = extract_text(page, "div[data-track-load='description_content']")#, ul[class=]
        print("text_blocks:",text_blocks)



        # html = page.content()
        # soup = BeautifulSoup(html, "html.parser")
        # _title=soup.find("")
        # # print("soup:",soup)
        # text_blocks = soup.find("div", {"class": "_1l1MA"}).text
        error=False
            


            # 构建 HTML
            # title_decorator = '*' * n
            # problem_title_html = title_decorator + f'<div id="title">{title}</div>' + '\n' + title_decorator
            # problem_html = problem_title_html + str(soup.find("div", {"class": "_1l1MA"})) + '<br><br><hr><br>'

            # # 追加内容到 HTML 文件
            # with open("out.html", "ab") as f:
            #     f.write(problem_html.encode(encoding="utf-8"))

            # # 创建并追加章节到 EPUB
            # c = epub.EpubHtml(title=title, file_name=f'chap_{problem_num}.xhtml', lang='hr')
            # c.content = problem_html
            # chapters.append(c)

            # # 写入章节列表到 pickle 文件
            # dump_chapters_to_file(chapters)
            # # 更新已下载的问题
            # update_tracker('track.conf', problem_num)

        print(f"Writing problem num {problem_num} with url {url} successful")


    except Exception as e:
        print(f"Failed Writing!! {e}")

    entry = {"date": datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"), "error": error, "url": full_url,'text_blocks':text_blocks}
    with open("Leecode_data.jsonl", "a", encoding="utf-8") as file:
        # for entry in data:
        json.dump(entry, file, ensure_ascii=False)
        file.write("\n")





import requests

# 获取LeetCode算法题目的数据
url = "https://leetcode.com/api/problems/algorithms/"
response = requests.get(url)
algorithms_problems_json = response.json()

# 从数据中提取题目信息
# for problem in data['stat_status_pairs']:
#     question_title_slug = problem['stat']['question__title_slug']
#     print(question_title_slug)

links=[]
for child in algorithms_problems_json["stat_status_pairs"]:
    # Only process free problems
    if not child["paid_only"]:
        question__title_slug = child["stat"]["question__title_slug"]
        question__article__slug = child["stat"]["question__article__slug"]
        question__title = child["stat"]["question__title"]
        frontend_question_id = child["stat"]["frontend_question_id"]
        difficulty = child["difficulty"]["level"]
        links.append(
            (question__title_slug, difficulty, frontend_question_id, question__title, question__article__slug))

completed_upto=2200
    
has_new_problems = (completed_upto != len(links) - 1)#2242
print("has_new_problems:",has_new_problems)


links = sorted(links, key=lambda x: (x[1], x[2]))
downloaded_now = 0
ALGORITHMS_BASE_URL = "https://leetcode.com/problems/"

try:
    for i in range(completed_upto + 1, len(links)):
        question__title_slug, _, frontend_question_id, question__title, question__article__slug = links[i]
        full_url = ALGORITHMS_BASE_URL + question__title_slug
        print(f"Downloading problem num {frontend_question_id} with url {full_url}")
        title = f"{frontend_question_id}. {question__title}"

        # Download each file as html and write chapter to chapters.pickle
        with sync_playwright() as playwright:
            download(i, full_url, title, question__article__slug,playwright=playwright)
        downloaded_now += 1

        # if downloaded_now == MAXIMUM_NUMBER_OF_PROBLEMS_PER_INSTANCE:
        #     break
        # # Sleep for 5 secs for each problem and 2 mins after every 30 problems
        # if i % 30 == 0:
        #     print(f"Sleeping 120 secs\n")
        #     time.sleep(120)
        # else:
        #     print(f"Sleeping {SLEEP_TIME_PER_PROBLEM_IN_SECOND} secs\n")
        #     time.sleep(SLEEP_TIME_PER_PROBLEM_IN_SECOND)


except Exception as e:
    print(e)
    print("can not find url or text")


# from playwright.sync_api import sync_playwright
# import json
# import datetime
# def extract_text(page, selector):
#     elements = page.query_selector_all(selector)
#     print(page.content())
#     return "\n".join([element.inner_text() for element in elements if element.inner_text().strip()])

# def run(playwright):
#     browser = playwright.chromium.launch(headless=False)
#     # # 同步方式
#     # storage = context.storage_state(path="state.json")

#     # # 异步方式
#     # storage = await context.storage_state(path="state.json")

#     # # 同步方式
#     # context = browser.new_context(storage_state="state.json")

#     # # 异步方式
#     # context = await browser.new_context(storage_state="state.json")



#     context = browser.new_context()
    
#     # 打开 BBC 新闻主页
#     page = context.new_page()
#     page.goto("https://www.bbc.com/news")

#     # 获取所有新闻链接
#     news_links = page.query_selector_all("a[data-testid='internal-link']")
#     urls = [link.get_attribute("href") for link in news_links if link.get_attribute("href")]
#     print('urls:',urls)

#     # 遍历链接并提取信息
#     for url in urls:#[20:26]
#         # endswith a number:
#         if not url[-1].isdigit():
#             print("not endswith a number skip",url)
#             continue
#         full_url=f"https://www.bbc.com{url}"
#         print("url:",full_url)
#         page.goto(full_url)
#         text_blocks=None

#         # 提取页面标题和文本
#         # title = page.query_selector("h1")  # 假设标题总是在 h1 标签中
#         # content = page.query_selector("article")  # 假设主要内容在 article 标签中
#         try:
#             text_blocks = extract_text(page, "section[data-component='text-block']")#, ul[class=]
#             print("text_blocks:",text_blocks)

#             # element=page.locator("section[data-component='text-block']")
#             # text_blocks = element.inner_text()
#             error=False


#         except Exception as e:  
#             print(e)
#             print("can not find text_blocks")
#             error=True


#         entry = {"date": datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"), "error": error, "url": full_url,'text_blocks':text_blocks}
#         with open("BBCdata.jsonl", "a", encoding="utf-8") as file:
#             # for entry in data:
#             json.dump(entry, file, ensure_ascii=False)
#             file.write("\n")

#         print("\n----------\n")

#     # 关闭浏览器
#     context.close()
#     browser.close()

# with sync_playwright() as playwright:
#     run(playwright)
