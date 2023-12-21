from playwright.sync_api import sync_playwright
import json
from datetime import datetime

def scrape_wikipedia_new_pages(limit=50):
    with sync_playwright() as playwright:
        # 启动浏览器
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # 导航至 Wikipedia 新页面列表
        page.goto(f"https://en.wikipedia.org/w/index.php?title=Special:NewPages&offset=&limit={limit}")

        # 选择所有链接
        links = page.query_selector_all("ul li a")

        data = []
        for link in links:
            # 提取链接的 URL 和文本
            error=True
            text=None
            url=None
            try:
                url = link.get_attribute("href")
                text = link.inner_text()
                error=False
            except Exception as e:
                print(e)
                print("can not find url or text")


            # 将数据添加到列表中
            # data.append({
            #     "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            #     "error": error,
            #     "url": f"https://en.wikipedia.org{url}",
            #     "text": text
            # })
            entry={"date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "error": error,
                "url": f"https://en.wikipedia.org{url}",
                "text": text
            }
            with open("wikipedia_new_pages.jsonl", "a", encoding="utf-8") as file:
                json.dump(entry, file, ensure_ascii=False)
                file.write("\n")

        context.close()
        browser.close()

        return data

new_pages_data = scrape_wikipedia_new_pages()
print("Data saved to 'wikipedia_new_pages.jsonl'")
