# -*- encoding: utf-8 -*-
# Author: MingCrash

from Components.Downloader import Downloader
from Tool.Loader import load_module
from Tool.Helper import get_locationtime
from Tool.Helper import cburl2newrq
import logging, json

logger = logging.getLogger('__name__')

#处理器做为一个 （下载+分析） 单位工作
class Processor(object):
    '''处理器做为一个 （下载+分析） 单位工作
       包含：
            下载器-1.从任务池taskPool获取任务
                  2.暂存当前执行任务信息
                  3.执行下载任务
                  4.将请求失败的请求任务put进errorPool,不创建,并在记录到errorPool定性为请求型失败

            分析器-1.接受下载器传来的请求结果
                  2.1分析内容，判断内容是否有效，无效内容从新生成新任务添加retrycounter字段并放到taskPool
                  2.2抽取新连接生成新任务放到taskPool
                  3.1分析内容，判断内容是否有效，持久化保存数据，将任务扔到logPool
    '''

    def __init__(self,fileName='',filePath='',taskqueue=None,errTxtpath=None,logTxtpath=None,
                 cookie='',delay=0,dlt=60,cont=5,usa='',persist=None):
        super(Processor, self).__init__()
        self.parser = load_module(module_name=fileName, module_path=filePath)
        if self.parser is None or persist is None or taskqueue is None or errTxtpath is None or logTxtpath is None:
            logger.warning('处理器初始化失败')
            return
        self.persist = persist
        self.taskqueue = taskqueue
        self.errTxtpath = errTxtpath
        self.errbuff = []
        self.logTxtpath = logTxtpath
        '''关闭处理器的信号'''
        self._quit = False
        '''暂存当前任务'''
        self.curtask = None
        self.downloader = Downloader(cookijar=cookie,delay=delay,dlTimeOut=dlt,conTimeOut=cont,ua=usa)

    def __del__(self):
        if self.errbuff:
            with open(self.errTxtpath, 'a+') as f:
                f.writelines(self.errbuff)
                self.errbuff.clear()

    def quit(self):
        self._quit = True

    def on_task(self,task):
        if task['task_status'] >= 10:
            if len(self.errbuff) <= 10:
                self.errbuff.append(json.dumps(task))
            else:
                self.errbuff.append(json.dumps(task))
                with open(self.errTxtpath, 'a+') as f:
                    f.writelines(self.errbuff)
                    self.errbuff.clear()
            # with open(self.logTxtpath,'a+') as f:
            #     f.write(json.dumps(task)+'\n')
            return False

        task = self.downloader.fetch(task)
        if task['task_status'] == 1:
            self.taskqueue.put(obj=task)    #下载器-4
            return False

        cell = self.parser.Parser_Mainfunction(callbackname=task['task_callback'],url=task['request']['url'],content=task['response']['content'])
        if not len(cell['error']) == 0:
            task['task_status'] = 2
            task['retry'] += 1
            task['task_logs'] += '{time}:[解析阶段报错]{err}\n'.format(time=get_locationtime(),err=cell['error'])
            try:
                del task['response']
            except:
                pass
            self.taskqueue.put(obj=task)
            return False
        else:
            for item in cell['content']:
                self.persist.process_item(item=item)

        '''根据urllinks创建新任务'''
        if not len(cell['urllinks']) == 0:
            for cburl in cell['urllinks']:
                newrq = cburl2newrq(str=cburl,tsName=task['task_Name'],refer=task['request'].setdefault('url',''))
                self.taskqueue.put(newrq)

        return True

    def run_loop(self):
        logger.info('Processor starting....')
        while not self._quit:
            if not self.taskqueue.isempty:
                self.curtask = self.taskqueue.put()
                self.on_task(self.curtask)
            else:
                pass

        logger.info('Processor exiting....')









