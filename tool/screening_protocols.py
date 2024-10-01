import re
import linecache
import os
log = u"D:/Users/User/PycharmProjects/Configuration_table_check/tool/协议.log"
content1 = linecache.getlines(log)
report = 0
filepath = 'D:/Users/User/PycharmProjects/Configuration_table_check/tool/report0.log'
for i in range(500):
    while os.path.exists(filepath):
        report += 1
        filepath = 'D:/Users/User/PycharmProjects/Configuration_table_check/tool/report' + str(report) + '.log'

need_write = []
for content in content1:
    if "发送协议" in content:
        protpcpl = content.split("===>", 1)[1]
        need_write.append(protpcpl)
with open(filepath, 'w', encoding='utf-8') as f:
    for j in need_write:
        f.write(j)



