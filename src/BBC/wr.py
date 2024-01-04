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
    # print(page.content())
    return "\n".join([element.inner_text() for element in elements if element.inner_text().strip()])

def run(playwright,config):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    
    # 打开 BBC 新闻主页
    page = context.new_page()
    page.goto("https://www.bbc.com/news")

    # 获取所有新闻链接
    news_links = page.query_selector_all("a[data-testid='internal-link']")
    urls = [link.get_attribute("href") for link in news_links if link.get_attribute("href")]
    print('urls:',urls)

    # 遍历链接并提取信息
    for url in urls:#[20:26]
        # endswith a number:
        if not url[-1].isdigit():
            print("not endswith a number skip",url)
            continue
        full_url=f"https://www.bbc.com{url}"
        print("url:",full_url)
        page.goto(full_url)
        text_blocks=None

        # 提取页面标题和文本
        # title = page.query_selector("h1")  # 假设标题总是在 h1 标签中
        # content = page.query_selector("article")  # 假设主要内容在 article 标签中
        try:
            text_blocks = extract_text(page, "section[data-component='text-block']")#, ul[class=]
            print("text_blocks:",text_blocks)

            # element=page.locator("section[data-component='text-block']")
            # text_blocks = element.inner_text()
            error=False


        except Exception as e:  
            print(e)
            print("can not find text_blocks")
            error=True


        entry = {"date": datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"), "error": error, "url": full_url,'text_blocks':text_blocks}
        with open(config['save_path'], "a", encoding="utf-8") as file:
            # for entry in data:
            json.dump(entry, file, ensure_ascii=False)
            file.write("\n")

        print("\n----------\n")

    # 关闭浏览器
    context.close()
    browser.close()

def wr_bbc(config=None):
    if  config is None:
        config={}
        config['save_path']='.data/BBC_data.jsonl'

    with sync_playwright() as playwright:
        run(playwright,config)
