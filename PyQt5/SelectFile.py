import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class ListViewDemo(QWidget):
    def __init__(self, parent = None):
        super(ListViewDemo, self).__init__(parent)
        self.setWindowTitle('QListView Demo')
        self.resize(500,270)
        self.initUI()
       
    def initUI(self):
        layout = QVBoxLayout()
        self.listWidget = QListWidget()

        self.buttonOpenFile = QPushButton('Select File')
        self.buttonOpenFile.clicked.connect(self.LoadPath) 
        layout.addWidget(self.buttonOpenFile)

        self.buttonRemoveFile = QPushButton('Remove File')
        self.buttonRemoveFile.clicked.connect(self.RemovePath)
        layout.addWidget(self.buttonRemoveFile)

        self.buttonRemoveAll = QPushButton('Remove All')
        self.buttonRemoveAll.clicked.connect(self.DelListItem)
        layout.addWidget(self.buttonRemoveAll)

        self.listview = QListView()
        #建立一個空的模型
        self.listModle = QStringListModel()
        self.list = ["列表項1", "列表項2", "列表項3"]

         #將數據放到空的模型內
        self.listModle.setStringList(self.list)
        self.listview.setModel(self.listModle)
        layout.addWidget(self.listview)

        self.buttonClip = QPushButton('Edit Video')
        self.buttonClip.clicked.connect(self.VideoEdit)
        layout.addWidget(self.buttonClip)

        self.setLayout(layout)
    

    def LoadPath(self):
        fname,_ = QFileDialog.getOpenFileName(self, '打開文件', '.', '文件(*.MOV *.mp4)')
        if len(fname) != 0 :
            row = self.listModle.rowCount()  # 獲得最後一行的行數       
            self.listModle.insertRow(row)  # 數據模型添加行
            index = self.listModle.index(row,0)  # 獲得數據模型的索引
            self.listModle.setData(index,fname) 
            
    def RemovePath(self):
        selected  = self.listview.selectedIndexes() # 根據所有獲取item
        for i in selected:
            self.listModle.removeRow(i.row())
    
    def DelListItem(self):
        row1 = self.listModle.rowCount()
        for i in range(row1):
            self.listModle.removeRow(self.listview.modelColumn())

    def VideoEdit(self):
        pass

        
if __name__ == "__main__" :
    app = QApplication(sys.argv)
    win = ListViewDemo()
    win.show()
    sys.exit(app.exec_())