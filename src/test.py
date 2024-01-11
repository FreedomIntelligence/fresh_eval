from playwright.sync_api import sync_playwright

def run():
    # 启动浏览器
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()

        # 创建一个新的浏览器上下文
        context = browser.new_context()

        # 创建一个新的页面
        page = context.new_page()

        # 导航到 Google 主页
        page.goto('https://www.google.com')

        # 截取屏幕截图
        page.screenshot(path='screenshot.png')

        # 关闭浏览器
        browser.close()

run()