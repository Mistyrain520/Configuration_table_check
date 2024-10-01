import sys
sys.path.append("D:/Users/User/PycharmProjects/Configuration_table_check/")
import file
import json
import table_operation
import re
import config
tb = table_operation.Table()
slot_dir = u'D:/doc2/6配置文档/棋盘'
slot = file.File.get_file_dir(slot_dir, file_type=".json")
mission_id = tb.change_two_col_dict(
    config.DOC_DIR,
    "/Z战斗表.xls",
    "Sheet1",
    "id",
    "mission_id")
mission_name = tb.change_two_col_dict(
    config.DOC_DIR, "/F副本表.xls", "Sheet1", "id", "name")
targer = tb.change_two_col_dict(
    config.DOC_DIR,
    "/Z战斗表.xls",
    "Sheet1",
    "id",
    "target_type")
chess = tb.change_two_col_dict(
    config.DOC_DIR,
    "/Q棋盘表.xls",
    "Sheet1",
    "id",
    "level")
# "gridsList" "addLists" "walkPaths" "eventGroups"
qipanconfig = {}
for i in slot:
    # if i != '\\level_5412011.json':
    #     continue
    # print(i)
    if "slot" in i:
        continue
    chess_level = re.split(r'[\\.]', i)[1]
    full_path = slot_dir + i
    with open(full_path, encoding='utf-8', mode="r") as f:
        data = json.loads(f.read())
        # 新版棋盘应该采用下面这种方式
        walk_path = data.get("walkPaths", [])
        if len(walk_path) == 0:
            walk = 1
        else:
            walk = len(walk_path[0].get("path", -1))
        qipanconfig[chess_level] = walk

new_chess = {}
for key in chess.keys():
    new_chess[str(key)] = str(chess[key])
for key in new_chess.keys():
    level = new_chess[key]
    target_type = targer[str(key)]
    mission = mission_id[key]
    if level not in qipanconfig.keys():
        print("棋盘表不存在这个棋盘文件", level, "对应关卡名称", mission, mission_name[mission])
        continue
    if qipanconfig[level] > 1:
        if target_type != 2:
            print(
                "正在检查的棋盘",
                level,
                "棋盘对应的战斗表id如下",
                key,
                mission,
                mission_name[mission],
                "棋盘目标",
                target_type,
                "棋盘配置文件路径长度",
                qipanconfig[level])
    if qipanconfig[level] <= 1:
        if target_type != 1:
            print(
                "正在检查的棋盘",
                level,
                "棋盘对应的战斗表id如下",
                key,
                mission,
                mission_name[mission],
                "棋盘目标",
                target_type,
                "棋盘配置文件路径长度",
                qipanconfig[level])
