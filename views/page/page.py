from flask import session, render_template, redirect, Blueprint, request, jsonify, url_for
from utils.base_page import *
from utils.getEchartsData import *
from spiders.main import main as startSpider, main_2
from utils.topicAnalysis import *
from utils.topicAnalysis2 import getWeiAI

page_app = Blueprint('page', __name__, url_prefix='/page', template_folder='templates')


@page_app.route('/yuqingChar')
def yuqingChar():
    username = session.get('username')
    negative_articleList = getAllNegativeArticle()
    neutral_articleList = getAllNeutralArticle()
    positive_articleList = getAllPositiveArticle()
    return render_template('yuqingChar.html',
                           username=username,
                           negative_articleList=negative_articleList,
                           neutral_articleList=neutral_articleList,
                           positive_articleList=positive_articleList
                           )


@page_app.route('/delete_all_articles', methods=['POST'])
def delete_all_articles_route():
    try:
        if delete_all_articles():
            return jsonify({'status': 'success', 'message': '所有文章成功删除'})
        else:
            return jsonify({'status': 'failure', 'message': '删除失败'}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@page_app.route('/delete_articles', methods=['POST'])
def delete_articles_route():
    try:
        data = request.get_json()
        article_ids = data.get('articleIds', [])
        if delete_articles(article_ids):
            return jsonify({'status': 'success', 'message': '文章成功删除'})
        else:
            return jsonify({'status': 'failure', 'message': '文章删除失败'}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@page_app.route('/deleteData')
def deleteData():
    username = session.get('username')
    articeList = getAllArticleData()
    return render_template('deleteData.html',
                           username=username,
                           articeList=articeList
                           )


@page_app.route('/commentsData')
def commentsData():
    username = session.get('username')
    top_comments_list = get_top_100_comments()
    # print(top_comments_list[0])
    return render_template('commentsData.html',
                           username=username,
                           top_comments_list=top_comments_list
                           )


# 爬取指定文章
@page_app.route('/spiderArticle', methods=['GET'])
def spiderArticle():
    message = ''
    username = session.get('username')
    url = request.args.get('url')
    type_str = request.args.get('type')
    print(url)
    print(type_str)
    try:
        if url:
            if not url.startswith('https://weibo.com/'):
                message = '地址错误'
                return render_template('spiderData.html',
                                       username=username,
                                       message=message
                                       )
            articleId = main_2(url, type_str)
            # message = '成功爬取单个文章数据'
            return redirect(url_for('page.articleChar', articleId=articleId))
    except Exception as e:
        print(e)
        error_message = str(e)
        print(f"An unexpecccccccted error occurred: {error_message}")
        if error_message == 'You should supply an encoding or a list of encodings to this method that includes input_ids, but you provided []':
            return render_template('spiderData.html',
                                   username=username,
                                   message='地址错误'
                                   )
        return render_template('spiderData.html',
                               username=username,
                               message=error_message
                               )

    return render_template('spiderData.html',
                           username=username,
                           message=message
                           )


# 爬取多个文章
@page_app.route('/spiderArticles', methods=['GET'])
def spiderArticles():
    # 获取当前视图文件所在的文件夹路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 获取项目的根目录（假设根目录为 weibo）
    project_root = os.path.dirname(os.path.dirname(current_dir))  # 获取 'weibo' 目录
    # 拼接路径到 'spiders/data' 文件夹
    spider_data_dir = os.path.join(project_root, 'spiders', 'data')
    # 拼接出 CSV 文件路径
    csv_path = os.path.join(spider_data_dir, 'articleCategory.csv')
    # 打印出路径，确保路径正确
    # print(f"CSV file path: {csv_path}")
    # spiderArticleCategory.start(csv_path)
    # 读取 CSV 文件
    articleCategory = pd.read_csv(csv_path)
    # 获取 'typeName' 列的数据
    type_name_data = articleCategory['typeName']
    # 如果需要以列表形式返回数据
    type_name_list = type_name_data.tolist()

    print(type_name_list)  # 打印出来查看是否读取成功

    message = ''
    username = session.get('username')
    try:
        types = request.args.get('types')
        page = request.args.get('page')
        print("Selected types: {}, Selected page: {}".format(types, page))
        if page is not None:
            page = int(page)
        else:
            # 提供默认值或者进行错误处理
            page = 1  # 或者其他默认值
        if types is not None:
            startSpider(types, page)
            message = '爬取成功'
            return redirect(url_for('page.articleData_temp'))
    except Exception as e:
        error_message = str(e)
        print(f"An unexpected error occurred: {error_message}")
        if error_message == 'You should supply an encoding or a list of encodings to this method that includes input_ids, but you provided []':
            return render_template('spiderData.html',
                                   username=username,
                                   message='文章类型太少或页数太少',
                                   type_name_list=type_name_list
                                   )
        elif error_message.find('Expecting value: line') == 0:
            return render_template('spiderData.html',
                                   username=username,
                                   message='Cookie失效',
                                   type_name_list=type_name_list
                                   )
        return render_template('spiderData.html',
                               username=username,
                               message=error_message,
                               type_name_list=type_name_list
                               )


@page_app.route('/articleData_temp', methods=['GET'])
def articleData_temp():
    username = session.get('username')
    articeList = getAllArticleData()
    print(123)
    return render_template('articleData_temp.html',
                           username=username,
                           articeList=articeList
                           )


from spiders import spiderArticleCategory
import pandas as pd


@page_app.route('/spiderData', methods=['GET'])
def spiderData():
    username = session.get('username')
    # 获取当前视图文件所在的文件夹路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 获取项目的根目录（假设根目录为 weibo）
    project_root = os.path.dirname(os.path.dirname(current_dir))  # 获取 'weibo' 目录
    # 拼接路径到 'spiders/data' 文件夹
    spider_data_dir = os.path.join(project_root, 'spiders', 'data')
    # 拼接出 CSV 文件路径
    csv_path = os.path.join(spider_data_dir, 'articleCategory.csv')
    # 打印出路径，确保路径正确
    # print(f"CSV file path: {csv_path}")
    # spiderArticleCategory.start(csv_path)
    # 读取 CSV 文件
    articleCategory = pd.read_csv(csv_path)
    # 获取 'typeName' 列的数据
    type_name_data = articleCategory['typeName']
    # 如果需要以列表形式返回数据
    type_name_list = type_name_data.tolist()

    print(type_name_list)  # 打印出来查看是否读取成功
    return render_template('spiderData.html',
                           username=username,
                           type_name_list=type_name_list
                           )


@page_app.route('/topic')
def topic():
    username = session.get('username')
    try:
        ciTiaoList = getCiTiaoList()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return render_template('topic.html',
                           username=username,
                           ciTiaoList1=ciTiaoList[:10],
                           ciTiaoList2=ciTiaoList[10:]
                           )


@page_app.route('/analysisTopic')
def analysisTopic():
    username = session.get('username')
    try:
        ciTiao = request.args.get('ciTiao')
        description_list, emotion, word_cloud, typical_viewpoint_list = getWeiboAI(ciTiao)
        generate_wordcloud(word_cloud, ciTiao)
        names, nums = getCharData(emotion)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        message = "暂无分析结果，请重新选择话题"
        ciTiaoList = getCiTiaoList()
        return render_template('topic.html',
                               username=username,
                               message=message,
                               ciTiaoList1=ciTiaoList[:10],
                               ciTiaoList2=ciTiaoList[10:]
                               )
    return render_template('analysisTopic.html',
                           username=username,
                           description_list=description_list[:5],
                           emotion=json.dumps(emotion),
                           names=names,
                           nums=nums,
                           ciTiao=ciTiao,
                           typical_viewpoint_list=typical_viewpoint_list[:10]
                           )


@page_app.route('/updateData')
def updateData():
    username = session.get('username')
    articeList = getAllArticleData()
    return render_template('updateData.html',
                           username=username,
                           articeList=articeList
                           )


@page_app.route('/home')
def home():
    username = session.get('username')
    articleLenMax, likeCountMaxAuthorName, cityMax, articleList = getHomeTagsData()
    commentsLikeCountTopFore = getHomeCommentsLikeCountTopFore()
    xData, yData = getHomeArticleCreatedAtChart(articleList)
    typeChart = getHomeTypeChart(articleList)
    emotionData = getEmotion()
    return render_template('index.html',
                           username=username,
                           articleLenMax=articleLenMax,
                           likeCountMaxAuthorName=likeCountMaxAuthorName,
                           cityMax=cityMax,
                           commentsLikeCountTopFore=commentsLikeCountTopFore,
                           xData=xData,
                           yData=yData,
                           typeChart=typeChart,
                           emotionData=emotionData
                           )


@page_app.route('/articleData')
def tableData():
    username = session.get('username')
    articeList = getAllArticleData()
    return render_template('articleData.html',
                           username=username,
                           articeList=articeList
                           )


# 分析
@page_app.route('/articleChar', methods=['GET'])
def articleChar():
    username = session.get('username')
    articleIDList = getArticleID()
    # 检查文章ID列表是否为空
    if not articleIDList:
        # 可以记录日志，或者设置一个错误消息
        errorMsg = "暂无文章数据，请稍后再试。"
        return render_template('error.html', username=username, errorMsg=errorMsg)
    typeList = getTypeList()
    defaultArticleID = articleIDList[0]
    if request.args.get('articleId'): defaultArticleID = request.args.get('articleId')
    commentsList = getCommentsData(str(defaultArticleID))
    article = getArticleData(str(defaultArticleID))
    commentRegionData = getIPCharByCommentsRegion(commentsList)
    sentimentData = getCommentSentimentData(commentsList)
    time_dates, time_counts = getTimeData(commentsList)
    return render_template('articleChar.html',
                           username=username,
                           articleIDList=articleIDList,
                           typeList=typeList,
                           defaultArticleID=defaultArticleID,
                           likeNum=article[0][1],
                           commentsLen=article[0][2],
                           reposts_count=article[0][3],
                           region=article[0][4],
                           content=article[0][5],
                           created_at=article[0][6],
                           type=article[0][7],
                           detailUrl=article[0][8],
                           authorName=article[0][9],
                           authorDetail=article[0][10],
                           commentsList=commentsList,
                           sentimentData=sentimentData,
                           commentRegionData=commentRegionData,
                           time_dates=time_dates,
                           time_counts=time_counts
                           )
