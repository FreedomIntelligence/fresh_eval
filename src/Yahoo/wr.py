
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
    import pdb
    pdb.set_trace()
    # news_links = page.query_selector_all("a:has(> u.StretchedBox)")
    news_links = page.query_selector_all("a:has(> h3)")
    
    # 在你提到的选择器"a:has(> u.StretchedBox)"中，使用的是CSS选择器的:has()伪类功能，这是一个相对较新的添加到CSS选择器中的功能，旨在提供一种选择器内查询的方式。它允许你选择那些包含特定后代元素的父元素。不过，要注意的是，:has()选择器在写作时有着一定的限制，特别是在Web自动化测试框架如Playwright中的支持情况可能会有所不同。
    # :has(): 伪类选择器，用于选择包含符合括号内条件的元素的父元素。
    # >: 是一个直接子代选择器，用于选择直接位于某元素内部的子元素。
    # u.StretchedBox: 指的是具有StretchedBox类的<u>元素。
    # 因此，"a:has(> u.StretchedBox)"的含义是：选择直接包含有类名为StretchedBox的<u>元素作为直接子元素的<a>元素。

    # news_links = 
    #slingstoneStream-0-Stream > ul > li:nth-child(41) > div > div > div.Ov\(h\).Pend\(44px\).Pstart\(25px\) > h3
    # news_links = page.query_selector_all("h3[>a[title][href]]")

    # news_links = page.query_selector_all("a[title][href]")
    # # page.query_selector_all("a:has(>href)")
    # page.query_selector_all("a:has(title)")
    # len(urls)
    # urls[:-40]
    # news=[url for url in urls if 'news' in url]


    # '''//*[@id="nimbus-app"]/section/section/section/article/section[6]/div/div[1]/div/div/ul/li[3]/section/div/a'''

    # page.query_selector_all("a:has(> u.StretchedBox)")#[5].inner_text()
    # page.query_selector_all("div[class='Pos(r) Z(2) Fw(b)']")[0]#.get_attribute("h3")# h3 a
    # news_links = page.query_selector_all("a[data-testid='internal-link']")


    urls = [link.get_attribute("href") for link in news_links if link.get_attribute("href")]
    urls=[url for url in urls if 'news' in url]
    print(len(urls),'urls:',urls)
    # 遍历链接并提取信息
    for url in urls:#[20:26]
        # endswith a number:
        if not url.endswith("html"):
            print("not endswith a html skip",url)
            continue
        # full_url=f"https://finance.yahoo.com/{url}"
        full_url=url
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
