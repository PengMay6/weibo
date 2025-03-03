import requests
import csv
import numpy as np
from globalVariable import *


def init(articleCategoryFilePath):
    # 检查文件是否存在，如果存在则清空文件内容
    if os.path.exists(articleCategoryFilePath):
        with open(articleCategoryFilePath, 'w', encoding='utf-8', newline='') as csvFile:
            pass  # 打开文件并关闭，这会清空文件内容
    # 写入标题行
    with open(articleCategoryFilePath, 'a', encoding='utf-8', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow([
            'typeName',  # 文章类别名
            'gid',
            'containerid'
        ])


def writerRow(row, articleCategoryFilePath):
    with open(articleCategoryFilePath, 'a', encoding='utf-8', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)


def get_data(url):
    params = {
        'is_new_segment': 1,
        'fetch_hot': 1
    }
    response = requests.get(url, headers=headers2, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None
def parse_json(response, articleCategoryFilePath):
    navList = np.append(response['groups'][3]['group'], response['groups'][4]['group'])
    for nav in navList:
        navName = nav['title']
        gid = nav['gid']
        containerid = nav['containerid']
        writerRow([
            navName,
            gid,
            containerid
        ], articleCategoryFilePath)
def start(articleCategoryFilePath):
    init(articleCategoryFilePath)
    url = 'https://weibo.com/ajax/feed/allGroups'
    response = get_data(url)
    parse_json(response, articleCategoryFilePath)


if __name__ == '__main__':
    start(r'data\articleCategory.csv')
