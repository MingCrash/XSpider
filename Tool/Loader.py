# -*- encoding: utf-8 -*-
# Author: MingCrash

import importlib.util,logging
logger = logging.getLogger('Loader.load_module')

def load_module(module_name='',module_path='',mainfunc='Parser_Mainfunction'):
    module_spec = importlib.util.spec_from_file_location(name=module_name,location=module_path)
    if module_spec is None:
        logger.warning("Module :{} not found".format(module_name))
        return None
    try:
        # ['__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__']
        module = importlib.util.module_from_spec(module_spec)
        # ['BytesIO', 'PySpider', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'pycurl']
        module_spec.loader.exec_module(module)
    except:
        logger.warning(logger.name,'解析文件加载失败')
        return None
    if mainfunc not in dir(module):
        logger.warning(logger.name,'解析文件中找不到 %s 启动函数'% mainfunc)
        return None

    return module






