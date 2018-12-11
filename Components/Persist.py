# -*- encoding: utf-8 -*-
# Author: MingCrash

class Persist(object):
    buffer_list = None
    filename = None

    def __init__(self,path=''):
        if path == '':return
        self.path = path
        self.buffer_list = []

    def __del__(self):
        if not len(self.buffer_list) == 0:
            with open(self.path,'a+',encoding='utf-8') as f:
                f.writelines(self.buffer_list)
                self.buffer_list.clear()

    def process_item(self, item=None):
        if item is None: return False
        if len(self.buffer_list) <= 10:
            self.buffer_list.append(item)
        else:
            self.buffer_list.append(item)
            with open(self.path,'a+',encoding='utf-8') as f:
                f.writelines(self.buffer_list)
                self.buffer_list.clear()

        return True
