import time
import pyautogui as pag
import os


def click(x, y, count):
    for i in range(count):
        if i == 500 or i == 800:
            print("{}次拉".format(i))
        pag.click(x, y,)
        # time.sleep(0.02)


if __name__ == "__main__":
    start = time.time()
    time.sleep(5)
    click(368, 1009, 1)
    end = time.time()
    print(end - start, "结束")
    pag.press(['ctrl', 'a'])
    pag.press(['backspace'])
    # try:
    #     while True:
    #         print("Press Ctrl-C to end")
    #         x, y = pag.position()  # 返回鼠标的坐标
    #         posStr = "Position:" + str(x).rjust(4) + ',' + str(y).rjust(4)
    #         print(posStr)  # 打印坐标
    #         time.sleep(5)
    #         os.system('cls')  # 清楚屏幕
    # except  KeyboardInterrupt:
    #     print('end....')
        # Position: 368,1009


