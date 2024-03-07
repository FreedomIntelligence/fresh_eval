
from playwright.sync_api import sync_playwright
import json
import datetime
import random
import pdb
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
    browser = playwright.chromium.launch(headless=config['headless'],executable_path='C:\Program Files\Google\Chrome\Application\chrome.exe')
    # 2281255574@qq.com

    context = browser.new_context()
    
    # 打开 BBC 新闻主页
    page = context.new_page()
    page.goto(f"https://www.gjopen.com/leaderboards/questions", timeout=120000)

    page.get_by_label("Email").fill("2281255574@qq.com")
    page.get_by_label("Password").click()
    # page.get_by_label("Password").click()

    sleep_time = (round(random.uniform(2, 3), 1))
    print(f'sleeping for {sleep_time} seconds')
    import time
    time.sleep(sleep_time)
    page.get_by_label("Password").fill("Fresh_bench123!")

    page.get_by_role("button", name="Sign in").click()

    
    for page_ in range(5,256):
        # page_=1
        with open(config['save_path'], "a", encoding="utf-8") as file:
            # for entry in data:
            # json.dump(url, file, ensure_ascii=False)
            file.write(f"page:{page_}\n")
        print(f"https://www.gjopen.com/leaderboards/questions?page={page_}")
        # page.goto(f"https://www.gjopen.com/leaderboards/questions?page={page}",
        page.goto(f"https://www.gjopen.com/leaderboards/questions?page={page_}", timeout=120000)

        # import pdb
        # pdb.set_trace()


        # random_scroll(page,3)#TODO

        # 获取所有新闻链接
        # news_links = page.query_selector_all("a[data-testid='internal-link']")

        # news_links = page.query_selector_all("div[class='Pos(r) Z(2) Fw(b)'] h3 a")
        import pdb
        # news_links = page.query_selector_all("a:has(> u.StretchedBox)")
        # news_links = page.query_selector_all("a:has(> h3)")
        
        try:
            # click_button_if_exists(page)
            # text_blocks = extract_text(page, "div[class='caas-body'] p")#, ul[class=]
            # text_blocks = extract_text(page, "div[class='row row-table-row'] > div > a")#, ul[class=]
            # pdb.set_trace()

            JSHandle_list=page.query_selector_all("div[class='row row-table-row'] > div > a")
            url_list=[]

            for i in JSHandle_list:
                part_url=i.evaluate('(element) => element.getAttribute("href")')
                url='https://www.gjopen.com/'+part_url.replace('/leaderboards/','')
                url_list.append(url)
                with open(config['save_path'], "a", encoding="utf-8") as file:
                    # for entry in data:
                    json.dump(url, file, ensure_ascii=False)
                    file.write("\n")
        except:
            import traceback
            with open('log.log') as f:
                print(f'{page_} failed')
                f.write(f'{page_} failed')

                print(f'trackback:{traceback.format_exc()}')
                f.write(f'trackback:{traceback.format_exc()}')
                pdb.set_trace()

    # print("\n----------\n")

    # 关闭浏览器
    context.close()
    browser.close()


# with sync_playwright() as playwright:
#     run(playwright)
def wr_gjo(config=None):
    if  config is None:
        config={}
        config['save_path']='./gjo.jsonl'
    config['headless']=False
    with sync_playwright() as playwright:
        run(playwright,config)
wr_gjo()