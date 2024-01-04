import argparse
import bs4
import requests
import pyperclip
import re
import pypandoc
import os
import datetime
import json
from bs4 import BeautifulSoup


base_apiV2_url = "https://www.wattpad.com/apiv2/"
base_apiV3_url = "https://www.wattpad.com/api/v3/"
dev_error_msg = "Please check the url again, for valid story id. Contact the developer if you think this is a bug."
"""
https://www.wattpad.com/api/v3/stories/{{story_id}}?drafts=0&mature=1&include_deleted=1&fields=id,title,createDate,modifyDate,voteCount,readCount,commentCount,description,url,firstPublishedPart,cover,language,isAdExempt,user(name,username,avatar,location,highlight_colour,backgroundUrl,numLists,numStoriesPublished,numFollowing,numFollowers,twitter),completed,isPaywalled,paidModel,numParts,lastPublishedPart,parts(id,title,length,url,deleted,draft,createDate),tags,categories,rating,rankings,tagRankings,language,storyLanguage,copyright,sourceLink,firstPartId,deleted,draft,hasBannedCover,length
"""

def get_chapter_id(url):
    """Extracts the chapter ID from the given URL."""
    search_id = re.compile(r'\d{5,}')
    id_match = search_id.search(url)
    if id_match:
        return id_match.group()
    return None


def download_webpage(url):
    """Downloads the webpage content from the given URL."""
    try:
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        res.raise_for_status()
        return res.text
    except requests.exceptions.RequestException as exc:
        print("There was a problem: %s" % (exc))
        return None


def extract_useful_data(json_data):
    """Extracts useful data from the JSON response."""
    summary = json_data.get('description', '')
    tags = json_data.get('tags', '')
    chapters = json_data.get('parts', '')
    storyName = json_data.get('title', '')
    author = json_data.get('user', '')
    cover = json_data.get('cover', '')
    return summary, tags, chapters, storyName, author, cover


def save_html_file(file_name, story_name, author, cover, tags, summary, chapters):
    """Saves the HTML file with the given data."""
    
    for i, chapter in enumerate(chapters[-1:]):
        print('chapters[-1:]',chapters[-1:])# TODO
        # print(f"Getting latest Chapter {chapter + 1}....")
        chapter_url = base_apiV2_url + f"storytext?id={chapter['id']}"
        chapter_content = download_webpage(chapter_url)
        if chapter_content:
            soup_res = bs4.BeautifulSoup(chapter_content, 'html.parser')
            
            # text_blocks=soup_res.prettify()
            error=False
            # remove the html tags
            # text_blocks = soup_res.find_all('p')
            # text_blocks = [x.text() for x in text_blocks]
            text_blocks=soup_res.getText()
            # text_blocks
            full_url=chapter_url
            entry = {"date": datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"), "error": error, "url": full_url,'text_blocks':text_blocks}
            return entry
def main(url):
    story_id = get_chapter_id(url)
    if not story_id:
        print(dev_error_msg)
        return

    # Getting JSON data from Wattpad API.
    story_info_url = base_apiV3_url + f"stories/{story_id}?drafts=0&mature=1&include_deleted=1&fields=id,title,createDate,modifyDate,description,url,firstPublishedPart,cover,language,user(name,username,avatar,location,numStoriesPublished,numFollowing,numFollowers,twitter),completed,numParts,lastPublishedPart,parts(id,title,length,url,deleted,draft,createDate),tags,storyLanguage,copyright"
    json_data  = requests.get(story_info_url, headers={'User-Agent': 'Mozilla/5.0'}).json()
    try:
        if json_data.get('result') == 'ERROR':
            error_message = json_data.get('message', 'Unknown error')
            print(f"Error: {error_message}")
            print(dev_error_msg)
            return
        
        if json_data.get('error_type') :
            error_message = json_data.get('message', 'Unknown error')
            print(f"Error: {error_message}")
            print(dev_error_msg)
            return
        
    
        if json_data.get('result') == 'ERROR':
            error_message = json_data.get('message', 'Unknown error')
            print(f"API Error: {error_message}")
            return
    except Exception as exc:
        print(f"Error retrieving JSON data from the API: {exc}")
        return

    # Extracting useful data from JSON.
    summary, tags, chapters, story_name, author, cover = extract_useful_data(json_data)

    # Saving HTML file.
    html_file_name = f"{story_name}.html"
    html_file_name = html_file_name.replace('/', ' ')
    entry=save_html_file(html_file_name, story_name, author, cover, tags, summary, chapters)
    return entry

    # Converting HTML to EPUB.
    # save_epub_file(html_file_name, story_name, cover)


def get_new_story_urls():
    # new_index_url='https://www.wattpad.com/stories/new/new'
    url = "https://www.wattpad.com/stories/new/new"

    response = requests.get(url,headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'html.parser')

    story_urls = []

    for a in soup.find_all('a', {'class':"title meta on-story-preview"}):
        story_url = a['href']
        if 'story/'in story_url:
            story_urls.append('wattpad.com'+story_url)
        else:
            # story_urls.append('wattpad.com/'+story_url)
            print('not story',story_url)
    print(story_urls)
    return story_urls
    
def rq_wattpad(config=None):
    if  config is None:
        config['save_path']='wattpad_data.jsonl'
    story_urls=get_new_story_urls()
    for urls in story_urls[:100]:
        with open(config['save_path'], "a", encoding="utf-8") as file:
            # for entry in data:
            entry=main(urls)
            json.dump(entry, file, ensure_ascii=False)
            file.write("\n")
            print(entry)


if __name__ == "__main__":
    rq_wattpad()
