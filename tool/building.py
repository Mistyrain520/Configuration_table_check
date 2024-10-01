import config
import xlrd
import re
import math
import table_operation
from collections import Counter

def list_only(list):
    b = dict(Counter(list))
    no_only = [key for key, value in b.items() if value > 1]
    if no_only:
        return no_only
    else:
        return
# 1是音乐2是文娱3是景点4是影视5是商业
tb = table_operation.Table()
sys_industrial_building_level = "/C产业园建筑等级表.xls"
sys_industrial_building = "/C产业园建筑表.xls"
sys_industrial_building_quality = "/C产业园建筑品质表.xls"
sys_industrial_building_affect = "/C产业园建筑BUFF表.xls"
sys_industrial_building_star = "/C产业园建筑星级表.xls"
building_id = 3221
building_star = 1
project_buff = 0.05 + 0.1 + 0.05 + 0.15 + 0.05 + 0.1 + 0.2 + 0.1+0.3+0.15+0.15+0.4+0.4
buff =0.03 + project_buff
# 建筑升级消耗=基础消耗/100 （1+消耗加成）
all_level = tb.get_content_by_col_name(config.DOC_DIR, sys_industrial_building_level, "Sheet1", "id")
# jichu_xiaohao = tb.get_cell_value(config.DOC_DIR, sys_industrial_building, "Sheet1", "id", building_id, "base_level_cost")
# print("你所查询的建筑", building_id)
# for level in all_level:
#     xiaohao_jiacheng = tb.get_cell_value(config.DOC_DIR, sys_industrial_building_level, "Sheet1", "id", level, "cost")
#     result = (jichu_xiaohao/100) * (1 + xiaohao_jiacheng/10000)
#     print("等级", level)
#     print("升级消耗", result, math.ceil(result))

# 客户端收益计算
chushi_shouru = tb.get_cell_value(config.DOC_DIR, sys_industrial_building, "Sheet1", "id", building_id, "base_product")
# 客户端基础收益(建筑详情客户端显示)
# all_star = [1,2,3,4,5]
# pingzhi = tb.get_cell_value(config.DOC_DIR, sys_industrial_building, "Sheet1", "id", building_id, "quality")
# pingzhi_jiacheng = tb.get_cell_value(config.DOC_DIR, sys_industrial_building_quality, "Sheet1", "id", pingzhi, "product_add")
# for star in all_star:
#     xingji_jiacheng = tb.get_cell_value2(config.DOC_DIR, sys_industrial_building_star, "Sheet1", "building_id", building_id,
#                                          "star", star, "product_add")
#     print("星级",star)
#     result = []
#     for level in all_level:
#         level_jiacheng = tb.get_cell_value(config.DOC_DIR, sys_industrial_building_level, "Sheet1", "id", level,
#                                            "product_add")
#         jichu_shouru = chushi_shouru / 100 * (1 + xingji_jiacheng/10000 + level_jiacheng/10000 + pingzhi_jiacheng/10000)
#         print("等级",level,"客户端基础收益(建筑详情客户端显示)",jichu_shouru)
#         result.append(math.ceil(jichu_shouru))
#     if list_only(result):
#         print(list_only(result),"@@@@@@@@@@@@")

# 服务端计算总收入
for building_level in range(1, 1001):
    xingji_jiacheng = tb.get_cell_value2(config.DOC_DIR, sys_industrial_building_star, "Sheet1", "building_id", building_id,"star", building_star, "product_add")
    level_jiacheng = tb.get_cell_value(config.DOC_DIR, sys_industrial_building_level, "Sheet1", "id", building_level, "product_add")
    pingzhi = tb.get_cell_value(config.DOC_DIR, sys_industrial_building, "Sheet1", "id", building_id, "quality")
    pingzhi_jiacheng = tb.get_cell_value(config.DOC_DIR, sys_industrial_building_quality, "Sheet1", "id", pingzhi, "product_add")
    zhouqi = tb.get_cell_value(config.DOC_DIR, sys_industrial_building, "Sheet1", "id", building_id, "product_time")
    jichushouru = (chushi_shouru / 100 * (1 + xingji_jiacheng/10000 + level_jiacheng/10000 + pingzhi_jiacheng/10000))
    result = (jichushouru+jichushouru * buff) * zhouqi
    # 计算每秒收入
    result1 = (jichushouru + jichushouru * buff)*zhouqi
    print("等级",building_level,"服务端每个周期收入",result,"每秒收入",jichushouru + jichushouru * buff, "@@@@@@@",jichushouru,"客户端每周期收入",result1)