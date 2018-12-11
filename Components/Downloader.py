# -*- encoding: utf-8 -*-
# Author: MingCrash

import logging
import pycurl
import certifi
import time
from Tool.Helper import get_locationtime, conv2list
from urllib.parse import urlencode
from io import BytesIO

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
        req = task_dict['request']

        if 'delay' in req.keys():
            if not req['delay'] == 0:
                time.sleep(req['delay'])
        else:
            time.sleep(self._delay)

        if 'header' in req.keys():
            headers = req['header']
            if isinstance(headers, dict):
                headers = conv2list(headers)
            self.curlDownloader.setopt(pycurl.HTTPHEADER, headers)  # 列表格式['accept:XXXX']

        if 'cookie' in req.keys():
            self.curlDownloader.setopt(pycurl.COOKIEJAR, req['cookie'])

        if 'useragent' in req.keys():
            self.curlDownloader.setopt(pycurl.USERAGENT, req['useragent'])

        if 'post_data_dic' in req.keys():
            self.curlDownloader.setopt(pycurl.POSTFIELDS, urlencode(req['post_data_dic']))
            # 如果设置了这个参数，那么就是post请求。如果没有，那么就是get请求。

        self.curlDownloader.setopt(pycurl.URL, req['url'])

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

        task_dict['response'] = {}  # 添加response
        task_dict['response']['status_code'] = self.curlDownloader.getinfo(pycurl.RESPONSE_CODE)
        task_dict['response']['htmsize'] = self.curlDownloader.getinfo(pycurl.SIZE_DOWNLOAD)
        task_dict['response']['url'] = self.curlDownloader.getinfo(pycurl.EFFECTIVE_URL)
        task_dict['response']['content'] = self.bio.getvalue().decode(req.setdefault('encoding', 'utf-8'))
        return task_dict

    def fetch(self,task_dict):
        return self.byCurl(task_dict)










