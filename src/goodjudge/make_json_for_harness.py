import pandas as pd
import json
import os
import datetime
import pdb


data=pd.read_csv('gjo.csv')
'''
Question,Started_time,Closed_time,Challenges_list,Tags_list,Description,Possible_Answers_dict
Will Representative Dean Phillips cease to be a candidate for the 2024 Democratic nomination for US president before 9 June 2024?,"Feb 09, 2024 06:00PM UTC","Mar 06, 2024 07:30PM UTC","['In the News 2024', '2024 US Election Challenge']","['Leader Entry/Exit', 'US Politics', 'Elections and Referenda']",Minnesota Representative Dean Phillips has continued his challenge to President Biden's quest for the 2024 Democratic nomination despite overwhelming odds (USA Today). Examples of what will count for resolution of this question include an official announcement that Phillips no longer seeks the Democratic Party nomination for president or that he is fully suspending his campaign.,"{'Yes': {'Correct?': True, 'Final Crowd Forecast': '86%'}, 'No': {'Correct?': False, 'Final Crowd Forecast': '14%'}}"
'''
parse_time=lambda x:datetime.datetime.strptime(x, "%b %d, %Y %I:%M%p UTC")
data['Started_time']=data['Started_time'].apply(parse_time).dt.strftime('%Y-%m-%d')
data['Closed_time']=data['Closed_time'].apply(parse_time).dt.strftime('%Y-%m-%d')
# replace eval with ast.literal_
import ast
data['Possible_Answers_dict']=data['Possible_Answers_dict'].apply(ast.literal_eval)
data['Challenges_list']=data['Challenges_list'].apply(ast.literal_eval)
data['Tags_list']=data['Tags_list'].apply(ast.literal_eval)
# import a
data['choices']=data['Possible_Answers_dict'].apply(lambda x: list(x.keys()))
# data['Possible_Answers_dict'].apply(lambda x: list(eval(x).keys()))
def get_target(x):
    # x=eval(x)
    for k,v in x.items():
        if v['Correct?']:
            return k
# pdb.set_trace()

data['target']=data['Possible_Answers_dict'].apply(get_target)
# to json
data.to_json('gjo.json',orient='records',lines=True)