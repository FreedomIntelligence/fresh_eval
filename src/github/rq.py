import requests
import json
from datetime import datetime, timedelta

def get_hottest_repositories_in_last_week():
    # Calculate the date 7 days ago
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    # GitHub API URL for searching repositories
    api_url = 'https://api.github.com/search/repositories'
    
    # Parameters for the API request
    params = {
        'q': f'created:>{seven_days_ago}',
        'sort': 'stars',
        'order': 'desc',
    }
    
    headers = {
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # Send the HTTP GET request to the GitHub API
    response = requests.get(api_url, params=params, headers=headers)
    urls=[]
    if response.status_code == 200:
        data = response.json()
        for item in data['items'][:40]:  # Print the top 3 repositories
            print(f"Name: {item['name']}")
            print(f"Description: {item['description']}")
            print(f"Language: {item['language']}")
            print(f"Watchers Count: {item['watchers_count']}")
            print(f"HTML URL: {item['html_url']}")
            print("\n")
            urls.append(item['html_url'])
        return urls
    else:
        print(f"Failed to fetch data from GitHub API. Status code: {response.status_code}")
        return None

# if __name__ == "__main__":
#     get_hottest_repositories_in_last_week()


import requests

def get_github_repository_code(repo_url,config):
    # Extract the repository owner and name from the URL
    parts = repo_url.split('/')
    owner = parts[-2]
    repo_name = parts[-1]

    # GitHub API URL for fetching the repository content
    api_url = f'https://api.github.com/repos/{owner}/{repo_name}/contents'


    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            content=''
            readme_content=None
            for item in data:
                if item['name'].lower() == 'readme.md':
                    readme_url = item['download_url']
                    readme_response = requests.get(readme_url)
                    if readme_response.status_code == 200:
                        readme_content = readme_response.text
                        # You can save the README content to a file or process it as needed
                        
                        print('README.md content has been found.')
                    else:
                        print('Failed to fetch README content.')
                # Skip .pyc files and other non-Python files
                elif not item['name'].lower().endswith('.pyc') and item['type'] == 'file':  
                    item_url = item['download_url']
                    item_response = requests.get(item_url)
                    if item_response.status_code == 200:

                        item_content = item_response.text
                        if len(item_content)>5000:
                            print(f'item_content too long skip:{item["name"]}')
                            continue
                        print(f'item_content added:{item["name"]}')
                        content+=item_content+'\n\n\n'
                        if len(content)>10000:
                            print(f'total_content >4000:{len(content)}')
                            break
            with open(config['save_path'], 'a', encoding='utf-8') as file:
                if not readme_content is None:
                    content=readme_content+content
                entry = {"date": datetime.now().strftime("%Y-%m-%d-%H-%M"), "error": False, "url": repo_url,'text_blocks':content}
                # readme_file.write(entry)
                print(content[:20])
                json.dump(entry, file, ensure_ascii=False)
                file.write("\n")
                
                    # break
    except Exception as e:
        print(f"An error occurred: {e}")




def rq_github(config=None):
    if config is None:
        config={'save_path':'./github_data.json'}
    # repo_url = input("请输入GitHub仓库地址（如 https://github.com/用户名/仓库名）：")
    urls=get_hottest_repositories_in_last_week()
    if urls is None:
        logging.error('get_hottest_repositories_in_last_week failed')
        print('get_hottest_repositories_in_laast_week failed')
        exit()
    # repo_url='https://github.com/matt8707/ha-fusion'
    print(len(urls),'########################')
        
    for repo_url in urls:
        print(f'processing {repo_url}')
        get_github_repository_code(repo_url,config=config)
        


if __name__ == "__main__":

    rq_github()
