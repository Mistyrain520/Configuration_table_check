# -*- coding: utf-8 -*-
# 请先自行安装模块
from xmindparser import xmind_to_dict
import os
xmind_forder = u'D:/doc/11测试文档/用例'


# FutureWarning: The behavior of this method will change in future versions.
# Use specific 'len(elem)' or 'elem is not None' test instead.
def find_key(file_lokking, check_dict, key):
    for k in check_dict:
        if isinstance(check_dict[k], dict):
            # 过滤一下图片等其他类型
            if isinstance(check_dict[k]['title'], str):
                if key in check_dict[k]['title']:
                    print(check_dict[k]['title'],file_lokking)
            find_key(file_lokking,check_dict[k],key)
        if isinstance(check_dict[k], list):
            for value in check_dict[k]:
                if isinstance(value, dict):
                    if isinstance(value['title'], str):
                        if key in value['title']:
                            print(value['title'], file_lokking)
                    find_key(file_lokking, value, key)
file_list=[]
for root, dirs, files in os.walk(xmind_forder, topdown=True):
    for file_name in files:
        if os.path.splitext(file_name)[1] == '.xmind':
            file_list.append(os.path.join(root, file_name))
for xmind_file in file_list:
    out_list = xmind_to_dict(xmind_file)
    for content in out_list:
        find_key(xmind_file,content, '体力')#改这里关键词，查找关键词所在用例

