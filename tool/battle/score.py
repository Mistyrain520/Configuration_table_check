import table_operation
import config
# from tool import card_attribute as ca
tb = table_operation.Table()
your_crad_id = 110102
level = 1
star = 0
shuxing_buff = 0.005
shuxing = {
    '1': "唱功",
    '2': "舞艺",
    '3': "演技",
    '4': "口才",
    '5': "颜值",
}
# 关卡加成比例和修正属性
mission_id = 51105
attr_add = tb.get_cell_value(config.DOC_DIR, "/Z战斗表.xls", "Sheet1", "mission_id", mission_id, "attr_add")
card_attr = tb.get_cell_value(config.DOC_DIR, "/Z战斗表.xls", "Sheet1", "mission_id", mission_id, "card_attr")
print("副本修正值", attr_add, "副本加成比例", card_attr)



