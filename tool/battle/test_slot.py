from unittest import TestCase
import file
import json
import table_operation
import re
import config

class TestTable(TestCase):
    def setUpClass(self):
        tb = table_operation.Table()
        slot_dir = u'D:/doc/6配置文档/棋盘'
        slot = file.File.get_file_dir(slot_dir, file_type=".json")
        battle = tb.change_two_col_dict(config.DOC_DIR, "/Z战斗表.xls", "Sheet1", "mission_id", "first_res")
        chess = tb.change_two_col_dict(config.DOC_DIR, "/F副本表.xls", "Sheet1", "id", "first_res")
