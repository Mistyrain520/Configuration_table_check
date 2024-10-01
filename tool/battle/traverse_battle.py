import time
import random
import pyautogui as pag
import os
# import table_operation
# import config
import threading
from pynput import keyboard
from pynput.mouse import Controller
def on_press(key):
    # pass
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    # print('{0} released'.format(
    #     key))
    if key == keyboard.Key.esc:
        os.system("taskkill /F /IM python.exe")
        # Stop listener
        return False
    # if key == keyboard.KeyCode.from_char('1'):
    #     click(369, 136, 1)

def run_listener():
    # Collect events until released
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()

    # ...or, in a non-blocking fashion:
    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    listener.start()

def click(x, y, count,stay=0.02):
    for i in range(count):
        if i in [1000, 2000, 5000,10000]:
            print("{}次拉".format(i))
        pag.click(x, y,)
        time.sleep(stay)


def rangeclick(x, y, x1, y1, count, stay=0.02):
    for i in range(count):
        x2 = random.randint(x, x1)
        y2 = random.randint(y, y1)
        if i in [1000, 2000, 5000, 10000]:
            print("{}次拉".format(i))
        pag.click(x2, y2,)
        time.sleep(stay)
def move_click(x, y, count):
    for i in range(count):
        pag.mouseDown(x, y)
        type = random.randint(1, 4)
        # 1,往下滑动，2往上滑动，3往左滑动，4往右滑动
        if type == 1:
            pag.moveTo(x, y+50)
        if type == 2:
            pag.moveTo(x, y-50)
        if type == 3:
            pag.moveTo(x-50, y)
        if type == 4:
            pag.moveTo(x+50, y)
        pag.mouseUp()
        # time.sleep(0.02)
def get_pos():
    time.sleep(5)
    try:
        for i in range(3):
            x, y = pag.position()  # 返回鼠标的坐标
            posStr = "Position:" + str(x).rjust(4) + ',' + str(y).rjust(4)
            print(posStr)  # 打印坐标
        return x, y
    except KeyboardInterrupt:
        print('failed.You need to try again.')


def clear(x, y,):
    click(x, y, 2)
    time.sleep(0.05)
    pag.keyDown('ctrl')
    pag.keyDown('a')
    pag.keyUp('ctrl')
    pag.keyUp('a')
    pag.press(['backspace'])


def write_mess(x, y, x1, y1, mess, count=1):
    clear(x, y,)
    pag.typewrite(mess, 0.01)
    time.sleep(0.05)
    click(x1, y1, count)


def enter_battle():
    # x命令窗口位置，x1发送按钮位置，x2进入战斗关卡的指令位置, x3为通关当前三消的命令位置,x4空白位置
    x, y, x1, y1 = pos()
    x2, y2, x3, y3, x4, y4 = battle_pos()
    # mission_id = tb.get_content_by_col_name(config.DOC_DIR, "/F副本表.xls", "Sheet1", "id")
    group = 51100
    mission_id = tb.get_content_by_col_value(config.DOC_DIR, "/F副本表.xls", "Sheet1", "group_id", group, 1)
    write_mess(x, y, x1, y1, "props copper 10000")
    for i in mission_id:
        # mess = "debug 2300 {\"missionId\":"+str(i)+",\"cardIds\":[{\"playerId\":1001100000000024,\"cardId\":110102}]}"
        mess = "missionId={};cardIds=110102".format(i)
        click(x2, y2, 1)
        time.sleep(0.2)
        write_mess(x, y, x1, y1, mess)
        print(mess)
        time.sleep(2)
        click(x3, y3, 1)
        time.sleep(1)
        click(x4, y4, 2)
        time.sleep(2)
        pag.keyDown('ctrl')
        pag.keyDown('b')
        pag.keyUp('ctrl')
        pag.keyUp('b')
        time.sleep(0.2)


# 副本一键三星
def auto_three_stars():
    group_id = tb.get_content_by_col_name(config.DOC_DIR, "/F副本组表.xls", "Sheet1", "id")
    x, y, x1, y1 = pos()
    for i in group_id:
        mess = "props missionGroup " + str(i)
        print(mess)
        write_mess(x, y, x1, y1, mess)

# 自动升级建筑
def auto_upgrade_build():
    x, y, x1, y1 = pos()
    build_id = tb.get_content_by_col_name(config.DOC_DIR, "/C产业园建筑表.xls", "Sheet1", "id")
    print(build_id)
    for i in build_id:
        mess = "debug 2603 {\"levelTimes\":99,\"buildingId\":%d}"%i
        write_mess(x, y, x1, y1, mess, 1)

# 升级升星材料一键获取
def get_item():
    x, y, x1, y1 = pos()
    des = ['提升天赋道具', '提升技能道具', '作品升星道具']
    item = []
    for i in des:
        temp = []
        temp = tb.get_cell_value(config.DOC_DIR, "/D道具表.xls", "Sheet1", "use_desc", i, "id", False)
        item += temp
    for i in item:
        mess = "props item " + str(i)
        write_mess(x, y, x1, y1, mess, 1)
def pos():
    print("------识别命令窗口位置------")
    x, y = get_pos()
    print("识别命令窗口位置为", x, y)
    print("------识别发送按钮位置------")
    x1, y1 = get_pos()
    print("发送按钮识别位置为", x1, y1)
    return x, y, x1, y1
def battle_pos():
    print("------识别战斗关卡指令位置------")
    x, y = get_pos()
    print("识别命令窗口位置为", x, y)
    print("------识别三消命令位置------")
    x1, y1 = get_pos()
    print("识别三消命令位置", x1, y1)
    print("------识别空白位置------")
    x2, y2 = get_pos()
    print("识别空白位置", x2, y2)
    return x, y, x1, y1,x2, y2

def auto_project():
    x, y, x1, y1 = pos()
    project = tb.get_content_by_col_name(config.DOC_DIR, "/Q企划中心-项目.xls", "Sheet1", "project_id")
    print(project)
    mess3 = "props power 100000"
    write_mess(x, y, x1, y1, mess3, 1)
    for i in project:
        time.sleep(1)
        mess = "debug 2608 {\"projectId\":%d}" % i
        mess2 = "props project 0"
        write_mess(x, y, x1, y1, mess, 1)
        time.sleep(1)
        write_mess(x, y, x1, y1, mess2, 2)

def auto_click():
    print("------识别左上角位置------")
    x, y = get_pos()
    print("识别左上角位置为", x, y)

    print("------识别右下角位置------")
    x3, y3 = get_pos()
    print("识别右下角位置为", x3, y3)
    while True:
        x2 = random.uniform(x, x3)
        y2 = random.uniform(y, y3)
        # click(x2, y2, 3)
        move_click(x2, y2, 3)
def auto_click2():
    print("------识别点击位置1------")
    x, y = get_pos()
    print("------识别点击位置2------")
    x1, y1 = get_pos()
    for i in range(20000):
        click(x, y, 1)
        click(x1, y1, 1)
def auto_click3():
    print("------识别点击位置1------")
    x, y = get_pos()
    print("------识别点击位置2------")
    x1, y1 = get_pos()
    for i in range(20000):
        rangeclick(x, y, x1, y1, 1)

if __name__ == "__main__":
    print("按esc可中止本程序")
    # tb = table_operation.Table()

    t1 = threading.Thread(target=run_listener)
    t2 = threading.Thread(target=auto_click3)
    t1.start()
    t2.start()


