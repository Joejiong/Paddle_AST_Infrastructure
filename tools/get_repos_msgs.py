'''
根据repo  获取其对应信息  并写入excel表格
'''

import requests
import json
import datetime
import re
import pandas as pd
from datetime import timedelta
import time
import random
from github import Github
import time
import pandas as pd

#获取某一个repo的信息
def get_msg(repo):
    #repo信息存储
    repo_msg = []
    
    #repo创作者信息list  分为组织和个人
    if repo.organization == None:
        user = repo.owner
        typ = '个人'
    else:
        user = repo.organization
        typ = '企业'
    #repo信息list
    repo_msg = [repo.full_name,repo.owner.login,typ,repo.stargazers_count,repo.forks,repo.size,repo.created_at,repo.description,user.location,user.email,user.blog]    
    
    return repo_msg

# 根据repo列表 生成 对应的repo msg 列表
def get_msgs(repo_list):
    repo_msgs = []
    i = 0
    s = 1
    sleep_count = 0
    while s == 1:
        try:
            if i == len(repo_list):
                break
            else:
                g = Github("a294895db60f2f76737b9dc5625ea459c4da262c")
                repo=g.get_repo(repo_list[i])
                repo_msg = get_msg(repo)
                repo_msgs.append(repo_msg)
                i = i+1
                #记录sleep次数
                sleep_count = 0
                print(i,repo.full_name)
        except:
            time.sleep(5)
            sleep_count = sleep_count + 1
            if sleep_count == 8:
                print('**',repo_list[i])
                i = i + 1
                continue
            else:
                continue
    return repo_msgs


# 根据 repo msg 列表，生成Excel
def create_excel(code,repo_msgs):
    repo_msgs_name = ['项目名称','个人/企业','拥有者','stars','forks','项目大小','创建时间','repo描述','用户位置','用户email','用户博客']
    repo_excel = pd.DataFrame(columns=repo_msgs_name, data=repo_msgs)
    Excel_repo = pd.ExcelWriter('./repo_msgs_' + code + '.xlsx') 
    repo_excel.to_excel(Excel_repo,sheet_name="repo_msgs", index=False)
    Excel_repo.save()





