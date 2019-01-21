# -*- encoding: utf-8 -*-
# Author: MingCrash

import logging
import pycurl
import certifi
import time
from Tool.Helper import get_locationtime, conv2list
from urllib.parse import urlencode
from io import BytesIO

# 任务结构参考
'''
task = {
    'task_tName':'朱志明的测试',
    'task_logs':'',
    'task_status': 0,  # 0-成功 1-请求型失败 2-解析型失败
    'task_callback':'getlink',
    'rq':'curl',
    'refer':'',
    'url':'https://www.baidu.com/',
    'cookie':'',
    'timeout': 30,
    'post_data_dic':'',     # 添加了这个代表执行POST请求
    'useragent':'',
    'delay':3,
    'encoding':'',  #需要指定的时候才添加此字段
    'header':{
        'Accept':'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Referer':'https://wenda.autohome.com.cn/'
    }
}

'''

logger = logging.getLogger('Downloader')

headers = {
    'Accept':'*/*',
    'Accept-Encoding':'gzip,deflate',
    'Accept-Language':'zh-CN,zh;q=0.8,en-us;q=0.6,en;q=0.5;q=0.4',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.691.400 QQBrowser/9.0.2524.400'
}

class Downloader(object):

    component_name = 'Downloader'

    def __init__(self,cookijar='',delay=0,dlTimeOut=60,conTimeOut=10,
                 ua='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'):
        super(Downloader, self).__init__()
        self.bio = BytesIO()
        self.curlDownloader = pycurl.Curl()
        self.curlDownloader.setopt(pycurl.VERBOSE, True)
        self.curlDownloader.setopt(pycurl.ENCODING, 'gzip, deflate')
        self.curlDownloader.setopt(pycurl.WRITEFUNCTION, self.bio.write)
        self.curlDownloader.setopt(pycurl.CAINFO, certifi.where())
        self.curlDownloader.setopt(pycurl.FOLLOWLOCATION, True)

        # Note: must be a string, not a file object.
        # self.curlDownloader.setopt(pycurl.COOKIEFILE, config['cookfilpath'])
        # Note: must be a string, not a file object.
        if not cookijar == '':self.curlDownloader.setopt(pycurl.COOKIEJAR, cookijar)
        self.curlDownloader.setopt(pycurl.TIMEOUT, dlTimeOut)
        self.curlDownloader.setopt(pycurl.CONNECTTIMEOUT, conTimeOut)
        self.curlDownloader.setopt(pycurl.USERAGENT, ua)
        self._delay = delay

    def __del__(self):
        self.curlDownloader.close()
        self.bio.close()

    def byCurl(self,task_dict):
        self.bio.truncate(0)  # 从0位置开始删除后面的字段

        if 'delay' in task_dict.keys():
            if not task_dict['delay'] == 0:
                time.sleep(task_dict['delay'])
        else:
            time.sleep(self._delay)

        if 'header' in task_dict.keys():
            headers = task_dict['header']
            if isinstance(headers, dict):
                headers = conv2list(headers)
            self.curlDownloader.setopt(pycurl.HTTPHEADER, headers)  # 列表格式['accept:XXXX']

        if 'cookie' in task_dict.keys():
            self.curlDownloader.setopt(pycurl.COOKIEJAR, task_dict['cookie'])

        if 'useragent' in task_dict.keys():
            self.curlDownloader.setopt(pycurl.USERAGENT, task_dict['useragent'])

        if 'post_data_dic' in task_dict.keys():
            self.curlDownloader.setopt(pycurl.POSTFIELDS, urlencode(task_dict['post_data_dic']))
            # 如果设置了这个参数，那么就是post请求。如果没有，那么就是get请求。

        self.curlDownloader.setopt(pycurl.URL, task_dict['url'])

        '''每个任务请求可重复3遍，提高成功率'''
        try:
            timeCount = 1
            while timeCount <= 3:
                self.curlDownloader.perform()
                if len(self.bio.getvalue()) == 0:
                    continue
                else:
                    break
        except Exception as e:
            task_dict['task_logs']+= '{time}:[请求阶段报错]{err}\n'.format(time=get_locationtime(),err=str(e))
            task_dict['task_status'] = 1
            task_dict['retry'] += 1
            return task_dict

        task_dict['status_code'] = self.curlDownloader.getinfo(pycurl.RESPONSE_CODE)
        task_dict['htmsize'] = self.curlDownloader.getinfo(pycurl.SIZE_DOWNLOAD)
        task_dict['effective_url'] = self.curlDownloader.getinfo(pycurl.EFFECTIVE_URL)
        task_dict['content'] = self.bio.getvalue().decode(task_dict.setdefault('encoding', 'utf-8'))

        return task_dict

    def byRequests(self,task_dict):
        return

    def fetch(self,task_dict):
        if task_dict['rq'] == 'curl':
            return self.byCurl(task_dict)
        elif task_dict['rq'] == 'rqs':
            return  self.byRequests(task_dict)
        return None











