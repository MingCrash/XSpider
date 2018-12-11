# encoding:utf-8


import requests,logging,time,json,sys,re
from requests.exceptions import ConnectTimeout,ConnectionError,ReadTimeout
from urllib3.exceptions import NewConnectionError,MaxRetryError

logger = logging.getLogger(__name__)

errorCode = ['100000','100001','100002','100004','100005','100301','100700',
             '100701','100702','100703','100704','100705','100706','100707',
             '100802','100803']

filename = 'store.txt'

meetEnd = False

def printdd():
    print(__name__)

def getUrlWithPars(dict):
    str = []
    for i in dict.keys():
        tmp = '{key}={val}'.format(key=i,val=dict[i])
        str.append(tmp)
    return '&'.join(str)

def time_cmp(first_time, second_time):
    if isinstance(first_time,str) :
        if len(first_time) <= 10 : first = time.mktime(time.strptime(first_time,'%Y-%m-%d'))
        if len(first_time) > 10 : first = time.mktime(time.strptime(first_time,'%Y-%m-%d %H:%M:%S'))
    if isinstance(second_time,str) :
        if len(second_time) <= 10 : second = time.mktime(time.strptime(second_time,'%Y-%m-%d'))
        if len(second_time) > 10 : second = time.mktime(time.strptime(second_time,'%Y-%m-%d %H:%M:%S'))

    return int(first)-int(second_time)

def get_locationtime():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

def get_createtime(secs):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(secs)))

def getUrlWithPars(dict):
    str = []
    for i in dict.keys():
        tmp = '{key}={val}'.format(key=i,val=dict[i])
        str.append(tmp)
    return '&'.join(str)

def backupFailRequest(url):
    # with open('bucket.txt','r+') as f:
    #     list = f.readlines()
    #     list.insert(0,url+'\n')
    #     f.seek(0)
    #     f.truncate()
    #     f.writelines(list)
    with open('bucket.txt','a+') as f:
        f.write(url)

def popRequst():
    with open('bucket.txt','r+') as f:
        rq_list=f.readlines()
        if len(rq_list) == 0:
            f.close()
            return None
        url=rq_list.pop(0)
        f.seek(0)
        f.truncate()
        f.writelines(rq_list)
    return url

def sysExit(staus,obj):
    try:
        sys.exit(staus)
    except:
        if obj:obj.close()


class SavePipeline(object):
    buffer_list = None
    filename = None

    def __init__(self):
        self.buffer_list = []

    def close(self):
        if not len(self.buffer_list) == 0:
            with open(filename,'a+',encoding='utf-8') as f:
                f.writelines(self.buffer_list)
                self.buffer_list.clear()

    def process_item(self, item, type):
        str = ''
        if type == 'article':
            str = '《Root》《S0》{s0}《/S0》《S1》{s1}《/S1》《S2》微信《/S2》《S3a》微信文章《/S3a》《S5》{s5}《/S5》《S3b》{s3b}《/S3b》《S9》1《/S9》《S11》{s11}《/S11》《S12》{s12}《/S12》《ID》1《/ID》《S4》{s4}《/S4》《S6》{s6}《/S6》《Q1》{q1}《/Q1》《G1》{g1}《/G1》《/Root》\n'.format(
                s0=item.setdefault('s0',''), s1=item.setdefault('s1',''), s3b=item.setdefault('s3b',''),
                s5=item.setdefault('s5',''), s4=item.setdefault('s4',''), s6=item.setdefault('s6',''),
                s11=item.setdefault('s11',''),s12=item.setdefault('s12',''),q1=item.setdefault('q1',''),
                g1=item.setdefault('g1',''))
        elif type == 'comment':
            str = '《Root》《S0》{s0}《/S0》《ID》{id}《/ID》《S1》{s1}《/S1》《S2》微信《/S2》《S3a》微信文章《/S3a》《S5》{s5}《/S5》《S3b》{s3b}《/S3b》《S6a》{s6a}《/S6a》《S9》2《/S9》《S11》{s11}《/S11》《S12》{s12}《/S12》《S4》{s4}《/S4》《S6》{s6}《/S6》《Q1》{q1}《/Q1》《G1》{g1}《/G1》《/Root》\n'.format(
                s0=item.setdefault('s0', ''), s1=item.setdefault('s1', ''), s3b=item.setdefault('s3b', ''),
                s5=item.setdefault('s5', ''), s4=item.setdefault('s4', ''), s6=item.setdefault('s6', ''),
                s11=item.setdefault('s11', ''), s12=item.setdefault('s12', ''), q1=item.setdefault('q1', ''),
                g1=item.setdefault('g1', ''),id=item.setdefault('id', ''),s6a=item.setdefault('s6a',''))
        elif type == 'reply':
            str = '《Root》《S0》{s0}《/S0》《S2》微信《/S2》《S3a》微信文章《/S3a》《S5》{s5}《/S5》《S4》{s4}《/S4》《S6》{s6}《/S6》《S6a》{s6a}《/S6a》《S9》3《/S9》《S13》{s13}《/S13》《Q1》{q1}《/Q1》《/Root》\n'.format(
                s0=item.setdefault('s0', ''),s5=item.setdefault('s5', ''), s4=item.setdefault('s4', ''), s6=item.setdefault('s6', ''),
                s6a=item.setdefault('s6a', ''),s9=item.setdefault('s9', ''),s13=item.setdefault('s13', ''),q1=item.setdefault('q1', ''))
        else:
            logger.warning('丢掉{t}:{s}'.format(t=type,s=str))
            return

        if len(self.buffer_list) <= 10:
            self.buffer_list.append(str)
        else:
            self.buffer_list.append(str)
            with open(filename,'a+',encoding='utf-8') as f:
                f.writelines(self.buffer_list)
                self.buffer_list.clear()

        return item

