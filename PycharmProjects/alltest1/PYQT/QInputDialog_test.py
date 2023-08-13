# Dialog
from PyQt5 import QtWidgets
import sys

app = QtWidgets.QApplication(sys.argv)

Form = QtWidgets.QWidget()
Form.resize(500, 500)


def show():
    text, ok = QtWidgets.QInputDialog().getDouble(Form, 'test', 'pls input words')
    print(text, ok)


btn = QtWidgets.QPushButton(Form)
btn.setGeometry(10, 10, 100, 30)
btn.setText('input')
btn.clicked.connect(show)

Form.show()
sys.exit(app.exec_())
