import requests
from bs4 import BeautifulSoup
import csv

import pdb
import re



def process(text):
    '''
    \n\n\n\n          Challenges\n        \n\n\nIn the News 2024\n\n\n2024 US Election Challenge\n\n\n\n\n\n          Tags\n        \n\n\nLeader Entry/Exit\n\xa0\n  \nUS Politics\n\xa0\n  \nElections and Referenda\n\xa0\n\n        \n\n\n\n\nAs of the end of January 2024, Nikki Haley was the last major challenger to Donald Trump for the GOP presidential nomination (Politico, Newsweek). The Michigan Republican primary is scheduled for 27 February 2024 (270 to Win).Confused? Check our\xa0FAQ\xa0or\xa0ask us for help. To learn more about Good Judgment and Superforecasting,\xa0click here.To learn more about how you can become a Superforecaster, see here.\xa0For other posts from our Insights blog, click here.The question closed "At least 20.0%, but less than 30.0%" with a closing date of 27 February 2024.See our FAQ to learn about\xa0how we resolve questions\xa0and\xa0how scores are calculated.\n
    '''
    try:
        challenges_pattern = r'Challenges\s*(.*?)\s*Tags'
        tags_pattern = r'Tags\s*(.*?)\s*Confused'
        # 提取 Challenges 列表
        challenges_list=[]
        challenges_match = re.search(challenges_pattern, text, re.DOTALL)
        if challenges_match:
            challenges_list = challenges_match.group(1).strip().split('\n')
            challenges_list = [item.strip() for item in challenges_list if len(item.strip()) > 0]


        # 提取 Tags 列表
        tags_list=[]
        description=''
        tags_match = re.search(tags_pattern, text, re.DOTALL)
        if tags_match:
            tags_list = tags_match.group(1).strip().split('\n')
            tags_list = [item.strip() for item in tags_list if len(item.strip()) > 0]
            description=tags_list[-1]
            tags_list = tags_list[:-1]# more check

        return challenges_list,tags_list,description
    except:
        print('error')
        with open ('error.txt','a',encoding='utf-8') as f:
            f.write(f'process have error in {text}')
            import traceback
            f.write(traceback.format_exc())

        return [],[],''
    


def craw_gjopen(url= "https://www.gjopen.com/questions/3247-what-percentage-of-the-vote-will-nikki-haley-receive-in-the-2024-michigan-republican-presidential-primary"):

    # 发送HTTP请求获取网页内容
    headers = { 'User-Agent': 'Mozilla/5.0' , 'Accept': 'text/html', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate', 'DNT': '1',
                'Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1', 'Cache-Control': 'max-age=0' }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    # pdb.set_trace()
    # 找到问题描述和答案
    # 提取题目
    question_heading = soup.find('h3', id='question-name-header').text.strip()

    # 提取开始时间和关闭时间
    '''<span class="info-heading">
    Started
    </span>
    <span>
    <small><span data-localizable-timestamp="2024-02-02T18:00:00Z">Feb 02, 2024 06:00PM UTC</span></small>
    </span>
    <br/>
    <span class="info-heading">
    Closed
    </span>
    <span>
    <small><span data-include-distance-of-time-in-words="true" data-localizable-timestamp="2024-02-27T08:01:00Z">Feb 27, 2024 08:01AM UTC</span></small>      
    </span>
    这里不能提取到，重写这块'''

    #  here next_simbling is the next tag, next_sibling is the next tag's next tag, but it is small not span?
    #  answer:
    # start_time = soup.find('span', text='\n  Started\n').next_sibling.next_sibling.text.strip() # 这里不能提取到，重写这块, do not use text to find the tag, use the class to find the tag
    started_time = soup.find('span', class_='info-heading',text='\n  Started\n').next_sibling.next_sibling.text.strip()

    closed_time = soup.find('span', class_='info-heading',text='\n  Closed\n').next_sibling.next_sibling.text.strip()



    # 提取相关信息
    info_div = soup.find('div', class_='smb').text
    # pdb.set_trace() 
    challenges_list,tags_list,description=process(info_div)

    # TODO 
    # additional_info = info_div.find_all('p')



    table_body = soup.find('tbody')

    # 初始化一个字典用于存储问题选项、正确答案和预测分数
    question_data = {}

    # 找到每一行数据并提取信息
    rows = table_body.find_all('tr')
    for row in rows:
        # TODO
        # pdb.set_trace()
        cells = row.find_all('td')
        if len(cells) == 3:
            # pdb.set_trace()
            possible_answer = cells[0].text.strip()
            '''
            <td>At least 20.0%, but less than 30.0%</td>
            <td class="text-center"><i class="fa fa-check-circle"></i></td>
            <td class="text-right">62%</td>
            '''
            # correct  check if have a <i>
                    # <td class="text-center"><i class="fa fa-check-circle"></i></td>
            correct = cells[1].find('i')
            # correct = cells[1].text.strip()
            forecast = cells[2].text.strip()

            # 将正确答案的标志设置为 True
            if correct:
                correct = True
            else:
                correct = False
            # 存储数据到字典中
            question_data[possible_answer] = {'Correct?': correct, 'Final Crowd Forecast': forecast}
    return {'Question': question_heading, 'Started_time': started_time, 'Closed_time': closed_time,
                      'Challenges_list': challenges_list, 'Tags_list': tags_list, 'Description': description,
                        'Possible_Answers_dict': question_data}



if __name__ == '__main__':
    rtns=craw_gjopen('https://www.gjopen.com/questions/3247-what-percentage-of-the-vote-will-nikki-haley-receive-in-the-2024-michigan-republican-presidential-primary')
    # pdb.set_trace()
    with open('test.csv', 'a', newline='',encoding='utf-8') as csvfile:

        fieldnames = ['Question', 'Started_time', 'Closed_time', 'Challenges_list', 'Tags_list', 'Description', 'Possible_Answers_dict']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # if header is not exist, write header

        writer.writerow(rtns)
        #started_time,closed_time,challenges_list,tags_list,description,question_data

        # 写入数据
        # for possible_answer, data in question_data.items():
        #     writer.writerow({'Question': question_heading, 'Started': started_time, 'Closed': closed_time, 'Challenges': challenges_list, 'Tags': tags_list, 'Description': description, 'Possible Answer': possible_answer, 'Correct?': data['Correct?'], 'Final Crowd Forecast': data['Final Crowd Forecast']})

    print("CSV文件已生成")
