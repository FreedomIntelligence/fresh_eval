# from playwright.sync_api import sync_playwright
# import json
# import datetime
# def extract_text(page, selector):
#     elements = page.query_selector_all(selector)
#     print(page.content())
#     return "\n".join([element.inner_text() for element in elements if element.inner_text().strip()])

# def run(playwright,config=None):
#     browser = playwright.chromium.launch(headless=False,executable_path='C:\Program Files\Google\Chrome\Application\chrome.exe')
#     context = browser.new_context()
    
#     # 打开 BBC 新闻主页
#     page = context.new_page()
#     context.set_extra_http_headers({
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#         'Accept-Language': 'en-US,en;q=0.9',
#         'Accept-Encoding': 'gzip, deflate, br',
#         # 可以根据需要添加其他头部信息
#     })
#     page.goto("https://www.reddit.com/r/all/new/?feedViewType=cardView")

#     # 获取所有新闻链接
#     input()
#     news_links = page.query_selector_all("a[slot='full-post-link']")
#     urls = [link.get_attribute("href") for link in news_links if link.get_attribute("href")]
#     print('urls:',urls)

#     # 遍历链接并提取信息
#     for url in urls[20:26]:#
#         # endswith a number:
#         if not 'news/articles/' in url:#TODO add more content type #url[-1].isdigit():
#             print("not articles skip",url)
#             continue
#         full_url=f"https://www.reddit.com{url}"
#         print("url:",full_url)
#         page.goto(full_url)
#         text_blocks=None

#         # 提取页面标题和文本
#         # title = page.query_selector("h1")  # 假设标题总是在 h1 标签中
#         # content = page.query_selector("article")  # 假设主要内容在 article 标签中
#         try:
#             text_blocks = extract_text(page, "div[slot='text-body'] div div p")#, ul[class=]
#             print("text_blocks:",text_blocks)
#             title = extract_text(page, "h1[slot='title']")
#             print("title:",title)
#             text_blocks=title+'\n'+text_blocks

#             # element=page.locator("section[data-component='text-block']")
#             # text_blocks = element.inner_text()
#             error=False


#         except Exception as e:  
#             print(e)
#             print("can not find text_blocks")
#             error=True


#         entry = {"date": datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"), "error": error, "url": full_url,'text_blocks':text_blocks}
#         with open(config['save_path'], "a", encoding="utf-8") as file:
#             # for entry in data:
#             json.dump(entry, file, ensure_ascii=False)
#             file.write("\n")

#         print("\n----------\n")

#     # 关闭浏览器
#     context.close()
#     browser.close()

# def wr_Yahoo(config=None):
#     if  config is None:
#         config={}
#         config['save_path']='.data/Yahoo_data.jsonl'

#     with sync_playwright() as playwright:
#         run(playwright,config)
