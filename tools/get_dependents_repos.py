'''
爬取某一个repo 的dependents repo列表

'''

import requests
from bs4 import BeautifulSoup

#获取 repos
def get_dependent_repos(url):
    print("GET " + url)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    
    repos = [
        "{}/{}".format(
            t.find('a', {"data-repository-hovercards-enabled":""}).text,
            t.find('a', {"data-hovercard-type":"repository"}).text
        )
        for t in soup.findAll("div", {"class": "Box-row"})
    ]
    paginationContainer = soup.find("div", {"class":"paginate-container"}).find('a')
    return repos,paginationContainer


# 写repos
def write_repos(repos):
    path = "./dependents_paddlepaddle-gpu.txt"
    for repo in repos:
        f = open(path, 'a', encoding='utf-8')
        f.write(repo + '\n')

#repo数
repo = "PaddlePaddle/Paddle"
#页数  你想爬取的repo的页数
page_num = 1300
#dependents 第一页的链接
url = 'https://github.com/{}/network/dependents?package_id=UGFja2FnZS01MjQwNzkyMA%3D%3D'.format(repo)
i = 0
repos_sum = []

#爬取  并实时写入
for i in range(page_num):
    i = i + 1
    repos,paginationContainer = get_dependent_repos(url)
    write_repos(repos)
    print(i,len(repos))
    if i > 1 :
        paginationContainer = paginationContainer.next_sibling
    print(paginationContainer.text)
    if paginationContainer:
        url = paginationContainer["href"]
    else:
        break
