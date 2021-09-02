import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class QFileDialogDemo(QWidget): 
    def __init__(self):
        super(QFileDialogDemo, self).__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
       
        self.button1 = QPushButton("選取文件")
        self.button1.clicked.connect(self.loadText)
        layout.addWidget(self.button1)

        self.contents = QTextEdit()
        layout.addWidget(self.contents)


        self.setLayout(layout)
        self.setWindowTitle('文件對話窗演示')

        layout.addWidget(self.contents)


    def loadText(self):
        fname,_ = QFileDialog.getOpenFileName(self, '打開文件', '.', '文件(*.MOV *.mp4)')
        self.contents.setText(fname)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QFileDialogDemo()
    main.show()
    sys.exit(app.exec_())