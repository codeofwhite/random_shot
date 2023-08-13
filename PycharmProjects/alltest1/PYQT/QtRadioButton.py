# 单选按钮
from PyQt5 import QtWidgets
import sys

app = QtWidgets.QApplication(sys.argv)

Form = QtWidgets.QWidget()
Form.resize(500, 500)

rb1 = QtWidgets.QRadioButton(Form)
rb1.setGeometry(30, 30, 100, 20)
rb1.setText('A')
rb1.setStyleSheet('''
    QRadioButton {
        color: #00f;
    }
    QRadioButton:hover {
        color:#f00;
    }
''')

rb2 = QtWidgets.QRadioButton(Form)
rb2.setGeometry(30, 90, 100, 20)
rb2.setText('B')
rb2.setChecked(True)

label = QtWidgets.QLabel(Form)
label.setGeometry(30, 150, 100, 20)


def show():
    if rb1.isChecked():
        label.setText("勾选A")
    else:
        label.setText("勾选B")


group1 = QtWidgets.QButtonGroup(Form)  # 在多个RadioButton时很好用，区别单选的群组
group1.addButton(rb1)
group1.addButton(rb2)
group1.buttonClicked.connect(lambda: show())

Form.show()
sys.exit(app.exec_())
