from playwright.sync_api import sync_playwright

# -------------------------------------------------------------
# Basic Playwright options
# -------------------------------------------------------------
def connect_chrome(playwright):
    # playwright = sync_playwright()
    browser = playwright.chromium.launch(headless=False,executable_path='C:\Program Files\Google\Chrome\Application\chrome.exe')
    # browser = playwright.chromium.launch(headless=False)
    # browser = playwright.chromium.launch(headless=True)
    # browser = playwright.chromium.launch(headless=config['headless'])

    # browser = playwright.chromium.launch(headless=False, args=['--incognito', '--no-sandbox', '--disable-dev-shm-usage'])
    context = browser.new_context()
    # 设置不加载图片
    # context.set_default_navigation_timeout(60000)
    # context.set_default_timeout(60000)
    page = context.new_page()
    page.set_viewport_size({"width": 1920, "height": 1080})
    return page, context, browser

# -------------------------------------------------------------
# question url crawler 
# -------------------------------------------------------------
def questions(topics_list=['topics_list']):
    url_bag = set()
    page, context, browser = connect_chrome()
    topic_index = -1
    loop_limit = len(topics_list)
    print('Starting the questions crawling')
    while True:
        print('--------------------------------------------------')
        topic_index += 1
        if topic_index >= loop_limit:
            print('Crawling completed')
            browser.close()
            break
        topic_term = topics_list[topic_index].strip()
        # Looking if the topic has an existing Quora url
        print('#########################################################')
        print('Looking for topic number : ', topic_index, ' | ', topic_term)
        try:
            url = topic_term
            page.goto(url)
            page.wait_for_timeout(5000)
        except Exception as e0:
            print('topic does not exist in Quora')
            continue

        # get browser source
        html_source = page.content()
        question_count_soup = BeautifulSoup(html_source, 'html.parser')
        all_question_htmls = question_count_soup.find_all('a', {'class': 'q-box qu-display--block qu-cursor--pointer qu-hover--textDecoration--underline Link___StyledBox-t2xg9c-0 dxHfBI'}, href=True)

        #  get total number of questions
        question_count = len(all_question_htmls)
        if question_count is None or question_count == 0:
            print('topic does not have questions...')
            continue

        # 爬取更多问题（如果有）
        # 注意：根据实际页面结构和行为调整此部分
        # Playwright 与 Selenium 不同，可能需要调整滚动和页面加载策略

        # get html page source
        html_source = page.content()
        soup = BeautifulSoup(html_source, 'html.parser')

        all_htmls = soup.find_all('a', {'class': 'q-box qu-display--block qu-cursor--pointer qu-hover--textDecoration--underline Link___StyledBox-t2xg9c-0 dxHfBI'}, href=True)
        question_count_after_scroll = len(all_htmls)
        print(f'number of questions for this topic : {question_count_after_scroll}')

        # add questions to a set for uniqueness
        for html in all_htmls:
            url_bag.add(html['href'])

        sleep_time = (round(random.uniform(15, 32), 1))
        page.wait_for_timeout(sleep_time * 1000)
        
    browser.close()
    return list(url_bag)

ls=questions()
print(ls,len(ls))