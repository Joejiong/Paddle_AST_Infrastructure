'''
获取nmae,readme,descripton中包含paddle关键字的非paddlepaddle官方repo
'''


import requests
import json
import datetime
import re
import pandas as pd
from datetime import timedelta
import time
import random

#URL  github search API 在nmae,readme,descripton中搜索paddle  去除paddlepaddle官方repo
 URL = "https://api.github.com/search/repositories?q=paddle-org:paddlepaddle+in:readme+in:name+in:descripton+created:"
#头部信息  模拟浏览器浏览
headers = {'User-Agent': 'Mozilla/5.0',
            'Authorization': 'token  0a302610198340313a1b063b2c4b60764d8e237b ',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
            }

#逐页获取repo，并放入列表
def get_other_repo(URL,header):
    response_list = []
    
    w = 1
    while w==1:
        try:
            msg = requests.request("GET", URL, headers=header)
            if msg.content:
                break
        except:
            print("ZZzzzz...")
            time.sleep(5)
            continue
    
    # 获取头信息中的Link内容
    try:
        header_info = msg.headers["Link"]
        # 消除<>和空格
        header_replace = re.sub('<|>| ', '', header_info)
        # 以,和;分割成一个列表
        header_split = re.split(',|;', header_replace)
        # 获取列表中rel="last"的索引
        last_index = header_split.index('rel=\"last\"')
        # 获取last的url链接
        num = header_split[last_index-1]
        # 获取last的url中的页码
        page_num = re.search('page=(\d+)', num)
        # 从1开始循环页码至最后一页
        i = 1
        page = 1
        # 发起对应页码url的请求  # 读取响应信息   # 存储响应信息至列表
        while i == 1:
            try:
                if page == int(page_num.group(1))+1:
                    break
                else:
                    response = requests.request("GET", URL + "&page=" + str(page), headers=header)
                    if response.content:
                        INFO = json.loads(response.text.encode('utf8'))
                        response_list.append(INFO)
                        page = page + 1
            except:
                print("ZZzzzz...")
                time.sleep(5)
                continue
    except:
        response_list.append(msg.json())
    return response_list


#将repo list里的repo名写入文件
def parse_repo(LIST, yesterday):
    for INFO in LIST:
        for repo_name in INFO['items']:
            f = open(repo_path, 'a', encoding='utf-8')
            f.write(repo_name['full_name'] + '\n')
    f.close()
    return True


#由于 github search API 每次最多能搜索到1000个repo，故分日期进行爬取，分日期存储到对应的txt文件里
def get_repos(dates):
    repos = []
    for date in dates:
        #print(date)
        path = './repos/repo_list_' + date + '.txt'
        repos_file = open(path)
        repos = repos + repos_file.read().splitlines()
    print(len(repos))
    return repos

#dates   2009至 2020
dates = ['2009-01-01..2010-01-01','2010-01-01..2011-01-01','2011-01-01..2012-01-01',
         '2012-01-01..2013-01-01','2013-01-01..2014-01-01','2014-01-01..2015-01-01',
         '2015-01-01..2016-01-01','2016-01-01..2016-07-01','2016-07-01..2017-01-01',
         '2017-01-01..2017-07-01','2017-07-01..2018-01-01', '2018-01-01..2018-07-01',
         '2018-07-01..2019-01-01','2019-01-01..2019-05-01','2019-05-01..2019-09-01',
        '2019-09-01..2020-01-01','2020-01-01..2020-05-01','2020-05-01..2020-08-05']

# 调用get_repos
repos = get_repos(dates)
