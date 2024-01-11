from playwright.sync_api import sync_playwright
import json
import datetime
from bs4 import BeautifulSoup
import re
import time
import random

def random_scroll(page, max_scrolls=5):
    for _ in range(max_scrolls):
        # Scroll to a random position on the page
        scroll_height = random.randint(500, 10000)
        page.evaluate(f"window.scrollBy(0, {scroll_height})")
        
        # Wait for a random amount of time
        random_wait = random.uniform(0.5, 3.0)
        page.wait_for_timeout(int(random_wait * 1000))


def extract_text(page, selector):
    elements = page.query_selector_all(selector)
    print(page.content())
    return "\n".join([element.inner_text() for element in elements if element.inner_text().strip()])

def run(playwright,config= None):
    if config is None:
        config["topic_quora"]=['Technology','Mathematics']
        config["save_path"]='Quora_data.jsonl'
    # browser = playwright.chromium.launch(headless=False,executable_path='C:\Program Files\Google\Chrome\Application\chrome.exe')
    # browser = playwright.chromium.launch(headless=False)
    # browser = playwright.chromium.launch(headless=True)
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

    page.goto("https://www.quora.com/")
    page.get_by_label("Email").click()
    sleep_time = (round(random.uniform(2, 3), 1))
    print(f'sleeping for {sleep_time} seconds')
    time.sleep(sleep_time)
    page.get_by_label("Email").fill("2281255574@qq.com")
    page.get_by_label("Password").click()
    
    sleep_time = (round(random.uniform(2, 3), 1))
    print(f'sleeping for {sleep_time} seconds')
    time.sleep(sleep_time)
    page.get_by_label("Password").fill("Fresh_bench123!")
    
    page.get_by_role("button", name="Login").click()
    sleep_time = (round(random.uniform(2, 7), 1))
    print(f'sleeping for {sleep_time} seconds')
    time.sleep(sleep_time)

    choose_list=["Technology","Health"]
    element=page.get_by_role("link", name=random.choice(choose_list)).click()
    sleep_time = (round(random.uniform(2, 3), 1))
    #go back
    page.keyboard.press("AltLeft+ArrowLeft")
    # with page.expect_popup() as page1_info:
    #     page.locator("#fiunlepovb > div > div > div > div:nth-child(3) > div:nth-child(3) > div > div > div").click()

    topics=config["topic_quora"]
    raw_save_path=config["save_path"]
    for topic in topics:
        new_save_path=raw_save_path[:raw_save_path.rfind('.')]+'_'+topic+raw_save_path[raw_save_path.rfind('.'):]
        config["save_path"]=new_save_path
        page.goto("https://www.quora.com/topic/"+topic)
        random_scroll(page, max_scrolls=10)# TODO
        page.wait_for_selector("span[class='q-box qu-userSelect--text']")
        boxes=page.query_selector_all("span[class='q-box qu-userSelect--text']")
        for box in boxes:
            box.click()
            sleep_time = (round(random.uniform(0.2, 0.4), 1))
            print('click')
        questions=page.query_selector_all("div[class='q-box qu-mb--tiny']")
        questions_text_list=[]# 
        for question in questions:
            questions_text_list.append(question.inner_text())
        # <div class="q-box qu-mb--tiny" style="box-sizing: border-box;"><div class="q-text qu-dynamicFontSize--regular_title qu-fontWeight--bold qu-color--gray_dark_dim qu-passColorToLinks qu-lineHeight--regular qu-wordBreak--break-word" style="box-sizing: border-box;"><span class="CssComponent__CssInlineComponent-sc-1oskqb9-1 UserSelectableText___StyledCssInlineComponent-lsmoq4-0"><span class="CssComponent__CssInlineComponent-sc-1oskqb9-1 TitleText___StyledCssInlineComponent-sc-1hpb63h-0  hiLnej"><a class="q-box Link___StyledBox-t2xg9c-0 dFkjrQ puppeteer_test_link qu-display--block qu-cursor--pointer qu-hover--textDecoration--underline" href="https://www.quora.com/How-are-governments-and-tech-companies-addressing-concerns-about-user-privacy-in-the-digital-age" target="_blank" style="box-sizing: border-box; border-radius: inherit;"><div class="q-click-wrapper qu-display--block qu-tapHighlight--white qu-cursor--pointer qu-hover--textDecoration--underline ClickWrapper___StyledClickWrapperBox-zoqi4f-0 iyYUZT" tabindex="0" style="box-sizing: border-box; font: inherit; padding: 0px; color: inherit; text-align: inherit;"><div class="q-flex qu-flexDirection--row" style="box-sizing: border-box; display: flex;"><div class="q-inline qu-flexWrap--wrap" style="box-sizing: border-box; display: inline; max-width: 100%;"><div class="QuestionTitle___StyledText-exj38m-0 chNUqN puppeteer_test_question_title"><span class="q-box qu-userSelect--text" style="box-sizing: border-box;"><span style="background: none;">How are governments and tech companies addressing concerns about user privacy in the digital age?</span></span></div></div></div></div></a></span></span></div></div>
        # answers=page.query_selector_all("span[class='q-box qu-userSelect--text']")
        answers_text_list=[]#
        answers=page.query_selector_all("div[class='q-box spacing_log_answer_content puppeteer_test_answer_content']")

        for answer in answers:
            answers_text_list.append(answer.inner_text())
        for i in range(len(questions_text_list)):
            print(i,"question:",questions_text_list[i],'\n',answers_text_list[i][:30])
            text_blocks=f"{questions_text_list[i]},'\n',{answers_text_list[i]}"
            entry = {"date": datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"), "error": False, "url": questions_text_list[i],'text_blocks':text_blocks}
            with open( config["save_path"],"a", encoding="utf-8") as file:#config['save_path'],
                # for entry in data:
                json.dump(entry, file, ensure_ascii=False)
                file.write("\n")
        # input('check')
    context.close()
    browser.close()



def wr_quora(config=None):
    
    with sync_playwright() as playwright:
        run(playwright,config)