class Downloader(object):
    def __init__(self):
        super(Downloader, self).__init__()
        self.headers = {"Accept-Encoding": "gzip","Connection": "close"}

    def download(self,url):
        timeCount = 1
        while timeCount <= 10:
            logger.warning('第{t}次请求:{u}'.format(t=timeCount,u=url))
            try:
                rs = requests.get(url,self.headers)
            except (ReadTimeout, ConnectTimeout) as e:
                logger.warning('请求超时-ReadTimeout or ConnectTimeout: {}'.format(e))
                backupFailRequest(url)
                return None
            except (NewConnectionError, ConnectionError) as e:
                logger.warning('连接失效-NewConnectionError or ConnectionError: {}'.format(e))
                backupFailRequest(url)
                return None
            except MaxRetryError as e:
                logger.warning('多次重试失败-MaxRetryError: {}'.format(e))
                backupFailRequest(url)
                return None

            json_obj = rs.json()
            print(json_obj)
            if json_obj['retcode'] in errorCode or json == None or json == '':
                logger.warning('retcode返回异常参数:{}'.format(json_obj['retcode']))
                time.sleep(2)
                timeCount+=1
                continue
            return json_obj
        logger.warning('重试失败，保存失败连接，退出Sys解析器')
        backupFailRequest(url)
        sys.exit(0)

class Parse(object):
    def __init__(self):
        super(Parse, self).__init__()
        self.pars = {
            'apikey':'Rg44X2fsMoOFneg2QHNMSJIBaT28OXPdYgOmodOqWD2q7dRw2K6WbNsMfSrLWaRM',
            'biz':None}
        self.sp = SavePipeline()

    def createNewLINK(self,json,url):
        if json['hasNext'] == True:
            self.pars['pageToken'] = json['pageToken']
            self.pars['biz'] = re.search('biz=(\S+)==',url).group(1)+'=='
            newurl = 'http://api01.idataapi.cn:8000/post/weixinpro?{}'.format(getUrlWithPars(self.pars))
            logger.info('NewUrl:{}'.format(newurl))
            return newurl
        else:
            logger.warning('hasNext为False,停止爬取！！')
            self.sp.close()
            sys.exit(0)

    def parse(self, json):
        if json == None:
            logger.warning('接受到的JSON无效，退出解析')
            return

        for article in json['data']:
            artdict = {}
            artdict['id'] = 1
            artdict['s0'] = article['id']
            artdict['s1'] = article['url']
            artdict['s3b'] = article['biz']
            artdict['s5'] = get_locationtime()
            artdict['s4'] = article['title']
            artdict['s6'] = article['publishDateStr']
            artdict['s9'] = 1
            artdict['s11'] = article['viewCount']
            artdict['s12'] = article['commentCount']
            artdict['q1'] = article['content']
            artdict['g1'] = article['posterScreenName']
            self.sp.process_item(item=artdict,type='article')
            if article['comments']:
                for comment in article['comments']:
                    comdict = {}
                    comdict['id'] = comment['id']
                    comdict['s0'] = article['id']
                    comdict['s1'] = article['url']
                    comdict['s3b'] = article['biz']
                    comdict['s4'] = article['title']
                    comdict['s5'] = get_locationtime()
                    comdict['s6'] = comment['publishDateStr']
                    comdict['s6a'] = article['publishDateStr']
                    comdict['s9'] = 2
                    comdict['s12'] = comment['commentCount']
                    comdict['s13'] = article['likeCount']
                    comdict['q1'] = comment['content']
                    comdict['g1'] = comment['commenterScreenName']
                    self.sp.process_item(item=comdict,type='comment')
                if comment['replies']:
                    for reply in comment['replies']:
                        repdict = {}
                        repdict['s0'] = article['id']
                        repdict['s4'] = comment['content']
                        repdict['s5'] = get_locationtime()
                        repdict['s6'] = reply['publishDateStr']
                        repdict['s6a'] = comment['publishDateStr']
                        repdict['s9'] = 3
                        repdict['s13'] = article['likeCount']
                        repdict['q1'] = reply['content']
                        self.sp.process_item(item=repdict, type='reply')

            if time_cmp('2017-7-01',int(article['publishDate'])) >= 0:
                logger.warning('到了指定时间 2017-7-01 ，停止执行')
                meetEnd = True
                self.sp.close()
                sys.exit(0)

import requests

# if __name__ == "__main__":
#     ps = Parse()
#     dl = Downloader()
#     url = popRequst()
#     print(url)
#     if not url:
#         logger.warning('任务池已空，退出进程')
#         sys.exit(0)
#
#     meetEnd = False
#     while True:
#         json_obj = dl.download(url)
#         ps.parse(json_obj)
#         url = ps.createNewLINK(json_obj,url)
#         if meetEnd:break



    # timeStruct = time.strptime('2018-7-03 12:30:45','%Y-%m-%d %H:%M:%S')
    # timeStamp = time.mktime(timeStruct)
    # print(timeStruct,timeStamp,int(int(timeStamp)))

    # if time_cmp('2017-07-01', int('1586289954')) >= 0:print('yes')
    # if time_cmp('2017-07-01', int('1330592245')) >= 0:print('no')


