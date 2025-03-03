import os
import pymysql
import pandas as pd
from dbutils.pooled_db import PooledDB

# 创建数据库连接池
pool = PooledDB(
    creator=pymysql,  # 使用 pymysql
    host='localhost',
    user='root',
    password='123456',
    database='weibo_data',
    port=3306,
    maxconnections=5,
)


# 使用 query 方法
# def query(sql, params, query_type='no_select'):
#     # print(params,123)
#     # print(len(params))
#     try:
#         # 从连接池中获取连接
#         conn = pool.connection()
#         with conn.cursor() as cursor:
#             # 如果是批量插入，使用 executemany()
#             if isinstance(params, list) and len(params) > 0:
#                 cursor.executemany(sql, params)
#             else:
#                 # 如果只有一条数据，则将其封装为一个列表再执行
#                 cursor.execute(sql, params)  # 单条执行
#
#             # 如果是查询（SELECT），获取数据
#             if query_type != 'no_select':
#                 data_list = cursor.fetchall()
#                 return data_list
#             else:
#                 # 提交事务以确保更改被保存
#                 conn.commit()
#                 return '数据库语句执行成功!'
#     except pymysql.err.InterfaceError:
#         print("数据库连接已断开，尝试重新连接...")
#         return query(sql, params, query_type)  # 递归调用以重新尝试
#     except pymysql.MySQLError as e:
#         print(f"数据库错误: {e}")
#         conn.rollback()  # 发生数据库错误时回滚事务
#     except Exception as e:
#         print(f"其他错误: {e}")
#         conn.rollback()  # 发生其他错误时回滚事务
#     finally:
#         conn.close()  # 确保连接被关闭

def query(sql, params, query_type='no_select'):
    try:
        # 从连接池中获取连接
        conn = pool.connection()
        with conn.cursor() as cursor:
            # 确保单条数据参数是元组
            if not isinstance(params, (list, tuple)):
                params = (params,)

            # 如果是批量插入，使用 executemany()
            if isinstance(params, list) and len(params) > 0 and isinstance(params[0], (list, tuple)):
                cursor.executemany(sql, params)
            else:
                # 如果只有一条数据，则将其封装为一个列表再执行
                cursor.execute(sql, params)  # 单条执行

            # 如果是查询（SELECT），获取数据
            if query_type != 'no_select':
                data_list = cursor.fetchall()
                return data_list
            else:
                # 提交事务以确保更改被保存
                conn.commit()
                return '数据库语句执行成功!'
    except pymysql.err.InterfaceError:
        print("数据库连接已断开，尝试重新连接...")
        return query(sql, params, query_type)  # 递归调用以重新尝试
    except pymysql.MySQLError as e:
        print(f"数据库错误: {e}")
        conn.rollback()  # 发生数据库错误时回滚事务
    except Exception as e:
        print(f"其他错误: {e}")
        conn.rollback()  # 发生其他错误时回滚事务
    finally:
        if 'conn' in locals() and conn:
            conn.close()  # 确保连接被关闭

def query2(sql, params, query_type='no_select'):
    # print(params,123)
    # print(len(params))
    try:
        # 从连接池中获取连接
        conn = pool.connection()
        with conn.cursor() as cursor:
            # 如果是批量插入，使用 executemany()
            if isinstance(params, list):
                cursor.executemany(sql, params)
            else:
                # 如果只有一条数据，则将其封装为一个列表再执行
                cursor.execute(sql, params)  # 单条执行

            # 如果是查询（SELECT），获取数据
            if query_type != 'no_select':
                data_list = cursor.fetchall()
                return data_list
            else:
                # 提交事务以确保更改被保存
                conn.commit()
                return '数据库语句执行成功!'
    except pymysql.err.InterfaceError:
        print("数据库连接已断开，尝试重新连接...")
        return query(sql, params, query_type)  # 递归调用以重新尝试
    except pymysql.MySQLError as e:
        print(f"数据库错误: {e}")
        conn.rollback()  # 发生数据库错误时回滚事务
    except Exception as e:
        print(f"其他错误: {e}")
        conn.rollback()  # 发生其他错误时回滚事务
    finally:
        conn.close()  # 确保连接被关闭



def check_connection():
    try:
        # 从连接池中获取连接
        conn = pool.connection()
        conn.ping(reconnect=True)  # 检查连接是否可用
        conn.close()  # 关闭连接
    except pymysql.MySQLError as e:
        print(f"数据库连接失败: {e}")
        raise


