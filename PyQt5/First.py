import sys

from PyQt5.QtWidgets import QApplication, QWidget

if __name__ == '__main__':
    # 創建 QApplication 類的實例
    app = QApplication(sys.argv)
    # 創建一個窗口
    w = QWidget()
    #設置窗口的尺寸
    w.resize(400,400)
    # 移動窗口
    w.move(300,300)

    # 設置窗口標題
    w.setWindowTitle('第一個基於PyQt5的桌面應用')
    # 顯示窗口
    w.show()

    # 進入程序的主循環
    sys.exit(app.exec_())