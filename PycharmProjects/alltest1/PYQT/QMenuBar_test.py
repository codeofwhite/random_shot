from PyQt5 import QtWidgets, QtGui
import sys

app = QtWidgets.QApplication(sys.argv)

Form = QtWidgets.QWidget()
Form.setWindowTitle('oxxo.studio')
Form.resize(300, 200)


def open():
    filePath, filterType = QtWidgets.QFileDialog.getOpenFileNames()  # 選擇檔案對話視窗
    print(filePath, filterType)


def close():
    print('close')
    app.quit()


menubar = QtWidgets.QMenuBar(Form)

menu_file = QtWidgets.QMenu('File')

action_open = QtWidgets.QAction('Open')
action_open.triggered.connect(open)
menu_file.addAction(action_open)  # 把open放入file中

action_close = QtWidgets.QAction('Close')
action_close.triggered.connect(close)
menu_file.addAction(action_close)

menubar.addMenu(menu_file)

Form.show()
sys.exit(app.exec_())
