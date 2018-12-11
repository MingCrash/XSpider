# -*- encoding: utf-8 -*-
# Author: MingCrash


from Components.Downloader import Downloader

task = {
    'task_tName':'朱志明的测试',
    'task_logs':'',
    'task_status': 0,  # 0-成功 1-请求型失败 2-解析型失败
    'task_callback':'getlink',
    'request':{
        'refer':'',
        # 'url':'https://wenda.autohome.com.cn/home/getindexdata?pageindex=2',
        'url':'https://www.baidu.com/',
        'cookie':'',
        'timeout': 30,
        'post_data_dic':'',     # 添加了这个代表执行POST请求
        'useragent':'',
        'delay':3,
        'header':{
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-CN,zh;q=0.9',
            'Referer':'https://wenda.autohome.com.cn/'
        }
    }
}

oj = Downloader(delay=3)
print(oj.fetch(task_dict=task))


# import requests
#
# print(requests.get(url=task['request']['url'],header=task['request']['header']))
