import pymysql
import tk_ui as tk_login
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.messagebox import *
from PIL import Image, ImageTk
from tkinter import filedialog

connect_ = pymysql.connect(host="localhost", user="root", port=3307, password="Jason20040903", database="user_info",
                           charset="utf8")

tk_login.user_name = '123456'


class User_Gui():
    def __init__(self):
        self.main_screen = tk.Tk()

    def set_init_window(self):
        self.main_screen.geometry('600x500')
        self.main_screen.resizable(False, False)
        self.main_screen.title('user')

        canvas = tk.Canvas(self.main_screen, width=1000, height=1000)
        # 图片
        image_ = Image.open(
            'C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/imgs/login_bg.gif')
        image_bg = ImageTk.PhotoImage(image_)
        image = canvas.create_image(100, 0, anchor='n', image=image_bg)
        canvas.pack()
        tk.Label(self.main_screen, text='欢迎回到飞机大战', font=('宋体', 20), fg="blue", bg='Light Sea Green',
                 relief=SUNKEN).place(x=200,
                                      y=20)
        tk.Label(self.main_screen, text='用户:' + tk_login.user_name, font=('宋体', 20), fg="blue",
                 bg='Light Sea Green',
                 relief=SUNKEN).place(x=200,
                                      y=50)
        cur = connect_.cursor()
        sql = "SELECT score FROM user_base_info WHERE user_name = %s"
        cur.execute(sql, (tk_login.user_name))
        row = cur.fetchone()
        score = row[0]
        tk.Label(self.main_screen, text="您的总分数为" + str(score), font=('宋体', 20), fg="blue",
                 bg='Light Sea Green', relief=SUNKEN).place(x=200, y=80)

        # 设置头像，统一头像，或用户存入的头像
        user_img = Image.open(
            'C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/imgs/user_img_100x100.jpg')
        user_tk_img = ImageTk.PhotoImage(user_img)
        canvas_ = tk.Canvas(self.main_screen, width=90, height=90)  # 设置头像画布的宽度和高度为100
        canvas_.create_image(0, 0, anchor='nw', image=user_tk_img)  # 在 Canvas 中放入圖片
        canvas_.place(x=50, y=50)  # 设置头像画布的位置为左上角

        # 退出按钮
        btn_quit = tk.Button(self.main_screen, text='登出', width=10, height=1, activebackground="RoyalBlue",
                             relief=RIDGE, command=lambda: self.quit_in(),
                             bg="Cyan")
        btn_quit.place(x=250, y=400)

        self.main_screen.mainloop()

        # 更换头像（选做）

    def quit_in(self):
        tk.messagebox.showinfo("提示", "登出成功！")
        self.main_screen.destroy()
        self.main_screen.quit()
        tk_login.is_logged_in = False


if __name__ == '__main__':
    main = User_Gui()
    main.set_init_window()
