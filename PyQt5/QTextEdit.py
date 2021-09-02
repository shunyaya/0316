import sys
from PyQt5.QtWidgets import *

class QTextEditDemo(QWidget):
    def __init__(self):
        super(QTextEditDemo, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('QTextEdit Demo')
        
        self.resize(300, 280)

        self.textEdit = QTextEdit()
        self.button_Text = QPushButton('顯示文本')
        self.button_HTML = QPushButton('顯示HTML')

        layout = QVBoxLayout()
        layout.addWidget(self.textEdit)
        layout.addWidget(self.button_Text)
        layout.addWidget(self.button_HTML)

        self.setLayout(layout)

        self.button_Text.clicked.connect(self.on_clicked_ButtonText)
        self.button_HTML.clicked.connect(self.on_clicked_ButtonHTML)

    def on_clicked_ButtonText(self):
        self.textEdit.setPlainText('Hello World')

    def on_clicked_ButtonHTML(self):
        self.textEdit.setHtml('<font color="blue" size="5"> Hello World</font>')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QTextEditDemo()
    main.show()
    sys.exit(app.exec_())
