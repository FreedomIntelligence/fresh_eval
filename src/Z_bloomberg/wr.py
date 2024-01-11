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
def extract_text(page, selector):
    elements = page.query_selector_all(selector)
    print(page.content())
    return "\n".join([element.inner_text() for element in elements if element.inner_text().strip()])

def run(playwright):
    # browser = playwright.chromium.launch(headless=False,executable_path='C:\Program Files\Google\Chrome\Application\chrome.exe')
    # browser = playwright.chromium.launch(headless=False)
    browser = playwright.chromium.launch(headless=config['headless'])

    context = browser.new_context()
    
    # 打开 BBC 新闻主页
    page = context.new_page()
    context.set_extra_http_headers({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        # 可以根据需要添加其他头部信息
    })
    page.goto("https://www.bloomberg.com")

    # 获取所有新闻链接
    news_links = page.query_selector_all("div[data-component='headline'] a")
    urls = [link.get_attribute("href") for link in news_links if link.get_attribute("href")]
    print('urls:',urls)

    # 遍历链接并提取信息
    for url in urls[20:26]:#
        # endswith a number:
        if not 'news/articles/' in url:#TODO add more content type #url[-1].isdigit():
            print("not articles skip",url)
            continue
        full_url=f"https://www.bloomberg.com{url}"
        print("url:",full_url)
        page.goto(full_url)
        text_blocks=None

        # 提取页面标题和文本
        # title = page.query_selector("h1")  # 假设标题总是在 h1 标签中
        # content = page.query_selector("article")  # 假设主要内容在 article 标签中
        try:
            text_blocks = extract_text(page, "p[data-component='paragraph']")#, ul[class=]
            print("text_blocks:",text_blocks)
            title = extract_text(page, "p[data-component='hed-and-dek']")
            print("title:",title)
            text_blocks=title+'\n'+text_blocks

            # element=page.locator("section[data-component='text-block']")
            # text_blocks = element.inner_text()
            error=False


        except Exception as e:  
            print(e)
            print("can not find text_blocks")
            error=True


        entry = {"date": datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"), "error": error, "url": full_url,'text_blocks':text_blocks}
        with open("BBCdata.jsonl", "a", encoding="utf-8") as file:
            # for entry in data:
            json.dump(entry, file, ensure_ascii=False)
            file.write("\n")

        print("\n----------\n")

    # 关闭浏览器
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
