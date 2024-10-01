import pymysql
import decimal
import time
import random,os,sys
sys.path.append("../../Configuration_table_check")
import table_operation,config
class Server(object):
    def __init__(self, ip, user, password, tb_name):
        # QA服
        self.ip = ip
        self.user = user
        self.password = password
        self.tb_name = tb_name
        self.conn = pymysql.connect(self.ip, self.user, self.password, self.tb_name)
        # self.conn.select_db()
        # 内网服
        # self.conn = pymysql.connect('192.168.212.248', 'root', 'dreamroot', 'idol_dev')
        if not self.conn:
            print("连接失败!")

    def _GetConnect(self):
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "连接数据库失败")
        else:
            return cur
    def Cloconnect(self):
        self.conn.close()
    def ExecQuery(self, sql,val=None) -> tuple:
        # print(sql,"@@",val)
        cur = self._GetConnect()
        cur.execute(sql, val)
        result = cur.fetchall()
        return result

    def update(self, sql, val=None):
        cur = self._GetConnect()
        cur.execute(sql, val)
        self.conn.commit()
        result = cur.fetchall()
        return result

    # 切换数据库
    def selectdb(self, dataname):
        self.conn.select_db(dataname)

    # 处理数据库返回的tuple数据,通常都是二层嵌套tuple，返回无嵌套的列表
    def dealdata(self,tu_data):
        result = []
        for i in tu_data:
            for j in i:
                result.append(j)
        return result
    # 测试,返回所有玩家
    def test1(self):
        # log = ["log_action_daily_0","log_action_daily_1","log_action_daily_2","log_action_daily_3","log_action_daily_4","log_action_daily_5","log_action_daily_6","log_action_daily_7","log_action_daily_8","log_action_daily_9",]
        log = ["log_action_level_0","log_action_level_1","log_action_level_2","log_action_level_3","log_action_level_4","log_action_level_5","log_action_level_6","log_action_level_7","log_action_level_8","log_action_level_9",]

        sql = """select distinct player_id from log_action_daily_0
        union select distinct player_id from log_action_daily_1
        union select distinct player_id from log_action_daily_2
        union select distinct player_id from log_action_daily_3
        union select distinct player_id from log_action_daily_4
        union select distinct player_id from log_action_daily_5
        union select distinct player_id from log_action_daily_6
        union select distinct player_id from log_action_daily_7
        union select distinct player_id from log_action_daily_8
        union select distinct player_id from log_action_daily_9;"""
        for i in log:
            sql1 = "select distinct player_id from " + i

            print(self.ExecQuery(sql1), "@", i)
        return self.ExecQuery(sql)
    # 指定玩法操作次数报表
    def test2(self):
        t0 = time.perf_counter()
        result = {}
        log = ["log_action_daily_0","log_action_daily_1","log_action_daily_2","log_action_daily_3","log_action_daily_4","log_action_daily_5","log_action_daily_6","log_action_daily_7","log_action_daily_8","log_action_daily_9",]
        sql = """select distinct player_id from log_action_daily_0
        union select distinct player_id from log_action_daily_1
        union select distinct player_id from log_action_daily_2
        union select distinct player_id from log_action_daily_3
        union select distinct player_id from log_action_daily_4
        union select distinct player_id from log_action_daily_5
        union select distinct player_id from log_action_daily_6
        union select distinct player_id from log_action_daily_7
        union select distinct player_id from log_action_daily_8
        union select distinct player_id from log_action_daily_9;"""
        # tuple
        all_play = self.ExecQuery(sql)
        for play_id in all_play:
            for daily_log in log:
                # type来指定玩法，sum来算出这个玩法的点击次数
                # {value: 0, label: '全部'},
                # {value: 1, label: '战斗'},
                # {value: 2, label: '扫荡'},
                # {value: 3, label: '招募'},
                # {value: 4, label: '购买体力'},
                # {value: 5, label: '卡牌升星'},
                # {value: 6, label: '卡牌升级'},
                # {value: 7, label: '卡牌觉醒'},
                # {value: 8, label: '编队次数'},
                # {value: 9, label: '普通商店购买 '},
                # {value: 10, label: '普通商店购买'},
                # {value: 11, label: '建筑部署'},
                # {value: 12, label: '建筑升级'},
                # {value: 13, label: '建筑升星'}
                sql1 = "SELECT SUM(times) FROM " + daily_log + " where type = 1 and player_id = "  + str(play_id[0]) + " and gmt_create < 1588176000 and gmt_create > 1585670400 and server_id = 110"
                # print(sql1, "@@@@@@@@")
                # print(daily_log,play_id)
                if self.ExecQuery(sql1)[0][0] == None:
                    continue
                # print(str(play_id[0]), "@@", self.ExecQuery(sql1)[0][0])
                if str(play_id[0]) in result.keys():
                    result[str(play_id[0])] = result[str(play_id[0])] + self.ExecQuery(sql1)[0][0]
                else:
                    result[str(play_id[0])] = self.ExecQuery(sql1)[0][0]
        print(result)

        t1 = time.perf_counter()
        print('Running time: %s Seconds' % (t1 - t0))

    # 全服玩家等级停留统计
    def test3(self):
        t0 = time.perf_counter()
        result = {}
        log = ["log_action_level_0","log_action_level_1","log_action_level_2","log_action_level_3","log_action_level_4","log_action_level_5","log_action_level_6","log_action_level_7","log_action_level_8","log_action_level_9",]
        sql = """select distinct player_id from log_action_level_0
                union select distinct player_id from log_action_level_1
                union select distinct player_id from log_action_level_2
                union select distinct player_id from log_action_level_3
                union select distinct player_id from log_action_level_4
                union select distinct player_id from log_action_level_5
                union select distinct player_id from log_action_level_6
                union select distinct player_id from log_action_level_7
                union select distinct player_id from log_action_level_8
                union select distinct player_id from log_action_daily_9;"""
        all_play = self.ExecQuery(sql)
        for play_id in all_play:
            for daily_log in log:
                sql1 = "SELECT MAX(level) FROM "+ daily_log+ " where gmt_create < 1588176000 and gmt_create > 1585670400 and server_id = 110 and player_id = " + str(play_id[0])
                if self.ExecQuery(sql1)[0][0] == None:
                    continue
                if str(play_id[0]) in result.keys():
                    result[str(play_id[0])] = max(result[str(play_id[0])], self.ExecQuery(sql1)[0][0])
                else:
                    result[str(play_id[0])] = self.ExecQuery(sql1)[0][0]
        print(result)
        t1 = time.perf_counter()
        print('Running time: %s Seconds' % (t1 - t0))


    # 指定等级停留时长
    def test4(self):
        log = ["log_action_level_0","log_action_level_1","log_action_level_2","log_action_level_3","log_action_level_4","log_action_level_5","log_action_level_6","log_action_level_7","log_action_level_8","log_action_level_9",]
        level = 3
        n_level = level +1
        for level_log in log:
            print("查询的表",level_log)
            sql1 = "select distinct player_id from " + level_log
            # print(self.ExecQuery(sql1))
            for play_id in self.ExecQuery(sql1):
                sql2 = "select player_id,gmt_create,level from "+ level_log + " where player_id = "+ str(play_id[0]) +" and gmt_create > 1582992000 and gmt_create < 1588176000 and (level = " + str(level) + " or level = "+ str(n_level) +")"
                # print(sql2,"@@@@@@@@@@@@@@")
                if len(self.ExecQuery(sql2)) >= 2:
                    cretime = [i[1] for i in self.ExecQuery(sql2)]
                    print(self.ExecQuery(sql2),cretime,"@@",cretime[1] - cretime[0])


    def rank(self):
        sql2 ="INSERT INTO p_activity (id, act_id, rewards, param1, param2, param3, param4, refresh_time, gmt_create, gmt_modified) VALUES (%s, 5000, '11008:0;11009:0;11010:1;11011:1;11012:0;11013:0;11014:0;11015:0;11016:0;11017:0;11018:0;11019:0;11000:2;11001:2;11002:0;11003:0;11004:0;11005:0;11006:0;11007:0', 0, 0, 0, %s, 1590496224, 1590496224, 0);"
        # val = (121, random.randint(1, 20000))
        # return self.update(sql, val)
        sql1 = "select id from idol_qa.p_player where nickname like 'qa%';"
        play_id = self.ExecQuery(sql1)
        for i in play_id:
            val1 = (i[0], random.randint(1, 200000))
            self.update(sql2, val1)

    def write_device_code(self):
        for i in range(10):
            # sql1 = "select distinct player_id from log_player_login_" + str(i)
            sql1 = "update log_player_login_{} set device_code = player_id;".format(str(i))
            self.update(sql1)
            # play_er = self.ExecQuery(sql=sql1)
            # for play_er_id in play_er:
            #     sql2 = "update log_player_login_"+str(i) +" set device_code = {} where player_id = {};".format(str(play_er_id[0]), str(play_er_id[0]))
            #     self.update(sql2)
    # 写一些邮件数据去测试200封邮件
    def write_email(self):
        sql1 = "insert into p_mail values ('100100000094',%s,%s,'基督教','哈喽','1603296000','','','0','0','1603184574','0');"
        j = 2
        for i in range(1,200):
            j+=1
            val1 = (i, "这是第{}邮件".format(j))
            self.update(sql1, val1)

    # 统计一下抽卡
    def probability_card(self):
        play_id = 111000000066
        tb = table_operation.Table()
        list1,list2,list3,list4 = [],[],[],[]
        trans_good = tb.change_two_col_dict(config.DOC_DIR, "/K卡牌表.xls", "Sheet1", "id", "transform_goods")
        card_color = tb.change_two_col_dict(config.DOC_DIR, "/K卡牌表.xls", "Sheet1", "id", "color")
        sql1 = "select card_id from p_card where id={}".format(play_id)
        card_id = self.ExecQuery(sql1)
        for i in card_id:
            valu = list(trans_good[i[0]].keys())[0]
            sql2 = "select count from p_goods where id={} and model_id={}".format(play_id, valu)
            if not self.ExecQuery(sql2):
                temp = (i[0], 1)
            else:
                temp = (i[0],sum([val[0] for val in self.ExecQuery(sql2)])+1)
            if card_color[i[0]] == 1:
                list1.append(temp)
            if card_color[i[0]] == 2:
                list2.append(temp)
            if card_color[i[0]] == 3:
                list3.append(temp)
            if card_color[i[0]] == 4:
                list4.append(temp)
        n = sum([vv for e,vv in list1]) - 1 #减去默认的第一张卡110102
        r = sum([vv for e, vv in list2])
        sr = sum([vv for e, vv in list3])
        ssr = sum([vv for e, vv in list4])
        print("品质为1",list1,"总和",n,len(list1))
        print("品质为2",list2,"总和",r,len(list2))
        print("品质为3",list3,"总和",sr,len(list3))
        print("品质为4",list4,"总和",ssr,len(list4))
        print(n+r+sr+ssr)
        print("ssr概率:", ssr/(n+r+sr+ssr))
        print("sr概率:", sr / (n + r + sr + ssr))
        print("r概率:", r / (n + r + sr + ssr))
        print("n概率:", n / (n + r + sr + ssr))

    # 随机超市次数购买表造数据用
    def market(self):
        for i in range(1,100000):
            # sql2 = "update p_card set level = 100 where id = {}".format(play_id)
            sql1 = "insert into sys_city_market_refresh_times (id, type_id, times, price, gmt_create, gmt_modified) values (%s,3,%s,0,0,0)"
            val1 = (i,i)
            self.update(sql1, val1)



if __name__ == '__main__':
    print("@@")
    # a = Server('192.168.212.52', 'root', 'dreamroot', 'idol_qa')
    # a = Server('192.168.212.248', 'root', 'dreamroot', 'idol_qa_sys')
    # a.market()

