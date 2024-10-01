import file
import config
import pandas as pd
# 只支持xlsx
def write_excel(excel, df):
    # 先清除格式，再写入，才能成功
    pd.io.formats.excel.header_style = None
    with pd.ExcelWriter(excel) as writer:
        df.to_excel(writer, sheet_name='Sheet1', startrow=0, index=False, header=False)
        workbook = writer.book
        worksheets = writer.sheets
        worksheet = worksheets['Sheet1']
        worksheet.set_column('A:AD', 20)
        format1 = workbook.add_format({
            # 'bold': True,  # 字体加粗
            # 'border': 20,  # 单元格边框宽度
            # 'align': 'left',  # 水平对齐方式
            # 'valign': 'vcenter',  # 垂直对齐方式
            'fg_color': '#FFC000',  # 单元格背景颜色
            # 'text_wrap': True,  # 是否自动换行
        })
        for k in range(2, 5):
            worksheet.set_row(k, 20, format1)
        format2 = workbook.add_format({'fg_color': '#5B9BD5'})
        worksheet.set_row(1, 20, format2)
        for j in range(5, 15):
            worksheet.set_row(j, 20)


pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
rule_excel = file.File.get_file_dir(config.RULE_DIR, file_type=".xlsx")
for r_excel in rule_excel:
    # if r_excel != "\C产业园公司任务表.xls":
    #     continue
    print("正在处理表格文件:", r_excel)
    aa = config.RULE_DIR + r_excel
    bb = config.DOC_DIR + r_excel[:-1]
    data_rule = pd.read_excel(aa, sheet_name=0, header=[1])
    data_config = pd.read_excel(bb, sheet_name=0, header=[1], nrows=3)
    # print(data_rule.columns[24], 'Unnamed' in data_rule.columns[24])
    # print("@@@@@@@@@@@@@@@@@@")
    # print(data_config.columns)
    # print("@@@@@@@@@@@@@@@@@@")
    need_drop = []
    # 遍历规则表，如果表头（第二列）不存在配置表表头中，则移除该列数据
    for rule_col in data_rule.columns:
        if 'Unnamed' in rule_col:
            need_drop.append(rule_col)
        if rule_col not in data_config.columns:
            need_drop.append(rule_col)
    data_rule.drop(need_drop, inplace=True, axis=1)
    # 遍历配置表，如果配置表表头不存在规则表表头，则添加该列数据；如果配置表存在Unnamed（即没有表头的意思，pd数据删除该列）
    # 判断Unnamed是为了纠正配置表表头，后面规则表重排reindex可以按照纠正后的配置表表头排列
    # print(data_rule)
    # print(data_config)
    # print("@@@@@@@@@@@@@@@@@@")
    for config_col, config_row in data_config.items():
        if 'Unnamed' in config_col:
            # print(config_col, "移除的一列")
            data_config.drop(config_col, inplace=True, axis=1)
            continue
        if config_col not in data_rule.columns:
            data_rule[config_col] = data_config[config_col]
            continue
        for i in range(3):
            if data_rule.at[i, config_col] != config_row[i]:
                data_rule.at[i, config_col] = config_row[i]
    result = data_rule.reindex(data_config.columns, axis="columns")
    # print(data_rule)
    # print("@@@@@@@@@@@@@@@@@@")
    result.loc[-1] = result.columns
    excel_name = pd.read_excel(bb, sheet_name=0, header=[0], nrows=0).columns[0]
    need_append = [excel_name] + ['']*(len(result.columns)-1)
    result.loc[-2] = need_append
    result.sort_index(inplace=True)
    write_excel(aa, result)
    # your_excel = result.to_excel(aa, startrow=0, index=False, header=False)
