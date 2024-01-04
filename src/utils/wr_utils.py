import time
import random

def random_delay(min_seconds=0.1, max_seconds=0.6):
    """
    在指定的最小和最大秒数之间生成随机延迟。
    """
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)

# 示例使用随机延迟
    
# if __name__ == "__main__":
#     for i in range(10):
#         print(f"操作 {i}")
#         random_delay(0.1, 0.5)  # 在1秒到5秒之间随机延迟

#     print("完成！")


def random_scroll(page, max_scrolls):
    for _ in range(max_scrolls):
        # Scroll to a random position on the page
        scroll_height = random.randint(500, 10000)
        page.evaluate(f"window.scrollBy(0, {scroll_height})")
        
        # Wait for a random amount of time
        random_wait = random.uniform(0.5, 3.0)
        page.wait_for_timeout(int(random_wait * 1000))

'''
# files under src/SiteFolder
from ...utils import random_delay
random_delay(0.1, 0.5)
'''