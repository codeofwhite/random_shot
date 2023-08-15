import tkinter.messagebox
import pymysql
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.messagebox import *
from PIL import Image, ImageTk

is_logged_in = False


class My_Gui():
    def __init__(self):
        self.main_screen = tk.Tk()

    def set_init_window(self):
        self.main_screen.geometry('600x500')
        self.main_screen.title('login')

        canvas = tk.Canvas(self.main_screen, width=1000, height=1000)
        # 图片
        image_ = Image.open(
            'C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/imgs/login_bg.gif')
        image_bg = ImageTk.PhotoImage(image_)
        image = canvas.create_image(100, 0, anchor='n', image=image_bg)
        canvas.pack()
        tk.Label(self.main_screen, text='欢迎来到飞机大战', font=('宋体', 20), fg="blue", bg='Light Sea Green',
                 relief=SUNKEN).place(x=250,
                                      y=80)

        tk.Label(self.main_screen, text='用户名:', font=('华文行楷', 20), fg="blue", cursor='heart',
                 bg="Powder Blue").place(
            x=80,
            y=170)
        tk.Label(self.main_screen, text='密码:', font=('华文行楷', 20), fg="blue", cursor='heart',
                 bg="Powder Blue").place(
            x=100,
            y=210)

        user_name = tk.StringVar()
        user_name.set('buymeacoffee@python.com')
        entry_user_name = tk.Entry(self.main_screen, textvariable=user_name, font=('Arial', 14), relief=SUNKEN)
        entry_user_name.place(x=200, y=175)

        user_pw = tk.StringVar()
        entry_user_pw = tk.Entry(self.main_screen, textvariable=user_pw, font=('Arial', 14), show='·', relief=SUNKEN)
        entry_user_pw.place(x=200, y=215)

        # 第6步，login and sign up 按钮
        btn_login = tk.Button(self.main_screen, text='登入', width=10, height=1, activebackground="RoyalBlue",
                              relief=RIDGE,
                              bg="Cyan", command=lambda: self.login_event(entry_user_name.get(), entry_user_pw.get()))
        btn_login.place(x=180, y=260)
        btn_sign_up = tk.Button(self.main_screen, text='注册', command=lambda: self.sign_up(canvas), width=10, height=1,
                                activebackground="RoyalBlue",
                                relief=RIDGE, bg="Cyan")
        btn_sign_up.place(x=300, y=260)

        self.main_screen.mainloop()

    def sign_up(self, canvas):
        # self.main_withdraw.withdraw() 直接让主页面消失

        # 定义长在窗口上的窗口
        window_sign_up = tk.Toplevel(self.main_screen)
        window_sign_up.geometry('450x300')
        window_sign_up.title('注册界面')

        # 在子窗口添加颜色和图片
        canvas_top = Canvas(window_sign_up, width=500, height=600)
        canvas_top.pack(fill="both", expand=True)
        img_top = Image.open(
            "C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/imgs/signup_bg.jpg")
        img_top = img_top.resize((600, 400))
        window_sign_up.photo = ImageTk.PhotoImage(img_top)  # 要修改成这样才可以显示图片，不然会被当垃圾回收了
        canvas_top.create_image(0, 0, anchor=NW, image=window_sign_up.photo)
        canvas.create_window(0, 0, anchor=NW)

        new_name = tk.StringVar()  # 将在entry输入的注册名赋值给变量
        new_name.set('buymemorecoffee@python.com')  # 初始一个用户名放着
        tk.Label(window_sign_up, width=9, height=1, text='用户名： ', font=("华文行楷", 20), relief=SUNKEN,
                 bg="Pale Turquoise").place(x=10,
                                            y=10)
        entry_new_name = tk.Entry(window_sign_up, textvariable=new_name, font=('Arial', 14))
        entry_new_name.place(x=140, y=15)

        new_pw = tk.StringVar()
        tk.Label(window_sign_up, width=9, height=1, text='密码: ', font=("华文行楷", 20), relief=SUNKEN,
                 bg="Pale Turquoise").place(x=10,
                                            y=50)
        entry_user_pwd = tk.Entry(window_sign_up, textvariable=new_pw, show='*', font=('Arial', 14))
        entry_user_pwd.place(x=140, y=55)

        new_pwd_confirm = tk.StringVar()
        tk.Label(window_sign_up, width=9, height=1, text='确认密码: ', font=("华文行楷", 20), relief=SUNKEN,
                 bg="Pale Turquoise").place(
            x=10,
            y=90)
        entry_user_pwd_confirm = tk.Entry(window_sign_up, textvariable=new_pwd_confirm, show='·', font=('Arial', 14))
        entry_user_pwd_confirm.place(x=140, y=95)

        # 注册按钮
        btn_confirm_sign_up = tk.Button(window_sign_up, text='注册', activebackground="RoyalBlue", width=7, height=1,
                                        relief=RIDGE, bg="Cyan", font=("华文行楷", 15),
                                        command=lambda: self.sign_event(entry_new_name.get(), entry_user_pwd.get(),
                                                                        entry_user_pwd_confirm.get()))
        btn_confirm_sign_up.place(x=180, y=130)

    def login_event(self, entry_name, entry_pass):
        conn = pymysql.connect(host="localhost", user="root", port=3307, password="Jason20040903", database="user_info",
                               charset="utf8")
        if entry_name == "" or entry_pass == "":
            tkinter.messagebox.showwarning("提示", "请输入账号密码！")
        # 在数据库比对
        else:
            global is_logged_in
            is_logged_in = True
            tkinter.messagebox.showinfo("提示", "登入成功！")
            self.main_screen.destroy()
            self.main_screen.quit()

    def sign_event(self, entry_name, entry_pass, entry_pass_con):
        if entry_name == "" or entry_pass == "" or entry_pass_con == "":
            tkinter.messagebox.showwarning("提示", "请输入账号密码！")
        elif entry_pass != entry_pass_con:
            tkinter.messagebox.showwarning("提示", "两次密码不一致！")
        # 在数据库比对
        else:
            tkinter.messagebox.showinfo("提示", "注册成功！")


if __name__ == '__main__':
    my = My_Gui()
    my.set_init_window()
