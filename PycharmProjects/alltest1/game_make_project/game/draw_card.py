import random
import sys
import tkinter as tk  # 导入一个第三方库，用于制作桌面软件
import tkinter.font as tf
from PIL import Image, ImageTk

# 数据部分
R = {
    "name": "R",
    "color": "blue",
    "size": "20",
    "font": "微软雅黑",
    "data": ["冷刃", "黑缨枪", "白缨枪", "翡玉法球", "飞天大御剑", "暗铁剑", "旅行剑", "钢轮弓",
             "吃鱼虎刀", "沾染龙血的剑", "以理服人", "异世界行记", "甲级宝钰", "翡玉法球"],
    "person": []
}
SR = {
    "name": "SR",
    "color": "purple",
    "size": "20",
    "font": "微软雅黑",
    "data": ["腐殖之剑", "祭礼剑", "西风剑", "试作斩岩", "笛剑", "螭骨剑", "钢轮弓", "西风猎弓",
             "钢轮弓", "绝弦", "祭礼弓", "万国诸海图谱", "匣里日月", "千岩古剑", "黑岩绯玉"],
    "person": ["香菱", "菲谢尔", "菲谢尔", "北斗", "芭芭拉", "北斗", "凝光", "托马", "重云",
               "砂糖", "烟绯", "安柏", "凯亚", "丽莎", "诺艾尔"]
}
SSR = {
    "name": "SSR",
    "color": "yellow",
    "size": "20",
    "font": "微软雅黑",
    "data": ["天空之卷", "四风原典", "天空之傲", "天空之脊", "风鹰剑", "风鹰剑", "狼的末路"],
    "person": ["迪卢克", "七七", "琴", "莫娜", "刻晴"]
}

ten_count = 0
ninety_count = 0
max_count = 0
person_up = "优菈"
data_up = "松籁响起之时"
ALL = [R, SR, SSR]
tag_id = "0"


class draw_cards:
    def __init__(self):
        # 建立一个主窗口 root
        self.root = tk.Tk()
        # 设置窗口标题
        self.root.title("原神模拟抽卡器")
        # 设置单抽图片
        self.img_one = Image.open(
            "C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/imgs/signup_bg.jpg")
        self.img_one = self.img_one.resize((40, 40))
        self.image_one = ImageTk.PhotoImage(self.img_one)
        # 设置十连抽图片
        self.img_ten = Image.open(
            "C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/imgs/signup_bg.jpg")
        self.img_ten = self.img_ten.resize((40, 40))
        self.image_ten = ImageTk.PhotoImage(self.img_ten)
        # 在窗口上创建一个按钮 button，用于单抽,它依赖于父窗口root
        self.button_one = tk.Button(self.root, text="单抽", image=self.image_one, command=self.one)
        self.button_ten = tk.Button(self.root, text="十连抽", image=self.image_ten, command=self.ten)
        # 布局创建的按钮，rou代表行，column代表列
        self.button_one.grid(row=0, column=0)
        self.button_ten.grid(row=0, column=1)
        # 创建一个文本框，用于打印抽奖日志
        self.text = tk.Text(self.root, bg="black")
        # columnspan代表合并两列
        self.text.grid(row=1, columnspan=2)
        # 运行窗口
        self.root.mainloop()

    # 单抽
    def one(self):
        _res = self.get()
        self.count_flush(_res["level"], _res["thing"])
        self.insert_text(conf=_res["level"], message=_res["thing"])
        self.text.insert("end", "\n")
        self.text.see("end")

    # 十连
    def ten(self):
        self.text.tag_add('tag', "end")
        self.text.tag_config('tag', foreground="white")
        self.text.insert("end", "\nstart\n", 'tag')
        for i in range(10):
            self.one()
        self.text.insert("end", f"\nend{ten_count}/{ninety_count}/{max_count}\n", "tag")
        self.text.see("end")

    # 根据抽奖出的物品index获取物品等级
    def found(self, index):
        for i in ALL:
            if pool[index] in i["person"]:
                return i
            if pool[index] in i["data"]:
                return i

    # 每次抽卡后刷新当前计数器
    def count_flush(self, level, thing):
        global ten_count
        global ninety_count
        global max_count
        if level["name"] == "SR":
            ten_count = 0
        if level["name"] == "SSR":
            ninety_count = 0
        if level["name"] == "SSR" and ((thing in person_up) or (thing in data_up)):
            max_count = 0

    # 抽卡规则
    def get(self):
        global ten_count
        global ninety_count
        global max_count
        level = None
        ten_count += 1
        ninety_count += 1
        max_count += 1
        if ten_count == 10:
            level = SR
        if ninety_count == 90:
            level = SSR
        if level is SR or level is SSR:
            index = random.randrange(len(level[what]))
            thing = level[what][index]
        if max_count != ninety_count and level is SSR:
            level = SSR
            thing = person_up if what == "person" else data_up
        if max_count == 180:
            level = SSR
            thing = person_up if what == "person" else data_up
        if level is None:
            index = random.randrange(len(pool))
            level = self.found(index)
            thing = pool[index]
        return {
            "level": level,
            "thing": thing
        }

    # 添加日志到Text框
    def insert_text(self, message, conf):
        global tag_id
        # 设置字体大小和颜色
        ft = tf.Font(family=conf["font"], size=conf["size"])
        self.text.tag_add('tag' + tag_id, "end")
        self.text.tag_config('tag' + tag_id, foreground=conf["color"], font=ft)
        self.text.insert("end", message + "\n", "tag" + tag_id)
        self.text.see("end")
        tag_id = str(int(tag_id) + 1)


# mian函数，程序会运行这里面的东西
if __name__ == '__main__':
    # 修改为武器抽武器池
    what = "角色"
    if what == "角色":
        what = "person"
    if what == "武器":
        what = "data"
    if what not in ["data", "person"]:
        sys.exit(1)
    # 把up角色和武器加入池
    SSR["data"].append(data_up)
    SSR["person"].append(person_up)
    # 合并在一个总池,实现概率，可以通过算法实现，难得弄..
    pool = list()
    for i in range(90):
        pool.extend(R["data"])
    for i in range(10):
        pool.extend(SR[what])
    pool.extend(SSR[what])
    draw_ui = draw_cards()

