import os
import config
class File(object):
    @staticmethod
    def get_file_dir(path, file_type=""):
        path_list, name_list = [], []
        for root, dirs, files in os.walk(path, topdown=True):
            # print('\\' in root)
            # print(root,"@",dirs,"@",files,"@@")
            # 根据'\'是否在root中判断是否有子目录，将子目录拆开，把表格记为['\\D道具表.xls','\\season\\道具表.xls', '\\season\\season2\\道具表.xls']
            if "\\" in root:
                pre_name = '\\' + root.split('\\', 1)[1]
            else:
                pre_name = ''
            for name in files:
                if "~" in name:
                    continue
                if file_type == "":
                    name_list.append(pre_name + '\\' + name)
                else:
                    if os.path.splitext(name)[1] == file_type:
                        name_list.append(pre_name + '\\'+name)
        return name_list

    def exec(self):
        pass

# 测试用
# print(File.get_file_dir(config.RULE_DIR))
