from src.BBC.wr import wr_bbc as wr_bbc
from src.Wiki.wr import wr_wiki as wr_wiki
from src.wattpad.rq import rq_wattpad as rq_wattpad
from src.arxiv.rq import rq_arxiv as rq_arxiv 
from src.arxiv.rq_year import rq_arxiv as rq_arxiv_year# this is used to crawl a special year's arxiv

from src.Yahoo.wr import wr_Yahoo as wr_Yahoo
from src.reddit.praw import praw_reddit as praw_reddit
from src.quora.wr import wr_quora as wr_quora
from src.github.rq import rq_github as rq_github

from src.checkFile.check_crawl import check_crawl

import os
import datetime
import logging
import time
import json
logging.basicConfig(level=logging.INFO,filename='./app.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.info("start up")



doday=datetime.datetime.now().strftime("%Y-%m-%d")

# os.mkdir(f"/data/{doday}",exist_ok=True)
os.makedirs(f"./data/{doday}", exist_ok=True)

# crawl_list=[rq_github,wr_wiki,wr_quora,rq_arxiv,praw_reddit,wr_bbc,rq_wattpad,wr_Yahoo,]#,
crawl_list=[praw_reddit,rq_wattpad,]#,rq_github,wr_wiki,wr_quorawr_Yahoo#wr_bbc
# crawl_list=[wr_Yahoo]
# crawl_list=[rq_arxiv_year]
for crawler in crawl_list:
    config={}
    st_time=time.time()
    config['save_path']=f"./data/{doday}/{crawler.__name__}.jsonl"
    config['save_folder_pdf_arxiv']=f"./data/{doday}/{crawler.__name__}_pdfs"
    config["topic_quora"]=['Technology','Mathematics','Health','Movies']
    # config['headless']=True
    config['headless']=False
    


    try:
        crawler(config)
        logging.info(f"crawler {crawler.__name__} done, time_used:{round(time.time()-st_time,2)}")
    #     #read file and get how many lines
    #     with open (config['save_path'],'r') as f:
    #         lines=f.readlines()
    #         logger.info(f"crawler {crawler.__name__} done, total lines:{len(lines)}")
            
    #         for line in lines:
    #             data = json.loads(line.strip())
                
    #             # 检查text_blocks是否存在并且长度是否超过300
    #             num_10,num_300,num_5000=0
    #             if 'text_blocks' in data and len(data['text_blocks']) > 10:
    #                 num_10+=1
    #                 if len(data['text_blocks']) > 300:
    #                     num_300+=1
    #                 if len(data['text_blocks']) > 5000:
    #                     num_5000+=1
    #             logger.info(f'num_10:{num_10},num_300:{num_300},num_5000:{num_5000}')
    #             if num_10<50:
    #                 logger.error(f'num_10:{num_10} is less than 50, please check crawler {crawler.__name__}')


    except Exception as e:
        import traceback
        logging.error(f"crawler {crawler.__name__} failed, time_used:{round(time.time()-st_time,2)}, error:{e},trackback:{traceback.format_exc()}")
