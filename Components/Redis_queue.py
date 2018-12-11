#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<roy@binux.me>
#         http://binux.me
# Created on 2015-04-27 22:48:04

import time
import redis
import umsgpack
from six.moves import queue as BaseQueue

# 表级别的操作
class RedisQueue(object):
    """
    A Queue like message built over redis
    """

    def __init__(self, name, host='localhost', port=6379, db=0,maxsize=10,
                 maxtimeout=0.3, lazy_limit=True, password=None, cluster_nodes=None):
        """
        Constructor for RedisQueue

        maxsize:    an integer that sets the upperbound limit on the number of
                    items that can be placed in the queue.
        lazy_limit: redis queue is shared via instance, a lazy size limit is used
                    for better performance.
        """
        self.name = name
        # if(cluster_nodes is not None):
        #     from rediscluster import StrictRedisCluster
        #     self.redis = StrictRedisCluster(startup_nodes=cluster_nodes)
        # else:
        self.Empty = BaseQueue.Empty
        self.Full = BaseQueue.Full
        self.max_timeout = maxtimeout
        self.redis = redis.StrictRedis(host=host, port=port, db=db, password=password)
        self.maxsize = maxsize
        self.lazy_limit = lazy_limit
        self.last_qsize = 0

    '''获取列表长度'''
    def qsize(self):
        self.last_qsize = self.redis.llen(self.name)
        return self.last_qsize

    '''判断列表长度是否为空'''
    def isempty(self):
        if self.qsize() == 0:
            return True
        else:
            return False

    '''判断列表是否到达最长大小'''
    def isfull(self):
        if self.maxsize and self.qsize() >= self.maxsize:
            return True
        else:
            return False

    '''不会等待队列有空闲位置再放入数据，如果数据放入不成功就直接崩溃'''
    def put_nowait(self, obj):
        if self.lazy_limit and self.last_qsize < self.maxsize:
            pass
        elif self.isfull():
            raise self.Full
        self.last_qsize = self.redis.lpush(self.name, umsgpack.packb(obj))
        return True

    def put(self, obj, block=True, timeout=None):
        if not block:
            return self.put_nowait(obj)

        start_time = time.time()
        while True:
            try:
                return self.put_nowait(obj)
            except self.Full:
                if timeout:
                    lasted = time.time() - start_time
                    if timeout > lasted:
                        time.sleep(min(self.max_timeout, timeout - lasted))
                    else:
                        raise
                else:
                    time.sleep(self.max_timeout)

    '''队列为空，取值的时候不等待，但是取不到值那么直接崩溃了'''
    def get_nowait(self):
        ret = self.redis.rpop(self.name)
        if ret is None:
            raise self.Empty
        return umsgpack.unpackb(ret)

    '''队列为空，使用get会等待，直到队列有数据以后再取值'''
    def get(self, block=True, timeout=None):
        if not block:
            return self.get_nowait()

        start_time = time.time()
        while True:
            try:
                return self.get_nowait()
            except self.Empty:
                if timeout:
                    lasted = time.time() - start_time
                    if timeout > lasted:
                        time.sleep(min(self.max_timeout, timeout - lasted))
                    else:
                        raise
                else:
                    time.sleep(self.max_timeout)

# Queue = RedisQueue
