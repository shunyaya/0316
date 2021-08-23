import sys
from PyQt5.QtWidgets import QHBoxLayout, QMainWindow, QApplication, QPushButton, QWidget 

class QuitApp(QMainWindow):
    def __init__(self):
        super(QuitApp, self).__init__()
        self.resize(300, 120)
        self.setWindowTitle('Quit Application')

        # Add button
        self.button1 = QPushButton('Quit app')
        # 將信號與槽關聯
        self.button1.clicked.connect(self.onClick_Button)

        layout = QHBoxLayout()
        layout.addWidget(self.button1)

        mainFrame = QWidget()
        mainFrame.setLayout(layout)

        self.setCentralWidget(mainFrame)

        
    # 按鈕單擊事件方法
    def onClick_Button(self):
        sender = self.sender
        print(sender.text()+'push button')
        app = QApplication.instance()
        app.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QuitApp()
    main.show()
    sys.exit(app.exec_())