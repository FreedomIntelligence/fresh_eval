# %%
from bs4 import BeautifulSoup
import requests
import os
from tqdm import tqdm
# from datetime import datetime 
import datetime 



# %%
# path_list = []

# https://arxiv.org/search/advanced?advanced=1&terms-0-operator=AND&terms-0-term=&terms-0-field=title&classification-physics=y&classification-include_cross_list=exclude&date-year=&date-filter_by=date_range&date-from_date=2023-12-18&date-to_date=2023-12-19&date-date_type=submitted_date_first&abstracts=hide&size=100&order=-announced_date_first&start=0
# https://arxiv.org/search/advanced?advanced=1&terms-0-operator=AND&terms-0-term=&terms-0-field=title&classification-physics=y&classification-include_cross_list=exclude&date-year=&date-filter_by=date_range&date-from_date=2023-12-20&date-to_date=2023-12-25&date-date_type=submitted_date_first&abstracts=hide&size=10&order=-announced_date_first&start=0
# %%
import requests
from requests.exceptions import RequestException
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm.notebook import tqdm
import time
import threading

def download_pdf(pdf_url, path, total_size, max_retries=3, timeout=10, update_progress=None):
    pdf_name = pdf_url.split('/')[-1]
    file_path = os.path.join(path, f'{pdf_name}.pdf')

    attempts = 0
    while attempts < max_retries:
        try:
            with requests.get(pdf_url, stream=True, timeout=timeout) as r:
                r.raise_for_status()
                with open(file_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            if update_progress:
                update_progress()
            return True
        except RequestException as e:
            attempts += 1
            time.sleep(1)
            if attempts == max_retries:
                if update_progress:
                    update_progress()
                return False

def progress_monitor(total_tasks):
    progress = tqdm(total=total_tasks, desc="downloading", leave=True)
    while not progress_monitor.finished:
        progress.n = progress_monitor.completed_tasks
        progress.refresh()
        time.sleep(0.5)
    progress.n = progress_monitor.completed_tasks
    progress.refresh()
    progress.close()

def download_pdfs_concurrently(pdf_links, path, num_threads=10):
    os.makedirs(path, exist_ok=True)
    progress_monitor.completed_tasks = 0
    progress_monitor.finished = False

    def update_progress():
        progress_monitor.completed_tasks += 1

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(download_pdf, url, path, 0, update_progress=update_progress) for url in pdf_links]
        
        monitor_thread = threading.Thread(target=progress_monitor, args=(len(pdf_links),))
        monitor_thread.start()

        for future in as_completed(futures):
            pass

    progress_monitor.finished = True
    monitor_thread.join()
    


from PyPDF2 import PdfReader

def extract_first_n_chars_from_pdfs(folder_path, n,pdf_limit=100):
    extracted_texts = []
    pdf_count=0
    for filename in tqdm(os.listdir(folder_path)):
        if filename.endswith('.pdf'):
            file_path = os.path.join(folder_path, filename)
            pdf_count+=1
            if pdf_count>pdf_limit:
                break
            try:
                with open(file_path, 'rb') as file:
                    reader = PdfReader(file)
                    text = ""
                    for page in reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text
                            if len(text) >= n:
                                break
                    extracted_texts.append(text[:n])
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    return extracted_texts

import json

