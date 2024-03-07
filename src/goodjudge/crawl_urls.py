
from request_one_question import craw_gjopen
import json
import time
import pdb
import csv
import tqdm


urls=[]
with open ('gjo_no_dup.jsonl','r',encoding='utf-8') as f:
    lines=f.readlines()
    for line in lines:
        if 'http' in line:
            # print(line)
            urls.append(line.strip().replace('"',''))

    
print(len(urls),len(set(urls)),urls[0])
# pdb.set_trace()



with open('gjo.csv', 'a', newline='',encoding='utf-8') as csvfile:
    fieldnames = ['Question', 'Started_time', 'Closed_time', 'Challenges_list', 'Tags_list', 'Description', 'Possible_Answers_dict']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for url in tqdm.tqdm(urls[1838:]):# 1826 done 
        url=url.strip()
        rtns=craw_gjopen(url)
        writer.writerow(rtns)
        # time.sleep(0.5)

    


#        return {'Question': question_heading, 'Started_time': started_time, 'Closed_time': closed_time,
#                       'Challenges_list': challenges_list, 'Tags_list': tags_list, 'Description': description,
#                         'Possible_Answers_dict': question_data}



# if __name__ == '__main__':
#     rtns=craw_gjopen('https://www.gjopen.com/questions/3247-what-percentage-of-the-vote-will-nikki-haley-receive-in-the-2024-michigan-republican-presidential-primary')
#     # pdb.set_trace()
#     with open('test.csv', 'a', newline='',encoding='utf-8') as csvfile:

#         fieldnames = ['Question', 'Started_time', 'Closed_time', 'Challenges_list', 'Tags_list', 'Description', 'Possible_Answers_dict']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()

#         # if header is not exist, write header

#         writer.writerow(rtns)