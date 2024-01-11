
from playwright.sync_api import sync_playwright
import json
import datetime
def extract_text(page, selector):
    elements = page.query_selector_all(selector)
    # print(page.content())
    return "\n".join([element.inner_text() for element in elements if element.inner_text().strip()])

def random_scroll(page, max_scrolls=None):
    import random

    if max_scrolls is None:
        max_scrolls=7
    for _ in range(max_scrolls):
        # Scroll to a random position on the page
        scroll_height = random.randint(500, 10000)
        page.evaluate(f"window.scrollBy(0, {scroll_height})")
        
        # Wait for a random amount of time
        random_wait = random.uniform(0.5, 3.0)
        page.wait_for_timeout(int(random_wait * 1000))

def run(playwright,config):
    # browser = playwright.chromium.launch(headless=False)
    browser = playwright.chromium.launch(headless=config['headless'])

    
    context = browser.new_context()
    
    # 打开 BBC 新闻主页
    page = context.new_page()
    page.goto("https://en.wikipedia.org/wiki/Special:NewPagesFeed")
    random_scroll(page=page,max_scrolls=config['max_scrolls'] if 'max_scrolls' in config else None)

    # 获取所有新闻链接
    parent_div_selector = "div.mwe-vue-pt-info-pane"
    # Find the first div inside the parent div
    news_links = page.query_selector_all(f"{parent_div_selector} > div > div > span > a") 


    # news_links = page.query_selector_all("a[data-testid='internal-link']")
    urls = [link.get_attribute("href") for link in news_links if link.get_attribute("href")]
    urls = [link for link in urls if link.startswith("/wiki")]

    print('urls:',urls)

    # 遍历链接并提取信息
    for url in urls:#[20:26]
        # endswith a number:
        # if not url[-1].isdigit():
        #     print("not endswith a number skip",url)
        #     continue
        full_url=f"https://en.wikipedia.org{url}"
        print("url:",full_url)
        page.goto(full_url)
        text_blocks=None

        # 提取页面标题和文本
        # title = page.query_selector("h1")  # 假设标题总是在 h1 标签中
        # content = page.query_selector("article")  # 假设主要内容在 article 标签中
        try:
            selector='#mw-content-text > div.mw-content-ltr.mw-parser-output'
            text_blocks = extract_text(page, selector)#, ul[class=]
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



def wr_wiki(config=None):
    if config is None:
        config={}
        config['max_scrolls']=7
        config['save_path']='.data/Wiki_data.jsonl'
    with sync_playwright() as playwright:
        run(playwright,config)

