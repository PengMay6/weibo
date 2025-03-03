import os
from datetime import datetime

from fake_useragent import UserAgent

# 生成一个模拟随机浏览器的User-Agent
UserAgents = UserAgent().random
# 定义请求头
headers = {
    "User-Agent": f"{UserAgents}",
    "Cookie": "SINAGLOBAL=3693746055516.003.1682675638184; SCF=AsLPXsxAikxVY8TFoR58dtKO7IppYqsssLDGDdBCA6y2szMvicwSQ-hNjENALvFOYo48mTG1LxCG9HNXSe5CSQY.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFCxqlq7eTeps_AxHK5CQDH5JpX5KMhUgL.FoMXeozRShnN1K-2dJLoI7yB9g4rKg84Sntt; ALF=1742553192; SUB=_2A25KscM4DeRhGeFK6VAZ9CbLwjmIHXVpz1rwrDV8PUJbkNANLXaskW1NQ5RWgHYpNPkL-MiTZ8sNhbNa4QeI4CnI; XSRF-TOKEN=a4cBiYmSckBenM4FbRazAOQC; _s_tentry=weibo.com; Apache=4367559675339.8184.1739968180718; ULV=1739968180760:6:4:2:4367559675339.8184.1739968180718:1739962882717; WBPSESS=Ll5Bou_DsD4z-e3djBkGsil7cjuwv15ND3pc3BKJBrYDyV_n0RrsN6IoFvpa9Uvsuqq-TVE1mhDnFCJq0ozdoVhgFd7bX1GEQegrbMyKxY8DMlD00Z1nefJrJxjk-RTgzDBrIe0QPfm76_s3EhxJFA=="
}

headers2 = {
    "Cookie": "SINAGLOBAL=3693746055516.003.1682675638184; SCF=AsLPXsxAikxVY8TFoR58dtKO7IppYqsssLDGDdBCA6y2szMvicwSQ-hNjENALvFOYo48mTG1LxCG9HNXSe5CSQY.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFCxqlq7eTeps_AxHK5CQDH5JpX5KMhUgL.FoMXeozRShnN1K-2dJLoI7yB9g4rKg84Sntt; ULV=1740045809522:8:6:4:5706921203295.154.1740045809501:1740032669769; XSRF-TOKEN=syzRFXrQV_3HG4C45qzb_gaL; ALF=1743158223; SUB=_2A25Kup6fDeRhGeFK6VAZ9CbLwjmIHXVpuZ5XrDV8PUJbkNAYLVLjkW1NQ5RWgF4updfBUmSUNBqNY8y3MryPT8Cw; WBPSESS=Ll5Bou_DsD4z-e3djBkGsil7cjuwv15ND3pc3BKJBrYDyV_n0RrsN6IoFvpa9Uvsuqq-TVE1mhDnFCJq0ozdobDyG_-mejSXr0XB8JV4rM_ERO_DyN27cpuGBYyXl2jLkAl7PWZ1ktomO4bzY4DPSA==" ,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
}

headers3 = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
}


def initGlobalVariable():
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
    articleDataFilePath = r'spiders\data\articleContent_' + formatted_time + '.csv'
    articleCommentsFilePath = r'spiders\data\articleComments_' + formatted_time + '.csv'
    articleCategoryFilePath = r'spiders\data\articleCategory.csv'
    return articleCategoryFilePath, articleDataFilePath, articleCommentsFilePath


if __name__ == '__main__':
    print(initGlobalVariable())
