import sys
from PyQt5.QtWidgets import QMainWindow, QApplication 
from PyQt5.QtGui import QIcon

class FirstMainWin (QMainWindow):
    def __init__(self):
        super(FirstMainWin, self).__init__()

        #設置主窗口的標題
        self.setWindowTitle('智慧影音接軌')

        self.resize(400, 300)

        self.status = self.statusBar()

        self.status.showMessage('只存在五秒的消息', 5000)

        self.file_paths = []
        self.index = 0


if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setWindowIcon(QIcon('./PyQt5/Dragon.ico'))
    main = FirstMainWin()
    main.show()

    sys.exit(app.exec_())
