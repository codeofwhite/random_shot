# 导入tkinter和PIL模块
import tkinter as tk
from PIL import Image, ImageTk

# 创建一个主窗口对象
root = tk.Tk()

# 创建一个画布对象，并放置在主窗口上
canvas = tk.Canvas(root, width=200, height=200)
canvas.pack()

# 打开头像图片
img = Image.open("C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/imgs/user_img.jpg")

# 获取画布和图片的尺寸
canvas_width = canvas.winfo_reqwidth()
canvas_height = canvas.winfo_reqheight()
img_width, img_height = img.size

# 计算缩放比例和裁剪区域
scale = min(canvas_width / img_width, canvas_height / img_height)
new_width = int(img_width * scale)
new_height = int(img_height * scale)
x1 = (img_width - new_width) // 2
y1 = (img_height - new_height) // 2
x2 = x1 + new_width
y2 = y1 + new_height

# 缩放和裁剪图片
img = img.resize((new_width, new_height), Image.LANCZOS)
img = img.crop((x1, y1, x2, y2))

# 在画布上显示图片
tk_img = ImageTk.PhotoImage(img)
canvas.create_image(canvas_width // 2, canvas_height // 2, image=tk_img)

# 启动主窗口的消息循环
root.mainloop()