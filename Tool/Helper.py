# -*- encoding: utf-8 -*-
# Author: MingCrash

import time

def get_locationtime():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

def get_createtime(secs):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(secs)))

def printformat(str1,str2):
    str1 = str(str1)
    str2 = str(str2)
    return str2+' '+str1+' '+str2

def getUrlWithPars(dict):
    str = []
    for i in dict.keys():
        tmp = '{key}={val}'.format(key=i,val=dict[i])
        str.append(tmp)
    return '&'.join(str)

# def time_cmp(first_time, second_time):
#     if isinstance(first_time,str) :
#         if len(first_time) <= 10 : first = time.mktime(time.strptime(first_time,'%Y-%m-%d'))
#         if len(first_time) > 10 : first = time.mktime(time.strptime(first_time,'%Y-%m-%d %H:%M:%S'))
#     if isinstance(second_time,str) :
#         if len(second_time) <= 10 : second = time.mktime(time.strptime(second_time,'%Y-%m-%d'))
#         if len(second_time) > 10 : second = time.mktime(time.strptime(second_time,'%Y-%m-%d %H:%M:%S'))
#
#     return int(first)-int(second_time)

def cburl2newrq(str='',tsName='',refer=''):
    if str=='':return None
    tmp = str.split(":")
    if not len(tmp) == 2:return None
    return {'task_Name':tsName,
            'task_logs':'',
            'task_status': 0,  # 0-成功 1-请求型失败 2-解析型失败
            'task_callback':tmp[0],
            'retry':0,
            'request':{
                'refer':refer,
                'url':tmp[1]
            }}

def conv2list(dict):
    tmp = []
    for key in dict.keys():
        str = '{k}:{v}'.format(k=key,v=dict[key])
        tmp.append(str)
    return tmp