def delete_articles(article_ids):
    try:
        if isinstance(article_ids, int):
            article_ids = [article_ids]  # 将整数转换为列表
        sql_query = "DELETE FROM article WHERE id IN (%s)" % ','.join(['%s'] * len(article_ids))
        query(sql_query, article_ids)

        sql_query = "DELETE FROM comments WHERE articleId IN (%s)" % ','.join(['%s'] * len(article_ids))
        query(sql_query, article_ids)

        return True
    except Exception as e:
        print(f"Error deleting articles: {e}")
        return False


def delete_all_articles():
    try:
        query("DELETE FROM article", [])
        query("DELETE FROM comments", [])
        return True
    except Exception as e:
        print(f"Error deleting all articles: {e}")
        return False


def getAllArticleData():
    # check_connection()
    try:
        sql = "SELECT * FROM article"
        articleList = query(sql, [], 'select')
        return articleList
    except pymysql.MySQLError as e:
        print(f"数据库错误: {e}")
        return []
    except Exception as e:
        print(f"其他错误: {e}")
        return []


def getAllArticleData_temp():
    # check_connection()
    try:
        sql = "SELECT * FROM article_temp"
        articleList = query(sql, [], 'select')
        return articleList
    except pymysql.MySQLError as e:
        print(f"数据库错误: {e}")
        return []
    except Exception as e:
        print(f"其他错误: {e}")
        return []


def get_top_100_comments():
    # check_connection()
    try:
        # 查询 likes_counts 排名前 100 的评论
        sql = """
            SELECT DISTINCT * FROM comments
            ORDER BY likes_counts DESC
            LIMIT 100
        """
        top_comments = query(sql, [], 'select')

        # 将结果转换为列表
        top_comments_list = [list(comment) for comment in top_comments]

        return top_comments_list
    except Exception as e:
        print(f"发生错误: {e}")
        return []


def getAllNegativeArticle():
    # check_connection()
    try:
        sql = "SELECT * FROM article ORDER BY negative_ratio DESC LIMIT 10"
        articleList = query(sql, [], 'select')
        return articleList
    except pymysql.MySQLError as e:
        print(f"数据库错误: {e}")
        return []
    except Exception as e:
        print(f"其他错误: {e}")
        return []


def getAllNeutralArticle():
    # check_connection()
    try:
        sql = "SELECT * FROM article ORDER BY neutral_ratio DESC LIMIT 10"
        articleList = query(sql, [], 'select')
        return articleList
    except pymysql.MySQLError as e:
        print(f"数据库错误: {e}")
        return []
    except Exception as e:
        print(f"其他错误: {e}")
        return []


def getAllPositiveArticle():
    # check_connection()
    try:
        sql = "SELECT * FROM article ORDER BY positive_ratio DESC LIMIT 10"
        articleList = query(sql, [], 'select')
        return articleList
    except pymysql.MySQLError as e:
        print(f"数据库错误: {e}")
        return []
    except Exception as e:
        print(f"其他错误: {e}")
        return []


def getAllCommentsData():
    commentsList = query('select * from comments', [], 'select')
    return commentsList


