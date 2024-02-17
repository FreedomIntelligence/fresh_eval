
from playwright.sync_api import sync_playwright
import json
import datetime
import random

import re
def clean_special_char(text = "your text with special characters like \u200b\u200c\n\t."):
# 
    # Regular expression to match unwanted characters
    pattern = r'[\u200b\u200c\n\t]+'
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text

def extract_text(page, selector):
    elements = page.query_selector_all(selector)
    print(page.content())
    ans="\n".join([element.inner_text() for element in elements if element.inner_text().strip()])
    return clean_special_char(ans)

def click_button_if_exists(page):
    button_selector = "button.link.caas-button.collapse-button"
    # Check if the button exists
    button = page.query_selector(button_selector)
    if button:
        # Click the button if it exists
        button.click()

def random_scroll(page, max_scrolls):
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
    page.goto("https://finance.yahoo.com/",timeout=120000)

    random_scroll(page,3)#TODO

    # 获取所有新闻链接
    # news_links = page.query_selector_all("a[data-testid='internal-link']")

    # news_links = page.query_selector_all("div[class='Pos(r) Z(2) Fw(b)'] h3 a")
    news_links = page.query_selector_all("a:has(> u.StretchedBox)")
    # page.query_selector_all("a:has(> u.StretchedBox)")#[5].inner_text()
    # page.query_selector_all("div[class='Pos(r) Z(2) Fw(b)']")[0]#.get_attribute("h3")# h3 a
    # news_links = page.query_selector_all("a[data-testid='internal-link']")


    urls = [link.get_attribute("href") for link in news_links if link.get_attribute("href")]
    print(len(urls),'urls:',urls)
    # 遍历链接并提取信息
    for url in urls:#[20:26]
        # endswith a number:
        if not url.endswith("html"):
            print("not endswith a html skip",url)
            continue
        full_url=f"https://finance.yahoo.com/{url}"
        print("url:",full_url)
        page.goto(full_url)
        text_blocks=None

        # 提取页面标题和文本
        # title = page.query_selector("h1")  # 假设标题总是在 h1 标签中
        # content = page.query_selector("article")  # 假设主要内容在 article 标签中
        try:
            click_button_if_exists(page)
            text_blocks = extract_text(page, "div[class='caas-body'] p")#, ul[class=]
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


# with sync_playwright() as playwright:
#     run(playwright)
def wr_Yahoo(config=None):
    if  config is None:
        config={}
        config['save_path']='.data/Yahoo_data.jsonl'

    with sync_playwright() as playwright:
        run(playwright,config)
