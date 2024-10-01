import os, sys
sys.path.append("D:/Users/User/PycharmProjects/Configuration_table_check")
from tkinter import *
from tkinter import scrolledtext
import configparser
import table_operation
# class Interface(object):
#     pass
#变动指定文本的颜色
def search(text_widget, keyword, tag):
    pos = '1.0'
    while True:
        idx = text_widget.search(keyword, pos, stopindex=END)
        print(idx)
        if not idx:
            break
        pos = '{}+{}c'.format(idx, len(keyword))
        text_widget.tag_add(tag, idx, pos)
        print(tag,idx,pos)
def callback():
    print("点了一次")
    T1.delete(0.0, END)
    file_list = []
    # commad_dir = u'D:/测试文档/指令'
    proDir = os.path.split(os.path.realpath(__file__))[0]
    print(proDir)
    configPath = os.path.join(proDir, "config.ini")
    con = configparser.ConfigParser()
    con.read(configPath, encoding="utf-8-sig")
    commad_dir = proDir + con.get("config", "commad_dir")
    print(commad_dir)
    for root, dirs, files in os.walk(commad_dir, topdown=True):
        for name in files:
            if os.path.splitext(name)[1] == '.txt':
                file_list.append(os.path.join(root, name))
    if not E1.get():
        for file_path in file_list:
            with open(file_path, mode="r", encoding='utf8', errors='ignore') as f:
                for line in f.readlines():
                    T1.insert(INSERT, '\n' + line + file_path + '\n')
            f.close()
        return
    k = E1.get()
    for file_path in file_list:
        with open(file_path, mode="r",encoding='utf8', errors='ignore') as f:
            for line in f.readlines():
                if k in line:
                    T1.insert(INSERT, '\n'+ line + file_path +'\n')
        f.close()
        T1.tag_config("红色", background='red')
        search(T1, k, "红色")
def get_item():
    proDir = os.path.split(os.path.realpath(__file__))[0]
    print(proDir)
    configPath = os.path.join(proDir, "config.ini")
    con = configparser.ConfigParser()
    con.read(configPath, encoding="utf-8-sig")
    doc_dir = con.get("config", "doc_dir")
    T1.delete(0.0, END)
    wbk = tb.open_workbook(doc_dir, "/D道具表.xls")
    sheet = wbk.sheet_by_name("Sheet1")
    if not E2.get():
        for i in range(5, sheet.nrows):
            T1.insert(INSERT, '\n' + str(sheet.cell_value(i, 0)) + "      " + str(sheet.cell_value(i, 2)) + '\n')
            T1.tag_config("红色", background='red')
        return
    all_content = re.split("，", E2.get())
    for content in all_content:
        for i in range(5, sheet.nrows):
            if content in str(sheet.cell_value(i, 2)) or content in str(int(sheet.cell_value(i, 0))):
                T1.insert(INSERT, '\n' + str(sheet.cell_value(i, 0)) + "      " + str(sheet.cell_value(i, 2)) + '\n')
                T1.tag_config("红色", background='red')
                search(T1, content, "红色")
def enter(event):
    callback()
def item(event):
    get_item()


top = Tk()
top.title("查询指令")
# frame1 = Frame(top)

L1 = Button(top, text="查询",command=callback)
L1.grid(row=0)
addr = StringVar(value='')
E1 = Entry(top, bd=5,)
E1.grid(row=1, column=0)
E1.bind("<Return>", enter)

E2 = Entry(top, bd=5, textvariable=addr, )
E2.grid(row=1, column=1)
E2.bind("<Return>", item)

T1 = scrolledtext.ScrolledText(top, width=70, height=30, font=("隶书", 10),)
# T1.pack(side=BOTTOM, expand=YES, fill=BOTH)
T1.grid(row=2,columnspan=2)

tb = table_operation.Table()
top.mainloop()

