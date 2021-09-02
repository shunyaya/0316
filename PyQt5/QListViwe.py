import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class ListViewDemo(QWidget):
    def __init__(self, parent = None):
        super(ListViewDemo, self).__init__(parent)
        self.setWindowTitle('QListView Demo')
        self.resize(300,270)
        layout = QVBoxLayout()

        listview = QListView()
        #建立一個空的模型
        listModle = QStringListModel()
        self.list = ["列表項1", "列表項2", "列表項3"]

        #將數據放到空的模型內
        listModle.setStringList(self.list)

        listview.setModel(listModle)
        listview.clicked.connect(self.clicked)
        layout.addWidget(listview)

        self.setLayout(layout)

    
    
    #def clicked(self, index):
        #對畫框顯示
     #   QMessageBox.information(self, "QListView", "您選擇了： " + self.list[index.row()]) #單擊第幾行(row)

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    win = ListViewDemo()
    win.show()
    sys.exit(app.exec_())