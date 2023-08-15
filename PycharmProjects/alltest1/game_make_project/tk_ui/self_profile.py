import tkinter.messagebox
import pymysql
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.messagebox import *
from PIL import Image, ImageTk


class User_Gui():
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

        btn_quit = tk.Button(self.main_screen, text='登出', width=10, height=1, activebackground="RoyalBlue",
                             relief=RIDGE, command=lambda: self.quit_in(),
                             bg="Cyan")
        btn_quit.place(x=180, y=260)

        self.main_screen.mainloop()

    def quit_in(self):
        tkinter.messagebox.showinfo("提示", "登出成功！")
        self.main_screen.destroy()
        self.main_screen.quit()


if __name__ == '__main__':
    my = User_Gui()
    my.set_init_window()
