# -*- encoding: utf-8 -*-
# Author: MingCrash

from Components.Processor import Processor
from Components.Persist import Persist
from Components.Redis_queue import RedisQueue
import os

task = {
    'task_Name':'朱志明的测试',
    'task_logs':'',
    'task_status': 0,  # 0-成功 1-请求型失败 2-解析型失败
    'task_callback':'getlink1',
    'request':{
        # 'refer':'',
        'url':'https://wenda.autohome.com.cn/home/getindexdata?pageindex=2',
        # 'url':'https://www.baidu.com/',
        'cookie':'',
        'timeout': 30,
        # 'encoding':'',
        # 'post_data_dic':'',
        'useragent':'',
        'delay':3,
        'header':{
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-CN,zh;q=0.9',
        }
    }

    # },
    # 'response':{
    #     'status_code':200,
    #     'htmsize':10439594,
    #     'effective_url':'',
    #     'content':''
    # }
}

# os.system('nohup redis-server {} &'.format('/Users/Ming/PycharmProjects/公司的代码库/Car/XSpider/redis_6379.conf'))   #nohup不挂断 &后台运行 一般一起用
os.system('redis-server {}'.format('/Users/Ming/PycharmProjects/公司的代码库/Car/XSpider/redis_6379.conf'))
# rds = RedisQueue(name='test',maxsize=10)
# ps = Persist(path='/Users/Ming/PycharmProjects/公司的代码库/Car/XSpider/sto.txt')
# pp = Processor(
#     fileName='pycurlGetandPost.py',
#     filePath='/Users/Ming/Desktop/pycurlGetandPost.py',
#     errTxtpath='/Users/Ming/PycharmProjects/公司的代码库/Car/XSpider/err.txt',
#     logTxtpath='/Users/Ming/PycharmProjects/公司的代码库/Car/XSpider/log.txt',
#     taskqueue=rds,
#     persist=ps,
#     )
#
# pp.on_task(task)

