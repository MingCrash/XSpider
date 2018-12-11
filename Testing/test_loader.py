# -*- encoding: utf-8 -*-
# Author: MingCrash

from Tool.Loader import load_module


mo = load_module(module_path='/Users/Ming/Desktop/pycurlGetandPost.py',module_name='pycurlGetandPost')
print(mo.Parser_Mainfunction())
print(dir(mo))