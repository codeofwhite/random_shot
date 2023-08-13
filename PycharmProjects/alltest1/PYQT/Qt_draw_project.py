# 使用PYQT绘画
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
MainWindow.setObjectName("MainWindow")
MainWindow.setWindowTitle("oxxo.studio")
MainWindow.resize(520, 300)  # 主视窗大小

canvas = QPixmap(400, 240)  # 建立 QPixmap 元件作為畫布，並設定畫布大小
canvas.fill(QColor('#ffffff'))  # 畫布填滿白色

label = QtWidgets.QLabel(MainWindow)  # 建立 QLabel
label.setGeometry(0, 0, 400, 240)  # 設定大小位置，下方留下一些空白
label.setPixmap(canvas)  # 放入畫布

last_x, last_y = None, None  # 設定兩個變數紀錄滑鼠座標
penSize = 10  # 畫筆預設粗細
penColor = QColor('#000000')  # 畫筆預設顏色


# 放開滑鼠的函式
def release(self):
    global last_x, last_y
    last_x, last_y = None, None  # 清空座標內容


# 按下滑鼠的函式
def mousePress(self):
    global penColor, penSize
    qpainter = QPainter()  # 建立 QPainter 元件
    qpainter.begin(label.pixmap())  # 在畫布中開始繪圖
    qpainter.setPen(QPen(QColor(penColor), penSize, Qt.SolidLine, Qt.RoundCap))  # 設定畫筆樣式
    qpainter.drawPoint(self.x(), self.y())  # 下筆畫出一個點
    qpainter.end()  # 結束繪圖
    MainWindow.update()  # 更新主視窗內容
    # print(last_x, last_y)


# 按下滑鼠並移動滑鼠的函式
def draw(self):
    global last_x, last_y, penColor, penSize
    if last_x is None:
        last_x = self.x()  # 紀錄滑鼠當下的座標
        last_y = self.y()
        return
    qpainter = QPainter()  # 建立 QPainter 元件
    qpainter.begin(label.pixmap())  # 在畫布中開始繪圖
    qpainter.setPen(QPen(penColor, penSize, Qt.SolidLine, Qt.RoundCap))  # 設定畫筆樣式
    qpainter.drawLine(last_x, last_y, self.x(), self.y())  # 下筆畫出一條線
    qpainter.end()  # 結束繪圖
    MainWindow.update()  # 更新主視窗內容
    last_x = self.x()  # 紀錄結束座標
    last_y = self.y()
    print(last_x, last_y)


# 按下按钮重置画布的函数
def reset_canvas():
    global canvas, label
    canvas.fill(QColor('#ffffff'))  # 畫布填滿白色
    label.setPixmap(canvas)  # 放入畫布
    MainWindow.update()  # 更新主視窗內容


label.mousePressEvent = mousePress  # 設定按下滑鼠並移動的事件
label.mouseMoveEvent = draw  # 設定按下滑鼠的事件
label.mouseReleaseEvent = release  # 設定放開滑鼠的事件

btn1 = QtWidgets.QPushButton(MainWindow)
btn1.setGeometry(412, 0, 100, 60)  # 设置位置和大小
btn1.setText("Reset")  # 设置文本内容
btn1.clicked.connect(reset_canvas)  # 连接按钮点击信号和重置画布函数


# 點擊按鈕更換顏色函式
def changeColor(self, color):
    global penColor, btn
    penColor = QColor(color)  # 設定畫筆顏色
    for i in btn:
        btn[i].setDisabled(False)  # 啟用所有按鈕
    self.setDisabled(True)  # 停用所點擊的按鈕


# 設定顏色清單
colors = ['#ff0000', '#ff8800', '#ffee00', '#00cc00', '#0066ff', '#0000cc', '#cc00cc', '#000000', '#ffffff']
btn = {}  # 因為有很多按鈕，所以使用字典方式紀錄元件
# 依序讀取顏色清單中的顏色
for i in colors:
    index = colors.index(i)  # 取得該顏色的位置 ( 按鈕定位使用 )
    btn[i] = QtWidgets.QPushButton(MainWindow)  # 建立按鈕元件
    # 設定樣式，當中額外設定禁用時的樣式
    btn[i].setStyleSheet('''
        QPushButton{
            background: ''' + i + ''';
            margin-right:5px;
        }
        QPushButton:disabled{
            border:3px solid #000;
        }
    ''')
    btn[i].setGeometry(index * 30 + 10, 250, 30, 30)  # 設定每個按鈕的位置
    btn[i].clicked.connect(lambda checked, b=btn[i], c=i: changeColor(b, c))  # 設定點擊事件


def changeSize(self, size):
    global penSize
    btn_s.setDisabled(False)  # 啟用「細」的按鈕
    btn_m.setDisabled(False)  # 啟用「中」的按鈕
    btn_l.setDisabled(False)  # 啟用「粗」的按鈕
    penSize = size  # 設定畫筆粗細
    self.setDisabled(True)  # 停用所點選的按鈕


btn_s = QtWidgets.QPushButton(MainWindow)  # 建立「細」的按鈕
btn_s.setText('細')
btn_s.setGeometry(280, 250, 45, 30)  # 設定位置
btn_s.clicked.connect(lambda: changeSize(btn_s, 3))  # 設定點擊事件
btn_m = QtWidgets.QPushButton(MainWindow)  # 建立「中」的按鈕
btn_m.setText('中')
btn_m.setGeometry(315, 250, 45, 30)  # 設定位置
btn_m.setDisabled(True)  # 因為預設中，所以先停用中的按鈕
btn_m.clicked.connect(lambda: changeSize(btn_m, 10))  # 設定點擊事件
btn_l = QtWidgets.QPushButton(MainWindow)  # 建立「粗」的按鈕
btn_l.setText('粗')
btn_l.setGeometry(350, 250, 45, 30)  # 設定位置
btn_l.clicked.connect(lambda: changeSize(btn_l, 20))  # 設定點擊事件


def newFile():
    ret = mbox.question(MainWindow, "question", 'SURE OPEN FILE?')
    if ret == mbox.Yes:
        canvas.fill(QColor('#ffffff'))
        label.setPixmap(canvas)
    else:
        return


def saveFile():
    filePath, filterType = QtWidgets.QFileDialog.getSaveFileName(MainWindow, '另存新檔', '',
                                                                 'JPG(*.jpg)')  # 建立開啟檔案對話視窗，設定成存檔方式
    label.pixmap().save(filePath, 'JPG', 90)  # 儲存為 jpg，品質 90


def closeFile():
    app.quit()


mbox = QtWidgets.QMessageBox(MainWindow)
menubar = QtWidgets.QMenuBar(MainWindow)
menu_file = QtWidgets.QMenu("FILE")
action_new = QtWidgets.QAction("new")
action_save = QtWidgets.QAction('save')
action_close = QtWidgets.QAction("close")
action_new.triggered.connect(newFile)
action_save.triggered.connect(saveFile)
action_close.triggered.connect(closeFile)

menubar.addMenu(menu_file)
menu_file.addActions([action_new, action_save, action_close])

MainWindow.show()
sys.exit(app.exec_())