def save_to_sql(articleDataFilePath, articleCommentsFilePath):
    try:
        # 读取新的 CSV 数据
        articlePd = pd.read_csv(articleDataFilePath)
        commentPd = pd.read_csv(articleCommentsFilePath)

        # 批量插入文章数据
        articles_data = [tuple(row) for row in articlePd.values]
        article_sql = """
            INSERT INTO article (id,likeNum,commentsLen,reposts_count,region,content,created_at,type,detailUrl,authorName,authorDetail,
            negative_ratio,neutral_ratio,positive_ratio,emotion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        query(article_sql, articles_data)

        # 批量插入评论数据
        comments_data = [tuple(row) for row in commentPd.values]
        comment_sql = """
            INSERT INTO comments (articleId,created_at,likes_counts,region,content,authorName,authorGender,authorAddress,sentiment)
            VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s)
        """
        query(comment_sql, comments_data)

    except Exception as e:
        print(f"发生错误: {e}")


def save_to_sql_temp(articleDataFilePath, articleCommentsFilePath):
    try:
        query("DELETE FROM article_temp", [])
        query("DELETE FROM comments_temp", [])
    except Exception as e:
        print(f"Error deleting all articles: {e}")
        return False

    try:
        # 读取新的 CSV 数据
        articlePd = pd.read_csv(articleDataFilePath)
        commentPd = pd.read_csv(articleCommentsFilePath)

        # 批量插入文章数据
        articles_data = [tuple(row) for row in articlePd.values]
        article_sql = """
            INSERT INTO article_temp (id,likeNum,commentsLen,reposts_count,region,content,created_at,type,detailUrl,authorName,authorDetail,
            negative_ratio,neutral_ratio,positive_ratio,emotion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        query(article_sql, articles_data)

        # 批量插入评论数据
        comments_data = [tuple(row) for row in commentPd.values]
        comment_sql = """
            INSERT INTO comments_temp (articleId,created_at,likes_counts,region,content,authorName,authorGender,authorAddress,sentiment)
            VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s)
        """
        query(comment_sql, comments_data)

    except Exception as e:
        print(f"发生错误: {e}")


# def save_to_article(articleDataFilePath, articleCommentsFilePath, articleId):
#     delete_articles(articleId)
#
#     try:
#         # 读取新的 CSV 数据
#         articlePd = pd.read_csv(articleDataFilePath)
#         commentPd = pd.read_csv(articleCommentsFilePath)
#
#         # 批量插入文章数据
#         articles_data = [tuple(row) for row in articlePd.values]
#         article_sql = """
#             INSERT INTO article (id,likeNum,commentsLen,reposts_count,region,content,created_at,type,detailUrl,authorName,authorDetail,
#             negative_ratio,neutral_ratio,positive_ratio,emotion)
#             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#         """
#         query(article_sql, articles_data)
#
#         # 批量插入评论数据
#         comments_data = [tuple(row) for row in commentPd.values]
#         comment_sql = """
#             INSERT INTO comments (articleId,created_at,likes_counts,region,content,authorName,authorGender,authorAddress,sentiment)
#             VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s)
#         """
#         query(comment_sql, comments_data)
#
#     except Exception as e:
#         print(f"发生错误: {e}")
import pandas as pd
import math

def save_to_article(articleDataFilePath, articleCommentsFilePath, articleId):
    delete_articles(articleId)

    try:
        # 读取新的 CSV 数据
        articlePd = pd.read_csv(articleDataFilePath)
        commentPd = pd.read_csv(articleCommentsFilePath)

        # 检查文章数据是否存在 nan 值
        print("文章数据是否存在 nan 值:")
        print(articlePd.isna().any())

        # 检查评论数据是否存在 nan 值
        print("评论数据是否存在 nan 值:")
        print(commentPd.isna().any())

        # 处理文章数据中的 nan 值和缺失的 type 字段
        def handle_nan(data):
            for i in range(len(data)):
                for j in range(len(data[i])):
                    if isinstance(data[i][j], float) and math.isnan(data[i][j]):
                        data[i][j] = None  # 或者替换为 0
                    if j == articlePd.columns.get_loc('type') and pd.isna(data[i][j]):
                        data[i][j] = "无"
            return data

        # 批量插入文章数据
        articles_data = [list(row) for row in articlePd.values]
        articles_data = handle_nan(articles_data)
        articles_data = [tuple(row) for row in articles_data]
        article_sql = """
            INSERT INTO article (id,likeNum,commentsLen,reposts_count,region,content,created_at,type,detailUrl,authorName,authorDetail,
            negative_ratio,neutral_ratio,positive_ratio,emotion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        query(article_sql, articles_data)

        # 批量插入评论数据
        comments_data = [list(row) for row in commentPd.values]
        comments_data = handle_nan(comments_data)
        comments_data = [tuple(row) for row in comments_data]
        comment_sql = """
            INSERT INTO comments (articleId,created_at,likes_counts,region,content,authorName,authorGender,authorAddress,sentiment)
            VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s)
        """
        query(comment_sql, comments_data)

    except Exception as e:
        print(f"发生错误: {e}")

def getArticleData(id):
    return query('select * from article where id=%s', [id], 'select')


def getCommentsData(id):
    if id is not None:
        # 使用DISTINCT关键字来选择不重复的评论
        commentsList = query('SELECT DISTINCT * FROM comments WHERE articleId=%s', [id], 'select')
        commentsList = list(commentsList)
        # 根据需要的字段对评论进行排序
        commentsList.sort(key=lambda x: x[2], reverse=True)
        return commentsList
    return []


def getAllCommentsData():
    allCommentList = query('select * from comments', [], 'select')
    return allCommentList
