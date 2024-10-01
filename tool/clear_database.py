from sql import Server
import argparse
def dele_data():
    sql1 = "show tables;"
    result = s.update(sql1)
    for table in result:
        sql3 = "delete from {}".format(table[0])
        s.update(sql3)
    s.selectdb("idol_qa_log")
    sql2 = "show tables;"
    result2 = s.ExecQuery(sql2)
    for table in result2:
        sql4 = "delete from {}".format(table[0])
        s.update(sql4)


s = Server('192.168.212.52', 'root', 'dreamroot', 'idol_qa')
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--search", action='store', required=True, help="search the string you use here")
args = parser.parse_args()
if args.search:
    search = args.search
else:
    search = False
if search == "True":
    dele_data()
    print("成功删除数据库！！！恭喜你！")
else:
    print("不执行删库操作")
s.Cloconnect()
