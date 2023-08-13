# 使用按钮连接事件
from PyQt5 import QtWidgets, QtCore
import sys

app = QtWidgets.QApplication(sys.argv)

Form = QtWidgets.QWidget()
Form.setWindowTitle("button_test")
Form.resize(500, 500)

a = 0


# def show():
#     global a
#     a += 1
#     label.setText(str(a))

def show(e):
    label.setText(e)


label = QtWidgets.QLabel(Form)
label.setText('0')
label.setStyleSheet('font-size:20px;')
label.setGeometry(50, 30, 100, 30)

btn1 = QtWidgets.QPushButton(Form)
btn1.setText('A')
btn1.setGeometry(50, 60, 100, 30)
btn1.clicked.connect(lambda: show('A'))  # 有参数要带lambda

btn2 = QtWidgets.QPushButton(Form)
btn2.setText('B')
btn2.setGeometry(200, 60, 100, 30)
btn2.clicked.connect(lambda: show('B'))

Form.show()
sys.exit(app.exec_())