def rq_arxiv(config=None):
    

    BEGIN_DATE = (datetime.datetime.now()-datetime.timedelta(days=5)).strftime("%Y-%m-%d")
    END_DATE =  datetime.datetime.now().strftime("%Y-%m-%d")
    PAGE_SIZE = '100'
    START = '0'
    PAGE = 11
    # TYPE = '&classification-computer_science=y'
    # # TYPE = '&classification-mathematics=y'
    # TYPE = '&classification-physics=y'

    raw_save_path=config['save_path']
    if 'specific_year' not in config:
        specific_year='2018'
    else:
        specific_year=config['specific_year']
    types=[
    '&classification-computer_science=y',
    '&classification-mathematics=y',
    '&classification-physics=y',
    '&classification-q_biology=y',
    '&classification-q_finance=y',
    '&classification-statistics=y',
    '&classification-economics=y',
    '&classification-eess=y']

    sss='''computer_science
mathematics
physics
q_biology
q_finance
statistics
economics
eess'''
    topic_PATHs=sss.split('\n')
    for idx in range(len(types)):
        topic_this_PATH=topic_PATHs[idx]    
        TYPE=types[idx]
        print(f'topic_this_PATH:{topic_this_PATH} {TYPE}')
        new_save_path=raw_save_path[:raw_save_path.rfind('.')]+'_'+topic_this_PATH+raw_save_path[raw_save_path.rfind('.'):]
        config["save_path"]=new_save_path
    


    # PATH = 'arxiv_pdfs_phi'
    # if config is None:
    #     config={}
    #     config['max_scrolls']=7
    #     config['save_path']=r'.\data\2023-12-24\arxiv_data,jsonl'
        # config['save_path']=r'C:\Users\jijivski\Desktop\local_VS\uncheatable_eval\data\2023-12-24\arxiv_data.jsonl'
        path_list=[]
        for START in [str(i * int(PAGE_SIZE)) for i in range(PAGE)]:
        
            # url = f'https://arxiv.org/search/advanced?advanced=1&terms-0-operator=AND&terms-0-term=&terms-0-field=title{TYPE}&classification-include_cross_list=exclude&date-year=&date-filter_by=date_range&date-from_date={BEGIN_DATE}&date-to_date={END_DATE}&date-date_type=submitted_date_first&abstracts=hide&size={PAGE_SIZE}&order=-announced_date_first&start={START}'
            # url = f'https://arxiv.org/search/advanced?advanced=1&terms-0-operator=AND&terms-0-term=&terms-0-field=title{TYPE}&classification-include_cross_list=exclude&date-year=&date-filter_by=date_range&date-from_date={BEGIN_DATE}&date-to_date={END_DATE}&date-date_type=submitted_date_first&abstracts=hide&size={PAGE_SIZE}&order=-announced_date_first&start={START}'
            url = f'https://arxiv.org/search/advanced?advanced=1&terms-0-operator=AND&terms-0-term=&terms-0-field=title{TYPE}&classification-include_cross_list=include&date-filter_by=specific_year&date-year={specific_year}&date-from_date=&date-to_date=&date-date_type=submitted_date&abstracts=show&size={PAGE_SIZE}&order=-announced_date_first&start={START}'
            print(f'url:{url}')

            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            papers = soup.find_all('li', class_='arxiv-result')

            pdf_links = [paper.find('a', string='pdf')['href'] for paper in papers if paper.find('a', string='pdf')]

            print(f"start:{START} success:{len(pdf_links)}")
            
            path_list += pdf_links
            
            if len(pdf_links) == 0:
                break
        print('len(path_list)',len(path_list))
        path_list=path_list[:100]
        print(f'total:{len(path_list)}')
        download_pdfs_concurrently(path_list, config['save_folder_pdf_arxiv'])
        
        max_sample = 1000
        begin = 0
        # end = 5000
        end = 50000


        assert begin < end

        extracted_texts = extract_first_n_chars_from_pdfs(config['save_folder_pdf_arxiv'], end,pdf_limit=10)

        extracted_texts = [text.encode('utf-8', 'ignore').decode('utf-8') for text in extracted_texts]

        extracted_texts = [x[begin: end] for x in extracted_texts]

        extracted_texts = [x for x in extracted_texts if len(x) > 50]

        extracted_texts = extracted_texts[:max_sample]

        print(len(extracted_texts))

        print([len(x) for x in extracted_texts])
        with open(config['save_path'], "a", encoding="utf-8") as file:
            # for entry in data:
            # entry=main(urls)
            for x in extracted_texts:
                entry = {"date": datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"), "error": False, "url": 'PDF','text_blocks':x}
                json.dump(entry, file, ensure_ascii=False)

                file.write("\n")
                print(entry)


# if __name__ == "__main__":
    # config['save_path']=r'arxiv_data,jsonl'
    # rq_arxiv()




