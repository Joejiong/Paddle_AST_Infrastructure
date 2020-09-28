'''
根据get_paddle_repos.py里获取的repo，提取出代码里包含import paddle的repo
'''

import requests
import json
import datetime
import re
import pandas as pd
from datetime import timedelta
import time
import random

headers = {'User-Agent': 'Mozilla/5.0',
            'Authorization': 'token a5f3b77bf6c6664c6b3d7048281ea8424128c6f7',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
            }
#dates 与get_paddle_repos.py里 的 dates对应
dates = ['2009-01-01..2010-01-01','2010-01-01..2011-01-01','2011-01-01..2012-01-01',
         '2012-01-01..2013-01-01','2013-01-01..2014-01-01','2014-01-01..2015-01-01',
         '2015-01-01..2016-01-01','2016-01-01..2016-07-01','2016-07-01..2017-01-01',
         '2017-01-01..2017-07-01','2017-07-01..2018-01-01', '2018-01-01..2018-07-01',
         '2018-07-01..2019-01-01','2019-01-01..2019-05-01','2019-05-01..2019-09-01',
        '2019-09-01..2020-01-01','2020-01-01..2020-05-01','2020-05-01..2020-08-05']
#判断某个repo 里 是否存在code里包含import paddle 的Python文件
URL = "https://api.github.com/search/code?q=\"import paddle\"+in:file+language:python+repo:"

#判断 import paddle 的次数 0 or 其他
def get_import_paddle_count(repo,URL,header):
    url = URL + repo
    i = 1
    while i == 1:
        try:
            count = None
            msg = requests.request("GET", url, headers=header)
            if msg.headers['status'] == '422 Unprocessable Entity':
                count = 0
            else:
                count = msg.json()['total_count']
            if count != None:
                print(repo)
                break
        except:
            print('zzzzz...')
            time.sleep(5)
            continue
    print(count)
    return count

#按照dates  将 repo集成到repos里
def get_repos(dates):
    repos = []
    for date in dates:
        #print(date)
        path = './repos_tf/repo_list_' + date + '.txt'
        repos_file = open(path)
        repos = repos + repos_file.read().splitlines()
    print(len(repos))
    return repos
'''
输出三个文件
repos_import paddle_list.txt ————  import paddle 的repo列表
repos_import paddle_dic  ———— import paddle的repo列表及其对应的import次数
repos_import paddle_0.txt  ———— 没有import paddle 的列表
'''
def get_import_paddle(repos,URL,header):
    repo_dic = {}
    repos_0 = []
    i = 0
    for repo in repos:
        path_list = "./repos_import paddle/repos_import paddle_list.txt"
        path_dic = "./repos_import paddle/repos_import paddle_dic.txt"
        path_0 = "./repos_import paddle/repos_import paddle_0.txt"
        count = get_import_paddle_count(repo,URL,header)
        print(i)
        i = i+1
        if count != 0:
            repo_dic[repo] = count
            f = open(path_list, 'a', encoding='utf-8')
            f.write(repo + '\n')
            ff = open(path_dic, 'a', encoding='utf-8')
            ff.write(repo + ' ' + str(count) + '\n')
        else:
            repos_0.append(repo)
            f_0 =open(path_0, 'a', encoding='utf-8')
            f_0.write(repo + '\n')
    f.close()
    ff.close()
    f_0.close()
    print(len(repo_dic),len(repos_0))
    return repo_dic,repos_0



repos = get_repos(dates)
repo_dic,repos_0 = get_import_paddle(repos,URL,headers)
