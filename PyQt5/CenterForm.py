# QDesktopWidget

import sys
from PyQt5.QtWidgets import QDesktopWidget, QMainWindow, QApplication 
from PyQt5.QtGui import QIcon

class CenterForm (QMainWindow):
    def __init__(self):
        super(CenterForm, self).__init__()

        #設置主窗口的標題
        self.setWindowTitle('讓窗口居中')

        self.resize(400, 300)

    def center(self):
        # 獲取屏幕座標系
        screen = QDesktopWidget().screenGeometry()
        # 獲取窗口座標系
        size = self.geometry()
        newLeft = (screen.width() - size.width()) / 2
        newTop = (screen.height() - size.height) / 2
        self.move((newLeft, newTop))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = CenterForm()
    main.show()

    sys.exit(app.exec_())
