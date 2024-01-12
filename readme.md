
# still under construction
env, this repo uses playwright and request to crawl the latest data from the Internet

```bash
set PIP_INDEX_URL=https://pypi.douban.com/simple
export PIP_INDEX_URL=https://pypi.douban.com/simple
pip install playwright
playwright install
```


how to use:
```bash
cd your_path/uncheatable_eval/
python cmd_crawl.py
```

what you will get:
under uncheatable_eval/data/YYYY-MM-DD there will be some jsonl data
each line is like {"date": "2024-01-11-22-30", "error": false, "url": "https://github.com/ProgrammingHero1/B9A1-New-Year-New-Mission", "text_blocks": "pass"}



how to config:
```
in cmd_crawl.py there are a list 

crawl_list=[rq_github,wr_wiki,wr_quora,rq_arxiv,praw_reddit,wr_bbc,rq_wattpad,wr_Yahoo,]

config={} can set some topic and output path
```


## Data Types and Sources
| Data Type          | Representative Website  | URL                                                          |
|:------------------:|:-----------------------:|:------------------------------------------------------------:|
| Financial News     | Yahoo                   | [Yahoo.com](https://www.Yahoo.com)                           |
| Political News     | BBC News                | [bbc.com/news](https://www.bbc.com/news)                     |
| Discussion         | Reddit                  | [reddit_new.com](https://www.reddit.com/r/all/new/) (Crawling the latest content without a specific theme) |
| Online Literature  | Wattpad                 | [wattpad.com](https://www.wattpad.com)                       |
| Encyclopedia       | Wikipedia Latest Changes | [en.wikipedia.org/wiki/Special:NewPages](https://en.wikipedia.org/wiki/Special:NewPages) |
| Academic Papers    | arXiv                   | [arxiv.org](https://arxiv.org) (Crawling the latest content in various fields) |
| Code               | GitHub Trending         | [github.com/trending](https://github.com/trending)           |
| Forum              | Quora                   | [quora_week.com](https://www.quora.com/search?q=new&time=week) (Currently choose a few topics) |

Quora is currently crawling 'Technology', 'Mathematics', 'Health', 'Movies' four popular topics.
arXiv covers 'computer_science', 'mathematics', 'physics', 'q_biology', 'q_finance', 'statistics', 'economics', 'eess' 8 topics.
Potential content to expand in the future

| Data Type                                  | Representative Website | URL                               |
|:------------------------------------------:|:----------------------:|:---------------------------------:|
| Blogs (stuck due to anti-crawling)         | Medium                 | [medium.com](https://medium.com)  |
| Coding Problems (uncertain about new problems, and relatively few in number) | LeetCode              | [leetcode.com](https://leetcode.com) |


---

### chinese table

| 数据类型 | 代表性网站 | 网址 |
|:------:|:------:|:------:|
| 金融新闻 | Yahoo | [Yahoo.com](https://www.Yahoo.com) |
| 政治新闻 | BBC News | [bbc.com/news](https://www.bbc.com/news) |
| 讨论 | Reddit | [reddit_new.com](https://www.reddit.com/r/all/new/)(无主题,爬取最新的内容)|
| 网文 | Wattpad | [wattpad.com](https://www.wattpad.com) |
| 百科 | Wikipedia 最新更改 | [en.wikipedia.org/wiki/Special:NewPages](https://en.wikipedia.org/wiki/Special:NewPages) |
| 论文 | arXiv | [arxiv.org](https://arxiv.org)(分领域爬取最新的内容)|
| 代码 | GitHub Trending | [github.com/trending](https://github.com/trending) |
| 论坛 | Quora | [quora_week.com](https://www.quora.com/search?q=new&time=week)(目前爬取部分主题) |

Quora 目前爬取了'Technology','Mathematics','Health','Movies' 四个热门主题
arXiv 共有'computer_science,','mathematics','physics','q_biology','q_finance','statistics','economics','eess' 8个主题
之后可能继续扩展的内容
| 数据类型 | 代表性网站 | 网址 |
|:------:|:------:|:------:|
| 博客(反爬卡住了) | Medium | [medium.com](https://medium.com) |
| 代码题目(不能确定新题,而且量比较少) | LeetCode | [leetcode.com](https://leetcode.com) |
