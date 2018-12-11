# -*- coding: utf-8 -*-

task = {
    'task_Name':'朱志明的测试',
    'task_logs':'',
    'task_status': 0,  # 0-成功 1-请求型失败 2-解析型失败
    'task_callback':'',
    'retry':0,
    'request':{
        'dff':'syss',
        'refer':'',
        'url':'http://item.yhd.com/squ/comment/getCommentDetail.do?productId=1067048&callback=commentDetailCallback',
        'cookie':'UM_distinctid=16421691bb86d6-0ef98de69e9c7-17376952-fa000-16421691bb918d; __gads=ID=7e3d0032b8c16b5c:T=1529568894:S=ALNI_MYFyZoi9SD0kiv7EKLvEtI2Fe_PJg; vjuids=74f9ab854.16421692230.0.90d2390b8f698; _ntes_nnid=29806cb61d8ee65e5a2193432811945a,1529568895552; _ntes_nuid=29806cb61d8ee65e5a2193432811945a; __oc_uuid=1c79a150-8347-11e8-8d09-535c19dd5410; usertrack=ezq0pFtDCmhJ6byqD+YSAg==; __utmz=187553192.1533621655.3.3.utmcsr=open.163.com|utmccn=(referral)|utmcmd=referral|utmcct=/; vjlast=1529568896.1537494865.11; vinfo_n_f_l_n3=c3cbb21decd5900b.1.10.1529568895581.1537498846952.1537501846350; _iuqxldmzr_=32; WM_TID=hiwjPgLrMMlFEBUBQBc9eF6Bde3zZ8WX; WM_NI=iq4ObYzB%2BhdKTGic56V%2F%2BlODXzxtADg4VeIdpqkYpIJIz0Y7MSkKYlzaHaBt9t%2BDbFADsledRuu1BJqnWEgfAQjOv%2BtUVES1ZzQv4YevNTl9WgDeYSTqfS%2FYnTMSiv7oM1Y%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeabcb668e9b9c98c87dadef8bb6d54e968e9bafb86e81b78ab8ee6b8193b6d8b42af0fea7c3b92aabaffcb0e153ba9ee589e7419899a784b83e96f1e58dce509ca6b895c450a5ec9a86cc70b4afa5baf3438a97b6d1dc3d8f8da5acdc68babf8882c180fbace5a5e14e839cbd8de87092abbbd2c142b3b299a6e66e838fa6b0f521b88b9aa6d23b9aa69f97b753a7aa82b5ef3395b98c86dc5998afaab4ae53ae8c83b4ec7ef5b183d2dc37e2a3; hb_MA-BFF5-63705950A31C_source=www.baidu.com; __f_=1541043637502; hb_MA-BFF5-63705950A31C_u=%7B%22utm_source%22%3A%20%22baidu%22%2C%22utm_medium%22%3A%20%22cpc%22%2C%22utm_campaign%22%3A%20%22affiliate%22%2C%22utm_content%22%3A%20%22SEM%22%2C%22utm_term%22%3A%20%2211tiyanke%22%2C%22promotional_id%22%3A%20%22%22%7D; __utma=187553192.157808804.1531120208.1542077188.1542166033.6; JSESSIONID-WYYY=nHlMs7duF%2F3%2FQzQ0qrNZqUQz%5CoSyPbahIz0rp%2BK%2BCcq66ZH7ayvzY%2Bt8T3wrI85GqQ8WCugufscWY5lRJZmwSvAl0%2BXgFEm%2Fj9nwkYk%2F2K%5Cd4vSQG4EYgjRVpkSSteEybmH9gT8dopagpbhI7AyJ9vHaPbnoaStZgzo%5CBdN3FX%5CxUuxD%3A1543204642465; __utma=94650624.1037246517.1538542982.1539346896.1543202843.4; __utmc=94650624; __utmz=94650624.1543202843.4.4.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmb=94650624.2.10.1543202843',
        'timeout': 30,
        'post_data_dic':'',
        'useragent':'',
        'delay':'',
        'header':'',
    },
    'response':{
        'status_code':200,
        'htmsize':10439594,
        'effective_url':'',
        'content':''
    }
}

# import Helper
#
# print(Helper.saveFormat('zhuzhiming',"<haha>"))

import traceback
#
print('########################################################')
print("1/0 Exception Info")
print('---------------------------------------------------------')
try:
    int('a')
except Exception as e:
    print('str(Exception):\t', str(Exception))
    print('str(e):\t\t', str(e))
    print('repr(e):\t', repr(e))
    print('e.message:\t', e)
    print('traceback.print_exc():', traceback.print_exc(e))
    print('traceback.format_exc():\n%s' % traceback.format_exc(e))
print('########################################################')
# print("i = int('a') Exception Info")
# import json, umsgpack
#
# print(type(json.dumps(task)),json.dumps(task))
# print(type(umsgpack.dumps(task)))

# def rr(ss=''):
#     print(ss)
#
# rr(ss=task['request'].setdefault('dff',''))