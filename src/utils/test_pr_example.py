from playwright.sync_api import sync_playwright

def test_google_search():
    # 启动 Playwright 并创建一个浏览器实例
    with sync_playwright() as p:
        # browser = p.chromium.launch(headless=False)  # 设置 headless=False 以在有头模式下运行
        # browser = playwright.chromium.launch(headless=True)
        browser = playwright.chromium.launch(headless=config['headless'])

        
        page = browser.new_page()

        # 打开 Google 主页
        page.goto("https://www.google.com")

        # 确认页面已正确加载
        assert "Google" in page.title()

        # 在搜索框中输入查询并提交
        page.fill("input[name=q]", "Playwright GitHub")
        page.press("input[name=q]", "Enter")

        # 等待搜索结果页面加载
        page.wait_for_selector("text=GitHub - microsoft/playwright: Node.js library to")

        # 验证结果页面是否包含预期的文本
        assert "GitHub - microsoft/playwright: Node.js library to" in page.content()

        # 关闭浏览器
        browser.close()

# 请注意，此测试脚本需要在测试框架（如 pytest）下运行。


# playwright codegen https://www.bbc.com/news
        